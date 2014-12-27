from setuptools import setup

from clnews.config import VERSION
setup(
    name='clnews',
    version=VERSION,
    author='Alexandros Ntavelos',
    author_email='a.ntavelos@gmail.com',
    packages=['clnews', 'clnews.test'],
    # scripts=[],
    url='https://github.com/antavelos/clnews',
    license='LICENSE.txt',
    description='Advanced news feed reader',
    long_description=open('README.rst').read(),
    install_requires=[
        "colorama==0.3.2",
        "feedparser==5.1.3",
        "termcolor==1.1.0",
    ],
)
