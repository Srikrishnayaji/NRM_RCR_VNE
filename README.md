# Virtual Network Embedding based on Computing, Network and Storage Resource Constraints
Our project is an implementation of the VNE research paper using VNEP/alib simulation tool.

## Requirements
The code is written in python2 and the required python libraries are gurobipy, numpy, cPickle, networkx 1.9, matplotlib, pip2. 

## Usage
To start with the setup execute the following command in the alib directory.
```bash
pip install .
```

To run the code execute the run.py file.
```bash
python2 run.py
```
The command line input is to be given. The substrate network parameters are to be given followed by the virtual network data.

## Modules of interest
The implementation of the research paper given, is present in the VNE folder.

```bash
VNE/
├── algorithm.py
├── graph_generator.py
├── __init__.py
├── __init__.pyc
├── mapping_wrapper.py
├── __pycache__
│   ├── algorithm.cpython-39.pyc
│   └── mapping_wrapper.cpython-39.pyc
├── substrate_wrapper.py
└── utils.py
```
