from setuptools import setup

setup(
    name='gallery2smugmug',
    version='0.1',
    py_modules=['gallery2smugmug'],
    entry_points='''
        [console_scripts]
        gallery2smugmug=g2s.gallery2smugmug:cli
    ''',
)
