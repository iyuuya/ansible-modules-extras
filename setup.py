from setuptools import setup, find_packages
from codecs import open
from os import path

package_name = 'ansible-modules-extras'
root_dir = path.abspath(path.dirname(__file__))

def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]

setup(
    name=package_name,
    version='0.0.1',
    license='GPL3',
    install_requires=_requirements(),
    tests_require=[], # TODO
    author='iyuuya',
    author_email='i.yuuya@gmail.com',
    url='https://github.com/iyuuya/ansible-modules-extras',
    description='Ansible modules for iyuuya',
    packages=['ansible/modules'],
    classifiers=[
        'Framework :: Ansible',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Ansible Modules'
    ]
)
