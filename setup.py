from distutils.core import setup

setup(
    name='clnews',
    version='0.1.0',
    author='Alexandros Ntavelos',
    author_email='a.ntavelos@gmail.com',
    packages=['clnews', 'clnews.test'],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/clews/',
    license='LICENSE.txt',
    description='Advanced news feed reader',
    long_description=open('README.txt').read(),
    install_requires=[
        "colorama==0.3.2",
        "feedparser==5.1.3",
        "termcolor==1.1.0",
    ],
)