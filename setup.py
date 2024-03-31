import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "resume_worth",
    version = "0.0.1",
    author = "Luis Rodrigues, PhD",
    author_email = "luisrodriguesphd@gmail.com",
    description = ("Discover your market value with ResumeWorth receiving a salary estimate through an advanced AI analysis"),
    license = "apache-2.0",
    keywords = ["NLP", "data indexing", "information retrieval"],
    url = "https://huggingface.co/spaces/luisrodriguesphd/resume-worth",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=read('README.md'),
)
