from setuptools import setup, find_packages  

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name = 'FinStats',
    description = 'A query engine for generating financial statistics.',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    version = '0.0.1',
    author = 'Jay Alfaras',
    author_email = 'alfarasjb@gmail.com',
    url = '',
    packages = find_packages(),
    include_package_data = True,
    install_requres = [
        'customtkinter>=5.2.0',
        'matplotlib>=3.5.2',
        'fpdf>=2.7.6',
        'pandas>=1.4.4',
        'numpy>=1.26.0',
        'scipy>=1.9.1',
        'yfinance>=0.2.20',
        'seaborn>=0.11.2',
        'pytest>=7.1.2'
    ]
    )