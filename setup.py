# coding: utf-8
import os
import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.md'), "r") as fh:
    readme = fh.read()

setuptools.setup(
    name='oai_repo',
    version="0.4.3",
    license='Apache License 2.0',
    description='OAI-PMH Repository Server',
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Nate Collins",
    author_email="npcollins@gmail.com",
    url='https://github.com/MSU-Libraries/oai_repo',
    project_urls={
        "Documentation": "https://msu-libraries.github.io/oai_repo/",
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "Cerberus >= 1.3",
        "jsonpath-ng >= 1.6",
        "lxml >= 4.9",
        "requests >= 2.31",
        "validators >= 0.22",
    ]
)
