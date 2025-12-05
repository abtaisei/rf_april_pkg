from setuptools import setup

package_name = 'tag_bridge_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abtaisei',
    maintainer_email='g2212005@tcu.ac.jp',
    description='Bridge AprilTagDetectionArray to Int32 tag ID',
    license='MIT',
    entry_points={
        'console_scripts': [
            'tag_bridge = tag_bridge_pkg.tag_bridge:main',
        ],
    },
)
