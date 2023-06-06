import configparser
import re

config = configparser.ConfigParser()
config.read('.env',encoding='utf-8')
envs = config['env']

for i in envs:
    if envs[i][0] == '"' and envs[i][-1] == '"':
        envs[i] = envs[i][1:-1]
    elif envs[i][0] == "'" and envs[i][-1] == "'":
        envs[i] = envs[i][1:-1]

    if re.search(r'\$\{(.*)\}',envs[i]):
        envs[i] = re.sub(r'\$\{(.*)\}',lambda x:envs[x.group(1)],envs[i])

def env(key,default=None):
    global envs
    if key in envs:
        if envs[key].lower() == 'true':
            return True
        
        if envs[key].lower() == 'false':
            return False
        
        
        return envs[key]
    
    return default