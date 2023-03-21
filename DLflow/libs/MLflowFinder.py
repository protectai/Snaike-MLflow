from libnmap.parser import NmapParser


class MLflowFinder:
    def __init__(self, report_path):
        self.report_path = report_path

    def run(self):
        report = self.get_nmap_file()
        mlflow_hosts = self.get_mlflow_hosts(report)
        return mlflow_hosts

    def get_nmap_file(self):
        report = NmapParser.parse_fromfile(self.report_path)
        return report

    def get_mlflow_hosts(self, report):
        mlflow_hosts = []
        for host in report.hosts:
            for service in host.services:
                if "<title>MLflow</title><script\\x20defer" in service.servicefp:
                    address = host.address
                    port = str(service.port)
                    location = f"http://{address}:{str(port)}"
                    mlflow_hosts.append(location)
        return mlflow_hosts
