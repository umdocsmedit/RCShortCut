import os
from setuptools import setup  # type: ignore


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
        name="UMREDCap",
        version="0.0.1",
        author="Kevin Davis",
        author_email="kevin.davis@med.miami.edu",
        description=("Package of classes and functions for UM DOCS MedIT"
                     "Specific functions related to REDCap"),
        license="BSD",
        keywords="UM DOCS MedIT REDCap",
        url="http://github.com/umdocsmedit/umredcap",
        packages=['umredcap', 'tests'],
        long_description=read('README.md'),
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Education',
            'Programming Language :: Python',
            'Topic :: Utilities'
            ]
        )
