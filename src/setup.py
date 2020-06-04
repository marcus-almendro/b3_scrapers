from setuptools import setup, find_packages


setup(
    name='b3_scrapers',
    version='0.1',
    description='Scrapers da B3',
    url='https://github.com/marcus-almendro/b3_scrapers',
    author='Marcus Almendro',
    author_email='marcus.almendro@gmail.com',
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'pandas', 'lxml', 'html5lib', 'chromedriver-binary==83.0.4103.39.0', 'selenium', 'tqdm'],
)