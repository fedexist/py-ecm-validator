from setuptools import setup
import os

requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'requirements.txt')

with open(requirements_path) as requirements_file:
	requires = requirements_file.readlines()


setup(
	name='py-ecm_validator',
	version='',
	packages=['ecm_validator'],
	url='',
	license='',
	author='Federico "fedexist" D\'Ambrosio',
	author_email='fedexist@gmail.com',
	description="XTM parser and validator",
	install_requires=requires
)
