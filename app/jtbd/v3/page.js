const q=document.getElementById('q'),sel=document.getElementById('screen'),only=document.getElementById('onlynow'),hits=document.getElementById('hits'),NS=__NS__;
let view='now';
function apply(){
  const v=q.value.trim().toLowerCase(), s=sel.value, on=only.checked; let k=0;
  document.querySelectorAll('#v-list .scr').forEach(sec=>{ const inS=!s||sec.id===s; let ks=0;
    sec.querySelectorAll('.tj').forEach(tj=>{ let kt=0; tj.querySelectorAll('.job').forEach(j=>{ const show=inS&&(!v||j.dataset.t.includes(v))&&(!on||j.dataset.now==='1'); j.classList.toggle('hide',!show); if(show)kt++; }); tj.style.display=kt?'':'none'; ks+=kt; });
    sec.style.display=ks?'':'none'; k+=ks; });
  let kn=0; document.querySelectorAll('#v-now tbody tr').forEach(r=>{ const show=(!s||r.dataset.s===s)&&(!v||r.textContent.toLowerCase().includes(v)); r.style.display=show?'':'none'; if(show)kn++; });
  let ke=0; document.querySelectorAll('#v-en .enc').forEach(c=>{ const show=(!s||c.dataset.sc.split(' ').includes(s))&&(!v||c.dataset.t.includes(v)); c.style.display=show?'':'none'; if(show)ke++; });
  document.querySelectorAll('#v-notes tbody tr').forEach(r=>{ r.style.display=(!v||r.textContent.toLowerCase().includes(v))?'':'none'; });
  document.querySelectorAll('.nav a').forEach(a=>a.classList.toggle('on',a.dataset.s===s));
  const pre=s?sel.options[sel.selectedIndex].text+': ':'';
  hits.textContent= view==='list'? pre+k+' tactical jobs'+(s?'':' across '+NS+' screens') : view==='now'? pre+kn+' start now jobs' : view==='en'? pre+ke+' enablers' : '';
  try{localStorage.setItem('jtbd3-screen',s);localStorage.setItem('jtbd3-view',view);}catch(e){}
}
function setView(x){ view=x; document.querySelectorAll('.view').forEach(el=>el.classList.toggle('on',el.id==='v-'+x)); document.querySelectorAll('.tab').forEach(b=>b.setAttribute('aria-pressed',b.dataset.v===x?'true':'false')); apply(); }
document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>{setView(b.dataset.v); window.scrollTo({top:0});}));
q.addEventListener('input',apply); only.addEventListener('change',apply);
sel.addEventListener('change',()=>{apply(); window.scrollTo({top:0});});
document.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault(); sel.value=a.dataset.s; if(view!=='list'&&view!=='now'&&view!=='en') setView('list'); apply(); window.scrollTo({top:0});}));
document.addEventListener('click',ev=>{
  const jl=ev.target.closest('.jl'); if(jl){ ev.preventDefault(); q.value=''; only.checked=false; sel.value=jl.dataset.s; setView('list'); const t=document.querySelector(jl.getAttribute('href')); if(t){ t.scrollIntoView({block:'center'}); t.style.background='var(--soft)'; setTimeout(()=>t.style.background='',1600);} return; }
  const en=ev.target.closest('.en'); if(en){ ev.preventDefault(); q.value=''; sel.value=''; setView('en'); const t=document.getElementById('en-'+en.dataset.en); if(t){ t.scrollIntoView({block:'start'}); t.style.borderColor='var(--accent)'; setTimeout(()=>t.style.borderColor='',1600);} }
});
(function(){ let s='',vw='now'; try{s=localStorage.getItem('jtbd3-screen')||''; vw=localStorage.getItem('jtbd3-view')||'now';}catch(e){} if([...sel.options].some(o=>o.value===s)) sel.value=s; setView(['now','list','en','notes'].includes(vw)?vw:'now'); })();
