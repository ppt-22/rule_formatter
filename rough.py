import yaml
import os
from script_utils import get_data, check_last_update

# dirname = os.path.dirname(__file__)
# yaml_file = os.path.join(dirname, 'config.yaml')
# with open(yaml_file,'r') as f:
#     df = yaml.safe_load(f,)
#     rt_path = df['rt_path']
#     directory_path = df['directory_path']

# get_data()
check_last_update()