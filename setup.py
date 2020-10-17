from setuptools import setup

setup(
    name='MangaHeper',
    version='0.1.19',
    packages=['proj_manga'],
    url='https://www.vvbbnn00.top',
    license='GNU General Public License',
    author='不做评论',
    author_email='vvbbnn00@foxmail.com',
    description='解析漫画网站的漫画，下载并保存为pdf格式，发送至kindle',
    include_package_data=True,
    install_requires=['flask', 'bs4', 'fake_useragent', 'selenium', 'PyPDF2', 'pillow', 'requests', 'MySQL', 'gevent'],
)
