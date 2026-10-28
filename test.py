import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="Venz Virni Blanza | Portfolio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.session_state.setdefault("dark_mode", True)
dark = st.session_state.dark_mode

P = dict(
    bg="#09070f", card="#110e1a", card2="#1c1830",
    text="#f0ecff", sub="#7a7594", line="#252040",
    glow="rgba(194,94,83,.28)", nav="rgba(9,7,15,.88)"
) if dark else dict(
    bg="#f5f3fa", card="#ffffff", card2="#eeeaf8",
    text="#1a1528", sub="#6b6483", line="#dddaea",
    glow="rgba(194,94,83,.18)", nav="rgba(245,243,250,.92)"
)


@st.cache_data
def load_data():
    ml = pd.DataFrame({
        "Model": ["Logistic Regression", "Random Forest"],
        "Accuracy (%)": [94.5, 98.8], "Precision (%)": [91.2, 97.5],
        "Recall (%)": [93.0, 98.2], "F1-Score (%)": [92.1, 97.8], "ROC-AUC (%)": [96.4, 99.6]
    })
    smote = pd.DataFrame({
        "Class": ["Legitimate (0)", "Fraudulent (1)"],
        "Original": [284315, 492], "After SMOTE": [227452, 227452]
    })
    threshold = pd.DataFrame({
        "Threshold": np.round(np.linspace(0.1, 0.9, 9), 1),
        "Random Forest F1 (%)": [91.4, 94.8, 96.5, 97.4, 97.8, 97.5, 96.8, 95.1, 92.0],
        "Logistic Regression F1 (%)": [82.1, 86.4, 89.2, 91.0, 92.1, 91.5, 89.8, 87.0, 83.2]
    }).set_index("Threshold")
    features = pd.DataFrame({
        "Feature": ["V14", "V10", "V17", "V12", "V4", "V11", "Amount (Scaled)"],
        "Importance": [0.198, 0.145, 0.132, 0.108, 0.089, 0.074, 0.042]
    }).set_index("Feature")
    skills = pd.DataFrame({
        "Skill Domain": ["Backend & Logic", "Frontend & UI", "Mobile Architecture", "Database Design", "System & Tooling"],
        "Proficiency (%)": [92, 88, 84, 86, 94]
    })
    return ml, smote, threshold, features, skills


ml_data, smote_data, threshold_data, feature_data, skill_data = load_data()


def badges(items):
    return "".join(f'<span class="tech-badge">{i}</span>' for i in items)


def skill_bar(name, pct, delay=0):
    return (f'<div class="skill-item"><div class="skill-top">'
            f'<span class="skill-name">{name}</span><span class="skill-pct">{pct}%</span></div>'
            f'<div class="skill-bar"><div class="skill-fill" style="width:{pct}%;animation-delay:{delay}ms"></div></div></div>')


def proj_card(ptype, title, desc, tags, links):
    bgs = badges(tags)
    ln = "".join(f'<a href="{u}" target="_blank">{t}</a>' for t, u in links)
    return (f'<div class="proj-card"><div class="proj-accent"></div><div class="proj-body">'
            f'<div class="proj-type">{ptype}</div><div class="proj-title">{title}</div>'
            f'<p class="proj-desc">{desc}</p><div style="margin-bottom:.9rem">{bgs}</div>'
            f'<div class="proj-links">{ln}</div></div></div>')


# ── CSS ──────────────────────────────────────────────────────────────────────

st.markdown(f"""<style>
:root {{
  --bg:{P['bg']}; --card:{P['card']}; --card2:{P['card2']};
  --text:{P['text']}; --sub:{P['sub']}; --line:{P['line']};
  --acc:#c25e53; --acc2:#e8896b; --glow:{P['glow']}; --nav:{P['nav']};
}}
</style>""", unsafe_allow_html=True)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html,[data-testid="stMain"],section.main { scroll-behavior:smooth; }
.stApp { background:var(--bg); color:var(--text); font-family:'Inter',system-ui,sans-serif; }
header[data-testid="stHeader"] { background:transparent !important; pointer-events:none; }
header[data-testid="stHeader"] * { pointer-events:auto; }
footer { visibility:hidden; }
.block-container { padding-top:6rem !important; max-width:1160px; }
h1,h2,h3,h4 { font-family:'Sora',sans-serif !important; color:var(--text) !important; letter-spacing:-.025em; }
.anchor { scroll-margin-top:90px; }

/* Background atmosphere */
.stApp::before {
  content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(55% 45% at 12% 18%, rgba(194,94,83,.15), transparent 65%),
    radial-gradient(40% 35% at 88% 78%, rgba(110,75,195,.11), transparent 65%),
    radial-gradient(25% 20% at 58% 52%, rgba(140,65,170,.07), transparent 60%);
  animation:drift 22s ease-in-out infinite alternate;
}
.stApp::after {
  content:''; position:fixed; inset:0; z-index:0; pointer-events:none; opacity:.028;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat:repeat;
}
@keyframes drift { to { transform:translate(3%,5%) scale(1.06); } }
[data-testid="stMainBlockContainer"] { position:relative; z-index:1; }

/* Scroll */
#scroll-bar { position:fixed; top:0; left:0; height:2px; width:0; z-index:9999;
  background:linear-gradient(90deg,var(--acc),var(--acc2)); box-shadow:0 0 10px var(--acc); }
[data-rv] { transition:opacity .85s cubic-bezier(.2,.7,.2,1),transform .85s cubic-bezier(.2,.7,.2,1),filter .85s; }
[data-rv="0"] { opacity:0; transform:translateY(36px) scale(.988); filter:blur(4px); }
[data-rv="1"] { opacity:1; transform:none; filter:none; }
@media (prefers-reduced-motion:reduce) {
  [data-rv] { opacity:1 !important; transform:none !important; filter:none !important; transition:none !important; }
  .stApp::before { animation:none; }
}

/* Section typography */
.eyebrow {
  display:inline-flex; align-items:center; gap:.5rem;
  font-size:.73rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase;
  color:var(--acc); margin-bottom:.9rem;
}
.eyebrow::before { content:''; display:inline-block; width:20px; height:2px; background:var(--acc); border-radius:2px; }
.section-h { font-size:clamp(1.75rem,3vw,2.5rem); margin-bottom:.45rem; }
.section-sub { color:var(--sub); font-size:.97rem; line-height:1.65; margin-bottom:2rem; }

/* Hero */
.hero-badge {
  display:inline-flex; align-items:center; gap:.55rem;
  background:rgba(194,94,83,.1); border:1px solid rgba(194,94,83,.28);
  color:var(--acc); font-size:.74rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase;
  padding:.32rem .95rem; border-radius:999px; margin-bottom:1.5rem;
}
.hero-badge::before {
  content:''; width:6px; height:6px; border-radius:50%; background:var(--acc);
  animation:pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.3;transform:scale(.65)} }
.hero-name {
  font-size:clamp(2.8rem,6.5vw,5.2rem); font-weight:800; line-height:1.01; margin-bottom:1.1rem;
  background:linear-gradient(135deg, var(--text) 15%, #c4bde8 52%, var(--acc2) 76%, var(--acc) 100%);
  background-size:200% auto; -webkit-background-clip:text; background-clip:text; color:transparent;
  animation:shine 8s linear infinite;
}
@keyframes shine { to { background-position:200% center; } }
.hero-sub { color:var(--sub); font-size:1.05rem; line-height:1.78; max-width:54ch; margin-bottom:1.8rem; }
.hero-sub b { color:var(--text); font-weight:600; }
.hero-stats {
  display:flex; gap:2.4rem; flex-wrap:wrap;
  padding:1.4rem 0; margin-bottom:1.8rem;
  border-top:1px solid var(--line); border-bottom:1px solid var(--line);
}
.stat-val { font-family:'Sora',sans-serif; font-size:2rem; font-weight:800; color:var(--acc); line-height:1; }
.stat-lbl { font-size:.76rem; color:var(--sub); margin-top:.2rem; letter-spacing:.01em; }

/* Buttons */
.cta-row { display:flex; gap:.8rem; flex-wrap:wrap; }
.btn {
  display:inline-flex; align-items:center; gap:.45rem; padding:.8rem 1.7rem;
  border-radius:999px; font-weight:700; font-size:.9rem; text-decoration:none !important;
  transition:transform .25s cubic-bezier(.2,.7,.2,1),box-shadow .25s,background .25s;
}
.btn.primary { background:linear-gradient(135deg,var(--acc),var(--acc2)); color:#fff !important; box-shadow:0 8px 28px var(--glow); }
.btn.ghost { border:1.5px solid var(--line); color:var(--text) !important; }
.btn.primary:hover { transform:translateY(-3px); box-shadow:0 16px 40px var(--glow); }
.btn.ghost:hover { transform:translateY(-3px); border-color:rgba(194,94,83,.45); background:rgba(194,94,83,.08); }
.btn:active { transform:scale(.96) !important; }

/* Avatar placeholder */
.avatar-wrap {
  width:100%; max-width:320px; aspect-ratio:1; margin:auto;
  background:linear-gradient(145deg,var(--card2),var(--card));
  border:1px solid var(--line); border-radius:28px;
  display:flex; align-items:center; justify-content:center;
  font-size:5.5rem; font-weight:800; font-family:'Sora',sans-serif; color:var(--acc);
  box-shadow:0 32px 80px var(--glow), inset 0 1px 0 rgba(255,255,255,.05);
  position:relative; overflow:hidden;
}
.avatar-wrap::before {
  content:''; position:absolute; top:-30%; right:-15%; width:55%; height:55%;
  border-radius:50%; background:radial-gradient(circle,rgba(194,94,83,.18),transparent 70%);
}

/* Cards */
.card {
  background:var(--card); border:1px solid var(--line); border-radius:20px;
  padding:1.8rem; margin-bottom:1.2rem; position:relative; overflow:hidden;
  transition:transform .4s cubic-bezier(.2,.8,.2,1),box-shadow .4s,border-color .4s;
}
.card::after {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:radial-gradient(65% 55% at 50% 0%,rgba(194,94,83,.09),transparent);
  opacity:0; transition:opacity .4s;
}
.card:hover { transform:translateY(-6px); border-color:rgba(194,94,83,.4); box-shadow:0 24px 56px var(--glow); }
.card:hover::after { opacity:1; }
.card h3 { font-size:1.08rem; margin-bottom:.6rem; }
.card p { color:var(--sub); font-size:.92rem; line-height:1.65; margin:0; }

/* About gradient box */
.about-box {
  background:linear-gradient(150deg,#c25e53 0%,#8f3f4a 55%,#4a1e2e 100%);
  border-radius:20px; padding:2.4rem; color:#fff; position:relative; overflow:hidden; height:100%;
}
.about-box::before {
  content:''; position:absolute; top:-40%; right:-15%;
  width:340px; height:340px; border-radius:50%; background:rgba(255,255,255,.05);
}
.about-box::after {
  content:''; position:absolute; bottom:-30%; left:-10%;
  width:240px; height:240px; border-radius:50%; background:rgba(0,0,0,.14);
}
.about-box .inner { position:relative; z-index:1; }
.about-box .big-num { font-size:5rem; font-weight:800; font-family:'Sora',sans-serif; line-height:1; }
.about-box h2 { color:#fff !important; margin:.2rem 0 1rem; font-size:1.5rem; }
.about-box p { color:rgba(255,255,255,.82); line-height:1.72; font-size:.94rem; }

/* Skill bars */
.skill-item { margin-bottom:1.1rem; }
.skill-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:.42rem; }
.skill-name { font-size:.86rem; font-weight:600; color:var(--text); }
.skill-pct { font-size:.77rem; font-weight:700; color:var(--acc); font-family:'JetBrains Mono',monospace; }
.skill-bar { height:4px; background:var(--line); border-radius:999px; overflow:hidden; }
.skill-fill {
  height:100%; border-radius:999px;
  background:linear-gradient(90deg,var(--acc),var(--acc2));
  box-shadow:0 0 8px rgba(194,94,83,.4);
  transform-origin:left;
  animation:bar-in .9s cubic-bezier(.2,.8,.2,1) both;
}
@keyframes bar-in { from{transform:scaleX(0)} to{transform:scaleX(1)} }

/* Tech badges */
.tech-badge {
  display:inline-block; background:rgba(194,94,83,.1); color:var(--acc);
  border:1px solid rgba(194,94,83,.22); padding:.18rem .58rem; border-radius:999px;
  font-size:.75rem; font-weight:600; margin:.16rem .18rem .16rem 0; transition:all .2s;
}
.tech-badge:hover { background:var(--acc); color:#fff; transform:translateY(-2px); }

/* Project cards */
.proj-card {
  background:var(--card); border:1px solid var(--line); border-radius:20px; overflow:hidden;
  margin-bottom:1.2rem;
  transition:transform .4s cubic-bezier(.2,.8,.2,1),box-shadow .4s,border-color .4s;
}
.proj-card:hover { transform:translateY(-6px); border-color:rgba(194,94,83,.4); box-shadow:0 24px 56px var(--glow); }
.proj-accent { height:4px; background:linear-gradient(90deg,var(--acc),var(--acc2)); }
.proj-body { padding:1.6rem; }
.proj-type { font-size:.71rem; font-weight:700; letter-spacing:.15em; text-transform:uppercase; color:var(--acc); margin-bottom:.45rem; }
.proj-title { font-size:1.08rem; font-weight:700; font-family:'Sora',sans-serif; color:var(--text); margin-bottom:.55rem; }
.proj-desc { color:var(--sub); font-size:.9rem; line-height:1.65; margin-bottom:.9rem; }
.proj-links { display:flex; gap:1rem; padding-top:.75rem; border-top:1px solid var(--line); }
.proj-links a { font-size:.84rem; font-weight:600; color:var(--acc); text-decoration:none; transition:opacity .2s; }
.proj-links a:hover { opacity:.65; }

/* Streamlit widget overrides */
.stButton>button,.stFormSubmitButton>button {
  border-radius:999px !important; border:1.5px solid var(--line) !important;
  background:var(--card) !important; color:var(--text) !important; font-weight:700 !important;
  transition:all .25s cubic-bezier(.2,.7,.2,1) !important;
}
.stButton>button:hover,.stFormSubmitButton>button:hover {
  border-color:var(--acc) !important; color:#fff !important;
  background:linear-gradient(135deg,var(--acc),var(--acc2)) !important;
  box-shadow:0 10px 28px var(--glow) !important; transform:translateY(-2px) !important;
}
[data-testid="stMetric"] {
  background:var(--card) !important; border:1px solid var(--line) !important;
  border-radius:16px !important; padding:1.1rem 1.2rem !important; transition:all .3s !important;
}
[data-testid="stMetric"]:hover { transform:translateY(-4px); border-color:rgba(194,94,83,.4) !important; box-shadow:0 14px 32px var(--glow); }
[data-testid="stMetricValue"] { color:var(--text) !important; }
.stTabs [data-baseweb="tab-list"] { gap:.4rem; border-bottom:none; flex-wrap:wrap; padding-bottom:.6rem; }
.stTabs [data-baseweb="tab"] {
  border-radius:999px; padding:.48rem 1.1rem; background:var(--card); border:1px solid var(--line);
  color:var(--sub); font-weight:600; font-size:.87rem; transition:all .2s;
}
.stTabs [data-baseweb="tab"]:hover { border-color:rgba(194,94,83,.4); color:var(--text); }
.stTabs [aria-selected="true"] { background:var(--acc) !important; color:#fff !important; border-color:var(--acc) !important; }
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"] { display:none; }
.stTextInput input,.stTextArea textarea {
  border-radius:12px !important; background:var(--card2) !important;
  border-color:var(--line) !important; color:var(--text) !important; transition:box-shadow .25s !important;
}
.stTextInput input:focus,.stTextArea textarea:focus {
  box-shadow:0 0 0 3px var(--glow) !important; border-color:var(--acc) !important;
}
[data-testid="stForm"] { background:var(--card); border:1px solid var(--line); border-radius:20px; padding:1.6rem; }
hr { border-color:var(--line) !important; border-width:0 0 1px 0 !important; }
</style>""", unsafe_allow_html=True)


# ── SCROLL ENGINE ─────────────────────────────────────────────────────────────

components.html("""<script>
(function(){
  const w=window.parent,d=w.document;
  if(w.__rvInit)return; w.__rvInit=true;
  const bar=d.createElement('div'); bar.id='scroll-bar'; d.body.appendChild(bar);
  const code=`(function(){
    const t0=Date.now();
    const sc=document.querySelector('[data-testid="stMain"]')||document.querySelector('section.main');
    const upd=()=>{const h=sc.scrollHeight-sc.clientHeight;
      document.getElementById('scroll-bar').style.width=(h>0?sc.scrollTop/h*100:0)+'%';};
    sc.addEventListener('scroll',upd,{passive:true});
    const io=new IntersectionObserver(es=>{
      es.filter(e=>e.isIntersecting).forEach((e,i)=>{
        e.target.style.transitionDelay=(i*90)+'ms';
        e.target.dataset.rv='1'; io.unobserve(e.target);});
    },{root:sc,threshold:0.06,rootMargin:'0px 0px -5% 0px'});
    const sel='[data-testid="stMainBlockContainer"]>[data-testid="stVerticalBlock"]>*';
    const scan=()=>document.querySelectorAll(sel).forEach(el=>{
      if(el.dataset.rv||el.querySelector('iframe[height="0"]'))return;
      const r=el.getBoundingClientRect();
      const seen=r.top<innerHeight&&r.bottom>0;
      if(Date.now()-t0>3000&&seen){el.dataset.rv='1';return;}
      el.dataset.rv='0'; io.observe(el);});
    new MutationObserver(scan).observe(sc,{childList:true,subtree:true});
    document.addEventListener('click',ev=>{
      const a=ev.target.closest&&ev.target.closest('a[href^="#"]');
      if(!a||a.getAttribute('href').length<2)return;
      const el=document.getElementById(a.getAttribute('href').slice(1));
      if(!el)return; ev.preventDefault();
      const top=el.getBoundingClientRect().top-sc.getBoundingClientRect().top+sc.scrollTop-90;
      sc.scrollTo({top:top,behavior:'smooth'});
    },true);
    scan(); upd();
  })();`;
  const s=d.createElement('script'); s.textContent=code; d.head.appendChild(s);
})();
</script>""", height=0)


# ── NAV ───────────────────────────────────────────────────────────────────────

components.html(f"""<script>
(function(){{
  const w=window.parent,d=w.document;
  if(d.getElementById('venz-nav'))return;
  const style=d.createElement('style');
  style.textContent=`
    #venz-nav{{
      position:fixed;top:.8rem;left:50%;transform:translateX(-50%);z-index:2147483647;
      display:flex;align-items:center;gap:.3rem;padding:.42rem .55rem .42rem 1.1rem;
      border-radius:999px;background:{P['nav']};backdrop-filter:blur(20px);
      -webkit-backdrop-filter:blur(20px);border:1px solid {P['line']};
      box-shadow:0 12px 40px rgba(0,0,0,.28),0 1px 0 rgba(255,255,255,.04) inset;
      max-width:94vw;overflow-x:auto;font-family:'Inter',system-ui,sans-serif;
    }}
    #venz-nav .logo{{
      font-family:'Sora',sans-serif;font-weight:800;margin-right:.7rem;
      color:{P['text']};white-space:nowrap;font-size:.95rem;letter-spacing:-.02em;
    }}
    #venz-nav .logo b{{color:#c25e53;}}
    #venz-nav a{{
      color:{P['sub']};text-decoration:none;font-size:.85rem;font-weight:600;
      padding:.38rem .78rem;border-radius:999px;transition:all .22s;white-space:nowrap;
    }}
    #venz-nav a:hover{{color:#fff;background:#c25e53;}}
  `;
  d.head.appendChild(style);
  const nav=d.createElement('nav');
  nav.id='venz-nav';
  nav.innerHTML='<span class="logo">venz<b>.</b>dev</span>'+
    '<a href="#about">About</a><a href="#skills">Skills</a><a href="#projects">Projects</a>'+
    '<a href="#analytics">Analytics</a><a href="#play">Play</a><a href="#contact">Contact</a>';
  d.body.appendChild(nav);
  nav.addEventListener('click',function(ev){{
    const a=ev.target.closest('a[href^="#"]');
    if(!a)return;
    const hash=a.getAttribute('href').slice(1);
    const sc=d.querySelector('[data-testid="stMain"]')||d.querySelector('section.main');
    const target=d.getElementById(hash);
    if(!target||!sc)return;
    ev.preventDefault();
    const top=target.getBoundingClientRect().top-sc.getBoundingClientRect().top+sc.scrollTop-90;
    sc.scrollTo({{top:top,behavior:'smooth'}});
  }});
}})();
</script>""", height=0)


# ── HERO ──────────────────────────────────────────────────────────────────────

h1, h2 = st.columns([1.35, 1], vertical_alignment="center")
with h1:
    st.markdown("""
<div class="hero-badge">Available for internships &nbsp;·&nbsp; Cebu, Philippines</div>
<h1 class="hero-name">Venz Virni<br>T. Blanza</h1>
<p class="hero-sub">
  CS student at <b>CIT-U</b> turning complex architectures into software that's
  fast, accessible and beautiful — from <b>C# Blazor</b> SPAs and <b>JavaFX</b> desktop systems
  to <b>Kotlin MVP</b> mobile apps and ML fraud-detection pipelines.
</p>
<div class="hero-stats">
  <div><div class="stat-val">4+</div><div class="stat-lbl">Architectural domains</div></div>
  <div><div class="stat-val">1</div><div class="stat-lbl">Team led</div></div>
  <div><div class="stat-val">7+</div><div class="stat-lbl">Languages</div></div>
  <div><div class="stat-val">99.6%</div><div class="stat-lbl">Best ROC-AUC</div></div>
</div>
<div class="cta-row">
  <a class="btn primary" href="#contact">Say hello</a>
  <a class="btn ghost" href="#analytics">ML dashboard</a>
</div>""", unsafe_allow_html=True)

with h2:
    if os.path.exists("profile.jpg"):
        st.image("profile.jpg", width=320)
    else:
        st.markdown('<div class="avatar-wrap">VB</div>', unsafe_allow_html=True)


# ── ABOUT ─────────────────────────────────────────────────────────────────────

st.markdown('<div id="about" class="anchor"></div>', unsafe_allow_html=True)
a1, a2 = st.columns([1.6, 1], vertical_alignment="top")
with a1:
    st.markdown("""<div class="about-box"><div class="inner">
<div class="big-num">4+</div>
<p style="font-weight:700;font-size:.95rem;margin:.2rem 0 1.4rem;opacity:.88;">Core architectural domains &nbsp;·&nbsp; Team leader</p>
<h2>About me</h2>
<p>I'm a Computer Science student at <b>Cebu Institute of Technology – University</b>.
I lead one student engineering team — <b>Group Queue&lt;T&gt</b> —
with a hands-on focus on debugging, database normalization and system architecture.</p>
<p style="margin-top:1rem;padding:.9rem 1rem;background:rgba(0,0,0,.2);border-radius:14px;">
My engineering philosophy: ship software that is <b>correct</b> first, <b>beautiful</b> second,
and never sacrifice one for the other.
</p>
</div></div>""", unsafe_allow_html=True)

with a2:
    st.markdown("""<div class="card" style="margin-bottom:1rem;">
<h3>Beyond the compiler</h3>
<p>I rice my <b style="color:var(--text);">Arch Linux Hyprland</b> desktop with custom Caelestia dotfiles,
Listens to <b style="color:var(--text);">almost every genre, such as Pop songs from different countries, metal, rock, soul, blue and many more</b>, and chase all perfect combos or atleast full combos in
<i>Project Sekai</i>, <i>BanG Dream!</i> and <i>D4DJ</i>.</p>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div class="card">
<h3>Quick facts</h3>
<p><b style="color:var(--text);">Institution</b><br>CIT-U, Cebu — BS Computer Science</p>
<p style="margin-top:.8rem;"><b style="color:var(--text);">Role</b><br>Team Lead · Full-Stack Dev · ML Practitioner</p>
<p style="margin-top:.8rem;"><b style="color:var(--text);">Location</b><br>Mandaue / Cebu City, Philippines</p>
</div>""", unsafe_allow_html=True)


# ── SKILLS ────────────────────────────────────────────────────────────────────

st.markdown('<div id="skills" class="anchor"></div>', unsafe_allow_html=True)
st.markdown("""<p class="eyebrow">Technical skills</p>
<h2 class="section-h">What I build with</h2>
<p class="section-sub">Languages, frameworks and tools that power my day-to-day work.</p>""",
unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(f"""<div class="card"><h3>Programming languages</h3>
{skill_bar("C# (.NET)", 92)}
{skill_bar("Python", 88, 60)}
{skill_bar("Kotlin", 86, 120)}
{skill_bar("Java (Swing / JavaFX)", 84, 180)}
{skill_bar("C++ & x86 Assembly", 74, 240)}
</div>""", unsafe_allow_html=True)

with s2:
    st.markdown(f"""<div class="card"><h3>Web & databases</h3>
{skill_bar("C# Blazor + Tailwind", 90)}
{skill_bar("HTML5 / CSS3 / JS", 88, 60)}
{skill_bar("PHP & MySQL", 82, 120)}
{skill_bar("Room Database (Android)", 84, 180)}
{skill_bar("Django / Node.js", 78, 240)}
</div>""", unsafe_allow_html=True)

with s3:
    st.markdown("<div class=\"card\"><h3>Tools & platforms</h3><div style='display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.4rem'>" +
        badges(["Arch Linux (Hyprland)", "Git & GitHub CI/CD", "scikit-learn", "SMOTE",
                "Android Studio", "Visual Studio", "Google Colab", "Godot 3D"]) +
        "</div></div>", unsafe_allow_html=True)


# ── PROJECTS ──────────────────────────────────────────────────────────────────

st.markdown('<div id="projects" class="anchor"></div>', unsafe_allow_html=True)
st.markdown("""<p class="eyebrow">Featured projects</p>
<h2 class="section-h">Things I've built</h2>
<p class="section-sub">Four systems — web, desktop, mobile and ML — each solving a real problem.</p>""",
unsafe_allow_html=True)

p1, p2 = st.columns(2)
p1.markdown(proj_card(
    "Web app · C# Blazor",
    "DumGame — Pixel grid & game platform",
    "Single-page app with modular Blazor components, pixel-art grid-tapping mechanics "
    "and responsive state management built on Tailwind CSS.",
    ["C# (.NET)", "Blazor", "Tailwind CSS", "SPA"],
    [("GitHub repo", "https://github.com/venzblanz/DumGame")]
), unsafe_allow_html=True)

p1.markdown(proj_card(
    "Android · Kotlin MVP",
    "WildQuest — Academic review platform",
    "Offline-first quiz app with strict MVP separation, vertical slicing and "
    "local Room database persistence for academic review content.",
    ["Kotlin", "MVP Architecture", "Room SQLite", "Android"],
    [("GitHub repo", "https://github.com/venzblanz/wild-quest")]
), unsafe_allow_html=True)

p2.markdown(proj_card(
    "Desktop · JavaFX + Java Swing",
    "MedServe — Health centre queue system",
    "Real-time JavaFX queue manager for patient triage and priority routing. "
    "Paired with a modular Java Swing grocery POS built with Group Veritas.",
    ["JavaFX", "Java Swing", "OOP", "Event-Driven UI"],
    [("GitHub repo", "https://github.com/venzblanz/CSIT228-Capstone")]
), unsafe_allow_html=True)

p2.markdown(proj_card(
    "Machine learning · Python",
    "Credit card fraud detection pipeline",
    "Anomaly detection handling severe class imbalance with SMOTE, "
    "benchmarking Logistic Regression against Random Forest — 99.6% ROC-AUC.",
    ["Python", "scikit-learn", "SMOTE", "Random Forest"],
    [("Colab notebook", "https://colab.research.google.com/drive/1F5FkSjrzey6NulcirNAebXtAwbzNlDc2?usp=sharing")]
), unsafe_allow_html=True)


# ── ANALYTICS ─────────────────────────────────────────────────────────────────

st.markdown('<div id="analytics" class="anchor"></div>', unsafe_allow_html=True)
st.markdown("""<p class="eyebrow">Data & ML</p>
<h2 class="section-h">Fraud detection results</h2>
<p class="section-sub">Logistic Regression vs. Random Forest on 284,807 European card transactions
(0.17% fraud rate), balanced with SMOTE.
By <b style="color:var(--text);">Venz Virni Blanza & Juner John Caimor</b>.</p>""",
unsafe_allow_html=True)

cols = st.columns(5)
for col, (label, val, delta) in zip(cols, [
    ("RF Accuracy",  "98.8%", "+4.3% vs LR"),
    ("RF Precision", "97.5%", "+6.3% vs LR"),
    ("RF Recall",    "98.2%", "+5.2% vs LR"),
    ("RF F1-Score",  "97.8%", "+5.7% vs LR"),
    ("RF ROC-AUC",   "99.6%", "+3.2% vs LR"),
]):
    col.metric(label, val, delta)

st.write("")
t1, t2, t3, t4 = st.tabs(["Model performance", "SMOTE balance", "Threshold & features", "Skill proficiency"])

with t1:
    c1, c2 = st.columns([1.4, 1])
    with c1:
        sel = st.multiselect("Metrics:", ["Accuracy (%)", "Precision (%)", "Recall (%)", "F1-Score (%)", "ROC-AUC (%)"],
                             default=["Accuracy (%)", "Precision (%)", "Recall (%)", "F1-Score (%)"])
        if sel:
            st.bar_chart(ml_data.set_index("Model")[sel])
        else:
            st.warning("Select at least one metric.")
    with c2:
        st.markdown("**Full evaluation table**")
        st.dataframe(ml_data.set_index("Model"), use_container_width=True)
        st.caption("Random Forest cut false positives by +6.3% precision and caught 98.2% of all fraud cases.")

with t2:
    a, b = st.columns(2)
    a.markdown("**Before SMOTE — 0.17% fraud rate**")
    a.bar_chart(smote_data.set_index("Class")["Original"])
    b.markdown("**After SMOTE — 50 / 50 balance**")
    b.bar_chart(smote_data.set_index("Class")["After SMOTE"])
    st.info("Without SMOTE a classifier hits 99.8% accuracy by calling every transaction legitimate — it never catches real fraud. "
            "SMOTE synthesises minority-class neighbours so training sees both classes equally.")

with t3:
    a, b = st.columns(2)
    a.markdown("**F1-score across decision thresholds**")
    a.line_chart(threshold_data)
    a.caption("Random Forest peaks near the 0.50 threshold (97.8% F1).")
    b.markdown("**Top PCA features by Gini importance**")
    b.bar_chart(feature_data)
    b.caption("V14, V10 and V17 drove the largest Gini impurity reduction.")

with t4:
    a, b = st.columns([1, 1.3])
    a.markdown("**Self-assessed confidence**")
    a.dataframe(skill_data.set_index("Skill Domain"), use_container_width=True)
    b.markdown("**Distribution**")
    b.bar_chart(skill_data.set_index("Skill Domain"))


# ── GAME ──────────────────────────────────────────────────────────────────────

st.markdown('<div id="play" class="anchor"></div>', unsafe_allow_html=True)
st.markdown("""<p class="eyebrow">Mini game</p>
<h2 class="section-h">Tap rush</h2>
<p class="section-sub">Twenty seconds. Hit the lit tile on the bottom row — miss once and the run ends.</p>""",
unsafe_allow_html=True)

GAME_HTML = """<style>
*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,sans-serif;color:__TEXT__;display:flex;justify-content:center}
#g{position:relative;width:100%;max-width:340px;border-radius:24px;overflow:hidden;background:__CARD__;border:1px solid __LINE__;
  box-shadow:0 28px 64px __GLOW__;user-select:none;-webkit-user-select:none;touch-action:manipulation}
.hud{display:flex;justify-content:space-between;padding:16px 24px;background:linear-gradient(135deg,#c25e53,#8f3f4a);color:#fff}
.hud small{display:block;font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.72}
.hud b{font-size:2rem;font-weight:800;font-family:Sora,sans-serif;line-height:1.1}
.bar{height:3px;background:rgba(0,0,0,.3)}.bar i{display:block;height:100%;width:100%;background:rgba(255,255,255,.85);transition:width 1s linear}
.grid{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(5,1fr);aspect-ratio:4/5}
.c{border:1px solid __LINE__;display:flex;align-items:center;justify-content:center;cursor:pointer;-webkit-tap-highlight-color:transparent}
.t{width:82%;height:82%;border-radius:14px;background:linear-gradient(135deg,#c25e53,#e8896b);opacity:.25;transition:transform .08s}
.t.on{opacity:1;box-shadow:0 8px 22px __GLOW__;animation:pop .18s ease-out}
.x{width:82%;height:82%;border-radius:14px;background:#e5484d;box-shadow:0 0 22px rgba(229,72,77,.7);animation:shake .28s}
@keyframes pop{from{transform:scale(.6);opacity:.15}}
@keyframes shake{25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}
#ov{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;
  background:rgba(9,7,15,.84);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#fff;text-align:center;padding:2rem}
#ov h2{margin:0;font-size:1.75rem;font-weight:800;font-family:Sora,sans-serif}
#ov p{margin:0;opacity:.72;font-size:.93rem}
#btn{margin-top:18px;border:0;border-radius:999px;padding:12px 46px;font-size:.92rem;font-weight:700;color:#fff;cursor:pointer;
  background:linear-gradient(135deg,#c25e53,#e8896b);box-shadow:0 8px 24px __GLOW__;transition:transform .2s,box-shadow .2s}
#btn:hover{transform:translateY(-3px);box-shadow:0 14px 32px __GLOW__}
#btn:active{transform:scale(.94)}
#ov small{opacity:.4;margin-top:12px;font-size:.74rem}
</style>
<div id="g">
<div class="hud"><div><small>Time</small><b id="tm">20</b></div><div style="text-align:right"><small>Score</small><b id="sc">0</b></div></div>
<div class="bar"><i id="fill"></i></div>
<div class="grid" id="grid"></div>
<div id="ov">
  <h2 id="ttl">Tap Rush</h2>
  <p id="info">20 seconds. Hit the lit tile on the bottom row.</p>
  <button id="btn">Start</button>
  <small>Keyboard: D &nbsp;F &nbsp;J &nbsp;K</small>
</div></div>
<script>
var R=5,C=4,T=20,rows=[],score=0,left=T,playing=false,timer=null,best=0,err=null;
var grid=document.getElementById('grid'),ov=document.getElementById('ov');
function rnd(){return Math.floor(Math.random()*C)}
function draw(){grid.innerHTML='';
 for(var r=R-1;r>=0;r--)for(var c=0;c<C;c++){(function(r,c){
  var d=document.createElement('div');d.className='c';
  d.addEventListener('pointerdown',function(e){e.preventDefault();tap(r,c)});
  if(rows[r]===c){var t=document.createElement('div');t.className='t'+(r===0?' on':'');d.appendChild(t)}
  if(err&&err[0]===r&&err[1]===c){var x=document.createElement('div');x.className='x';d.appendChild(x)}
  grid.appendChild(d)})(r,c)}
 document.getElementById('sc').textContent=score;
 document.getElementById('tm').textContent=left;
 document.getElementById('fill').style.width=(left/T*100)+'%'}
function tap(r,c){if(!playing)return;
 if(r===0){if(rows[0]===c){score++;rows.shift();rows.push(rnd());draw()}else fail(r,c)}
 else if(rows[r]!==c)fail(r,c)}
function fail(r,c){err=[r,c];end('Missed!',400)}
function start(){rows=[];for(var i=0;i<R;i++)rows.push(rnd());err=null;score=0;left=T;playing=true;ov.style.display='none';
 clearInterval(timer);timer=setInterval(function(){left--;if(left<=0){left=0;draw();end("Time's up",0)}else draw()},1000);draw()}
function end(title,delay){playing=false;clearInterval(timer);best=Math.max(best,score);draw();
 setTimeout(function(){document.getElementById('ttl').textContent=title;
  document.getElementById('info').textContent='Score '+score+' · Best '+best;
  document.getElementById('btn').textContent='Play again';ov.style.display='flex'},delay)}
document.getElementById('btn').onclick=start;
document.addEventListener('keydown',function(e){var i='dfjk'.indexOf(e.key.toLowerCase());if(i>-1)tap(0,i)});
for(var i=0;i<R;i++)rows.push(rnd());draw();
</script>"""
for k, v in {"__TEXT__": P["text"], "__CARD__": P["card"], "__LINE__": P["line"], "__GLOW__": P["glow"]}.items():
    GAME_HTML = GAME_HTML.replace(k, v)

g1, g2 = st.columns([1, 1.05], vertical_alignment="center")
with g1:
    st.markdown("""<div class="card">
<h3>How to play</h3>
<p style="margin-bottom:.9rem;">Only the <b style="color:var(--text);">bottom row</b> counts.
Hit its lit tile and every row drops one step down.</p>
<p style="margin-bottom:.9rem;">Tap a wrong cell on any row, or let the 20-second timer run out,
and the run ends. Your best score persists for the session.</p>
<p style="margin:0;">A vanilla JS port of my Blazor tap game, themed to match this site.
On a keyboard use <b style="color:var(--text);">D, F, J, K</b> for the four columns.</p>
</div>""", unsafe_allow_html=True)

with g2:
    components.html(GAME_HTML, height=530)


# ── CONTACT ───────────────────────────────────────────────────────────────────

st.markdown('<div id="contact" class="anchor"></div>', unsafe_allow_html=True)
st.markdown("""<p class="eyebrow">Get in touch</p>
<h2 class="section-h">Let's work together</h2>
<p class="section-sub">Open to software engineering internships, full-stack collaborations and systems projects.</p>""",
unsafe_allow_html=True)

c1, c2 = st.columns([1.4, 1])
with c1:
    with st.form("contact_form", clear_on_submit=True):
        a, b = st.columns(2)
        name_in = a.text_input("Your name *")
        email_in = b.text_input("Your email *")
        st.text_input("Subject / role opportunity")
        msg_in = st.text_area("Your message *")
        if st.form_submit_button("Send message", icon=":material/send:", use_container_width=True):
            if name_in.strip() and email_in.strip() and msg_in.strip():
                st.success(f"Thanks, {name_in.split()[0]}! Message received.")
            else:
                st.error("Fill in your name, email and message first.")

with c2:
    st.markdown("""<div class="card">
<h3>Direct channels</h3>
<p style="margin-bottom:1.2rem;">I usually respond within a day — reach me on any platform below.</p>
<p><b style="color:var(--text);">GitHub</b><br>
  <a href="https://github.com/venzblanz" target="_blank" style="color:var(--acc);text-decoration:none;">github.com/venzblanz</a></p>
<p style="margin-top:.9rem;"><b style="color:var(--text);">LinkedIn</b><br>
  <a href="https://linkedin.com/in/venzblanz" target="_blank" style="color:var(--acc);text-decoration:none;">linkedin.com/in/venzblanz</a></p>
<p style="margin-top:.9rem;"><b style="color:var(--text);">Email</b><br>
  <a href="mailto:venzvirni.blanza@outlook.com" style="color:var(--acc);text-decoration:none;">venzvirni.blanza@outlook.com</a></p>
<p style="margin-top:.9rem;"><b style="color:var(--text);">Location</b><br>
  Mandaue / Cebu City, Philippines</p>
</div>""", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────

st.markdown("---")
f1, f2 = st.columns([3, 1.2])
f1.markdown(
    "<div style='color:var(--sub);font-size:.87rem;'>"
    "© 2026 <b style='color:var(--text);'>Venz Virni T. Blanza</b> · "
    "BS Computer Science, Cebu Institute of Technology – University"
    "<br><span style='font-size:.76rem;opacity:.55;'>Living document v4.0</span></div>",
    unsafe_allow_html=True
)
with f2:
    code = st.text_input("", placeholder="↑↑↓↓←→←→BA", label_visibility="collapsed")
    if code.strip().lower() in ["↑↑↓↓←→←→ba", "uuddlrlrba", "konami", "return_by_death", "isekai"]:
        st.balloons()
        st.code("[ARCH-HYPRLAND TTY1] >> Checkpoint saved.\nGuild Leader [EXODIA]", language="bash")