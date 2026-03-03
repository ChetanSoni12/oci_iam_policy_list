# OCI IAM Policy List

This repo has a python file to list out the OCI IAM policies in a CSV file

## Using this script

1. If your system-installed Python environment does not provide you with all of the modules you need, create a virtual environment:
   ```bash
   python3 -m venv "${PWD}/.venv"
   source "${PWD}/.venv/bin/activate"
   ```
1. Install the [Pip requirements](requirements.txt)
   ```bash
   python3 -m pip install -r "${PWD}/requirements.txt"
   ```
1. Make sure that you have a valid OCI CLI configuration file, for which the default location is `${HOME}/.oci/config`.
1. Run the policies script
   ```bash
   ./oci_iam_policies.py
   ```
