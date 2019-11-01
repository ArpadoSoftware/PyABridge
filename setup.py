from distutils.core import setup
setup(
    name='PyABridge',
    packages=['PyABridge'],
    version='1.0.3',
    license='MIT',
    description='',
    author='Arpado Software',
    author_email='support@arpado.site',
    url='https://github.com/ArpadoSoftware/PyABridge',
    download_url='https://github.com/ArpadoSoftware/PyABridge/dist/PyABridge-1.0.tar.gz',
    keywords=['VST', 'MIDI', 'AUDIO', 'ABRIDGE', 'ARPADO'],
    install_requires=[
        'PyDispatcher'
    ],
    package_dir={'PyABridge': 'PyABridge'},
    data_files=[('.', [
        'PyABridge/_ABridgeAdapter.pyd',
        'PyABridge/_ABridgeAdapter.so',
        'PyABridge/libwinpthread-1.dll',
    ])],
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
    include_package_data=True
)
