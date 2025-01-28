import os
import yaml
from .agent_runner import runAgent

def run(agent_name:str):
  am_folder_path = '.am'
  if not os.path.exists(am_folder_path):
    raise FileNotFoundError(f"The folder '{am_folder_path}' does not exist.")

  # Specify the path to your YAML files
  agents_yaml_file_path = os.path.join(am_folder_path, 'agents.yaml')
  if not os.path.exists(agents_yaml_file_path):
    agents_yaml_file_path = os.path.join(am_folder_path, 'agents.yml')

  # Open the YAML files and load their content
  with open(agents_yaml_file_path, 'r') as agents_file:
    agents_list = yaml.safe_load(agents_file)

  # Transform lists into dictionaries with names as keys
  agents = {item['name']: item for item in agents_list}
  
  runAgent(agents[agent_name])