from setuptools import setup

setup(name='ud-toolkit',
      version='0.0.2',
      description='NLP toolkit built around UDPipe.',
      url='http://github.com/eivindbergem/ud-toolkit',
      author='Eivind Alexander Bergem',
      author_email='eivind.bergem@gmail.com',
      license='GPL',
      packages=['udtk'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
          'ufal.udpipe==1.2.*',
          'tqdm'
      ])
