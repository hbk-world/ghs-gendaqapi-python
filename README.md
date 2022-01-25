# GEN DAQ API - Python Driver
> Setup, control and acquire data from the Genesis Highspeed systems via python.

[![Build Status](https://dev.azure.com/GenesisHighSpeed/GHS%20ESW/_apis/build/status/hbk-world.ghs-gendaqapi-python?branchName=main)](https://dev.azure.com/GenesisHighSpeed/GHS%20ESW/_build/latest?definitionId=117&branchName=main)

The GEN DAQ API can be used to control the HBM GEN Series tethered mainframes.

## Requirements

Python 3.10+

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install GEN DAQ API - Python Driver package.

```bash
pip install ghsapi
```

## Usage

Refer [examples](./examples) for detailed use cases

```python
from ghsapi import ghsapi

# create Gen Daq API's object
gen = ghsapi.GHS()

# connect to mainframe
gen.ghs_connect(IP_ADDRESS, PORT_NO)

# disconnect from mainframe
gen.ghs_disconnect()
```

## Development environment setup

Below are the steps to follow to setup devlopement enviroment for system integration and testing.

### Requirements

- `Python 3.10+`
- `Anaconda/Miniconda`

### Clone repo

```bash
git clone https://github.com/hbk-world/ghs-gendaqapi-python.git
```

### Virtual Environment

```bash
conda create --name <env> --file spec-file.txt
```

### Install dependencies

```bash
python install -r requirements.txt
```

## Run example files

Edit files in [examples](./examples) to enter mainframe IP and Port number

```bash
python examples\FILENAME
```

## Testing

Edit files in [functionaltest](./functionaltest) to enter mainframe IP and Port number

### Unit test

```bash
python unittest\FILENAME
```

### Functional test

```bash
python functionaltest\FILENAME
```
