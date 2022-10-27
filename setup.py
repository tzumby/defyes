import setuptools
# from package import Package
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="kpk-defi-protocols", # Replace with your own username
    version="0.0.6",
    author="dharmendrakariya",
    author_email="dharamendra.kariya@gmail.com",
    description="A simple kpk defi-protocols package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    # cmdclass={
    #     "package": Package
    # },
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
