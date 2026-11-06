"""Firefox QA: once-only entrances, portrait replacement, fallbacks and focus."""
import asyncio,base64,json
from pathlib import Path
import websockets
ROOT=Path(__file__).resolve().parents[1];REVIEW=ROOT.parent/'review'
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
   await call('script.addPreloadScript',{'functionDeclaration':'()=>{window.runtimeErrors=[];addEventListener("error",e=>runtimeErrors.push(e.message));}'})
   async def js(expression):
    r=await call('script.evaluate',dict(expression=expression,target={'context':context},awaitPromise=True))
    if r.get('type')=='exception':raise RuntimeError(r)
    return r.get('result',{}).get('value')
   async def settle():await js('new Promise(resolve=>setTimeout(()=>resolve(true),1800))')
   async def frames():await js('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))))')
   await call('browsingContext.setViewport',{'context':context,'viewport':{'width':1440,'height':1000}})
   await call('browsingContext.navigate',{'context':context,'url':'http://127.0.0.1:8876/website/?review=entrances-v1','wait':'complete'})
   await frames()
   assert await js('document.querySelector(".hero h1").classList.contains("scroll-reveal")')
   await settle()
   assert await js('Number(getComputedStyle(document.querySelector(".hero h1")).opacity)')==1
   assert await js('!document.querySelector(".hero-photo").classList.contains("scroll-reveal")')
   assert await js('!document.querySelector(".author-copy h2").classList.contains("is-revealed")')
   await js('document.querySelector(".author-copy h2").scrollIntoView({block:"center",behavior:"instant"});true')
   await frames();await settle()
   assert await js('document.querySelector(".author-copy h2").classList.contains("is-revealed")')
   assert await js('Number(getComputedStyle(document.querySelector(".author-copy h2")).opacity)')==1
   await js('document.querySelector(".author-portrait").decode().then(()=>true)')
   portrait=json.loads(await js('JSON.stringify({src:document.querySelector(".author-portrait").getAttribute("src"),width:document.querySelector(".author-portrait").naturalWidth,height:document.querySelector(".author-portrait").naturalHeight})'))
   assert portrait['src'].endswith('author-reading-dsc9346.avif') and (portrait['width'],portrait['height'])==(794,989),portrait
   await js('scrollTo({top:0,behavior:"instant"});true');await frames()
   assert await js('Number(getComputedStyle(document.querySelector(".author-copy h2")).opacity)')==1
   # Starting a fresh page, tab/focus into an unrevealed card: no invisible control.
   await call('browsingContext.navigate',{'context':context,'url':'http://127.0.0.1:8876/website/?review=entrances-focus','wait':'complete'})
   await js('document.querySelector(".book-card a").focus({preventScroll:true});true')
   assert await js('Number(getComputedStyle(document.querySelector(".book-card")).opacity)')==1
   # Runtime preference changes must reveal everything and stop parallax.
   await js('Object.defineProperty(motion,"matches",{value:true,configurable:true});setupScrollReveals();updateHero();true')
   assert await js('document.querySelectorAll(".scroll-reveal").length')==0
   assert await js('parseFloat(hero.style.getPropertyValue("--hero-shift"))')==0
   # An unsupported observer also leaves the site completely readable.
   await js('Object.defineProperty(motion,"matches",{value:false,configurable:true});window.IntersectionObserver=undefined;setupScrollReveals();true')
   assert await js('document.querySelectorAll(".scroll-reveal").length')==0
   results=[]
   for filename in ['index.html','o-mne.html','zachranene-vianoce.html','zamatovy-jez.html','mimoza.html','novinky.html']:
    for width in [390,1440]:
     await call('browsingContext.setViewport',{'context':context,'viewport':{'width':width,'height':1000}})
     await call('browsingContext.navigate',{'context':context,'url':'http://127.0.0.1:8876/website/'+filename+'?review=entrances-qa','wait':'complete'})
     await js('document.fonts.ready.then(()=>true)');await settle()
     assert await js('Number(getComputedStyle(document.querySelector("main h1")).opacity)')==1
     assert await js('document.documentElement.scrollWidth<=innerWidth')
     assert await js('JSON.stringify(runtimeErrors)')=='[]'
     # Full-page review captures the final appearance, not hidden offscreen entrances.
     await js('showAllReveals();Promise.all([...document.images].map(i=>{i.loading="eager";return i.decode().catch(()=>null)})).then(()=>true)')
     shot=await call('browsingContext.captureScreenshot',{'context':context,'origin':'document'})
     (REVIEW/f'{Path(filename).stem}-entrances-{width}.png').write_bytes(base64.b64decode(shot['data']))
     results.append(dict(page=filename,width=width,passed=True))
   (REVIEW/'entrance-checks.json').write_text(json.dumps(dict(portrait=portrait,layouts=results,once_only=True,keyboard_focus=True,reduced_motion=True,observer_fallback=True),indent=2))
   print('PASS Firefox: replacement portrait, once-only entrances, keyboard focus, reduced-motion/observer fallback, six pages at phone/desktop widths and no browser errors.')
  finally:await call('session.end',{})
asyncio.run(main())
