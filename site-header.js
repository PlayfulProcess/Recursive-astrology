/* Shared site header for The Recursive Astrology static site.
 * One definition, used by every page (root + viewer/). Style-isolated via
 * Shadow DOM so each page's own CSS can't override it. Path-aware so links
 * resolve from both the repo root and the /viewer/ subdir.
 *
 * Usage:  <script src="<path-to>site-header.js?v=1"></script>
 *         <site-header active="wheel"></site-header>
 * The `active` attribute highlights the matching tab; if omitted it is
 * auto-detected from the filename.
 *
 * Pattern mirrored from recursive-tarot/site-header.js (the family's pattern
 * source) — adapted here: astro branding (crescent + star), this repo's own
 * pages (Home, Wheel, Lenses, Course, Chart Viewer) plus a Grammars dropdown
 * listing every grammar in grammars/*.
 */
(function () {
  if (customElements.get('site-header')) return;

  // Path back to the repo root — depth-aware so it works at any nesting
  // (root AND /viewer/).
  const _segs = location.pathname.split('/').filter(Boolean);
  const PFX = '../'.repeat(Math.max(0, _segs.length - 1));

  // [key, label, href] — top-level tabs (few enough pages to show flat, not hidden in a menu).
  const TABS = [
    ['wheel',  'Wheel',        PFX + 'wheel.html'],
    ['lenses', 'Lenses',       PFX + 'lenses.html'],
    ['course', 'Course',       PFX + 'pages/course.html'],
    ['viewer', 'Chart Viewer', PFX + 'viewer/astrology-viewer.html'],
  ];
  // Every grammar in grammars/*, in the order they appear on the homepage gallery.
  const GRAMMAR_MENU = [
    ['historiographies-of-astrology', 'Historiographies of Astrology'],
    ['tetrabiblos-ashmand',           "Ptolemy — Tetrabiblos (Ashmand, 1822)"],
    ['alan-leo',                      "Alan Leo's Astrology"],
    ['proctor-skeptical-astrology',   "Proctor's Skeptical Astrology"],
    ['western-astrology-canonical',   'Western Astrology — Canonical'],
    ['casting-big-three',             'Casting — The Big Three'],
    ['casting-twelve-houses',         'Casting — The Twelve Houses'],
    ['casting-single-aspect',         'Casting — One Aspect'],
  ];
  const TOOLS = [
    ['github', 'GitHub ↗', 'https://github.com/PlayfulProcess/Recursive-astrology', 't-github', true],
  ];

  function autoActive() {
    const f = location.pathname.split('/').pop() || 'index.html';
    if (f.startsWith('wheel')) return 'wheel';
    if (f.startsWith('lenses')) return 'lenses';
    if (f.startsWith('course')) return 'course';
    if (f.startsWith('astrology-viewer')) return 'viewer';
    if (f === 'index.html' || f === '') return 'home';
    return 'home';
  }

  class SiteHeader extends HTMLElement {
    connectedCallback() {
      // Embedded (iframed into some other surface): render no header at all.
      if (new URLSearchParams(location.search).get('embed') === '1') { this.style.display = 'none'; return; }
      // Museum/Editorial webfonts — same families theme.css tokenises (--serif-display / --sans),
      // injected once into the document head so this shadow DOM and the light DOM both render in them.
      if (!document.getElementById('ra-fonts')) {
        const fl = document.createElement('link'); fl.id = 'ra-fonts'; fl.rel = 'stylesheet';
        fl.href = 'https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&display=swap';
        document.head.appendChild(fl);
      }
      const active = this.getAttribute('active') || autoActive();
      const root = this.attachShadow({ mode: 'open' });
      const tab = ([key, label, href, cls, ext]) =>
        `<a class="tab ${cls || ''}${key === active ? ' active' : ''}" href="${href}"${ext ? ' target="_blank" rel="noopener"' : ''}>${label}</a>`;
      const menuItem = ([slug, label]) =>
        `<a class="${active === 'home' && new URLSearchParams(location.search).get('grammar') === slug ? 'on' : ''}" href="${PFX}index.html?grammar=${slug}">${label}</a>`;
      root.innerHTML = `
        <style>
          :host{ display:block; position:sticky; top:0; z-index:50;
                 background:#fbf9f3; padding:0; margin:0; border:0; font-size:14px;
                 transition:transform .25s ease; will-change:transform; }
          @media (prefers-reduced-motion: reduce){ :host{ transition:none; } .tab, .dd-menu a, .brand{ transition:none !important; } }
          .bar{
            display:flex; align-items:center; gap:14px; flex-wrap:wrap;
            padding:13px 20px; background:#fbf9f3;
            border-bottom:1px solid #d8d2c6;
            font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;
          }
          .brand{ display:flex; flex-direction:row; align-items:center; gap:10px; margin-right:4px; }
          .brand-logo, .brand-name{ display:inline-flex; align-items:center; text-decoration:none; }
          .brand-logo{ border-radius:50%; }
          .brand-name .name{ font-family:"Fraunces",Georgia,serif; font-size:21px; font-weight:600; letter-spacing:.4px; color:#221f1a; white-space:nowrap; }
          .brand-name:hover .name{ color:#000; }
          .brand-name .name .gold{ color:#9a7322; }
          .brand svg{ flex-shrink:0; }
          .spacer{ flex:1 1 auto; }
          nav{ display:flex; gap:4px; flex-wrap:wrap; align-items:center; }
          .sep{ width:1px; height:20px; background:#d8d2c6; margin:0 6px; }
          .tab{
            color:#6b6457; text-decoration:none; font-size:13px; font-weight:500;
            padding:7px 9px; white-space:nowrap; transition:color .15s;
            border:0; border-bottom:1.5px solid transparent; border-radius:0;
          }
          .tab:hover{ color:#9a7322; }
          .tab.active{ color:#9a7322; font-weight:600; border-bottom-color:#9a7322; }
          .t-github{ color:#6b6457; border:0; border-bottom:1.5px solid transparent; border-radius:0; }
          .t-github:hover{ color:#9a7322; background:transparent; }
          /* dropdown */
          .dd{ position:relative; }
          .dd-btn{ background:none; font-family:inherit; cursor:pointer; }
          .dd-btn::after{ content:""; display:inline-block; width:5px; height:5px; margin-left:7px;
            border-right:1.4px solid currentColor; border-bottom:1.4px solid currentColor;
            transform:rotate(45deg) translateY(-2px); opacity:.5; }
          .dd-menu{ position:absolute; top:calc(100% + 8px); right:0; min-width:240px;
            max-width:min(320px,calc(100vw - 24px)); background:#ffffff; border:1px solid #d8d2c6;
            border-radius:8px; padding:7px; box-shadow:0 16px 44px -18px rgba(60,45,20,.45); display:none; z-index:60; }
          .dd-menu::before{ content:""; position:absolute; left:0; right:0; top:-10px; height:10px; }
          @media (max-width:760px){ .dd-menu{ position:fixed; left:12px; right:12px; top:54px; min-width:0; max-width:none; } }
          .dd:hover .dd-menu, .dd:focus-within .dd-menu, .dd.open .dd-menu{ display:block; }
          .dd.open .dd-btn::after{ transform:rotate(225deg) translateY(2px); opacity:.85; }
          .dd-menu a{ display:block; color:#4a4439; text-decoration:none; font-size:13px;
            padding:8px 10px; border-radius:7px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
          .dd-menu a:hover{ background:#f1ece1; color:#221f1a; }
          .dd-menu a[href*="recursive.eco"]{ color:#9333ea; }
          .dd-menu a.on{ color:#221f1a; background:#f1ece1; font-weight:600; }
          .dd-menu a.all{ border-top:1px solid #d8d2c6; margin-top:4px; padding-top:9px; font-weight:600; }
          @media (max-width:680px){
            .brand .sub{ display:none; }
            .tab{ padding:5px 8px; font-size:12px; }
            .sep{ display:none; }
          }
        </style>
        <div class="bar">
          <span class="brand">
            <a class="brand-logo" href="https://recursive.eco" target="_blank" rel="noopener" title="Part of recursive.eco — the parent project" aria-label="recursive.eco — the parent project">
              <span style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;background:#fff;border-radius:50%;flex-shrink:0">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#9a7322" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M17 4a7 7 0 1 0 3 11 5.6 5.6 0 0 1-3-11z" />
                  <path d="M8.5 4.5l.6 1.7 1.7.6-1.7.6-.6 1.7-.6-1.7-1.7-.6 1.7-.6z" />
                </svg>
              </span>
            </a>
            <a class="brand-name" href="${PFX}index.html" title="The Recursive Astrology — home">
              <span class="name">The <span class="gold">Recursive Astrology</span></span>
            </a>
          </span>
          <span class="spacer"></span>
          <nav aria-label="Site sections">
            <a class="tab${active === 'home' ? ' active' : ''}" href="${PFX}index.html">Home</a>
            ${TABS.map(tab).join('')}
            <span class="dd">
              <a class="tab dd-btn" role="button" tabindex="0" aria-haspopup="true" aria-expanded="false" aria-label="Grammars menu">Grammars</a>
              <span class="dd-menu">
                ${GRAMMAR_MENU.map(menuItem).join('')}
                <a class="all" href="${PFX}index.html#all-grammars">Browse all (Cards · Study · Tree) →</a>
              </span>
            </span>
            ${TOOLS.map(tab).join('')}
          </nav>
        </div>`;

      // Dropdown: keyboard + ARIA on top of the hover/focus-within CSS.
      root.querySelectorAll('.dd').forEach(dd => {
        const btn = dd.querySelector('.dd-btn');
        const set = open => btn && btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        dd.addEventListener('mouseenter', () => set(true));
        dd.addEventListener('mouseleave', () => set(false));
        dd.addEventListener('focusin', () => set(true));
        dd.addEventListener('focusout', () => { if (!dd.matches(':focus-within')) set(false); });
        dd.addEventListener('keydown', e => {
          if (e.key === 'Escape') { set(false); btn && btn.focus(); }
          if ((e.key === 'Enter' || e.key === ' ') && e.target === btn) {
            const first = dd.querySelector('.dd-menu a'); if (first) { e.preventDefault(); set(true); first.focus(); }
          }
        });
        // Touch / no-hover devices: tap the tab to toggle its menu (hover never fires).
        btn.addEventListener('click', e => {
          if (window.matchMedia('(hover: hover)').matches) return;
          e.preventDefault();
          const willOpen = !dd.classList.contains('open');
          root.querySelectorAll('.dd.open').forEach(o => { o.classList.remove('open'); const b = o.querySelector('.dd-btn'); if (b) b.setAttribute('aria-expanded', 'false'); });
          if (willOpen) { dd.classList.add('open'); set(true); }
        });
      });

      // Close any open menu when tapping outside the header (touch).
      document.addEventListener('click', e => {
        if (!e.composedPath().includes(this)) {
          root.querySelectorAll('.dd.open').forEach(o => { o.classList.remove('open'); const b = o.querySelector('.dd-btn'); if (b) b.setAttribute('aria-expanded', 'false'); });
        }
      });

      // Auto-hide on scroll down, reveal on scroll up — but never while the nav has keyboard focus.
      let lastY = window.scrollY || 0, host = this;
      window.addEventListener('scroll', () => {
        const y = window.scrollY || 0;
        const hide = y > 90 && y > lastY + 4 && !host.matches(':focus-within');
        host.style.transform = hide ? 'translateY(-100%)' : 'translateY(0)';
        lastY = y;
      }, { passive: true });
    }
  }
  customElements.define('site-header', SiteHeader);
})();
