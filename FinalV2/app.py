import streamlit as st
import streamlit.components.v1 as components
import xarray as xr
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile, os

st.set_page_config(page_title="PyClimaExplorer | Earth OS", page_icon="🌍",
                   layout="wide", initial_sidebar_state="expanded")

CSS_JS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
#MainMenu,footer,header{visibility:hidden!important}
.block-container{padding:0!important;max-width:100%!important}
.stApp{background:#000;min-height:100vh;overflow-x:hidden}
#c-stars{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1}
#c-grid{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:2;opacity:0.18}
#c-vignette{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:3;background:radial-gradient(ellipse 80% 80% at 50% 50%,transparent 40%,rgba(0,0,0,0.75) 100%)}
#splash{position:fixed;top:0;left:0;width:100%;height:100%;background:#000;z-index:99999;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity 1.5s ease;}
#splash.out{opacity:0;pointer-events:none}
.sp-logo{width:140px;height:140px;position:relative;margin-bottom:36px;}
.sp-ring{position:absolute;border-radius:50%;border:1px solid rgba(0,229,255,0.5);animation:sp-spin 8s linear infinite;}
.sp-ring:nth-child(1){width:140px;height:140px;top:0;left:0;}
.sp-ring:nth-child(2){width:110px;height:110px;top:15px;left:15px;animation-duration:5s;animation-direction:reverse}
.sp-ring:nth-child(3){width:80px;height:80px;top:30px;left:30px;animation-duration:3s}
.sp-earth{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:3.2rem;animation:sp-pulse 2s ease-in-out infinite alternate;}
.sp-dot{position:absolute;width:8px;height:8px;border-radius:50%;background:#00e5ff;box-shadow:0 0 14px #00e5ff;top:-4px;left:50%;margin-left:-4px;transform-origin:4px 74px;animation:sp-spin 3s linear infinite;}
@keyframes sp-spin{to{transform:rotate(360deg)}}
@keyframes sp-pulse{0%{filter:drop-shadow(0 0 15px rgba(0,229,255,0.7))}100%{filter:drop-shadow(0 0 35px rgba(0,229,255,1))}}
.sp-title{font-family:'Orbitron',monospace;color:#fff;font-size:2rem;font-weight:900;letter-spacing:8px;text-shadow:0 0 30px rgba(0,229,255,0.9);}
.sp-sub{font-family:'Exo 2',sans-serif;color:rgba(0,200,255,0.45);font-size:0.65rem;letter-spacing:5px;margin-top:8px;text-transform:uppercase}
.sp-bar{width:260px;height:1px;background:rgba(0,200,255,0.08);margin-top:36px;position:relative;overflow:hidden;}
.sp-bar::after{content:'';position:absolute;top:0;left:0;height:100%;background:linear-gradient(90deg,transparent,#00e5ff,#fff,#00e5ff,transparent);animation:sp-fill 2.4s ease-in-out forwards;}
@keyframes sp-fill{0%{width:0%}100%{width:100%}}
.sp-pct{font-family:'Share Tech Mono',monospace;color:rgba(0,200,255,0.4);font-size:0.65rem;margin-top:8px;letter-spacing:2px}
.main .block-container{position:relative;z-index:10;animation:reveal 1s ease both;animation-delay:2.6s;}
@keyframes reveal{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
section[data-testid="stSidebar"]{background:rgba(0,4,14,0.97)!important;border-right:1px solid rgba(0,200,255,0.1)!important;backdrop-filter:blur(20px)!important;z-index:20!important;}
section[data-testid="stSidebar"] > div{padding:0!important}
.logo-wrap{padding:24px 16px 18px;border-bottom:1px solid rgba(0,200,255,0.06);text-align:center;}
.logo-orb{width:72px;height:72px;margin:0 auto 14px;border-radius:50%;border:1px solid rgba(0,229,255,0.35);display:flex;align-items:center;justify-content:center;font-size:2.2rem;animation:orb-breathe 5s ease-in-out infinite;}
@keyframes orb-breathe{0%,100%{box-shadow:0 0 25px rgba(0,229,255,0.15)}50%{box-shadow:0 0 45px rgba(0,229,255,0.3)}}
.logo-name{font-family:'Orbitron',monospace;color:#e0f4ff;font-size:1.1rem;font-weight:800;letter-spacing:3px;text-shadow:0 0 20px rgba(0,229,255,0.7);}
.logo-tag{font-family:'Exo 2',sans-serif;color:rgba(0,200,255,0.3);font-size:0.55rem;letter-spacing:3px;margin-top:4px;text-transform:uppercase}
.nav-lbl{padding:16px 14px 4px;font-family:'Orbitron',monospace;font-size:0.48rem;color:rgba(0,200,255,0.25);letter-spacing:3px;text-transform:uppercase;display:flex;align-items:center;gap:8px;}
.nav-lbl::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(0,200,255,0.15),transparent)}
div[data-testid="stSelectbox"] label,div[data-testid="stSlider"] label,div[data-testid="stFileUploader"] label,div[data-testid="stRadio"] label{font-family:'Orbitron',monospace!important;color:rgba(0,200,255,0.45)!important;font-size:0.52rem!important;letter-spacing:2px!important;text-transform:uppercase!important;}
div[data-testid="stSelectbox"] > div > div{background:rgba(0,10,25,0.9)!important;border:1px solid rgba(0,200,255,0.14)!important;color:#a0d8ef!important;border-radius:6px!important;font-family:'Exo 2',sans-serif!important;}
div[data-testid="stRadio"] label span{font-family:'Exo 2',sans-serif!important;color:rgba(0,200,255,0.55)!important;font-size:0.8rem!important;}
.stButton > button{background:linear-gradient(135deg,rgba(0,180,255,0.08),rgba(0,100,200,0.05))!important;color:#80d4f0!important;border:1px solid rgba(0,200,255,0.22)!important;font-family:'Orbitron',monospace!important;font-size:0.58rem!important;letter-spacing:2.5px!important;border-radius:4px!important;width:100%!important;text-transform:uppercase!important;transition:all 0.25s!important;}
.stButton > button:hover{background:linear-gradient(135deg,rgba(0,180,255,0.18),rgba(0,100,200,0.12))!important;border-color:rgba(0,200,255,0.5)!important;transform:translateY(-2px)!important;}
.cmd-bar{position:relative;background:rgba(0,3,12,0.96);border-bottom:1px solid rgba(0,200,255,0.07);padding:10px 24px;display:flex;align-items:center;justify-content:space-between;overflow:hidden;z-index:15;}
.cmd-bar::before{content:'';position:absolute;bottom:0;left:0;width:300%;height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,255,0.8),rgba(100,200,255,1),rgba(0,229,255,0.8),transparent);animation:cmd-scan 7s linear infinite;}
@keyframes cmd-scan{0%{transform:translateX(-66%)}100%{transform:translateX(0%)}}
.cmd-logo{font-family:'Orbitron',monospace;color:#d0f4ff;font-size:1rem;font-weight:800;letter-spacing:3px;text-shadow:0 0 20px rgba(0,229,255,0.6)}
.cmd-info{font-family:'Exo 2',sans-serif;color:rgba(0,200,255,0.35);font-size:0.63rem;margin-top:2px}
.cmd-status{display:flex;align-items:center;gap:16px}
.cmd-online{font-family:'Orbitron',monospace;font-size:0.55rem;letter-spacing:2.5px;padding:5px 16px;border-radius:2px;border:1px solid rgba(0,255,150,0.28);color:#40e0a0;background:rgba(0,255,150,0.04);}
.cmd-clock{font-family:'Share Tech Mono',monospace;color:rgba(0,200,255,0.4);font-size:0.72rem;letter-spacing:2px;min-width:130px;text-align:right}
.g-card{background:rgba(0,10,28,0.7);border:1px solid rgba(0,200,255,0.1);border-radius:12px;padding:16px;position:relative;overflow:hidden;backdrop-filter:blur(12px);box-shadow:0 12px 40px rgba(0,0,0,0.6);transition:all 0.35s;animation:card-in 0.6s ease both;}
@keyframes card-in{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
.g-card:hover{border-color:rgba(0,200,255,0.2);transform:translateY(-2px);}
.g-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,255,0.5),transparent);animation:shimmer 6s ease-in-out infinite;}
@keyframes shimmer{0%,100%{opacity:0.3}50%{opacity:1}}
.g-card::after{content:'';position:absolute;bottom:8px;right:8px;width:14px;height:14px;border-bottom:1px solid rgba(0,200,255,0.2);border-right:1px solid rgba(0,200,255,0.2);}
.g-card-tl{position:absolute;top:8px;left:8px;width:14px;height:14px;border-top:1px solid rgba(0,200,255,0.2);border-left:1px solid rgba(0,200,255,0.2);}
.g-title{font-family:'Orbitron',monospace;color:#a0d8f8;font-size:0.66rem;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:2px;text-shadow:0 0 10px rgba(0,200,255,0.4)}
.g-sub{font-family:'Exo 2',sans-serif;color:rgba(0,180,255,0.28);font-size:0.6rem;margin-bottom:10px;font-style:italic}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:12px 16px 0}
.kpi{background:rgba(0,8,22,0.8);border:1px solid rgba(0,200,255,0.08);border-top:2px solid var(--c);border-radius:10px;padding:14px 16px;position:relative;backdrop-filter:blur(10px);transition:transform 0.3s;animation:kpi-rise 0.7s ease both;cursor:default;}
.kpi:nth-child(1){animation-delay:0.05s}.kpi:nth-child(2){animation-delay:0.1s}.kpi:nth-child(3){animation-delay:0.15s}.kpi:nth-child(4){animation-delay:0.2s}
@keyframes kpi-rise{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.kpi:hover{transform:translateY(-4px);}
.kpi-dot-tl{position:absolute;top:6px;left:6px;width:10px;height:10px;border-top:1px solid var(--c);border-left:1px solid var(--c);opacity:0.5}
.kpi-dot-br{position:absolute;bottom:6px;right:6px;width:10px;height:10px;border-bottom:1px solid var(--c);border-right:1px solid var(--c);opacity:0.5}
.kpi-lbl{font-family:'Orbitron',monospace;color:rgba(0,180,255,0.35);font-size:0.48rem;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:8px}
.kpi-num{font-family:'Orbitron',monospace;color:#f0f8ff;font-size:1.6rem;font-weight:800;line-height:1;text-shadow:0 0 20px var(--c)}
.kpi-unit{font-size:0.68rem;color:rgba(0,180,255,0.38);margin-left:4px;font-weight:400}
.kpi-delta{font-family:'Exo 2',sans-serif;font-size:0.63rem;margin-top:6px;color:var(--c);}
.sec-div{display:flex;align-items:center;gap:14px;padding:10px 16px 6px;font-family:'Orbitron',monospace;font-size:0.5rem;color:rgba(0,200,255,0.25);letter-spacing:3px;text-transform:uppercase;}
.sec-div-dot{width:5px;height:5px;border-radius:50%;background:rgba(0,229,255,0.5);box-shadow:0 0 8px rgba(0,229,255,0.8);flex-shrink:0}
.sec-div-line{flex:1;height:1px;background:linear-gradient(90deg,rgba(0,200,255,0.15),transparent)}
.story-card{background:rgba(0,8,22,0.85);border:1px solid rgba(0,200,255,0.08);border-left:2px solid var(--ac);border-radius:10px;padding:18px 20px;font-family:'Exo 2',sans-serif;color:rgba(160,220,255,0.78);font-size:0.84rem;line-height:1.8;backdrop-filter:blur(10px);animation:story-slide 0.5s ease both;}
@keyframes story-slide{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
.story-hed{font-family:'Orbitron',monospace;font-size:0.78rem;font-weight:700;color:var(--ac);letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;text-shadow:0 0 14px var(--ac)}
.fact-box{background:rgba(0,20,50,0.5);border:1px solid rgba(0,200,255,0.08);border-left:2px solid var(--ac);border-radius:6px;padding:10px 14px;margin-top:10px;font-family:'Exo 2',sans-serif;font-size:0.72rem;color:rgba(0,200,255,0.45);font-style:italic;line-height:1.6;}
.fact-box-tag{font-family:'Orbitron',monospace;font-size:0.48rem;letter-spacing:2px;color:var(--ac);display:block;margin-bottom:4px}
.info-banner{background:rgba(0,20,50,0.7);border:1px solid rgba(0,200,255,0.15);border-left:3px solid #00e5ff;border-radius:8px;padding:12px 16px;margin:8px 0;font-family:'Exo 2',sans-serif;color:rgba(140,210,255,0.7);font-size:0.78rem;line-height:1.6}
.info-banner-title{font-family:'Orbitron',monospace;color:#00e5ff;font-size:0.58rem;letter-spacing:2px;margin-bottom:6px}
.team-box{padding:0 14px;font-family:'Exo 2',sans-serif;color:rgba(0,170,230,0.45);font-size:0.68rem;line-height:2}
.team-name{font-family:'Orbitron',monospace;color:#60c8f0;font-size:0.68rem;font-weight:700;letter-spacing:2px;}
.footer{text-align:center;padding:18px;margin-top:24px;border-top:1px solid rgba(0,200,255,0.04);font-family:'Orbitron',monospace;color:rgba(0,140,200,0.14);font-size:0.48rem;letter-spacing:3px;text-transform:uppercase}
.ab{display:inline-flex;align-items:center;gap:5px;font-family:'Exo 2',sans-serif;font-size:0.68rem;padding:4px 10px;border-radius:4px;margin:3px 3px 0 0;}
.ab-hot{border:1px solid rgba(255,70,60,0.3);color:#ff8070;background:rgba(255,50,40,0.06)}
.ab-cold{border:1px solid rgba(0,180,255,0.3);color:#60c0ff;background:rgba(0,160,255,0.06)}
::-webkit-scrollbar{width:2px;height:2px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(0,200,255,0.14);border-radius:2px}
.stPlotlyChart{animation:chart-pop 0.5s ease both}
@keyframes chart-pop{from{opacity:0;transform:scale(0.96)}to{opacity:1;transform:scale(1)}}
body::after{content:'';position:fixed;top:-4px;left:0;width:100%;height:4px;background:linear-gradient(90deg,transparent,rgba(0,229,255,0.18),transparent);pointer-events:none;z-index:9999;animation:page-scan 12s linear infinite;}
@keyframes page-scan{0%{top:-4px}100%{top:100vh}}
div[data-testid="stFileUploader"]{background:rgba(0,10,28,0.7)!important;border:1px dashed rgba(0,200,255,0.14)!important;border-radius:8px!important;}
.stSpinner > div{border-color:rgba(0,200,255,0.6) transparent transparent!important}
.stDataFrame thead tr th{background:rgba(0,15,38,0.95)!important;color:rgba(0,200,255,0.55)!important;font-family:'Orbitron',monospace!important;font-size:0.52rem!important;}
.stDataFrame tbody tr td{background:rgba(0,6,18,0.7)!important;color:rgba(140,210,250,0.6)!important;font-family:'Share Tech Mono',monospace!important;font-size:0.73rem!important;}
</style>
<canvas id="c-stars"></canvas><canvas id="c-grid"></canvas><div id="c-vignette"></div>
<div id="splash">
  <div class="sp-logo"><div class="sp-ring"></div><div class="sp-ring"></div><div class="sp-ring"></div><div class="sp-earth">🌍</div><div class="sp-dot"></div></div>
  <div class="sp-title">PYCLIMAEXPLORER</div>
  <div class="sp-sub">Earth Observation System · Cosmos_Sync</div>
  <div class="sp-bar"></div>
  <div class="sp-pct" id="sp-pct">INITIALISING...</div>
</div>
"""

SCRIPT = """
<script>
(function(){
  var doc=window.parent.document, win=window.parent;
  var pcts=["LOADING DATA MODULES...","CALIBRATING SENSORS...","MAPPING COORDINATES...","SYSTEM ONLINE"];
  var pi=0;
  function tickPct(){var el=doc.getElementById('sp-pct');if(el&&pi<pcts.length)el.textContent=pcts[pi++];}
  tickPct();setInterval(tickPct,600);
  setTimeout(function(){var sp=doc.getElementById('splash');if(sp){sp.classList.add('out');setTimeout(function(){if(sp.parentNode)sp.parentNode.removeChild(sp);},1600);}},2700);
  var sc=doc.getElementById('c-stars');if(!sc)return;
  var sx=sc.getContext('2d'),W,H,stars=[],nebulae=[],comets=[];
  function rsz(){W=sc.width=win.innerWidth;H=sc.height=win.innerHeight;}
  rsz();win.addEventListener('resize',rsz);
  for(var i=0;i<380;i++)stars.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.6+0.1,a:Math.random(),da:0.002+Math.random()*0.008,dir:Math.random()>0.5?1:-1,blue:Math.random()>0.8,big:Math.random()>0.9});
  for(var i=0;i<7;i++)nebulae.push({x:Math.random()*W,y:Math.random()*H,r:100+Math.random()*200,a:0.01+Math.random()*0.02,h:180+Math.random()*60,ph:Math.random()*6.28,sp:0.001+Math.random()*0.003});
  function mkComet(){comets.push({x:Math.random()*W*0.6,y:Math.random()*H*0.3,len:80+Math.random()*150,sp:6+Math.random()*7,ang:Math.PI/5+Math.random()*0.4,a:1});}
  setInterval(mkComet,6000);
  function drawStars(){
    sx.clearRect(0,0,W,H);
    nebulae.forEach(function(n){n.ph+=n.sp;var p=0.75+0.25*Math.sin(n.ph),g=sx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r*p);g.addColorStop(0,'hsla('+n.h+',70%,50%,'+(n.a*1.6)+')');g.addColorStop(1,'transparent');sx.beginPath();sx.arc(n.x,n.y,n.r*p,0,6.28);sx.fillStyle=g;sx.fill();});
    stars.forEach(function(s){s.a+=s.da*s.dir;if(s.a>=1||s.a<=0.03)s.dir*=-1;sx.beginPath();sx.arc(s.x,s.y,s.r,0,6.28);sx.fillStyle=s.blue?'rgba(100,195,255,'+s.a+')':'rgba(220,232,255,'+s.a+')';sx.fill();});
    for(var i=comets.length-1;i>=0;i--){var c=comets[i];c.x+=Math.cos(c.ang)*c.sp;c.y+=Math.sin(c.ang)*c.sp;c.a-=0.015;if(c.a<=0){comets.splice(i,1);continue;}sx.beginPath();sx.moveTo(c.x,c.y);sx.lineTo(c.x-Math.cos(c.ang)*c.len,c.y-Math.sin(c.ang)*c.len);var cg=sx.createLinearGradient(c.x,c.y,c.x-Math.cos(c.ang)*c.len,c.y-Math.sin(c.ang)*c.len);cg.addColorStop(0,'rgba(200,235,255,'+c.a+')');cg.addColorStop(1,'transparent');sx.strokeStyle=cg;sx.lineWidth=1.8;sx.stroke();}
    win.requestAnimationFrame(drawStars);
  }
  drawStars();
  var gc=doc.getElementById('c-grid');if(!gc)return;var gx=gc.getContext('2d');
  function drawGrid(){gc.width=W;gc.height=H;gx.clearRect(0,0,W,H);var sz=60;gx.strokeStyle='rgba(0,200,255,0.18)';gx.lineWidth=0.4;for(var x=0;x<W;x+=sz){gx.beginPath();gx.moveTo(x,0);gx.lineTo(x,H);gx.stroke();}for(var y=0;y<H;y+=sz){gx.beginPath();gx.moveTo(0,y);gx.lineTo(W,y);gx.stroke();}var cg2=gx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*0.7);cg2.addColorStop(0,'rgba(0,0,0,0)');cg2.addColorStop(1,'rgba(0,0,0,0.95)');gx.fillStyle=cg2;gx.fillRect(0,0,W,H);}
  drawGrid();win.addEventListener('resize',function(){rsz();drawGrid();});
  function tick(){var el=doc.getElementById('clk');if(el){var d=new Date();el.textContent=d.toUTCString().slice(17,25)+' UTC';}setTimeout(tick,1000);}
  setTimeout(tick,2800);

  // ══ SOUND SYSTEM (Web Audio API — no external files) ══
  var AC = null;
  function getAC(){
    if(!AC){ try{ AC = new (win.AudioContext || win.webkitAudioContext)(); }catch(e){} }
    return AC;
  }

  // Boot sound — cinematic low hum rising to a chime
  function playBoot(){
    var ac = getAC(); if(!ac) return;
    // Layer 1: deep rumble sweep
    var osc1 = ac.createOscillator();
    var gain1 = ac.createGain();
    osc1.connect(gain1); gain1.connect(ac.destination);
    osc1.type = 'sine'; osc1.frequency.setValueAtTime(40, ac.currentTime);
    osc1.frequency.exponentialRampToValueAtTime(120, ac.currentTime+1.8);
    gain1.gain.setValueAtTime(0, ac.currentTime);
    gain1.gain.linearRampToValueAtTime(0.18, ac.currentTime+0.3);
    gain1.gain.linearRampToValueAtTime(0, ac.currentTime+2.0);
    osc1.start(ac.currentTime); osc1.stop(ac.currentTime+2.1);
    // Layer 2: mid sweep
    var osc2 = ac.createOscillator();
    var gain2 = ac.createGain();
    osc2.connect(gain2); gain2.connect(ac.destination);
    osc2.type = 'triangle'; osc2.frequency.setValueAtTime(200, ac.currentTime+0.5);
    osc2.frequency.exponentialRampToValueAtTime(800, ac.currentTime+2.0);
    gain2.gain.setValueAtTime(0, ac.currentTime+0.5);
    gain2.gain.linearRampToValueAtTime(0.1, ac.currentTime+1.0);
    gain2.gain.linearRampToValueAtTime(0, ac.currentTime+2.2);
    osc2.start(ac.currentTime+0.5); osc2.stop(ac.currentTime+2.3);
    // Layer 3: final chime
    var osc3 = ac.createOscillator();
    var gain3 = ac.createGain();
    osc3.connect(gain3); gain3.connect(ac.destination);
    osc3.type = 'sine'; osc3.frequency.setValueAtTime(1200, ac.currentTime+1.8);
    osc3.frequency.exponentialRampToValueAtTime(900, ac.currentTime+2.8);
    gain3.gain.setValueAtTime(0.12, ac.currentTime+1.8);
    gain3.gain.exponentialRampToValueAtTime(0.001, ac.currentTime+3.0);
    osc3.start(ac.currentTime+1.8); osc3.stop(ac.currentTime+3.1);
  }

  // Whoosh — for globe load
  function playWhoosh(){
    var ac = getAC(); if(!ac) return;
    var bufSize = ac.sampleRate * 0.6;
    var buf = ac.createBuffer(1, bufSize, ac.sampleRate);
    var data = buf.getChannelData(0);
    for(var i=0;i<bufSize;i++) data[i]=(Math.random()*2-1)*Math.pow(1-i/bufSize,2);
    var src = ac.createBufferSource();
    var filt = ac.createBiquadFilter();
    var gain = ac.createGain();
    src.buffer = buf;
    filt.type = 'bandpass'; filt.frequency.setValueAtTime(300,ac.currentTime);
    filt.frequency.exponentialRampToValueAtTime(3000,ac.currentTime+0.5);
    filt.Q.value = 0.8;
    gain.gain.setValueAtTime(0.25,ac.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001,ac.currentTime+0.6);
    src.connect(filt); filt.connect(gain); gain.connect(ac.destination);
    src.start(); src.stop(ac.currentTime+0.65);
  }

  // Click — short crisp tick
  function playClick(){
    var ac = getAC(); if(!ac) return;
    var osc = ac.createOscillator();
    var gain = ac.createGain();
    osc.connect(gain); gain.connect(ac.destination);
    osc.type = 'square'; osc.frequency.value = 1200;
    gain.gain.setValueAtTime(0.08, ac.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime+0.06);
    osc.start(ac.currentTime); osc.stop(ac.currentTime+0.07);
  }

  // Beep — soft sine ping for chart render
  function playBeep(){
    var ac = getAC(); if(!ac) return;
    var osc = ac.createOscillator();
    var gain = ac.createGain();
    osc.connect(gain); gain.connect(ac.destination);
    osc.type = 'sine'; osc.frequency.value = 660;
    gain.gain.setValueAtTime(0.07, ac.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime+0.35);
    osc.start(ac.currentTime); osc.stop(ac.currentTime+0.4);
  }

  // Ambient space drone — subtle continuous texture
  var ambientRunning = false;
  function startAmbient(){
    if(ambientRunning) return;
    ambientRunning = true;
    var ac = getAC(); if(!ac) return;
    // drone osc 1
    var d1 = ac.createOscillator(); var g1 = ac.createGain();
    d1.connect(g1); g1.connect(ac.destination);
    d1.type='sine'; d1.frequency.value=55;
    g1.gain.setValueAtTime(0,ac.currentTime);
    g1.gain.linearRampToValueAtTime(0.04,ac.currentTime+4);
    d1.start(); // runs indefinitely
    // drone osc 2 — slight detune for beating effect
    var d2 = ac.createOscillator(); var g2 = ac.createGain();
    d2.connect(g2); g2.connect(ac.destination);
    d2.type='sine'; d2.frequency.value=57.5;
    g2.gain.setValueAtTime(0,ac.currentTime);
    g2.gain.linearRampToValueAtTime(0.03,ac.currentTime+4);
    d2.start();
    // high shimmer
    var d3 = ac.createOscillator(); var g3 = ac.createGain();
    d3.connect(g3); g3.connect(ac.destination);
    d3.type='sine'; d3.frequency.value=220;
    g3.gain.setValueAtTime(0,ac.currentTime);
    g3.gain.linearRampToValueAtTime(0.015,ac.currentTime+5);
    d3.start();
  }

  // ── Trigger sounds ──
  // Boot: on FIRST user interaction (bypasses browser autoplay block)
  var bootPlayed = false;
  function triggerBoot(){
    if(bootPlayed) return;
    bootPlayed = true;
    playBoot();
    setTimeout(startAmbient, 500);
    doc.removeEventListener('click', triggerBoot, true);
    doc.removeEventListener('keydown', triggerBoot, true);
    doc.removeEventListener('touchstart', triggerBoot, true);
  }
  doc.addEventListener('click', triggerBoot, true);
  doc.addEventListener('keydown', triggerBoot, true);
  doc.addEventListener('touchstart', triggerBoot, true);

  // Whoosh: whenever a Plotly chart appears (MutationObserver)
  var chartCount = 0;
  var observer = new MutationObserver(function(mutations){
    mutations.forEach(function(m){
      m.addedNodes.forEach(function(n){
        if(n.classList && (n.classList.contains('js-plotly-plot') ||
           (n.querySelector && n.querySelector('.js-plotly-plot')))){
          playWhoosh();
          setTimeout(playBeep, 300);
        }
      });
    });
  });
  observer.observe(doc.body, {childList:true, subtree:true});

  // Click: all buttons and selectboxes
  setTimeout(function(){
    doc.addEventListener('click', function(e){
      var t = e.target;
      if(t.tagName==='BUTTON' || t.closest('button') ||
         t.closest('[data-testid="stSelectbox"]') ||
         t.closest('[data-testid="stRadio"]') ||
         t.closest('[data-testid="stSlider"]')){
        playClick();
      }
    }, true);
  }, 3000);

  function tick(){var el=doc.getElementById('clk');if(el){var d=new Date();el.textContent=d.toUTCString().slice(17,25)+' UTC';}setTimeout(tick,1000);}
  setTimeout(tick,2800);
})();
</script>
"""

st.markdown(CSS_JS, unsafe_allow_html=True)
components.html(SCRIPT, height=0, width=0)

# ── CHART BASE CONFIG ─────────────────────────────────────────────────────────
L = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="rgba(0,190,255,0.55)", family="Exo 2", size=10),
    margin=dict(l=6, r=6, t=28, b=6),
    xaxis=dict(gridcolor="rgba(0,200,255,0.05)", zeroline=False,
               tickfont=dict(color="rgba(0,170,255,0.38)", size=9),
               linecolor="rgba(0,200,255,0.07)"),
    yaxis=dict(gridcolor="rgba(0,200,255,0.05)", zeroline=False,
               tickfont=dict(color="rgba(0,170,255,0.38)", size=9),
               linecolor="rgba(0,200,255,0.07)"),
)

CS = {"temperature":"plasma","temp":"plasma","tas":"plasma",
      "precipitation":"ice","precip":"ice","pr_":"ice",
      "wind":"viridis","pressure":"magma","psl":"magma",
      "nao":"RdBu_r","nam":"RdBu_r","sam":"RdBu_r",
      "nino":"RdYlBu_r","sst":"thermal"}

def get_cscale(vname):
    vl = vname.lower()
    for k,v in CS.items():
        if k in vl: return v
    return "plasma"

# ── CHART BUILDERS ────────────────────────────────────────────────────────────
def make_globe(data, lats, lons, cscale="plasma", h=420):
    """Realistic orthographic globe with natural Earth colours + data overlay."""
    max_pts = 6000
    s = max(1, int(np.ceil(np.sqrt(len(lats) * len(lons) / max_pts))))
    la = lats[::s]; lo = lons[::s]; da = data[::s, ::s]
    LAT, LON = np.meshgrid(la, lo, indexing="ij")
    flat_dat = da.flatten()
    flat_lat = LAT.flatten()
    flat_lon = LON.flatten()
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lat=flat_lat, lon=flat_lon, mode="markers",
        marker=dict(
            color=flat_dat, colorscale=cscale,
            size=4.5, opacity=0.82,
            colorbar=dict(
                tickfont=dict(color="rgba(148,163,184,0.5)", size=8, family="Fira Mono"),
                thickness=6, len=0.55,
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(91,139,255,0.08)",
                title=dict(text="", font=dict(size=1)),
                outlinewidth=0,
            )
        ),
        showlegend=False,
        hovertemplate="<b>%{lat:.1f}°  %{lon:.1f}°</b><br>%{marker.color:.2f}<extra></extra>"
    ))
    fig.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=20, lat=20, roll=0),
        showland=True,
        landcolor="rgb(28, 44, 28)",
        showocean=True,
        oceancolor="rgb(4, 14, 42)",
        showlakes=True,
        lakecolor="rgb(6, 18, 52)",
        showrivers=True,
        rivercolor="rgba(40, 80, 160, 0.4)",
        riverwidth=0.5,
        showcoastlines=True,
        coastlinecolor="rgba(110, 170, 110, 0.55)",
        coastlinewidth=0.7,
        showcountries=True,
        countrycolor="rgba(80, 130, 80, 0.18)",
        countrywidth=0.4,
        lataxis=dict(showgrid=True, gridcolor="rgba(91,139,255,0.06)", dtick=30),
        lonaxis=dict(showgrid=True, gridcolor="rgba(91,139,255,0.06)", dtick=30),
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=h,
    )
    return fig
def make_globe_anim(ds, var, tc, lc, oc, cscale, mf=30):
    lats=ds[lc].values; lons=ds[oc].values
    s=3; la=lats[::s]; lo=lons[::s]
    LAT,LON=np.meshgrid(la,lo,indexing="ij")
    lf=LAT.flatten(); of=LON.flatten()
    nt=len(ds[tc]); ist=max(1,nt//mf)
    fidx=list(range(0,nt,ist))
    tl=[str(t)[:10] for t in ds[tc].values]
    vmin=float(ds[var].min()); vmax=float(ds[var].max())
    base=go.Scattergeo(lat=lf,lon=of,mode="markers",
        marker=dict(color=ds[var].isel({tc:0}).values[::s,::s].flatten(),
            colorscale=cscale,size=3.5,opacity=0.9,cmin=vmin,cmax=vmax,
            colorbar=dict(tickfont=dict(color="rgba(0,195,255,0.45)",size=8),
                          thickness=6,len=0.5,bgcolor="rgba(0,0,0,0)",
                          bordercolor="rgba(0,200,255,0.07)")),
        showlegend=False,
        hovertemplate="<b>%{lat:.1f}°N %{lon:.1f}°E</b><br>%{marker.color:.2f}<extra></extra>")
    frames=[go.Frame(data=[go.Scattergeo(lat=lf,lon=of,mode="markers",
        marker=dict(color=ds[var].isel({tc:fi}).values[::s,::s].flatten(),
                    colorscale=cscale,size=3.5,opacity=0.9,cmin=vmin,cmax=vmax),
        showlegend=False)],name=tl[fi]) for fi in fidx]
    fig=go.Figure(data=[base],frames=frames)
    fig.update_geos(projection_type="orthographic",
        showland=True,landcolor="rgba(5,14,32,0.95)",
        showocean=True,oceancolor="rgba(0,3,14,0.97)",
        showcoastlines=True,coastlinecolor="rgba(0,200,255,0.25)",coastlinewidth=0.6,
        showcountries=True,countrycolor="rgba(0,130,200,0.1)",
        showframe=False,bgcolor="rgba(0,0,0,0)")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",geo_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=0,b=0),height=440,
        updatemenus=[dict(type="buttons",showactive=True,x=0.06,y=0.02,
            xanchor="left",yanchor="bottom",
            bgcolor="rgba(0,15,35,0.9)",bordercolor="rgba(0,200,255,0.2)",
            font=dict(family="Orbitron",size=9,color="#80d4f0"),
            buttons=[
                dict(label="▶  PLAY",method="animate",
                     args=[None,dict(frame=dict(duration=160,redraw=True),fromcurrent=True,transition=dict(duration=60))]),
                dict(label="⏸  PAUSE",method="animate",
                     args=[[None],dict(frame=dict(duration=0,redraw=False),mode="immediate",transition=dict(duration=0))])],
            )],
        sliders=[dict(active=0,
            currentvalue=dict(font=dict(family="Orbitron",size=8,color="rgba(0,200,255,0.55)"),prefix="",visible=True,xanchor="center"),
            pad=dict(t=8,b=4),bgcolor="rgba(0,15,35,0.7)",bordercolor="rgba(0,200,255,0.15)",
            tickcolor="rgba(0,200,255,0.2)",font=dict(family="Exo 2",size=7,color="rgba(0,170,255,0.35)"),
            steps=[dict(args=[[f.name],dict(frame=dict(duration=0,redraw=True),mode="immediate")],
                        label=f.name,method="animate") for f in frames])])
    return fig

def make_flat(data, lats, lons, title, cscale="plasma", h=280):
    # Downsample if too large — always derive la2/lo2 FROM data shape, not lats/lons
    max_dim = 500
    sr = max(1, len(lats)//max_dim); sc2 = max(1, len(lons)//max_dim)
    d2 = data[::sr,::sc2]
    # recompute coordinate arrays to exactly match d2 shape
    la2 = np.linspace(float(lats[0]), float(lats[-1]), d2.shape[0])
    lo2 = np.linspace(float(lons[0]), float(lons[-1]), d2.shape[1])
    fig=px.imshow(d2,x=lo2,y=la2,color_continuous_scale=cscale,
                  origin="lower",aspect="auto",labels={"color":""})
    fig.update_layout(**L,height=h,
        title=dict(text=title,font=dict(color="rgba(0,220,255,0.65)",family="Orbitron",size=10),x=0),
        coloraxis_colorbar=dict(
            tickfont=dict(color="rgba(0,170,255,0.45)",size=8),
            thickness=6,len=0.6,
            title=dict(text="",font=dict(size=8)),
            bgcolor="rgba(0,0,0,0)",bordercolor="rgba(0,200,255,0.07)"))
    fig.update_xaxes(showgrid=False,title_text="",linecolor="rgba(0,200,255,0.07)")
    fig.update_yaxes(showgrid=False,title_text="",linecolor="rgba(0,200,255,0.07)")
    return fig

def make_ts(times, vals, color="#00e5ff", h=240, units=""):
    df=pd.DataFrame({"t":pd.to_datetime(times,errors="coerce"),"v":np.array(vals,dtype=float)})
    df["ma"]=df["v"].rolling(3,min_periods=1).mean()
    r,g,b=int(color[1:3],16),int(color[3:5],16),int(color[5:7],16)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df["t"],y=df["v"],mode="lines",
        line=dict(color=f"rgba({r},{g},{b},0.2)",width=1),showlegend=False))
    fig.add_trace(go.Scatter(x=df["t"],y=df["ma"],mode="lines",
        line=dict(color=color,width=2.2),
        fill="tozeroy",fillcolor=f"rgba({r},{g},{b},0.05)",name="Moving avg",showlegend=True))
    vals_arr=np.array(vals,dtype=float); mask=~np.isnan(vals_arr)
    if mask.sum()>=2:
        xn=np.arange(len(vals_arr),dtype=float)
        co=np.polyfit(xn[mask],vals_arr[mask],1)
        tv=np.polyval(co,xn); sd_v=co[0]*120
        fig.add_trace(go.Scatter(x=df["t"],y=tv,mode="lines",
            line=dict(color="#ff5555",width=1.8,dash="dash"),
            name=f"Trend {sd_v:+.2f}{units}/decade",showlegend=True))
    fig.update_layout(**L,height=h,legend=dict(
        font=dict(color="rgba(0,190,255,0.45)",family="Exo 2",size=8),
        bgcolor="rgba(0,0,0,0)",bordercolor="rgba(0,200,255,0.08)",borderwidth=0.5,x=0.01,y=0.99))
    return fig

def make_surface3d(data, lats, lons, title, cscale="plasma", h=420):
    import math
    # Cap to 100x100 max for 3D surface
    max_dim = 100
    s = max(3, max(len(lats)//max_dim, len(lons)//max_dim))
    la=lats[::s]; lo=lons[::s]; da=data[::s,::s]
    fig=go.Figure(go.Surface(z=da,x=lo,y=la,colorscale=cscale,opacity=0.94,
        contours=dict(z=dict(show=True,usecolormap=True,highlightcolor="rgba(0,229,255,0.4)",project_z=False)),
        colorbar=dict(tickfont=dict(color="rgba(0,190,255,0.45)",size=8),
                      thickness=6,len=0.5,bgcolor="rgba(0,0,0,0)",bordercolor="rgba(0,200,255,0.07)")))
    # Camera orbit frames for Z-axis rotation
    surf_frames = [go.Frame(
        layout=dict(scene_camera=dict(eye=dict(
            x=1.5*math.cos(a*math.pi/180),
            y=1.5*math.sin(a*math.pi/180),
            z=0.75
        ))), name=str(a)) for a in range(0, 360, 3)]
    fig.frames = surf_frames
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Lon",gridcolor="rgba(0,200,255,0.07)",tickfont=dict(color="rgba(0,170,255,0.35)",size=7),backgroundcolor="rgba(0,0,0,0)",showbackground=True),
            yaxis=dict(title="Lat",gridcolor="rgba(0,200,255,0.07)",tickfont=dict(color="rgba(0,170,255,0.35)",size=7),backgroundcolor="rgba(0,0,0,0)",showbackground=True),
            zaxis=dict(title="",gridcolor="rgba(0,200,255,0.07)",tickfont=dict(color="rgba(0,170,255,0.35)",size=7),backgroundcolor="rgba(0,0,0,0)",showbackground=True),
            camera=dict(eye=dict(x=1.3,y=1.3,z=1.0))),
        margin=dict(l=0,r=0,t=28,b=0), height=h,
        title=dict(text=title,font=dict(color="rgba(0,220,255,0.65)",family="Orbitron",size=10),x=0),
        updatemenus=[dict(
            type="buttons", showactive=False,
            visible=False, x=0, y=0,
            buttons=[dict(label="▶", method="animate",
                args=[None, dict(
                    frame=dict(duration=50, redraw=True),
                    loop=True, fromcurrent=False,
                    transition=dict(duration=0))])])])
    return fig
def make_windrose(vals, units="m/s", h=260):
    dirs=["N","NE","E","SE","S","SW","W","NW"]
    np.random.seed(42)
    rv=[float(np.mean(np.random.choice(vals,30))) for _ in dirs]
    cls=["#00e5ff","#0090ff","#5050ff","#a040ff","#ff4560","#ff8800","#00cc70","#00d4ff"]
    fig=go.Figure()
    for i,(d,v,c) in enumerate(zip(dirs,rv,cls)):
        fig.add_trace(go.Barpolar(r=[v],theta=[i*45],width=[44],
            marker_color=c,marker_opacity=0.72,showlegend=False,
            hovertemplate=f"{d}: {v:.2f} {units}<extra></extra>"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(tickfont=dict(color="rgba(0,170,255,0.35)",size=8),gridcolor="rgba(0,200,255,0.07)"),
            angularaxis=dict(tickfont=dict(color="rgba(0,170,255,0.5)",size=9,family="Orbitron"),gridcolor="rgba(0,200,255,0.06)")),
        margin=dict(l=15,r=15,t=28,b=15),height=h,
        title=dict(text="WIND DISTRIBUTION",font=dict(color="rgba(0,220,255,0.55)",family="Orbitron",size=9),x=0.5))
    return fig

def anomaly_detect(data, lats, lons, n=3):
    mean=np.nanmean(data); std=np.nanstd(data); res=[]
    d=data.copy()
    nr,nc=d.shape
    # map data indices back to original lats/lons (handles downsampled data)
    lat_idx=np.linspace(0,len(lats)-1,nr).astype(int)
    lon_idx=np.linspace(0,len(lons)-1,nc).astype(int)
    for _ in range(n*5):
        if not np.any(np.isfinite(d)): break
        idx=np.unravel_index(np.nanargmax(np.abs(d-mean)),d.shape)
        i,j=idx[0],idx[1]; v=d[i,j]; z=(v-mean)/(std+1e-9)
        if abs(z)>1.5:
            res.append({"lat":float(lats[lat_idx[i]]),"lon":float(lons[lon_idx[j]]),"val":float(v),"z":float(z)})
        d[max(0,i-3):i+4,max(0,j-3):j+4]=mean
        if len(res)>=n: break
    return res

# ── SMART DATASET PARSER ──────────────────────────────────────────────────────
def fc(ds, cands):
    for c in cands:
        if c in ds.coords: return c
    for c in cands:
        for k in ds.coords:
            if c in k.lower(): return k
    return None

def smart_parse(ds):
    lc = fc(ds,["lat","latitude","y","rlat"])
    oc = fc(ds,["lon","longitude","x","rlon"])
    tc = fc(ds,["time","date","t","TIME"])
    all_vars = list(ds.data_vars)
    vars_3d=[]; vars_2d=[]; vars_1d=[]
    if tc and lc and oc:
        for v in all_vars:
            dims=ds[v].dims
            if len(dims)==3 and tc in dims and lc in dims and oc in dims:
                vars_3d.append(v)
    if lc and oc:
        for v in all_vars:
            dims=ds[v].dims
            if len(dims)==2 and lc in dims and oc in dims:
                vars_2d.append(v)
    if tc:
        for v in all_vars:
            if len(ds[v].dims)==1 and tc in ds[v].dims:
                vars_1d.append(v)
    if vars_3d:
        return vars_3d, tc, lc, oc, True, "standard"
    elif vars_2d:
        return vars_2d, None, lc, oc, False, "cvdp_spatial"
    else:
        fb=[v for v in all_vars if ds[v].ndim>=2]
        return (fb or all_vars[:5]), tc, lc, oc, False, "other"

def safe_slice(ds, var, tc, tidx, lats, lons, is_3d):
    try:
        arr = ds[var].values.astype(float)
        if arr.ndim==2: return arr
        if arr.ndim==3:
            idx=min(tidx,arr.shape[0]-1); return arr[idx]
        if arr.ndim>3:
            while arr.ndim>3: arr=arr[0]
            return arr[min(tidx,arr.shape[0]-1)]
        if arr.ndim==1:
            row=arr[:len(lons)]; result=np.tile(row,(len(lats),1))
            if result.shape[1]<len(lons): result=np.pad(result,((0,0),(0,len(lons)-result.shape[1])),mode="edge")
            return result[:len(lats),:len(lons)]
        return np.full((len(lats),len(lons)),float(arr.flat[0]) if arr.size else 0.0)
    except Exception:
        return np.zeros((len(lats),len(lons)))

def clean2d(arr):
    if not np.any(np.isfinite(arr)): return np.zeros_like(arr)
    med=float(np.nanmedian(arr[np.isfinite(arr)]))
    return np.where(np.isfinite(arr),arr,med)

# ── SAMPLE DATA ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def sample_data():
    np.random.seed(42)
    lats=np.linspace(-90,90,73); lons=np.linspace(-180,180,144)
    times=pd.date_range("1990-01-01",periods=120,freq="MS")
    la,_=np.meshgrid(lats,lons,indexing="ij"); bt=30-0.5*np.abs(la)
    T=np.zeros((120,73,144),dtype=np.float32)
    P=np.zeros_like(T); W=np.zeros_like(T)
    for t,dt in enumerate(times):
        T[t]=(bt+10*np.cos(2*np.pi*(dt.month-7)/12)*(la/90)+np.random.normal(0,1.5,(73,144))+0.02*t).astype(np.float32)
        P[t]=np.clip(8*np.exp(-((la-5)**2)/(2*15**2))+np.abs(np.random.normal(0,0.8,(73,144))),0,None).astype(np.float32)
        W[t]=(12*np.exp(-((la-50)**2)/(2*8**2))+14*np.exp(-((la+50)**2)/(2*8**2))+np.abs(np.random.normal(0,2,(73,144)))).astype(np.float32)
    return xr.Dataset({
        "temperature":(["time","lat","lon"],T,{"units":"°C","long_name":"Surface Temperature"}),
        "precipitation":(["time","lat","lon"],P,{"units":"mm/day","long_name":"Precipitation Rate"}),
        "wind_speed":(["time","lat","lon"],W,{"units":"m/s","long_name":"Wind Speed"}),
    },coords={"time":times,"lat":lats,"lon":lons})

@st.cache_data(show_spinner=False)
def load_nc(b, fname="file.nc"):
    tmp=None
    try:
        with tempfile.NamedTemporaryFile(suffix=".nc",delete=False) as f:
            f.write(b); tmp=f.name
        try: ds=xr.open_dataset(tmp).load()
        except: ds=xr.open_dataset(tmp,decode_times=False).load()
        return ds
    finally:
        if tmp and os.path.exists(tmp):
            try: os.unlink(tmp)
            except: pass

@st.cache_data(show_spinner=False)
def load_nc_path(path):
    import glob as gl
    if os.path.isdir(path):
        files=sorted(gl.glob(os.path.join(path,"*.nc")))
        if not files: raise ValueError(f"No .nc files in: {path}")
        try: return xr.open_mfdataset(files,combine="by_coords",decode_times=False,chunks={"time":1})
        except: return xr.open_mfdataset(files,combine="nested",concat_dim="ensemble",decode_times=False,chunks={"time":1})
    else:
        try: return xr.open_dataset(path,chunks={"time":1})
        except: return xr.open_dataset(path,decode_times=False,chunks={"time":1})

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div class="logo-wrap"><div class="logo-orb">🌍</div>
    <div class="logo-name">PYCLIMA</div>
    <div class="logo-tag">Earth Observation System</div></div>""",unsafe_allow_html=True)
    st.markdown('<div class="nav-lbl"><span>Navigation</span></div>',unsafe_allow_html=True)
    page=st.radio("Navigation",["🌐 Earth View","🎬 Animated Globe","🏔️ 3D Surface","⚖️ Compare","📡 Story Mode"],label_visibility="collapsed")
    st.markdown('<div class="nav-lbl"><span>Data Source</span></div>',unsafe_allow_html=True)
    load_mode=st.radio("Load Mode",["⬆ Upload","📁 File Path","⚡ Sample"],label_visibility="collapsed")
    uploaded=None; file_path=None; use_sample=False; load_path_btn=False
    if load_mode=="⬆ Upload":
        uploaded=st.file_uploader("Upload NetCDF",type=["nc"],accept_multiple_files=True,label_visibility="collapsed")
    elif load_mode=="📁 File Path":
        st.markdown('<div style="font-size:0.7rem;color:rgba(0,200,255,0.5);padding:2px">Folder or .nc file path:</div>',unsafe_allow_html=True)
        file_path=st.text_input("Path",placeholder=r"E:\data\extract",label_visibility="collapsed")
        load_path_btn=st.button("⚡ Load from Path")
    else:
        use_sample=True
    st.markdown('<div class="nav-lbl"><span>Mission Team</span></div>',unsafe_allow_html=True)
    st.markdown("""<div class="team-box"><div class="team-name">COSMOS_SYNC</div>
    GLA University · Mathura<br><br>
    Aryan Agarwal · TX261925<br>Ashish Sindhi · TX262412<br>
    Aditya Mishra · TX262422<br>Sarthak Dubey · TX262429<br><br>
    <span style="color:rgba(0,140,190,0.3);font-size:0.6rem;font-family:'Orbitron',monospace;letter-spacing:1px">
    TECHNEX '26<br>HACK IT OUT<br>IIT (BHU) VARANASI</span></div>""",unsafe_allow_html=True)

# ── DATA LOADING ──────────────────────────────────────────────────────────────
if "ds" not in st.session_state:
    st.session_state.ds=sample_data(); st.session_state.src="SAMPLE DATASET"
if uploaded:
    try:
        with st.spinner("⏳ Loading..."):
            if len(uploaded)==1:
                st.session_state.ds=load_nc(uploaded[0].read(),uploaded[0].name)
                st.session_state.src=uploaded[0].name
            else:
                import tempfile as _tf
                tmps=[]
                for uf in uploaded:
                    with _tf.NamedTemporaryFile(suffix=".nc",delete=False) as f:
                        f.write(uf.read()); tmps.append(f.name)
                try:
                    try: dst=xr.open_mfdataset(tmps,combine="by_coords",decode_times=False); st.session_state.ds=dst.load()
                    except: dst=xr.open_mfdataset(tmps,combine="nested",concat_dim="ensemble",decode_times=False); st.session_state.ds=dst.load()
                finally:
                    for t in tmps:
                        try: os.unlink(t)
                        except: pass
                st.session_state.src=f"{len(uploaded)} files"
        st.success(f"✅ Loaded: {st.session_state.src}")
    except Exception as e: st.error(f"❌ {e}")
elif load_path_btn and file_path:
    if os.path.exists(file_path):
        try:
            with st.spinner(f"⏳ Loading {os.path.basename(file_path)}..."):
                st.session_state.ds=load_nc_path(file_path)
                st.session_state.src=os.path.basename(file_path)
            st.success(f"✅ Loaded: {st.session_state.src}")
        except Exception as e: st.error(f"❌ {e}")
    else: st.error(f"❌ Path not found: {file_path}")
elif use_sample:
    st.session_state.ds=sample_data(); st.session_state.src="SAMPLE DATASET"

ds=st.session_state.ds
dvars,tc,lc,oc,is_3d,dataset_type=smart_parse(ds)
lats=ds[lc].values if lc and lc in ds.coords else np.linspace(-90,90,73)
lons=ds[oc].values if oc and oc in ds.coords else np.linspace(-180,180,144)
if is_3d and tc:
    tarr=ds[tc].values; tlbl=[str(t)[:10] for t in tarr]; nt=len(tarr)
else:
    tarr=[]; tlbl=[v[:20] for v in dvars]; nt=len(dvars)

# ── COMMAND BAR ───────────────────────────────────────────────────────────────
src=st.session_state.get("src","SAMPLE DATASET")
st.markdown(f"""<div class="cmd-bar">
  <div><div class="cmd-logo">🌍 &nbsp;PYCLIMAEXPLORER</div>
  <div class="cmd-info">EARTH OBSERVATION SYSTEM &nbsp;·&nbsp; {src} &nbsp;·&nbsp; {len(dvars)} VARIABLES &nbsp;·&nbsp; {nt} TIME STEPS</div></div>
  <div class="cmd-status">
    <div class="cmd-clock" id="clk">-- : -- : -- UTC</div>
    <div class="cmd-online">● &nbsp;ONLINE</div>
  </div></div>""",unsafe_allow_html=True)

# CVDP banner
if dataset_type=="cvdp_spatial":
    st.markdown("""<div class="info-banner"><div class="info-banner-title">📡 CVDP DATASET DETECTED</div>
    This is a <b>Climate Variability Diagnostics Package (CVDP)</b> file containing 2D spatial patterns
    (NAO, SAM, NAM, PSL trends, ENSO composites, etc.). Each variable is a lat/lon pattern.
    Animated Globe requires a standard time-series NetCDF — use Sample Data for that demo.
    </div>""",unsafe_allow_html=True)

# ── CONTROLS ──────────────────────────────────────────────────────────────────
st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
ca,cb,cc=st.columns([1.4,1.6,3])
with ca:
    sel_v=st.selectbox("Variable",dvars,format_func=lambda v:ds[v].attrs.get("long_name",v).upper()[:40])
    units=ds[sel_v].attrs.get("units",""); lname=ds[sel_v].attrs.get("long_name",sel_v).title()
    cscale=get_cscale(sel_v)
with cb:
    sel_lat=st.slider("Latitude",float(lats.min()),float(lats.max()),20.0,step=2.5)
    sel_lon=st.slider("Longitude",float(lons.min()),float(lons.max()),77.0,step=2.5)
with cc:
    if is_3d and nt>1:
        t_range=st.select_slider("Time Range",options=list(range(nt)),value=(0,nt-1),
                                  format_func=lambda i:tlbl[i] if tlbl else str(i))
        t_start,t_end=t_range
        tidx=st.slider("View Step",t_start,max(t_end,t_start+1),t_start)
        st.caption(f"📅  {tlbl[tidx]}  |  Range: {tlbl[t_start]} → {tlbl[t_end]}")
    elif not is_3d and nt>1:
        tidx=st.select_slider("Pattern Index",options=list(range(nt)),format_func=lambda i:tlbl[i] if i<len(tlbl) else str(i))
        t_start,t_end=0,nt-1
        st.caption(f"📡  Showing: {tlbl[tidx] if tidx<len(tlbl) else sel_v}")
    else:
        tidx=0; t_start=0; t_end=0

# Get 2D slice
if not is_3d and dataset_type=="cvdp_spatial":
    display_var=dvars[min(tidx,len(dvars)-1)]
    sd=clean2d(safe_slice(ds,display_var,tc,0,lats,lons,False))
    current_label=ds[display_var].attrs.get("long_name",display_var).title()
else:
    sd=clean2d(safe_slice(ds,sel_v,tc,tidx,lats,lons,is_3d))
    current_label=lname

li=min(int(np.argmin(np.abs(lats-sel_lat))),sd.shape[0]-1)
oi=min(int(np.argmin(np.abs(lons-sel_lon))),sd.shape[1]-1)

# ── KPI ROW ───────────────────────────────────────────────────────────────────
cur=float(sd[li,oi]); mn=float(np.nanmin(sd)); mx=float(np.nanmax(sd)); mean_=float(np.nanmean(sd))
if is_3d and nt>=24 and tc and tc in ds[sel_v].dims:
    early=float(ds[sel_v].isel({tc:slice(0,12),lc:li,oc:oi}).mean().values)
    late=float(ds[sel_v].isel({tc:slice(-12,None),lc:li,oc:oi}).mean().values)
    tr=late-early; tdlbl=f">{'▲' if tr>=0 else '▼'} {abs(tr):.2f} {units}/decade"; tcol="#00ff96" if tr>=0 else "#ff5555"
else:
    tdlbl=f"({sel_lat:.0f}°, {sel_lon:.0f}°)"; tcol="#00e5ff"
kpis=[("#00e5ff","Target Location",f"{cur:.1f}",units,tdlbl,tcol),
      ("#00b4ff","Global Mean",f"{mean_:.1f}",units,f"Range {mn:.1f}–{mx:.1f}","#00b4ff"),
      ("#a060ff","Peak Value",f"{mx:.1f}",units,"Current time step","#a060ff"),
      ("#ff5555","Low Value",f"{mn:.1f}",units,"Current time step","#ff5555")]
st.markdown('<div class="kpi-row">',unsafe_allow_html=True)
cols=st.columns(4)
for col,(kc,kl,kv,ku,ks,sc) in zip(cols,kpis):
    with col:
        st.markdown(f"""<div class="kpi" style="--c:{kc}">
          <div class="kpi-dot-tl"></div><div class="kpi-dot-br"></div>
          <div class="kpi-lbl">{kl}</div>
          <div class="kpi-num">{kv}<span class="kpi-unit">{ku}</span></div>
          <div class="kpi-delta" style="color:{sc}">{ks}</div></div>""",unsafe_allow_html=True)
st.markdown('</div><div style="height:14px"></div>',unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def card_open(title,sub=""):
    st.markdown(f'<div class="g-card"><div class="g-card-tl"></div><div class="g-title">{title}</div>{"<div class=g-sub>"+sub+"</div>" if sub else ""}',unsafe_allow_html=True)
def card_close(): st.markdown('</div>',unsafe_allow_html=True)
def divider(label):
    st.markdown(f'<div class="sec-div"><div class="sec-div-dot"></div><span>{label}</span><div class="sec-div-line"></div></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: EARTH VIEW
# ══════════════════════════════════════════════════════════════════════════════
if page=="🌐 Earth View":
    c1,c2=st.columns([1.3,1],gap="medium")
    with c1:
        card_open("// 3D Earth Projection",f"{current_label.upper()} — Orthographic Globe")
        st.plotly_chart(make_globe(sd,lats,lons,cscale,h=410),width='stretch')
        anz=anomaly_detect(sd.copy(),lats,lons,3)
        if anz:
            st.markdown('<div style="margin-top:4px;display:flex;flex-wrap:wrap">',unsafe_allow_html=True)
            for a in anz:
                t2="hot" if a["z"]>0 else "cold"; ic="▲" if a["z"]>0 else "▼"
                st.markdown(f'<span class="ab ab-{t2}">{ic} {a["lat"]:.1f}°, {a["lon"]:.1f}° → {a["val"]:.2f} {units} (z={a["z"]:.1f}σ)</span>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
        card_close()
    with c2:
        card_open("// Flat Map","Equirectangular — selected point marked")
        ff=make_flat(sd,lats,lons,"",cscale,h=185)
        ff.add_trace(go.Scatter(x=[lons[oi]],y=[lats[li]],mode="markers",
            marker=dict(color="#ff5555",size=12,symbol="cross-thin",line=dict(color="#ff5555",width=3)),showlegend=False))
        st.plotly_chart(ff,width='stretch')
        # use linspace to match sd's actual shape
        _la=np.linspace(float(lats[0]),float(lats[-1]),sd.shape[0])
        _lo=np.linspace(float(lons[0]),float(lons[-1]),sd.shape[1])
        map_csv=pd.DataFrame(sd,index=[f"{v:.1f}" for v in _la],columns=[f"{v:.1f}" for v in _lo]).to_csv().encode()
        lbl=tlbl[tidx] if (tlbl and tidx<len(tlbl)) else str(tidx)
        st.download_button("⬇ Map CSV",map_csv,file_name=f"{sel_v}_{lbl}.csv",mime="text/csv",width='stretch')
        st.markdown('<div class="g-title" style="margin-top:6px">// Signal Time Series</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="g-sub">({sel_lat:.1f}°N, {sel_lon:.1f}°E)</div>',unsafe_allow_html=True)
        if is_3d and tc and tc in ds[sel_v].dims:
            ts_vals=ds[sel_v].isel({lc:li,oc:oi}).values.astype(float)
            st.plotly_chart(make_ts(tarr,ts_vals,"#00e5ff",155,units),width='stretch')
            ts_csv=pd.DataFrame({"Date":pd.to_datetime(tarr,errors="coerce"),lname:ts_vals}).to_csv(index=False).encode()
            st.download_button("⬇ Time Series CSV",ts_csv,file_name=f"{sel_v}_ts.csv",mime="text/csv",width='stretch')
        else:
            vals_across=[]
            for vn in dvars[:20]:
                try:
                    arr=ds[vn].values
                    vals_across.append(float(np.nanmean(arr[np.isfinite(arr)])) if arr.ndim>=2 else 0.0)
                except: vals_across.append(0.0)
            ma=np.mean(vals_across)
            fb=go.Figure(go.Bar(x=[v[:15] for v in dvars[:20]],y=vals_across,
                marker=dict(color=["#ff5555" if v>ma else "#00b4ff" for v in vals_across]),opacity=0.8))
            fb.update_layout(**L,height=155,title=dict(text="PATTERN GLOBAL MEANS",font=dict(color="rgba(0,220,255,0.55)",family="Orbitron",size=8),x=0))
            fb.update_xaxes(tickangle=-45,tickfont=dict(size=6))
            st.plotly_chart(fb,width='stretch')
        card_close()

    st.markdown('<div style="height:12px"></div>',unsafe_allow_html=True)
    r2a,r2b,r2c=st.columns([1.5,1.5,1.3],gap="medium")
    with r2a:
        card_open("// Monthly / Pattern Signal","Global mean per time step")
        if is_3d and tc and tc in ds[sel_v].dims and nt>=2:
            mv=[float(ds[sel_v].isel({tc:i}).mean().values) for i in range(nt)]
            ma=np.mean(mv); mc=["#ff5555" if v>ma else "#00b4ff" for v in mv]
            fb=go.Figure(go.Bar(x=tlbl[:len(mv)],y=mv,marker=dict(color=mc,line_width=0),opacity=0.8))
            fb.add_hline(y=ma,line_dash="dash",line_color="rgba(0,229,255,0.22)")
            fb.update_layout(**L,height=210); fb.update_xaxes(tickangle=-50,tickfont=dict(size=7))
            st.plotly_chart(fb,width='stretch')
            bar_csv=pd.DataFrame({"Date":tlbl[:len(mv)],f"Mean {lname}":mv}).to_csv(index=False).encode()
            st.download_button("⬇ Monthly CSV",bar_csv,file_name=f"{sel_v}_monthly.csv",mime="text/csv",width='stretch')
        else:
            mv=[]
            for vn in dvars[:30]:
                try:
                    arr=ds[vn].values
                    mv.append(float(np.nanmean(arr[np.isfinite(arr)])) if np.any(np.isfinite(arr)) else 0.0)
                except: mv.append(0.0)
            ma=np.mean(mv); mc=["#ff5555" if v>ma else "#00b4ff" for v in mv]
            fb=go.Figure(go.Bar(x=[v[:12] for v in dvars[:30]],y=mv,marker=dict(color=mc,line_width=0),opacity=0.8))
            fb.add_hline(y=ma,line_dash="dash",line_color="rgba(0,229,255,0.22)")
            fb.update_layout(**L,height=210); fb.update_xaxes(tickangle=-50,tickfont=dict(size=6))
            st.plotly_chart(fb,width='stretch')
        card_close()
    with r2b:
        card_open("// Zonal Profile","Latitude-band mean")
        zn=np.nanmean(sd,axis=1)
        fz=go.Figure(go.Scatter(x=zn,y=lats,mode="lines",line=dict(color="#a060ff",width=2.2),fill="tozerox",fillcolor="rgba(160,96,255,0.06)"))
        fz.update_layout(**L,height=210)
        fz.update_xaxes(title_text=units,gridcolor="rgba(0,200,255,0.05)",tickfont=dict(color="rgba(0,170,255,0.38)",size=8))
        fz.update_yaxes(title_text="Lat°",gridcolor="rgba(0,200,255,0.05)",tickfont=dict(color="rgba(0,170,255,0.38)",size=8))
        st.plotly_chart(fz,width='stretch')
        card_close()
    with r2c:
        wv=next((v for v in dvars if "wind" in v.lower()),None)
        if wv and is_3d and tc and tc in ds[wv].dims:
            wu=ds[wv].attrs.get("units","m/s")
            card_open("// Wind Rose","Directional distribution")
            st.plotly_chart(make_windrose(ds[wv].isel({lc:li,oc:oi}).values,wu,h=210),width='stretch')
        else:
            scols=["#00e5ff","#00ff96","#a060ff","#ff5555"]
            card_open("// All Channels","Variable sparklines")
            for vi,vn in enumerate(dvars[:4]):
                try:
                    if is_3d and tc and tc in ds[vn].dims:
                        vts=ds[vn].isel({lc:li,oc:oi}).values.astype(float)
                    else:
                        arr=ds[vn].values
                        import warnings; warnings.filterwarnings("ignore")
                        vts=np.nanmean(arr,axis=1) if arr.ndim==2 else arr.flatten()[:73]
                        vts=np.where(np.isfinite(vts),vts,0.0)
                    vl=ds[vn].attrs.get("long_name",vn).upper()[:20]; vu=ds[vn].attrs.get("units","")
                    sc_=scols[vi%4]; r_,g_,b_=int(sc_[1:3],16),int(sc_[3:5],16),int(sc_[5:7],16)
                    fsp=go.Figure(go.Scatter(x=list(range(len(vts))),y=vts,mode="lines",
                        line=dict(color=sc_,width=1.5),fill="tozeroy",fillcolor=f"rgba({r_},{g_},{b_},0.06)"))
                    fsp.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0,r=0,t=16,b=0),height=48,
                        title=dict(text=f"{vl} ({vu})",font=dict(color=sc_,family="Orbitron",size=7),x=0),
                        xaxis=dict(visible=False),yaxis=dict(visible=False))
                    st.plotly_chart(fsp,width='stretch')
                except: pass
        card_close()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ANIMATED GLOBE
# ══════════════════════════════════════════════════════════════════════════════
elif page=="🎬 Animated Globe":
    divider("Native Plotly Animation — Browser 60fps — No Reload")
    if not is_3d:
        card_open("// Pattern Gallery","CVDP 2D spatial patterns")
        st.markdown("""<div class="info-banner"><div class="info-banner-title">ℹ️ CVDP MODE</div>
        2D spatial patterns detected. Showing selected pattern globe + flat map.
        For time-animated globe, load a standard (time,lat,lon) NetCDF or use ⚡ Sample Data.
        </div>""",unsafe_allow_html=True)
        ia,ib=st.columns(2,gap="medium")
        with ia:
            cur_var=dvars[min(tidx,len(dvars)-1)]
            cur_data=clean2d(safe_slice(ds,cur_var,tc,0,lats,lons,False))
            st.plotly_chart(make_globe(cur_data,lats,lons,get_cscale(cur_var),h=360),width='stretch')
        with ib:
            st.plotly_chart(make_flat(cur_data,lats,lons,cur_var[:30],get_cscale(cur_var),h=360),width='stretch')
        card_close()
    else:
        card_open(f"// Global Timelapse — {current_label.upper()}","Press ▶ PLAY — smooth native animation · full scrubber")
        mf=st.slider("Max frames",10,min(60,nt),30,step=5,key="mfr")
        with st.spinner("Compiling animation..."):
            fig_a=make_globe_anim(ds,sel_v,tc,lc,oc,cscale,mf=mf)
        st.plotly_chart(fig_a,width='stretch')
        card_close()
        st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)
        ia,ib=st.columns(2,gap="medium")
        with ia:
            card_open("// Global Mean Over Time","Area average — full record")
            if tc in ds[sel_v].dims:
                gm=[float(ds[sel_v].isel({tc:i}).mean().values) for i in range(nt)]
                fg=go.Figure(go.Scatter(x=list(range(nt)),y=gm,mode="lines",line=dict(color="#00e5ff",width=2.2),fill="tozeroy",fillcolor="rgba(0,229,255,0.04)"))
                fg.add_vline(x=tidx,line_dash="dash",line_color="rgba(255,255,255,0.15)")
                fg.update_layout(**L,height=190)
                step=max(1,nt//10)
                fg.update_xaxes(tickvals=list(range(0,nt,step)),ticktext=tlbl[::step] if tlbl else [],tickfont=dict(size=8))
                st.plotly_chart(fg,width='stretch')
            card_close()
        with ib:
            card_open("// Hemisphere Split","Northern vs Southern mean")
            if tc in ds[sel_v].dims and lc:
                lm=len(lats)//2
                nh=[float(ds[sel_v].isel({tc:i}).values[:lm].mean()) for i in range(nt)]
                sh=[float(ds[sel_v].isel({tc:i}).values[lm:].mean()) for i in range(nt)]
                fh=go.Figure()
                fh.add_trace(go.Scatter(x=list(range(nt)),y=nh,name="Northern",line=dict(color="#ff5555",width=1.8),mode="lines"))
                fh.add_trace(go.Scatter(x=list(range(nt)),y=sh,name="Southern",line=dict(color="#00b4ff",width=1.8),mode="lines"))
                fh.update_layout(**L,height=190,legend=dict(font=dict(color="rgba(0,185,255,0.45)",size=8,family="Exo 2"),bgcolor="rgba(0,0,0,0)",x=0.01,y=0.99))
                step=max(1,nt//10)
                fh.update_xaxes(tickvals=list(range(0,nt,step)),ticktext=tlbl[::step] if tlbl else [],tickfont=dict(size=8))
                st.plotly_chart(fh,width='stretch')
            card_close()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: 3D SURFACE
# ══════════════════════════════════════════════════════════════════════════════
elif page=="🏔️ 3D Surface":
    divider("3D Surface Terrain Render — Drag · Rotate · Zoom")
    s1,s2=st.columns([2,1],gap="medium")
    with s1:
        card_open(f"// 3D Surface — {current_label.upper()}","Drag to rotate · scroll to zoom")
        st.plotly_chart(make_surface3d(sd,lats,lons,current_label.upper(),cscale,h=460),width='stretch')
        card_close()
    with s2:
        card_open("// Distribution","Histogram of current data")
        fh=go.Figure(go.Histogram(x=sd.flatten(),nbinsx=40,marker=dict(color="#a060ff",opacity=0.72,line=dict(width=0))))
        fh.update_layout(**L,height=190,bargap=0.04)
        st.plotly_chart(fh,width='stretch')
        card_close()
        st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)
        card_open("// Statistics")
        flat_=sd.flatten(); fin=flat_[np.isfinite(flat_)]
        skew_v=float(pd.Series(fin).skew()) if len(fin)>2 else 0.0
        sdf=pd.DataFrame({"Metric":["Mean","Median","Std Dev","Skewness","Min","Max"],
            "Value":[f"{np.nanmean(flat_):.3f}",f"{np.nanmedian(flat_):.3f}",f"{np.nanstd(flat_):.3f}",
                     f"{skew_v:.3f}",f"{np.nanmin(flat_):.3f}",f"{np.nanmax(flat_):.3f}"],"Unit":[units]*6})
        st.dataframe(sdf,width='stretch',hide_index=True)
        card_close()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: COMPARE
# ══════════════════════════════════════════════════════════════════════════════
elif "Compare" in page:
    divider("Temporal Comparison Module")
    c1,c2,c3=st.columns(3)
    if not is_3d:
        with c1: ia_=st.selectbox("Pattern A",range(len(dvars)),format_func=lambda i:dvars[i][:30],index=0)
        with c2: ib_=st.selectbox("Pattern B",range(len(dvars)),format_func=lambda i:dvars[i][:30],index=min(1,len(dvars)-1))
        with c3: dm=st.selectbox("Diff Mode",["Absolute (B−A)","Percentage (%)","Z-Score"])
        daa=clean2d(safe_slice(ds,dvars[ia_],tc,0,lats,lons,False))
        dab=clean2d(safe_slice(ds,dvars[ib_],tc,0,lats,lons,False))
        label_a=dvars[ia_][:20]; label_b=dvars[ib_][:20]
    else:
        with c1: ia_=st.selectbox("Time Step A",range(nt),format_func=lambda i:tlbl[i],index=0)
        with c2: ib_=st.selectbox("Time Step B",range(nt),format_func=lambda i:tlbl[i],index=min(12,nt-1))
        with c3: dm=st.selectbox("Diff Mode",["Absolute (B−A)","Percentage (%)","Z-Score"])
        daa=clean2d(ds[sel_v].isel({tc:ia_}).values.astype(float))
        dab=clean2d(ds[sel_v].isel({tc:ib_}).values.astype(float))
        label_a=tlbl[ia_]; label_b=tlbl[ib_]
    if dm=="Percentage (%)": diff=np.where(np.abs(daa)>0.01,(dab-daa)/np.abs(daa)*100,0); dt="DELTA % (B/A)"
    elif dm=="Z-Score": diff=(dab-np.nanmean(daa))/(np.nanstd(daa)+1e-9); dt="Z-SCORE (B)"
    else: diff=dab-daa; dt="DELTA (B−A)"
    m1,m2,m3=st.columns(3,gap="medium")
    for col,dat,ttl,cs in [(m1,daa,f"FRAME A · {label_a}",cscale),(m2,dab,f"FRAME B · {label_b}",cscale),(m3,diff,dt,"RdBu_r")]:
        with col: st.plotly_chart(make_flat(dat,lats,lons,ttl,cs,h=270),width='stretch')
    comp_csv=pd.DataFrame({f"A_{label_a}":daa.flatten(),f"B_{label_b}":dab.flatten(),"Diff":diff.flatten()}).to_csv(index=False).encode()
    st.download_button("⬇ Comparison CSV",comp_csv,file_name=f"comparison_{sel_v}.csv",mime="text/csv")
    divider("Statistical Analysis")
    ca,cb=st.columns(2,gap="medium")
    with ca:
        def sk(x):
            try: return float(pd.Series(x[np.isfinite(x)].flatten()).skew())
            except: return 0.0
        sdf2=pd.DataFrame({"Metric":["Mean","Min","Max","Std Dev","Skewness"],
            f"A ({label_a})":[f"{np.nanmean(daa):.3f}",f"{np.nanmin(daa):.3f}",f"{np.nanmax(daa):.3f}",f"{np.nanstd(daa):.3f}",f"{sk(daa):.3f}"],
            f"B ({label_b})":[f"{np.nanmean(dab):.3f}",f"{np.nanmin(dab):.3f}",f"{np.nanmax(dab):.3f}",f"{np.nanstd(dab):.3f}",f"{sk(dab):.3f}"],
            "Delta B−A":[f"{np.nanmean(dab)-np.nanmean(daa):+.3f}",f"{np.nanmin(dab)-np.nanmin(daa):+.3f}",f"{np.nanmax(dab)-np.nanmax(daa):+.3f}",f"{np.nanstd(dab)-np.nanstd(daa):+.3f}","—"]})
        st.dataframe(sdf2,width='stretch',hide_index=True)
    with cb:
        card_open("// Scatter A vs B","Point correlation between frames")
        st_=4; mn2=min(float(np.nanmin(daa)),float(np.nanmin(dab))); mx2=max(float(np.nanmax(daa)),float(np.nanmax(dab)))
        fs=go.Figure(go.Scattergl(x=daa[::st_,::st_].flatten(),y=dab[::st_,::st_].flatten(),mode="markers",marker=dict(color="#a060ff",size=2.5,opacity=0.38)))
        fs.add_trace(go.Scatter(x=[mn2,mx2],y=[mn2,mx2],mode="lines",line=dict(color="rgba(255,255,255,0.12)",dash="dash",width=1),showlegend=False))
        fs.update_layout(**L,height=200,xaxis_title=f"A ({units})",yaxis_title=f"B ({units})")
        st.plotly_chart(fs,width='stretch'); card_close()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: STORY MODE
# ══════════════════════════════════════════════════════════════════════════════
elif "Story" in page:
    divider("Climate Anomaly Intelligence — Guided Tour")
    def gv(i): return dvars[min(i,len(dvars)-1)]
    def gt(i): return min(i,nt-1) if is_3d else 0
    stories={
        "🌡️ Arctic Amplification":{"color":"#ff5555","var":gv(0),"tidx":gt(60),
            "body":"This is the most alarming signal in modern climate science — the Arctic is warming 3–4× faster than the global average. Look at the deep red hotspot over the polar region in this visualization. While the global mean temperature has risen ~1.1°C since pre-industrial times, the Arctic has already crossed +3°C. This 'Arctic Amplification' is caused by melting sea ice exposing dark ocean water, which absorbs far more solar heat than reflective ice — a dangerous feedback loop that is accelerating.",
            "fact":"🚨 Since 1979, Arctic sea ice has lost 13% of its extent per decade. Summer sea ice could vanish entirely before 2050 — something Earth has not seen in 3 million years."},
        "🌧️ Monsoon Intensification":{"color":"#00b4ff","var":gv(1),"tidx":gt(3),
            "body":"A warmer atmosphere holds 7% more moisture for every 1°C of warming — this is the Clausius-Clapeyron equation in action. The equatorial precipitation band visible here is intensifying. South Asia's monsoon, which sustains 1.5 billion people, is becoming more erratic — shorter but more intense bursts of rain are replacing steady seasonal rainfall. This threatens both flooding and drought in the same region within the same year.",
            "fact":"🌊 Extreme rainfall events have increased by 50% over India in the last 30 years. The 2013 Uttarakhand floods killed 6,000 people — an event made 5× more likely by climate change."},
        "💨 Jet Stream Disruption":{"color":"#a060ff","var":gv(2),"tidx":gt(0),
            "body":"The polar jet stream — visible here as the high wind-speed band at 50–60°N — is slowing down as the Arctic warms. A slower jet stream creates larger, more persistent weather 'waves' that lock heat domes, floods, and cold snaps in place for weeks. The 2021 Pacific Northwest heat dome (49.6°C in Canada) and the 2022 Pakistan floods that submerged 1/3 of the country are both linked to this disruption.",
            "fact":"⚡ The jet stream has slowed ~15% since 1980. Extreme weather events that used to last 5 days now persist for 2–3 weeks — causing far greater economic and human damage."},
        "❄️ Cryosphere Collapse":{"color":"#00e0a0","var":gv(0),"tidx":gt(6),
            "body":"The polar temperature signal shown here is ground truth for one of the most dangerous tipping points in Earth's climate system. The Greenland and Antarctic ice sheets together hold enough ice to raise global sea levels by 65 metres. Even a partial collapse — 1–2 metres by 2100 — would displace 1 billion people living in coastal cities. The cold blue poles in early decades vs the warming signal at decade 6 visually shows the trajectory we are on right now.",
            "fact":"🧊 Greenland is losing 280 billion tonnes of ice per year — 6× faster than in the 1990s. Miami, Mumbai, Shanghai, and Bangladesh face existential flooding risk this century."},
    }
    sl,sr=st.columns([1,2.8],gap="large")
    with sl:
        sk=st.radio("Story",list(stories.keys()),label_visibility="collapsed")
        info=stories[sk]; ac=info["color"]
        st.markdown(f"""<div class="fact-box" style="--ac:{ac}"><span class="fact-box-tag">DID YOU KNOW</span>{info['fact']}</div>""",unsafe_allow_html=True)
    with sr:
        st.markdown(f"""<div class="story-card" style="--ac:{ac}"><div class="story-hed">{sk}</div>{info['body']}</div>""",unsafe_allow_html=True)
        st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)
        sv=info["var"]; sda=clean2d(safe_slice(ds,sv,tc,info["tidx"],lats,lons,is_3d))
        sl2=ds[sv].attrs.get("long_name",sv).upper()[:30]; scs=get_cscale(sv)
        sa,sb=st.columns([1.4,1],gap="medium")
        with sa:
            card_open("// 3D Globe View",sl2)
            st.plotly_chart(make_globe(sda,lats,lons,scs,h=295),width='stretch')
            card_close()
        with sb:
            r_,g_,b_=int(ac[1:3],16),int(ac[3:5],16),int(ac[5:7],16)
            if is_3d and tc and tc in ds[sv].dims:
                gm=[float(ds[sv].isel({tc:i}).mean().values) for i in range(nt)]
                card_open("// Global Mean","Full record")
                fan=go.Figure(go.Scatter(x=list(range(nt)),y=gm,mode="lines",line=dict(color=ac,width=2.2),fill="tozeroy",fillcolor=f"rgba({r_},{g_},{b_},0.06)"))
                fan.add_vline(x=info["tidx"],line_dash="dash",line_color="rgba(255,255,255,0.18)")
                step=max(1,nt//10)
                fan.update_layout(**L,height=115,title=dict(text=f"MEAN {sl2[:20]}",font=dict(color="rgba(0,220,255,0.5)",family="Orbitron",size=8),x=0))
                fan.update_xaxes(tickvals=list(range(0,nt,step)),ticktext=tlbl[::step] if tlbl else [],tickfont=dict(size=7))
                st.plotly_chart(fan,width='stretch'); card_close()
                st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
            card_open("// Flat Map")
            st.plotly_chart(make_flat(sda,lats,lons,"",scs,h=135),width='stretch')
            card_close()

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""<div class="footer">
  PyClimaExplorer &nbsp;·&nbsp; Earth Observation System &nbsp;·&nbsp;
  Cosmos_Sync &nbsp;·&nbsp; GLA University Mathura &nbsp;·&nbsp;
  Technex '26 — Hack It Out &nbsp;·&nbsp; IIT (BHU) Varanasi
</div>""",unsafe_allow_html=True)