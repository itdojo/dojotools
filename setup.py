from setuptools import setup, find_packages

setup(
    name='dojotools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        scapy,
        requests,
        netifaces,
        subprocess,
        platform
    ],
    include_package_data=True,
    description='Colin's little pack of tools',
    author='Colin Weaver',
    author_email='colin@itdojo.com',
    url='https://github.com/itdojo/dojotools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
