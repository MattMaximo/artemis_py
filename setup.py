from setuptools import setup, find_packages

setup(
    name="PyArtemis",
    version="0.1.0",
    description="A package to interact with the Artemis API. Blame ChatGPT for errors.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/MattMaximo/PyArtemis",  
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