from setuptools import setup, find_packages

setup(
    name="artemis_py",
    version="0.1.0",
    description="A package to interact with the Artemis API. Blame ChatGPT for errors.",
    author="Matt Maximo",
    author_email="matt@pioneerdigital.org",
    url="https://github.com/MattMaximo/artemis_py",  
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "plotly"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)