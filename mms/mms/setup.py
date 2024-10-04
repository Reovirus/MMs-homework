from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Naive markov models'
LONG_DESCRIPTION = '''Just MM realised trough n-mer hypercube where n = depth'''
source = ['model_classes.py',
          'errors.py',
          '__init__.py']


def parse_reqs(requirements):
    with open(requirements, "r") as req_file:
        return [line.strip('\n') for line in req_file if not line.startswith('#')]

setup(
    name="naivemms",
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
