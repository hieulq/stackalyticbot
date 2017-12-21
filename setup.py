from setuptools import setup

setup(
    name='stackalyticbot',
    version='1.0.0',
    description='StackAlytic Bot for Telegram.',
    author='Hieu LE',
    author_email='sudo@rm-rf.cloud',
    license='Apache-2.0',
    url='https://github.com/hieulq/stackalyticbot/',
    packages=['telebot'],
    include_package_data=True,
    install_requires=[
        'telepot',
        'apscheduler',
        'python-telegram-telebot',
        'python-crontab',
        'pytz',
        'xlsxwriter',
        'emoji',
        'prettytable'
    ],
)
