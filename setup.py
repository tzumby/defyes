import setuptools
# from package import Package
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="defi-protocols",
    version="0.0.1",
    author="dharmendrakariya",
    author_email="dharmendra@karpatkey.com",
    description="A simple defi-protocols package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KarpatkeyDAO/defi-protocols",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'web3',
          'requests',
          'datetime',
          'pathlib',
          'eth_abi',
          'setuptools'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
