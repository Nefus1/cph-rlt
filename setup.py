import os
from fnmatch import fnmatchcase

from setuptools import setup, find_namespace_packages

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')


def find_package_data(where='.', package='', exclude=standard_exclude,
                      exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(os.path.normpath(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                if any(fnmatchcase(name, p) or fn.lower() == p.lower() for p in exclude_directories):
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    new_package = name if not package else package + '.' + name
                    stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                if any(fnmatchcase(name, p) or fn.lower() == p.lower() for p in exclude):
                    continue
                out.setdefault(package, []).append(prefix + name)
    return out


setup(
    name='docassemble.cphrlt',
    version='1.0.0',
    description='California joint (married couple) revocable living trust questionnaire.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='',
    author_email='',
    license='Proprietary',
    url='https://github.com/nefus1/cph-rlt',
    packages=find_namespace_packages(include=['docassemble.*']),
    install_requires=[],
    zip_safe=False,
    package_data=find_package_data(where='docassemble/cphrlt/', package='docassemble.cphrlt'),
)
