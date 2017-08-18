from setuptools import setup
import os

requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')

with open(requirements_path) as requirements_file:
	requires = requirements_file.readlines()


setup(
	name='ecm-validator',
	version='0.1.0',
	packages=['ecm_validator'],
	url='',
	license='',
	author='Federico "fedexist" D\'Ambrosio',
	author_email='fedexist@gmail.com',
	description="XTM parser and validator",
	install_requires=requires,
	scripts=['ecm_validator\\xtm_validator.py', 'ecm_validator\\xtm_parser.py']
)
