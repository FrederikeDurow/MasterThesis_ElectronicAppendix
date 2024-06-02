from setuptools import find_packages, setup

package_name = 'visualization'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'bt_visualization = visualization.bt_visualization:main',
            'bb_visualization = visualization.bb_visualization:main'

        ],
    },
)