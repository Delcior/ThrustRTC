from setuptools import setup
from codecs import open
import os

cmdclass = {}

try:
	from wheel.bdist_wheel import bdist_wheel
except ImportError:
	bdist_wheel = None

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def get_package_data():
	if os.name == 'nt':
		return 'PyThrustRTC.dll'
	elif os.name == "posix":
		return 'libPyThrustRTC.so'

if bdist_wheel is not None:
	class bdist_wheel_platform_tag(bdist_wheel):
		def finalize_options(self):
			bdist_wheel.finalize_options(self)
			self.root_is_pure = False

		def get_tag(self):
			_, _, plat = bdist_wheel.get_tag(self)
			return 'py3', 'none', plat

	cmdclass['bdist_wheel'] = bdist_wheel_platform_tag

setup(
	name = 'ThrustRTC',
	version = '0.3.20',
	description = 'Thrust for Python based on NVRTC',
	long_description=long_description,
	long_description_content_type='text/markdown',  
	url='https://github.com/fynv/ThrustRTC',
	license='Anti 996',
	author='Fei Yang',
	author_email='hyangfeih@gmail.com',
	keywords='GPU CUDA Thrust',
	packages=['ThrustRTC'],
	package_data = { 'ThrustRTC': get_package_data()},
	install_requires = ['cffi','numpy'],	
	cmdclass=cmdclass,
)
