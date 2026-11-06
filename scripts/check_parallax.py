"""Firefox check for foreground/background scroll separation in the local preview."""
import asyncio,base64,json
from pathlib import Path
import websockets
REVIEW=Path(__file__).resolve().parents[2]/'review'
async def main():
 async with websockets.connect('ws://127.0.0.1:9224/session',max_size=30_000_000) as ws:
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
  context=(await call('browsingContext.create',{'type':'tab'}))['context']
  async def js(expression):
   r=await call('script.evaluate',dict(expression=expression,target={'context':context},awaitPromise=True))
   if r.get('type')=='exception':raise RuntimeError(r)
   return r.get('result',{}).get('value')
  result=[]
  for width in [1440,768,390]:
   await call('browsingContext.setViewport',{'context':context,'viewport':{'width':width,'height':1000}})
   await call('browsingContext.navigate',{'context':context,'url':'http://127.0.0.1:8876/website/','wait':'complete'})
   await js('document.fonts.ready.then(()=>true)')
   positions=[]
   for y in [0,180,360,540]:
    await js(f'scrollTo({{top:{y},behavior:"instant"}});new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))))')
    position=json.loads(await js('JSON.stringify({y:scrollY,hero:document.querySelector(".hero").getBoundingClientRect().toJSON(),photo:document.querySelector(".hero-photo").getBoundingClientRect().toJSON(),text:document.querySelector(".hero-text").getBoundingClientRect().toJSON(),shift:parseFloat(document.querySelector(".hero").style.getPropertyValue("--hero-shift")),width:innerWidth,scrollWidth:document.documentElement.scrollWidth})'))
    assert position['scrollWidth']<=width,position
    if width>560:
     assert position['photo']['top']<=max(0,position['hero']['top'])+.5,position
     assert position['photo']['bottom']>=min(1000,position['hero']['bottom'])-.5,position
    else:assert position['shift']==0,position
    positions.append(position)
    if width==1440 and y in [0,360]:
     screenshot=await call('browsingContext.captureScreenshot',{'context':context,'origin':'viewport'})
     (REVIEW/f'parallax-{width}-scroll-{y}.png').write_bytes(base64.b64decode(screenshot['data']))
   if width>560:
    dy=positions[2]['y']-positions[1]['y']
    assert abs((positions[1]['photo']['top']-positions[2]['photo']['top'])/dy-.65)<.02,positions
    assert abs((positions[1]['text']['top']-positions[2]['text']['top'])/dy-1)<.02,positions
    # Exercise the JS reduced-motion branch without changing the user's browser preferences.
    await js('Object.defineProperty(motion,"matches",{value:true,configurable:true});updateHero();true')
    assert await js('parseFloat(hero.style.getPropertyValue("--hero-shift"))')==0
   result.append(dict(width=width,positions=positions,passed=True))
  (REVIEW/'parallax-checks.json').write_text(json.dumps(result,indent=2))
  print('PASS Firefox: distinct foreground/background speeds, no exposed edges or horizontal overflow, stationary phones and reduced-motion branch.')
  await call('session.end',{})
asyncio.run(main())
