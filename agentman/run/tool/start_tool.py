import yaml
import os
import importlib.util
from .tool import ToolRunner
from fastapi import FastAPI
import uvicorn

def runAllTools():
  am_folder_path = '.am'
  if not os.path.exists(am_folder_path):
    raise FileNotFoundError(f"The folder '{am_folder_path}' does not exist.")

  # Specify the path to your YAML files
  tools_yaml_file_path = os.path.join(am_folder_path, 'tools.yaml')
  if not os.path.exists(tools_yaml_file_path):
    tools_yaml_file_path = os.path.join(am_folder_path, 'tools.yml')

  # Open the YAML files and load their content
  with open(tools_yaml_file_path, 'r') as tools_file:
    tools_list = yaml.safe_load(tools_file)

  # Transform lists into dictionaries with names as keys
  tools = {item['name']: item for item in tools_list}


  # Now `tools` contains the parsed YAML content as Python dictionaries
  # tool_name = os.getenv('TOOL_NAME', 'GmailTool')
  mainApp = FastAPI()
  for tool_name in tools:
    tool_info = tools[tool_name]
    module_name, class_name = tool_info['tool'].rsplit('.', 1)
    spec = importlib.util.find_spec(module_name)
    if spec is None:
      raise ImportError(f"Module '{module_name}' not found.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tool_class = getattr(module, class_name)

    toolRunner = ToolRunner(tool_class)
    mainApp.mount(f'/{tool_name}', toolRunner.app)
  uvicorn.run(mainApp, host="0.0.0.0", port=3000)

def run(tool_name:str):
  am_folder_path = '.am'
  if not os.path.exists(am_folder_path):
    raise FileNotFoundError(f"The folder '{am_folder_path}' does not exist.")

  # Specify the path to your YAML files
  tools_yaml_file_path = os.path.join(am_folder_path, 'tools.yaml')
  if not os.path.exists(tools_yaml_file_path):
    tools_yaml_file_path = os.path.join(am_folder_path, 'tools.yml')

  # Open the YAML files and load their content
  with open(tools_yaml_file_path, 'r') as tools_file:
    tools_list = yaml.safe_load(tools_file)

  # Transform lists into dictionaries with names as keys
  tools = {item['name']: item for item in tools_list}


  # Now `tools` contains the parsed YAML content as Python dictionaries
  # tool_name = os.getenv('TOOL_NAME', 'GmailTool')
  tool_info = tools[tool_name]
  module_name, class_name = tool_info['tool'].rsplit('.', 1)

  # print(module_name, class_name)

  spec = importlib.util.find_spec(module_name)
  if spec is None:
    raise ImportError(f"Module '{module_name}' not found.")
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  tool_class = getattr(module, class_name)

  toolRunner = ToolRunner(tool_class)
  toolRunner.run()