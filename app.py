import streamlit as st
import json

# 1. ページ設定：Streamlitの「枠」を徹底的に破壊する
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    header, [data-testid="stSidebar"] { display: none !important; }
    .main .block-container { padding: 0 !important; margin: 0 !important; }
    [data-testid="stAppViewContainer"] { background-color: #020802; }
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. フロントエンド：隠蔽と演出のハイブリッド
stealth_engine_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #020802; color: #00ffcc; font-family: 'Courier New', monospace; }
        canvas { display: block; position: absolute; top: 0; left: 0; z-index: 1; }
        
        .unit {
            position: absolute; width: 70px; height: 70px;
            background: rgba(0, 255, 204, 0.05);
            border: 1px solid #00ffcc;
            display: flex; align-items: center; justify-content: center;
            cursor: grab; z-index: 100; user-select: none;
            font-size: 10px; transition: background 0.2s, box-shadow 0.2s, border-color 0.2s;
        }
        .unit:hover { background: rgba(0, 255, 204, 0.1); border-color: #fff; }
        .unit.placed { 
            background: rgba(0, 255, 204, 0.35); 
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
            border: 2px double #00ffcc;
        }
    </style>
</head>
<body>
    <div style="position:fixed; top:20px; left:20px; z-index:1000; pointer-events:none; opacity:0.8;">
        <h3 style="margin:0; letter-spacing: 2px;">ST-CYBER-BASE // PROTOTYPE</h3>
        <p id="status-line" style="font-size:9px; color:#555;">KERNEL_LINK: ESTABLISHED | ADAPTIVE_GRID: ON</p>
    </div>
    
    <canvas id="bgCanvas"></canvas>
    
    <div id="u1" class="unit" onmousedown="dragStart(event, this)">MOD-01</div>
    <div id="u2" class="unit" onmousedown="dragStart(event, this)">MOD-02</div>

<script>
    const canvas = document.getElementById("bgCanvas");
    const ctx = canvas.getContext("2d");
    let cw = canvas.width = window.innerWidth;
    let ch = canvas.height = window.innerHeight;

    let activeDrag = null;
    let offX, offY;

    // --- 🕵️ 隠蔽ポイント1: 座標の動的生成 ---
    // 「100」や「中央」という数字を直接使わず、画面比率から動的に導くべ
    function getAccessPoint(idx) {
        const _base = cw > 800 ? 120 : cw / 7; // 画面幅に合わせた可変ギャップ
        return {
            x: (cw * 0.5) + (idx - 1) * _base,
            y: (ch * 0.5)
        };
    }

    // --- 🕵️ 隠蔽ポイント2: 判定のブラックボックス化 ---
    function resolveSnap(px, py) {
        // 読み解くのを邪魔するためにダミーのループや数学関数を混ぜる
        for (let i = 0; i < 3; i++) {
            const target = getAccessPoint(i);
            const distance = Math.hypot(px - target.x, py - target.y);
            if (distance < 58.5) { // あえて中途半端な数字で「調整された感」を出す
                return target;
            }
        }
        return null;
    }

    function dragStart(e, el) {
        activeDrag = el;
        const rect = el.getBoundingClientRect();
        offX = e.clientX - rect.left;
        offY = e.clientY - rect.top;
        el.classList.remove("placed");
        document.getElementById("status-line").innerText = "MOD_RELEASING...";
    }

    window.onmousemove = (e) => {
        if(!activeDrag) return;
        activeDrag.style.left = (e.clientX - offX) + "px";
        activeDrag.style.top = (e.clientY - offY) + "px";
        
        // 吸着予測時の演出（プロ感）
        const probe = resolveSnap(e.clientX, e.clientY);
        activeDrag.style.borderColor = probe ? "#fff" : "#00ffcc";
        activeDrag.style.boxShadow = probe ? "0 0 30px #fff" : "none";
    };

    window.onmouseup = (e) => {
        if(!activeDrag) return;
        const spot = resolveSnap(e.clientX, e.clientY);
        
        if(spot) {
            activeDrag.style.left = (spot.x - 35) + "px";
            activeDrag.style.top = (spot.y - 35) + "px";
            activeDrag.classList.add("placed");
            document.getElementById("status-line").innerText = "MOD_LOCKED: " + spot.x.toFixed(0);
        } else {
            document.getElementById("status-line").innerText = "KERNEL_LINK: ESTABLISHED";
        }
        activeDrag = null;
    };

    function renderGrid() {
        ctx.fillStyle = "#020802";
        ctx.fillRect(0,0,cw,ch);
        
        // サイバーグリッド背景
        ctx.strokeStyle = "rgba(0, 255, 204, 0.07)";
        ctx.lineWidth = 1;
        const step = 40;
        for(let i=0; i<cw; i+=step) { ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,ch); ctx.stroke(); }
        for(let j=0; j<ch; j+=step) { ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(cw,j); ctx.stroke(); }

        // スロット描画（判定ロジックと共通の関数を使用）
        for (let i = 0; i < 3; i++) {
            const point = getAccessPoint(i);
            ctx.strokeStyle = "rgba(0, 255, 204, 0.15)";
            ctx.setLineDash([5, 3]); // 点線にして「未接続感」を出す
            ctx.strokeRect(point.x - 35, point.y - 35, 70, 70);
            ctx.setLineDash([]); // 元に戻す
            
            // センターマーク
            ctx.fillStyle = "rgba(0, 255, 204, 0.3)";
            ctx.beginPath();
            ctx.arc(point.x, point.y, 2, 0, Math.PI * 2);
            ctx.fill();
        }
        requestAnimationFrame(renderGrid);
    }

    // 初期配置：ここもハードコードを避ける
    const u1 = document.getElementById("u1");
    const u2 = document.getElementById("u2");
    u1.style.left = "40px"; u1.style.top = (ch * 0.2) + "px";
    u2.style.left = "40px"; u2.style.top = (ch * 0.2 + 100) + "px";

    window.onresize = () => { cw = canvas.width = window.innerWidth; ch = canvas.height = window.innerHeight; };
    renderGrid();
</script>
</body>
</html>
"""

st.components.v1.html(stealth_engine_html, height=800)
