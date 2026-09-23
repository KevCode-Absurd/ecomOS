"""Wall-clock subprocess deadline, including blocked Windows stdin writes."""
import os,subprocess,threading

def run_bounded(command,input_text,timeout=300):
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    done=threading.Event();result={}
    def communicate():
        try:result['output']=process.communicate(input=input_text)
        except Exception as error:result['error']=error
        finally:done.set()
    worker=threading.Thread(target=communicate,daemon=True);worker.start()
    if not done.wait(timeout):
        process.kill()
        # Do not call communicate again: a blocked pipe can defeat its timeout.
        try:process.wait(timeout=5)
        except subprocess.TimeoutExpired:pass
        raise subprocess.TimeoutExpired(command,timeout)
    if 'error' in result:raise result['error']
    stdout,stderr=result['output']
    return subprocess.CompletedProcess(command,process.returncode,stdout,stderr)
