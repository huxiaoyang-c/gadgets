from setuptools import setup, find_packages

setup(
    name='ext_cv2',
    version='0.0.1',
    author='huxiaoyang',
    author_email='545960442@qq.com',

    install_requires=['numpy', 'opencv-python'],

    packages=find_packages()
)
