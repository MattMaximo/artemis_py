from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="artemis-py",  
    version="0.2.1",
    description="A package to interact with the Artemis API. Blame ChatGPT for errors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Matt Maximo",
    author_email="matt@pioneerdigital.org",
    url="https://github.com/MattMaximo/artemis_py",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)