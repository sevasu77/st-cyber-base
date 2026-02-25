import streamlit as st

# 公開用：サイドバーなし設定
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    header, [data-testid="stSidebar"] { display: none !important; }
    .main .block-container { padding: 0 !important; margin: 0 !important; }
    [data-testid="stAppViewContainer"] { background-color: #020802; }
    </style>
    """, unsafe_allow_html=True)

# 音声ロジックを完全に排除したミニマル版
minimal_engine_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #020802; color: #00ffcc; font-family: monospace; }
        canvas { display: block; position: absolute; top: 0; left: 0; z-index: 1; }
        
        .furniture {
            position: absolute; width: 80px; height: 80px;
            background: rgba(0, 255, 204, 0.1);
            border: 1px solid #00ffcc;
            display: flex; align-items: center; justify-content: center;
            cursor: grab; z-index: 100; user-select: none;
            font-size: 10px;
        }
        .furniture.placed { background: rgba(0, 255, 204, 0.4); }
    </style>
</head>
<body>
    <div style="position:fixed; top:20px; left:20px; z-index:1000; pointer-events:none;">
        <h3>ST-CYBER-BASE-CORE</h3>
    </div>
    
    <canvas id="bgCanvas"></canvas>
    
    <div id="item1" class="furniture" onmousedown="dragStart(event, this)">UNIT-01</div>
    <div id="item2" class="furniture" onmousedown="dragStart(event, this)">UNIT-02</div>

<script>
    const canvas = document.getElementById("bgCanvas");
    const ctx = canvas.getContext("2d");
    let cw = canvas.width = window.innerWidth;
    let ch = canvas.height = window.innerHeight;

    const sockets = [
        { x: cw/2 - 120, y: ch/2 },
        { x: cw/2, y: ch/2 },
        { x: cw/2 + 120, y: ch/2 }
    ];

    let activeDrag = null;
    let offX, offY;

    function dragStart(e, el) {
        activeDrag = el;
        const rect = el.getBoundingClientRect();
        offX = e.clientX - rect.left;
        offY = e.clientY - rect.top;
        el.classList.remove("placed");
    }

    window.onmousemove = (e) => {
        if(!activeDrag) return;
        activeDrag.style.left = (e.clientX - offX) + "px";
        activeDrag.style.top = (e.clientY - offY) + "px";
    };

    window.onmouseup = (e) => {
        if(!activeDrag) return;
        sockets.forEach(s => {
            const dx = e.clientX - s.x;
            const dy = e.clientY - s.y;
            if(Math.sqrt(dx*dx + dy*dy) < 50) {
                activeDrag.style.left = (s.x - 40) + "px";
                activeDrag.style.top = (s.y - 40) + "px";
                activeDrag.classList.add("placed");
            }
        });
        activeDrag = null;
    };

    function draw() {
        ctx.fillStyle = "#020802";
        ctx.fillRect(0,0,cw,ch);
        
        // 背景のグリッド描画
        ctx.strokeStyle = "#0a2215";
        ctx.lineWidth = 1;
        for(let i=0; i<cw; i+=50) { ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,ch); ctx.stroke(); }
        for(let j=0; j<ch; j+=50) { ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(cw,j); ctx.stroke(); }

        // ソケットの描画
        sockets.forEach(s => {
            ctx.strokeStyle = "#00ffcc";
            ctx.strokeRect(s.x - 40, s.y - 40, 80, 80);
        });
        requestAnimationFrame(draw);
    }

    // 初期配置
    document.getElementById("item1").style.left = "40px"; document.getElementById("item1").style.top = "100px";
    document.getElementById("item2").style.left = "40px"; document.getElementById("item2").style.top = "200px";

    draw();
</script>
</body>
</html>
"""

st.components.v1.html(minimal_engine_html, height=800)
