const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
function closeMenu() {menuButton.setAttribute('aria-expanded', 'false');nav.classList.remove('is-open');}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));nav.classList.toggle('is-open', open);
});
nav.addEventListener('click', event => {if (event.target.closest('a')) closeMenu();});
document.addEventListener('keydown', event => {if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {closeMenu();menuButton.focus();}});
const hero = document.querySelector('.hero');
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const mobile = matchMedia('(max-width: 560px)');
let scheduled = false;
function updateHero() {
  scheduled = false;
  if (!hero) return;
  // Once the hero reaches the viewport top, let the portrait travel at 65%
  // of the foreground's scroll speed. The exposed top edge stays offscreen,
  // so the original crop needs no enlargement to cover the visible hero.
  const distance = Math.max(0, -hero.getBoundingClientRect().top);
  const shift = motion.matches || mobile.matches ? 0 : Math.min(distance, hero.offsetHeight) * .35;
  hero.style.setProperty('--hero-shift', `${shift}px`);
}
addEventListener('scroll', () => {if (!scheduled) {scheduled = true;requestAnimationFrame(updateHero);}}, {passive: true});
addEventListener('resize', updateHero);motion.addEventListener('change', updateHero);mobile.addEventListener('change', updateHero);updateHero();
document.querySelector('[data-year]').textContent = String(new Date().getFullYear());
const bookDialog = document.querySelector('#stastne-nahody');
if (bookDialog) {
let opener;
document.querySelector('[data-open-book]').addEventListener('click', async event => {
  opener = event.currentTarget;
  const container = bookDialog.querySelector('[data-collection-copy]');
  if (!container.children.length) {
    try {
      const response = await fetch('content/stastne-nahody.json');
      if (!response.ok) throw new Error('Content unavailable');
      const paragraphs = await response.json();
      for (const text of paragraphs) {const p = document.createElement('p');p.textContent = text;container.append(p);}
    } catch {const p = document.createElement('p');p.textContent = 'Text sa nepodarilo načítať. Skúste to, prosím, znova.';container.replaceChildren(p);}
  }
  bookDialog.showModal();
});
bookDialog.querySelector('.dialog-close').addEventListener('click', () => bookDialog.close());
bookDialog.addEventListener('click', event => {if(event.target === bookDialog) {const r=bookDialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)bookDialog.close();}});
bookDialog.addEventListener('close', () => opener?.focus());

}

// Quiet, one-time entrances; content remains visible if scripting or the
// observer is unavailable. Never animate the background parallax container.
let revealObserver;
const revealedElements = new WeakSet();
const revealSelector = [
  'main h1', 'main h2', '.hero-text > p', '.book-card', '.author-copy > p',
  '.about-introduction > p', '.writing-opening', '.writing-grid > div > p:not(.booklover)',
  '.resources-grid > div > p', '.publisher-list', '.book-opening > div > p',
  '.christmas-opening > div > p', '.book-quote', '.story-card',
  '.book-reasons > .reason-list', '.article-links > ul', '.mimosa-columns > div > p',
  '.mimosa-review > p', '.contact > p', '.contact > .email-link', '.meeting-copy', '.event-card > div'
].join(',');
function finishReveal(element, immediate = false) {
  const firstEntrance = !revealedElements.has(element);
  element.classList.add('is-revealed');
  revealedElements.add(element);
  revealObserver?.unobserve(element);
  // Explicit keyframes make these featured entrances visible even when the
  // observer fires before the browser has painted the initial CSS position.
  if (firstEntrance && !immediate && !motion.matches && typeof element.animate === 'function' && element.matches('.hero h1, .book-card')) {
    const title = element.matches('.hero h1');
    const distance = title ? (mobile.matches ? 32 : 44) : (mobile.matches ? 26 : 34);
    const delay = title ? 180 : [...element.parentElement.children].indexOf(element) * 110;
    const animation = element.animate([
      {opacity: 0, transform: `translate3d(0, ${distance}px, 0)`},
      {opacity: 1, transform: 'translate3d(0, 0, 0)'}
    ], {duration: title ? 1400 : 1150, delay, easing: 'cubic-bezier(.22,.61,.36,1)', fill: 'both'});
    animation.onfinish = () => animation.cancel();
  }
}
function showAllReveals() {
  revealObserver?.disconnect();
  document.querySelectorAll('.scroll-reveal').forEach(element => {
    element.getAnimations().forEach(animation => animation.cancel());
    element.classList.remove('scroll-reveal');
    element.style.removeProperty('--reveal-delay');
  });
}
function setupScrollReveals() {
  showAllReveals();
  if (motion.matches || !('IntersectionObserver' in window)) return;
  const candidates = [...document.querySelectorAll(revealSelector)];
  // A panel and its heading should enter together, not compound two effects.
  const elements = candidates.filter(element => !candidates.some(parent => parent !== element && parent.contains(element)));
  try {
    revealObserver = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting) finishReveal(entry.target);
    }, {threshold: .08, rootMargin: '0px 0px -40px 0px'});
    for (const element of elements) {
      if (revealedElements.has(element) || element.getBoundingClientRect().bottom < 0) continue;
      const delay = element.matches('.hero-text > p') ? 180 : element.matches('.book-card') ? [...element.parentElement.children].indexOf(element) * 70 : 0;
      element.style.setProperty('--reveal-delay', `${delay}ms`);
      element.classList.add('scroll-reveal');
      // Establish the resting start before the observer reveals visible text.
      revealObserver.observe(element);
    }
  } catch {showAllReveals();}
}
document.addEventListener('focusin', event => {
  const element = event.target.closest('.scroll-reveal');
  if (element) {element.getAnimations().forEach(animation => animation.cancel());element.classList.remove('scroll-reveal');element.style.removeProperty('--reveal-delay');finishReveal(element, true);}
});
motion.addEventListener('change', setupScrollReveals);
addEventListener('beforeprint', showAllReveals);
setupScrollReveals();
