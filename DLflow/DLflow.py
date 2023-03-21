from libs.PoolScraper import PoolScraper
from libs.MLflowFinder import MLflowFinder
import argparse
import os


class DownloadArtifacts:
    def __init__(self, mlflow_hosts, dir_path=None):
        self.mlflow_hosts = mlflow_hosts
        self.scraper = PoolScraper(json=True)
        self.dir_path = dir_path

    def run(self):
        # Experiments
        exp_resps = self.get_experiments()
        # Run IDs
        run_id_resps = self.get_run_id_resps(exp_resps)
        # Artifact Paths
        artifact_resps = self.get_artifact_resps(run_id_resps)
        # Artifacts
        artifact_paths_resps = self.get_artifact_paths(artifact_resps)
        # Artifact content
        artifacts_resps = self.get_artifacts(artifact_paths_resps)
        # Save artifacts
        self.save_artifacts(artifacts_resps)

    def get_experiments(self):
        reqs_data = []
        urls = [
            host + "/ajax-api/2.0/mlflow/experiments/search?max_results=9999"
            for host in self.mlflow_hosts
        ]
        for url in urls:
            method = "GET"
            data = None
            headers = None
            req_data = {"method": method, "url": url, "headers": headers, "data": data}
            reqs_data.append(req_data)

        resps = self.scraper.scrape(reqs_data)
        return resps

    def get_run_id_resps(self, resps):
        reqs_data = []
        for r in resps:
            if r:
                json_data = r.json()
                experiments = json_data["experiments"]
                for e in experiments:
                    method = "POST"
                    url = r.url.split("/ajax-api")[0] + "/ajax-api/2.0/mlflow/runs/search"
                    data = {
                        "experiment_ids": [e["experiment_id"]],
                        "max_results": 9999,
                        "run_view_type": "ACTIVE_ONLY",
                        "order_by": ["attributes.start_time DESC"],
                    }
                    headers = None
                    req_data = {
                        "method": method,
                        "url": url,
                        "data": data,
                        "headers": headers,
                    }
                    reqs_data.append(req_data)

        resps = self.scraper.scrape(reqs_data)
        return resps

    def get_artifact_resps(self, run_id_resps):
        reqs_data = []
        for r in run_id_resps:
            if r:
                # json_data = json.loads(r.text)
                json_data = r.json()
                if len(json_data) > 0:
                    for run in json_data["runs"]:
                        method = "GET"
                        run_uuid = run["info"]["run_uuid"]
                        url = (
                            r.url.split("/ajax-api")[0]
                            + f"/ajax-api/2.0/mlflow/artifacts/list?run_uuid={run_uuid}"
                        )
                        data = None
                        headers = None
                        req_data = {
                            "method": method,
                            "url": url,
                            "data": data,
                            "headers": headers,
                        }
                        reqs_data.append(req_data)

        resps = self.scraper.scrape(reqs_data)
        return resps

    def get_artifact_paths(self, artifact_resps):
        reqs_data = []
        for r in artifact_resps:
            if r:
                json_data = r.json()
                if "files" in json_data:
                    for file in json_data["files"]:
                        path = file["path"]
                        run_uuid = r.url.split("run_uuid=")[1]

                        method = "GET"
                        url = (
                            r.url.split("/ajax-api")[0]
                            + f"/ajax-api/2.0/mlflow/artifacts/list?run_uuid={run_uuid}&path={path}"
                        )
                        data = None
                        headers = None
                        req_data = {
                            "method": method,
                            "url": url,
                            "data": data,
                            "headers": headers,
                        }
                        reqs_data.append(req_data)

        resps = self.scraper.scrape(reqs_data)
        return resps

    def get_artifacts(self, artifacts_paths_resps):
        reqs_data = []
        for r in artifacts_paths_resps:
            if r:
                json_data = r.json()
                if "files" in json_data:
                    print(f"[+] Files found on {r.url}")
                    for file in json_data["files"]:
                        path = file["path"]
                        is_dir = file["is_dir"]
                        run_uuid = r.url.split("run_uuid=")[1].split("&")[0]

                        if not is_dir:
                            method = "GET"
                            url = (
                                r.url.split("/ajax-api")[0]
                                + f"/get-artifact?path={path}&run_uuid={run_uuid}"
                            )
                            data = None
                            headers = None
                            req_data = {
                                "method": method,
                                "url": url,
                                "data": data,
                                "headers": headers,
                            }
                            reqs_data.append(req_data)

        resps = self.scraper.scrape(reqs_data)
        return resps

    def save_artifacts(self, artifacts_resps):
        for r in artifacts_resps:
            if r:
                print(f"[+] Saving {r.url}")
                run_uuid = r.url.split("run_uuid=")[1].split("&")[0]
                path = r.url.split("path=")[1].split("&")[0].split("/")[-1]
                folder = r.url.split("/get-artifact")[0].split("//")[1]
                if not os.path.exists(folder):
                    os.mkdir(folder)
                subfolder = f"{folder}/{run_uuid}"
                if not os.path.exists(subfolder):
                    os.mkdir(subfolder)
                with open(f"{subfolder}/{path}", "wb+") as f:
                    f.write(r.content)


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Path to Nmap XML file", required=False)
    parser.add_argument(
        "-s",
        "--server",
        help="Specific MLflow protocol, server and port, e.g., http://1.2.3.4:5000",
        required=False,
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = args()
    if args.file:
        mf = MLflowFinder(args.file)
        hosts = mf.run()
    elif args.server:
        hosts = [f"{args.server}"]
    else:
        print(
            "[-] You must specify an Nmap XML file (-f filename.xml) or a specific server (-s http://1.2.3.4:5000)"
        )
        exit(1)

    da = DownloadArtifacts(hosts)
    da.run()
