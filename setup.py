from setuptools import setup, find_packages

setup(
    name='autosmile',
    version='0.1.0',
    description='A CLI tool and library to add or enhance smiles in images.',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'dlib',
        'face_recognition'
    ],
    entry_points={
        'console_scripts': [
            'autosmile=autosmile0:main',
        ],
    },
)
