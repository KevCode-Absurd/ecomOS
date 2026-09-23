"""Read-only authentication checks; never prints keys or raw error responses."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.runtime'))

def settings():
    result={}
    for line in (ROOT/'.env').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key,value=line.split('=',1)
            result[key.strip()]=value.strip().strip('\"').strip("'")
    return result

def main():
    import requests
    config=settings()
    checks=[]
    for name,url,key,candidates in [
        ('openai','https://api.openai.com/v1/models','OPENAI_API_KEY',['gpt-5.6-terra','gpt-5.6-sol','gpt-5.6-luna','gpt-5.4-mini','text-embedding-3-small']),
        ('deepseek','https://api.deepseek.com/models','DEEPSEEK_API_KEY',['deepseek-flash','deepseek-chat','deepseek-reasoner'])]:
        row={'provider':name}
        if not config.get(key):
            row['status']='missing_key'
        else:
            try:
                response=requests.get(url,headers={'Authorization':'Bearer '+config[key]},timeout=30,allow_redirects=False)
                row['http_status']=response.status_code
                if response.status_code==200:
                    models=[x['id'] for x in response.json().get('data',[])]
                    row.update(status='authenticated',candidate_models_available=[m for m in candidates if m in models],model_count=len(models))
                else:
                    row['status']='not_verified'
            except Exception as error:
                row.update(status='connection_failed',error_type=type(error).__name__)
        checks.append(row)
    (ROOT/'data/provider-check.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    print(json.dumps(checks))

if __name__=='__main__':
    main()
