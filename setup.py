from distutils.core import setup
setup(
    name='scsi_pt',
    version='0.1.1',
    license='LICENSE.txt',
    py_modules=['ScsiPT', 'Cmd', 'CDB', ],
    scripts=['settime', ],
    provides=['scsi_pt', 'ScsiPT', 'Cmd', 'CDB', ],
    install_requires=['listdict', ],
)
