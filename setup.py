from setuptools import setup, find_packages

setup(
    name='primehub-remote-deploy',
    version='0.1.0',
    python_requires='>=3.6',
    install_requires=[
        'Click',
        'primehub-python-sdk',
        'prettytable'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'primehub-remote-deploy = primehub_remote_deploy.main:main',
        ],
    },
)
