"""Check the static interior pages in Firefox using the existing local BiDi listener."""
import asyncio,base64,json
from pathlib import Path
import websockets
ROOT=Path(__file__).resolve().parents[1];REVIEW=ROOT.parent/'review'
PAGES=['o-mne.html','zachranene-vianoce.html','zamatovy-jez.html','mimoza.html','novinky.html']
async def main():
 async with websockets.connect('ws://127.0.0.1:9224/session',max_size=40_000_000) as ws:
  serial=0
  async def call(method,params):
   nonlocal serial
   serial+=1;await ws.send(json.dumps(dict(id=serial,method=method,params=params)))
   while True:
    r=json.loads(await ws.recv())
    if r.get('id')==serial:
     if r.get('type')=='error':raise RuntimeError(r)
     return r.get('result')
  await call('session.new',{'capabilities':{}})
  try:
   context=(await call('browsingContext.create',{'type':'tab'}))['context']
   errors=[]
   async def js(expression):
    r=await call('script.evaluate',dict(expression=expression,target={'context':context},awaitPromise=True))
    if r.get('type')=='exception':raise RuntimeError(r)
    return r.get('result',{}).get('value')
   results=[]
   for page in PAGES:
    for width in [360,390,768,1280,1440]:
     await call('browsingContext.setViewport',{'context':context,'viewport':{'width':width,'height':1000}})
     await call('browsingContext.navigate',{'context':context,'url':'http://127.0.0.1:8876/website/'+page+'?review=pages-v3','wait':'complete'})
     await js('document.fonts.ready.then(()=>true)')
     await js('window.pageErrors=[];addEventListener("error",e=>pageErrors.push(e.message));true')
     await js('Promise.all([...document.images].map(i=>{i.loading="eager";return i.decode().catch(()=>null)})).then(()=>true)')
     await js('scrollTo({top:300,behavior:"instant"});new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))))')
     state=json.loads(await js('JSON.stringify({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,broken:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),h1:document.querySelectorAll("h1").length,current:[...document.querySelectorAll("nav a[aria-current]")].map(a=>a.getAttribute("href")),nav:[...document.querySelectorAll("nav a")].map(a=>a.getAttribute("href")),errors:pageErrors,overflow:[...document.querySelectorAll("main *")].filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>({tag:e.tagName,cls:e.className,right:e.getBoundingClientRect().right}))})'))
     assert state['scrollWidth']<=width,(page,state)
     assert not state['broken'],(page,state)
     alphas=json.loads(await js('JSON.stringify([...document.images].filter(i=>i.src.endsWith(".avif")).map(img=>{const c=document.createElement("canvas");c.width=img.naturalWidth;c.height=img.naturalHeight;const ctx=c.getContext("2d");ctx.drawImage(img,0,0);return ctx.getImageData(0,0,1,1).data[3];}))'))
     assert all(alpha==0 for alpha in alphas),(page,alphas)
     assert state['h1']==1,(page,state)
     assert state['current']==[page],(page,state)
     assert not any(link.startswith('http') for link in state['nav']),(page,state)
     assert not state['errors'],(page,state)
     if width<=768:
      await js('document.querySelector(".menu-toggle").click();true')
      assert await js('document.querySelector(".menu-toggle").getAttribute("aria-expanded")')=='true'
      await js('document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape"}));true')
      assert await js('document.querySelector(".menu-toggle").getAttribute("aria-expanded")')=='false'
     if width in [390,1440]:
      await js('scrollTo({top:0,behavior:"instant"});true')
      shot=await call('browsingContext.captureScreenshot',{'context':context,'origin':'document'})
      (REVIEW/f'{Path(page).stem}-{width}-full.png').write_bytes(base64.b64decode(shot['data']))
     results.append(dict(page=page,**state))
   # Follow the home page's actual navigation, including its book cards.
   await call('browsingContext.navigate',{'context':context,'url':'http://127.0.0.1:8876/website/?review=interior-pages','wait':'complete'})
   for filename in PAGES:
    assert await js('!!document.querySelector('+json.dumps('nav a[href="'+filename+'"]')+')'), (filename,await js('JSON.stringify([...document.querySelectorAll("nav a")].map(a=>a.href))'))
   for filename in PAGES[1:4]:
    assert await js('!!document.querySelector('+json.dumps('.book-card a[href="'+filename+'"]')+')')
   # Source copy, including every reason, review and paragraph, must survive the rebuild.
   data=json.loads((ROOT/'content/pages.json').read_text())
   mapping=dict(about='o-mne.html',christmas='zachranene-vianoce.html',hedgehog='zamatovy-jez.html',mimosa='mimoza.html')
   def texts(value):
    if isinstance(value,str):yield value
    elif isinstance(value,list):
     for item in value:yield from texts(item)
    elif isinstance(value,dict):
     for item in value.values():yield from texts(item)
   for key,filename in mapping.items():
    await call('browsingContext.navigate',{'context':context,'url':'http://127.0.0.1:8876/website/'+filename+'?review=pages-v3','wait':'complete'})
    body=await js('document.querySelector("main").textContent')
    for text in texts(data[key]):
     assert ' '.join(text.split()) in ' '.join(body.split()),(filename,text[:80])
   (REVIEW/'interior-page-checks.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
   print('PASS Firefox: five pages × five viewport widths, local navigation and book links, current-page markers, source copy, images, no overflow or scroll errors, mobile menu and Escape.')
  finally:
   await call('session.end',{})
asyncio.run(main())
