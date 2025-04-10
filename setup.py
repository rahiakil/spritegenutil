from setuptools import setup, find_packages

setup(
    name='spirte-gen',
    version='0.1.1',
    author='Rahi Akil',
    author_email='plow.miner@gmail.com',
    description='A utility library for various tasks related to sprite generation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my-python-utility',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)