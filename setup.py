from setuptools import setup, find_packages

setup(
    name="health-check",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyyaml",
        "pytest"
    ],
    author="Mason R. Ware",
    author_email="masonware15@gmail.com",
    description="A simple API client for making HTTP requests.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simple_api_client",  # Replace with your repo link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
