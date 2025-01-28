from fastapi import FastAPI, Request
import uvicorn
import hashlib

def split_repo_string(input_string):
    # Initialize default values
    repo_url = None
    branch_name = "master"
    tool_name = None

    parts = input_string.rsplit('.', 1)
    tool_name = parts[-1]

    if len(parts) == 1:
        return None, None, tool_name

    if len(parts) == 2:
        repo_url = parts[0]
        repoparts = repo_url.split('#')
        if len(repoparts) == 2:
            repo_url = repoparts[0]
            branch_name = repoparts[1]
        elif len(repoparts) == 1:
            repo_url = repoparts[0]
        else :
            raise ValueError("Invalid repo url")
        return repo_url, branch_name, tool_name
    
def generateHash(repo_url, branch_name, tool_name):
    hash_input = f"{repo_url}#{branch_name}.{tool_name}"
    hash_object = hashlib.md5(hash_input.encode())
    return hash_object.hexdigest()

def handleOpenAIRequest(model: str, tools:list,payload: dict):
    messages = payload.get('messages', [])
    print(messages)
    for tool in tools:
        print(split_repo_string(tool['source']))
    reqPayload = {
        "model": model,
        "messages": messages
    }
    return reqPayload


def runAgent(agentData: dict):
    app = FastAPI()
    @app.post('/chat')
    async def conversations(payload: dict):
        if agentData['modelProvider'] == 'openai':
            reqPayload = handleOpenAIRequest(model=agentData["model"], tools=agentData["tools"],payload=payload)
        return reqPayload
        
    uvicorn.run(app, host="0.0.0.0", port=3000)