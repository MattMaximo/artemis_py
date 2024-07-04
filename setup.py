from setuptools import setup, find_packages

setup(
    name="PyArtemis",
    version="0.1.0",
    description="A package to interact with the Artemis API",
    author="Matt Maximo",
    author_email="matt@pioneerdigital.org",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "plotly"
    ],
    python_requires='>=3.6',
)