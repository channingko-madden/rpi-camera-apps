#!/user/bin/env python

from distutils.core import setup

setup(name='rpi-camera-apps',
        version='0.0.1',
        description='Raspberry Pi Camera Apps',
        author='Channing Ko-Madden',
        author_email='channingkomadden@gmail.com',
        url='https://github.com/channingko-madden/rpi-camera-apps',
        packages=['rca', 'rca.camera'],
        package_dir={'rca': 'src/rca', 'rca.camera': 'src/rca/camera'}
        )

