from setuptools import setup, find_packages

setup(
    name='idontwannadoresearch',  # Name of the package
    version='0.0.29',  # Initial version
    description='Research utilities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cychen2021/idontwannadoresearch',  # Your repo link
    author='Chuyang Chen',
    author_email='chuyangchen2018@outlook.com',
    license='MIT',  # License you choose
    packages=find_packages(),  # Finds submodules automatically
    install_requires=[
        'dill~=0.3.8'],  # List of dependencies
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',  # Minimum Python version
)