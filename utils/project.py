import inspect
import os
import subprocess


def root_dir():
    return os.path.normpath(
        os.path.join(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
            '..'))


def run_script(path, args):
    subprocess.run(['python', path, *args], cwd=root_dir())
