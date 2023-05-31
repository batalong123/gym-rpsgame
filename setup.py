from setuptools import setup, find_packages
from pathlib import Path   

setup(name='gym_rpsgame',
	version='1.0.0',
	description='A OpenAI Gym Env for Rock-Paper-Scissor game',
	long_description=Path("README.md").read_text(), 
	long_description_content_type="text/markdown",
	packages= find_packages(include="gym_rpsgame*"),
	url = 'https://github.com/batalong123/gym-rpsgame',
	author='Massock Batalong M.B.',
	author_email='lumierebatalong@gmail.com',
	license='GPL',
	install_requires=['gym', 'pygame', 'numpy'])