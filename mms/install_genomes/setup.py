from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'NCBI GenBank name installer'
LONG_DESCRIPTION = '''It try to make query and download results in fasta format. 
Unfortunately it works when subject have link to database only. 
And package always download last genome version'''
source = ['src/assembly_class.py',
          'src/install_functions.py',
          'src/multithreading_decorator.py']


def parse_reqs(requirements):
    with open(requirements, "r") as req_file:
        return [line.strip('\n') for line in req_file if not line.startswith('#')]


setup(
    name="ncbiinstaller",
    version=VERSION,
    author="Egor Pitikov",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    platforms="OS Independent",
    install_requires=parse_reqs("requirements.txt"),
    scripts=source,
    python_requires='>=3.7',
)
