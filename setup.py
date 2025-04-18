from setuptools import setup, find_packages

setup(
    name='scAnnI',
    version='0.1.2025',
    description='Toolkit AI-powered per penetration testing',
    author='Kita69',
    url='https://github.com/kita69/scAnnI',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'rich>=13.3.5',
        'fpdf>=1.7.2',
        'matplotlib>=3.7.0',
        'requests>=2.28.2',
    ],
    entry_points={
        'console_scripts': [
            'scanni = scAnnI:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Security Professionals',
        'License :: OSI Approved :: MIT License',
        'Topic :: Security :: Penetration Testing',
    ],
    python_requires='>=3.10',
)
