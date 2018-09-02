from distutils.core import setup

setup(
    name='Noted',
    version='0.1.0',
    author='L. Becker',
    author_email='lb@space8.me',
    packages=['noted', 'noted.prj_mode'],
    scripts=['bin/noted',],
    url='http://www.space8.me/noted',
    download_url='https://github.com/space8me/noted',
    license='LICENSE',
    description='The coolest Note program in the Universe. Also, I am learning Python.',
    long_description=open('README.md').read(),
    install_requires=[
        "cryptography >= 2.0",
    ],
)
