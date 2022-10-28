# Python package for Defi Protocols

## Install

[pip3 install defi-protocols](https://pypi.org/project/defi-protocols/0.0.1/)

## Config 

- First you will have to modify the `defi-config.json` under `/path/to/python/site-packages/general/defi-config.json`

- You should provide `RPC` endpoints and `EXPLORER API KEYS`


## Lerning

### How  I create the package and useful commands!!

- You will have to create `__init__.py` in each of the folder you want to make it work as a module

  - You can see we have three folders(modules) here `db` , `general` and `defi-protocols`

- Create `LICENCE` ( Which can be created during repo creation and its super easy)

- Create `MANIFEST.in` , in which you would mention the packaging of the files

- NOT MANDATORY: Create requirements.txt, with the help of this you can mention needed packages for this package, which should be installed as a dependencies and should be mentioned in `setup.py`

- Create `setup.py` , in that you can mention all the details needed, checkout the reference for the help! Google it , lol

- Create beautiful `README.md` so that people can grasp the shit you have created, lol

### Commands

- Run below commands in order to create the package and push it to `pypi`

  - First create account at pypi

- `python3 setup.py sdist bdist_wheel`

- `twine upload --verbose --repository pypi dist/* `

- Give `Username` and `Password` of your `pypi` account


## Take out: It should be really easy if you are not dumbfuck like me! Make sure you check you python path is set properly, otherwise you gonna rot in hell indefinitely, JK, this guide wont make you go through that!
