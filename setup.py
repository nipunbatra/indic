from distutils.core import setup

setup(
    name='indic',
    version='0.1.1',
    author='Nipun Batra',
    author_email='nipunb@iiitd.ac.in',
    packages=['indic'],
    scripts=[],
    url='https://github.com/nipunreddevil/indic',
    license='',
    description='Non Intrusive Load Monitoring',
    install_requires=[
        'numpy>=1.7', 'pandas>=0.12', 'matplotlib>=1.3', 'scikit-learn>=0.13', 'scipy>=0.13'

    ],
)
