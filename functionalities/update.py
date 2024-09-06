import os
import subprocess

def main_update():
    dirname = os.path.dirname(__file__)
    dirname = os.path.join(dirname,'..')
    subprocess.run(["git", "checkout", "main"], cwd=dirname)
    subprocess.run(["git", "pull"], cwd=dirname)