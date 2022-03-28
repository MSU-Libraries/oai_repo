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
    author="Nate Collins",
    author_email="npcollins@gmail.com",
    url='https://github.com/MSU-Libraries/oai_repo',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    python_requires=">=3.9",
    install_requires=[
        "Cerberus >= 1.3",
        "jsonpath-ng >= 1.5",
        "lxml >= 4.8",
        "requests >= 2.27",
    ]
)
