
 const D=JSON.parse(document.getElementById('dataset').textContent),$=id=>document.getElementById(id),models=['gpt-5.6-luna','gpt-5.6-terra','gpt-5.6-sol'],methods=['none','raw','selected'];
 function pre(text){let e=document.createElement('pre');e.textContent=typeof text==='string'?text:JSON.stringify(text,null,2);return e;}
 function detail(parent,title,value){let d=document.createElement('details'),s=document.createElement('summary');s.textContent=title;d.append(s,pre(value));parent.append(d);}
 D.tasks.forEach(t=>$('task').add(new Option(t.id+' — '+t.title,t.id)));
 for(const side of ['left','right'])for(const m of models)for(const method of methods)$(side).add(new Option(m+' / '+method,m+'|'+method));
 $('left').value='gpt-5.6-terra|none';$('right').value='gpt-5.6-terra|selected';
 $('overview').textContent=JSON.stringify(D.summary,null,2);$('brand').textContent=JSON.stringify({brand:D.brand,system:D.system},null,2);
 function render(){let tid=$('task').value,t=D.tasks.find(t=>t.id===tid),p=D.packets[tid];$('tasktitle').textContent=t.title;$('taskrequest').textContent=t.request;
 $('retrieval').textContent=JSON.stringify({queries:t.queries,raw_cards:p.raw_ids.length,selected_cards:p.selected_ids.length,raw_tokens:p.raw_tokens,selected_tokens:p.selected_tokens,search_ms:p.search_ms,selection_seconds:p.selection.seconds,selection:p.selection.output,audit:D.audits[tid]?.result?.output,keyword_ms:D.audits[tid]?.keyword_ms,cached_hybrid_ms:D.audits[tid]?.cached_hybrid_ms},null,2);
 $('cardlist').replaceChildren();for(const id of p.raw_ids){let x=D.cards[id];detail($('cardlist'),(p.selected_ids.includes(id)?'SELECTED · ':'EXCLUDED · ')+x.card.title+' ['+id+']',x);}
 for(const side of ['left','right']){let [model,method]=$(side).value.split('|'),r=D.runs[tid+'-'+model+'-'+method],box=$(side+'panel'),call=r.trace[$('stage').value];box.replaceChildren();
 detail(box,'Step 3: exact input sent to this model',{system:D.system,input:call.input});
 detail(box,'Metrics: tokens, costs, retrieval and total latency',r.metrics);
 detail(box,'Cards in this context ('+r.trace.card_ids.length+')',r.trace.card_ids.map(id=>({id,title:D.cards[id].card.title})));
 let h=document.createElement('h3');h.textContent='Step 4: complete '+$('stage').value+' output';box.append(h,pre(call.output?.answer_markdown||call.raw_content));
 detail(box,'Structured actions, questions and self-reported card use',call.output);
 detail(box,'Step 5: sandbox checks (limited field validation)',{first:r.trace.first_validation,final:r.trace.final_validation});
 detail(box,'Step 6: business-owner and agency-owner reviews of FINAL output',r.grades);
 detail(box,'Exact provider usage and request identifiers',{request_id:call.request_id,model:call.model,effort:call.effort,usage:call.usage,finish_reason:call.finish_reason});
 if(r.trace.superseded_final)detail(box,'Preserved superseded revision (original validator; excluded from quality comparison)',r.trace.superseded_final);}}
 ['task','stage','left','right'].forEach(id=>$(id).addEventListener('change',render));render();
 