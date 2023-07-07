import os

from setuptools import find_packages, setup  # noqa: H301

NAME = "svix-ksuid"
VERSION = "0.6.2"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "python-baseconv",
]

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=NAME,
    version=VERSION,
    description=" A pure-Python KSUID implementation",
    author="Svix",
    author_email="development@svix.com",
    url="https://github.com/svixhq/python-ksuid/",
    license="MIT",
    keywords=[
        "svix",
        "ksuid",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
        "Typing :: Typed",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    zip_safe=False,
    packages=find_packages(exclude=["test", "tests"]),
    package_data={
        "": ["py.typed"],
    },
    long_description=README,
    long_description_content_type="text/markdown",
)
