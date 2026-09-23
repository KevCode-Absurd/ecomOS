"""Isolated HTTP helper; stdout is consumed privately by the parent, never logged."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.runtime'),str(ROOT/'scripts')]
def main():
    args=json.load(sys.stdin)
    import requests
    from check_providers import settings
    destinations={'deepseek':('https://api.deepseek.com/chat/completions','DEEPSEEK_API_KEY'),'openai':('https://api.openai.com/v1/chat/completions','OPENAI_API_KEY'),'openai-embedding':('https://api.openai.com/v1/embeddings','OPENAI_API_KEY')}
    destinations['openai-responses']=('https://api.openai.com/v1/responses','OPENAI_API_KEY')
    url,key=destinations[args['provider']]
    response=requests.post(url,headers={'Authorization':'Bearer '+settings()[key]},json=args['payload'],timeout=(15,240),allow_redirects=False)
    if response.status_code!=200:
        try: detail=response.json().get('error',{})
        except ValueError: detail={}
        print(json.dumps({'status':response.status_code,'error_code':detail.get('code'),'error_param':detail.get('param'),'error_message':str(detail.get('message',''))[:350]}));return
    print(json.dumps({'status':200,'body':response.json()}))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'error_type':type(e).__name__}));sys.exit(1)
