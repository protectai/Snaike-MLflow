# Snaike-MLflow

Snaike: ProtectAI's Python AI red teaming toolsuite

MLflow: Platform for the machine learning lifecycle

## CVE-2023-1177-scanner
A tool for scanning MLflow servers for the LFI/RFI vulnerability CVE-2023-1177. 
See CVE-2023-1177-scanner/README.md for more information.

```bash
git clone https://github.com/protectai/Snaike-MLflow
cd Snaike-MLflow/CVE-2023-1177-scanner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python CVE-2023-1177-scanner.py -s http://1.2.3.4:5000
```

## MLFIflow
A tool for exploiting MLflow servers vulnerable to the LFI/RFI vulnerability CVE-2023-1177.
See MLFIflow/README.md for more information.

```bash
git clone https://github.com/protectai/Snaike-MLflow
cd Snaike-MLflow/MLFIflow
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python MLFIflow.py -s http://1.2.3.4:5000
```

## DLflow
This tool allows you to quickly download all files from a discovered MLflow server. 
See DLflow/README.md for more information.

```bash
git clone https://github.com/protectai/Snaike-MLflow
cd Snaike-MLflow/DLflow
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python DLflow.py -s http://1.2.3.4:5000
```

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
