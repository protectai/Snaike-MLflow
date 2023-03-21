# DLflow

DLflow is a tool for rapidly downloading all AI artifact files from an MLflow server. Requires only a server:port or an Nmap XML file with an MLflow server listed.

## Installation

```bash
git clone https://github.com/protectai/Snaike-MLflow
cd Snaike-MLflow/DLflow
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

To find MLflow servers on a network, install Nmap using your preferred method (apt-get, brew, yum, etc.) and run Nmap with -sV:
```bash
nmap -sV <1.2.3.4/24> -oX nmapscan.xml
python DLflow.py -f nmapscan.xml
````

Alternatively, you can specify a server:port:

```bash
python DLflow.py -s http://127.0.0.1:5000
```

## Example MLflow setup
The following will allow you to test DLflow on a local MLflow server.

```bash
git clone https://github.com/mlflow/mlflow
mkdir mlflowui
cd mlflowui
cp -r ../mlflow/examples/sklearn_elasticnet_wine .
python3 -m venv venv
source venv/bin/activate
pip install mlflow pandas
mlflow run --env-manager=local sklearn_elasticnet_wine -P alpha=0.5
mlflow ui --host 127.0.0.1:5000
```
Now you should have some artifacts stored in MLflow which allows you to test DLflow.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

Copyright 2023 ProtectAI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
