from fastapi import FastAPI, Request
import uvicorn


class ToolRunner:
    def __init__(self, Tool, **kargs):
      self.tool = Tool(**kargs)
      self.app = FastAPI()
      self.funcHash = {}
      self.generateFuncHash()
      self.setupRoutes()

    def run(self):
      uvicorn.run(self.app, host="0.0.0.0", port=3000)

    def generateFuncHash(self):
      for param in dir(self.tool):
        if param.startswith('__'):
          continue
        if callable(getattr(self.tool, param)):
          fun = getattr(self.tool, param)
          self.funcHash[fun.__kl__name__] = fun

    def setupRoutes(self):
      @self.app.get('/functions')
      def functions():
          functions_list = []
          for action in self.funcHash:
            functions_list.append({
              'name': action,
              'description': self.funcHash[action].__kl__doc__,
              'parameters': self.funcHash[action].__kl__parameters__,
              'required': self.funcHash[action].__kl__required__
            })
          return {
              'functions': functions_list
            }

      @self.app.post('/trigger')
      async def trigger(data: dict):
          function_name = data['function_name']
          kwargs = data.get('arguments', {})
          if not function_name:
            return {'error': 'function_name is required'}, 400
          func = self.funcHash.get(function_name)
          if not func:
            return {'error': f'Function {function_name} not found'}, 404
          if not callable(func):
            return {'error': f'{function_name} is not callable'}, 400
          try:
            result = func(**kwargs)
          except Exception as e:
            return {'error': str(e)}, 500
          return {'result': result}