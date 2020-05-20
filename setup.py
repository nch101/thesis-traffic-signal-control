try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = [
    'description': 'traffic-light-project',
    'author': 'Nguyen Cong Huy',
    'git repository': 'https://github.com/nch101/py-project.git',
    'author_email': 'huynguyencong98@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'python-socketio', 'python-dotenv', 'urllib3[secure]'],
    'packages': ['traffic-light'],
    'scripts': [],
    'name': 'py-project'
]

setup(**config)