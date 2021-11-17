from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyandroidkx',
    packages=find_packages(
            include=["pyandroidkx", "pyandroidkx.*"]
        ),
    version='1.0.0',
    description='A re-implementation of android java API in python with easy access to some Android functionality '
                'like Notification,Reading of Contacts, accessing Webview Cookies, etc...',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Akubue-Izundu Kenechukwu',
    author_email='kengoon19@gmail.com',
    url='https://github.com/yunus-ceyhan/Kvdroid',
    keywords=['Android', 'Androidx', 'Python', 'Kivy', 'KivyMD'],
    install_requires=["pyjnius"],
    classifiers=[],
)
