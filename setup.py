from setuptools import setup


setup(
    name='busta',
    version='0.1',
    description='Build static bundles',
    long_description='Build static bundles for JS, CSS, images and templates.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
    ],
    url='http://github.com/dreadatour/busta',
    author='Vladimir Rudnyh',
    author_email='dreadatour@gmail.com',
    license='MIT',
    package_dir={
        '': 'src'
    },
    packages=['busta'],
    entry_points={
        'console_scripts': [
            'busta=busta.command_line:main'
        ],
    },
    zip_safe=False
)
