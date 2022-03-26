# coding: utf-8
import os
import setuptools
import oai_repo

with open(os.path.join(os.path.dirname(__file__), 'README.md'), "r") as fh:
    readme = fh.read()

setuptools.setup(
    name='oai_repo',
    packages=['oai_repo'],
    version=oai_repo.__version__,
    license='Apache License 2.0',
    description='OAI-PMH Repository Server',
    long_description=readme,
    long_description_content_type="text/markdown",
    author=oai_repo.__author__,
    author_email='repoteam@lib.msu.edu',
    url='https://github.com/MSU-Libraries/oai-repo',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
