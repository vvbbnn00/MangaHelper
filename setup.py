from setuptools import setup

setup(
    name='MangaHeper',
    version='v0.1',
    packages=['proj_manga'],
    url='https://www.vvbbnn00.top',
    license='GNU General Public License',
    author='不做评论',
    author_email='vvbbnn00@foxmail.com',
    description='解析漫画网站的漫画，下载并保存为pdf格式，发送至kindle',
    include_package_data=True,
    install_requires=['flask'],
)
