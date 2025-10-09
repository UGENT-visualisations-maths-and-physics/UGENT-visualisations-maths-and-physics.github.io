from setuptools import setup, find_packages

#1. make virtual environment for python in overarching "UGENT-visualisations-maths-and-physics.github.io" directory

#2. execute:
# pip install setuptools

#allow working with relative paths:
#3. execute:
# pip install -e <path> 
# with <path>, the path to the overarching 'UGENT-visualisations-maths-and-physics.github.io' directory: for example '/Users/simonverbruggen/Desktop/UGENT-visualisations-maths-and-physics.github.io/

#4. pip install other required packages (if necessary)
#test
setup(
    name='math_visualisations',     # package name
    version='0.1',
    packages=find_packages(),
    install_requires = ['numpy', "pdf2image", "pyyaml"],   # specifies which packages get installed
    include_package_data=True,
    python_requires='>=3.6',        # specify Python version requirement
)