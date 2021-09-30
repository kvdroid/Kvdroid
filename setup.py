from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kvdroid',
    packages=['kvdroid'],
    version='0.2.4',
    description='Some Pyjnius tools for Kivy-Android developments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yunus Ceyhan',
    author_email='yunus.ceyhn@gmail.com',
    url='https://github.com/yunus-ceyhan/Kvdroid',
    keywords=['Android', 'Python', 'Kivy'],
    install_requires=[],
    classifiers=[],
)
