# Blockchain Workshop Project

This is a simple training project for a blockchain workshop.

## Initializing the Project

I used Anaconda to set up the project environment.

```powershell
conda create -n blockchain_workshop_project
conda activate blockchain_workshop_project
# If you don't have conda, you can use pip to install the required packages.
# pip install -r requirements.txt
conda list --export > requirements.txt
# Exports the conda environment to a YAML file.
conda env export > environment.yml
```

You can install the requirements using:

```powershell
# From requirements.txt
pip install -r requirements.txt

# Or from environment.yml (recommended for conda)
conda env create -f environment.yml -n blockchain_workshop_project
conda activate blockchain_workshop_project
```

> [!IMPORTANT] DEPENDENCIES
> Both files need to be updated whenever new packages are added to the project or existing ones are updated.

```powershell
conda list --export > requirements.txt & conda env export > environment.yml
```

An existing environment can be updated with:

```powershell
conda env update -f environment.yml -n blockchain_workshop_project
```