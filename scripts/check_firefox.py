import asyncio,json,base64
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT.parent / "review"
REVIEW.mkdir(exist_ok=True)
import websockets
async def main():
 async with websockets.connect('ws://127.0.0.1:9224/session',max_size=30_000_000) as ws:
  ident=0
  async def call(method,params):
   nonlocal ident
   ident+=1;await ws.send(json.dumps({'id':ident,'method':method,'params':params}))
   while True:
    r=json.loads(await ws.recv())
    if r.get('id')==ident:
     if r.get('type')=='error':raise RuntimeError(r)
     return r.get('result')
  print(await call('session.new',{'capabilities':{}}))
  context=(await call('browsingContext.create',{'type':'tab'}))['context']
  async def evaluate(expression):
   r=await call('script.evaluate',{'expression':expression,'target':{'context':context},'awaitPromise':True})
   return r.get('result',{}).get('value')
  results=[]
  for width in [360,390,768,1280,1440]:
   await call('browsingContext.setViewport',{'context':context,'viewport':{'width':width,'height':1000}})
   await call('browsingContext.navigate',{'context':context,'url':'http://127.0.0.1:8876/website/','wait':'complete'})
   await evaluate('document.fonts.ready.then(()=>true)')
   await evaluate('Promise.all([...document.images].map(i=>{i.loading="eager";return i.decode().catch(()=>null)})).then(()=>true)')
   result=json.loads(await evaluate('JSON.stringify({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,brokenImages:[...document.images].filter(i=>i.naturalWidth===0).map(i=>i.src),font:getComputedStyle(document.body).fontFamily,fontsLoaded:document.fonts.status,navVisible:getComputedStyle(document.querySelector("nav")).display})'))
   assert result['scrollWidth']<=result['width'],result
   assert not result['brokenImages'],result
   if width<=768:
    assert await evaluate('document.querySelector(".menu-toggle").click();document.querySelector(".menu-toggle").getAttribute("aria-expanded")')=='true'
    assert await evaluate('getComputedStyle(document.querySelector("nav")).display')=='flex'
    await evaluate('document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));true')
    assert await evaluate('document.querySelector(".menu-toggle").getAttribute("aria-expanded")')=='false'
   results.append(result)
   if width in [390,1440]:
    shot=await call('browsingContext.captureScreenshot',{'context':context,'origin':'document'})
    (REVIEW / f'home-{width}-full.png').write_bytes(base64.b64decode(shot['data']))
  await evaluate('document.querySelector("[data-open-book]").click();true')
  await asyncio.sleep(.4)
  assert await evaluate('document.querySelector("dialog").open') is True
  assert await evaluate('document.querySelector("[data-collection-copy]").textContent.includes("Coddington")') is True
  await evaluate('document.querySelector(".dialog-close").click();true')
  assert await evaluate('document.querySelector("dialog").open') is False
  assert await evaluate('document.activeElement.hasAttribute("data-open-book")') is True
  results.append({'mobile_menu':'passed','dialog_and_focus_return':'passed'})
  (REVIEW / 'browser-checks.json').write_text(json.dumps(results,indent=2))
  print(json.dumps(results,indent=2))
  await call('session.end',{})
asyncio.run(main())
