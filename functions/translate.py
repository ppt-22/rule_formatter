from subprocess import Popen,PIPE,STDOUT
import os

def main_translate(rule_id):
    dirname = os.path.dirname(__file__)
    one_file = os.path.join(dirname, 'one.py')
    args=["python3",one_file,rule_id]
    p = Popen(args,stdout=PIPE,stderr=STDOUT,universal_newlines=True)
    otpt = p.communicate()[0]
    print(otpt)
    p.kill()
    print("\n\033[38:5:208mPlease add 'recommended actions' and 'tags'\033[00m")