from setuptools import setup
from codecs import open
import os
import shutil
import subprocess

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
		return ['PyThrustRTC.dll']
	elif os.name == "posix":
		return ['libPyThrustRTC.so']
	return []

def build_native_library():
	build_dir = os.path.join(here, '_cmake_build')
	install_dir = os.path.join(build_dir, 'install')
	config = os.environ.get('BUILD_TYPE', 'Release')
	cmake_args = [
		'cmake',
		'-S', here,
		'-B', build_dir,
		'-DCMAKE_BUILD_TYPE=%s' % config,
		'-DCMAKE_INSTALL_PREFIX=%s' % install_dir,
	]
	if os.name == 'nt' and 'CMAKE_GENERATOR' not in os.environ:
		cmake_args.extend(['-G', 'NMake Makefiles'])
	if os.name != 'nt':
		cmake_args.append('-DCMAKE_CXX_FLAGS=-include cstdio')

	subprocess.check_call(cmake_args)
	subprocess.check_call(['cmake', '--build', build_dir, '--config', config])
	subprocess.check_call(['cmake', '--install', build_dir, '--config', config])

	for binary in get_package_data():
		src = os.path.join(install_dir, 'test_python', 'ThrustRTC', binary)
		dst = os.path.join(here, 'ThrustRTC', binary)
		if not os.path.exists(src):
			raise RuntimeError('Expected native library was not built: %s' % src)
		shutil.copy2(src, dst)

if bdist_wheel is not None:
	class bdist_wheel_platform_tag(bdist_wheel):
		def finalize_options(self):
			bdist_wheel.finalize_options(self)
			self.root_is_pure = False

		def run(self):
			build_native_library()
			bdist_wheel.run(self)

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
