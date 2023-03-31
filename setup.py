from setuptools import setup, find_packages


def requirements():
    with open('requirements.txt', 'r') as fileobj:
        requirement = [line.strip() for line in fileobj]
        return requirement


def long_description():
    with open('README.rst', 'r') as fileobj:
        return fileobj.read()


setup(
    name='vod-python-sdk',
    version='1.4.4',
    url='https://github.com/tencentyun/vod-python-sdk',
    license='MIT',
    author='vod',
    author_email='1654382995@qq.com',
    description='vod-python-sdk',
    long_description=long_description(),
    packages=find_packages(exclude=["test*"]),
    install_requires=requirements()
)
