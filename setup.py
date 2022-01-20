from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.split('#', 1)[0].strip(' \t\n') for line in f
        ] if s != ''
    ]

setup(
    name='localhttps',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_reqs,
    entry_points={
        'console_scripts': [
            'localhttps = localhttps:main',
        ],
    },
)
