from setuptools import find_packages, setup
# find_packages is equvalent to find_packages
from typing import List

def get_requirements()->List[str]:
    """
    This will return list of requirment as form of string
    """
    requirements_list: list[str] = []
    return requirements_list

setup(
    name="vista_macro",
    version="0.0.1",
    author="Tsegazab Tesfay",
    author_email="azutes321@gmail.com",
    packages=find_packages(),
    install_reqires = get_requirements()#["pymongo=4.2"],
)