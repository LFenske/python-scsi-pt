from distutils.core import setup
setup(
    name='scsi_pt',
    version='0.1.2',
    description='Python SCSI Toolkit',
    long_description='a set of classes to create and send SCSI CDBs through libsgutils using templates to create CDBs and data out and to interpret data in',
    license='LICENSE.txt',
    py_modules=['ScsiPT', 'Cmd', 'CDB', ],
    author="Larry Fenske",
    author_email="pypi@towanda.com",
    url="https://github.com/LFenske/python-scsi-pt",
    scripts=['settime', ],
    provides=['scsi_pt', 'ScsiPT', 'Cmd', 'CDB', ],
    install_requires=['listdict', ],
)
