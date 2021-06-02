import glob
from pathlib import Path
import subprocess
import re
import os

env = os.environ.copy()
files = glob.glob("*.cpp")
mm_regex = re.compile(r'([\w\/]+\.h)')

def determine_deps(file):
    mm = subprocess.check_output(['g++', '-MM', file, '-Iother_includes'], env=env).decode('utf-8')
    ret = mm_regex.findall(mm)
    print("getting deps for " + file)
    return { 'file_dep': ret }

def task_determine_dependencies():
    for file in files:
        yield {
            'name': file,
            'actions': [(determine_deps, [file])],
            'file_dep': [file]
        }

def task_compile():
    """I'm gonna try and compile stuff hot stuff"""
    
    yield {
        'basename': 'compile_x',
        'name': None,
        'doc': 'builds file x'
    }

    for file in files:
        yield {
            'name'    : file,
            'actions' : [f"g++ -c {file} -Iother_includes"],
            'file_dep': [file],
            'calc_dep': ["determine_dependencies:" + file],
            'targets' : [Path(file).with_suffix('.o')]
        }