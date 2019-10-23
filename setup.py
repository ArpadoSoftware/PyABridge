from distutils.core import setup
setup(
    name='PyAbridge',
    packages=['PyAbridge'],
    version='1.0',
    license='MIT',
    description='',
    author='Arpado Software',
    author_email='support@arpado.site',
    url='https://github.com/user/reponame',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['VST', 'MIDI', 'AUDIO', 'ABRIDGE'],
    install_requires=[
        'PyDispatcher',
        'trio'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
