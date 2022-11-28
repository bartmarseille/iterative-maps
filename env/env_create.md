# Setup a virtual environment using conda

used `parameters`:

- `<PROJECT DIR>` the project directory
- `<VIRTUAL ENV NAME>` the name of the new virtual environment

create/goto project folder

```commandline
cd projects/py
mkdir <PROJECT DIR>
cd <PROJECT DIR>
```

create environment file

```commandline
touch environment.yaml
```
  
edit environment file with required packages

```commandline
name: <VIRTUAL ENV NAME>
channels:
- conda-forge
- defaults
dependencies:
- python=3.9
- pip>=19.0
- jupyter
- numpy
- matplotlib
- <OTHER CONDA-FORGE PACKAGES>
- pip:
- <ALTERNATIVELY ANY PIP PACKAGES>
```
  
execute script in enviriment file

```commandline
conda env create
```
