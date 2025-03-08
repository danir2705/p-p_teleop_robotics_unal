from setuptools import find_packages, setup

package_name = 'phantom_planner'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ["launch/main_launch.py"])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='grupo-robotica',
    maintainer_email='',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'jacobian = phantom_planner.jacobian:main',
            'gui = phantom_planner.gui:main'
        ],
    },
)
