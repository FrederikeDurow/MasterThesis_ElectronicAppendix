from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'multiple_functions_v2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch','*launch.[pxy][yma]*'))), 
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.xml')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='frederike',
    maintainer_email='frdur16@student.sdu.dk',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tree_generator = multiple_functions_v2.tree_generator:main',
            'user_input_dummy =multiple_functions_v2.user_input_dummy:main'
        ],
    },
)
