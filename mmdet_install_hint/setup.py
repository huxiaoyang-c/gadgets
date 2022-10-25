from setuptools import setup, find_packages

setup(
    name='mmdet_install_hint',
    version='0.0.1',
    author='huxiaoyang',
    author_email='545960442@qq.com',

    install_requires=['requests', 'beautifulsoup4', 'lxml', 'tabulate'],

    entry_points={
      'console_scripts': [
          'mmdet_install_hint = mmdet_install_hint.mmdet_install_hint:main'
      ]
    },

    packages=find_packages()
)



