from flask import Flask, render_template_string
import datetime
import os

app = Flask(__name__)

# Получаем информацию о деплое
DEPLOY_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
COMMIT_HASH = os.popen('git rev-parse --short HEAD').read().strip() or "unknown"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IDU B IT — From AnyKey to DevOps</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0a0f;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 30% 30%, #1a1a2e, #0a0a0f);
            z-index: -2;
        }

        .orb-1, .orb-2, .orb-3 {
            position: fixed;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.3;
            z-index: -1;
            animation: float 12s infinite ease-in-out;
        }
        .orb-1 {
            width: 400px;
            height: 400px;
            background: #6c00ff;
            top: -100px;
            left: -100px;
        }
        .orb-2 {
            width: 300px;
            height: 300px;
            background: #00ccff;
            bottom: -80px;
            right: -80px;
            animation-delay: -4s;
        }
        .orb-3 {
            width: 200px;
            height: 200px;
            background: #ff00aa;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: -8s;
        }

        @keyframes float {
            0% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(50px, -30px) scale(1.1); }
            66% { transform: translate(-30px, 40px) scale(0.9); }
            100% { transform: translate(0, 0) scale(1); }
        }

        /* ===== АНИМАЦИИ ПО БОКАМ ===== */

        .stars-left {
            position: fixed;
            left: 20px;
            top: 0;
            width: 60px;
            height: 100%;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }
        .star {
            position: absolute;
            width: 3px;
            height: 3px;
            background: white;
            border-radius: 50%;
            animation: falling 5s infinite linear;
            box-shadow: 0 0 6px rgba(255,255,255,0.6);
        }
        .star:nth-child(1) { left: 10%; animation-delay: 0s; }
        .star:nth-child(2) { left: 30%; animation-delay: 1.2s; }
        .star:nth-child(3) { left: 50%; animation-delay: 2.5s; }
        .star:nth-child(4) { left: 70%; animation-delay: 0.7s; }
        .star:nth-child(5) { left: 90%; animation-delay: 3.3s; }
        .star:nth-child(6) { left: 20%; animation-delay: 4.1s; }
        .star:nth-child(7) { left: 60%; animation-delay: 1.8s; }
        .star:nth-child(8) { left: 80%; animation-delay: 0.3s; }

        @keyframes falling {
            0% { top: -10%; opacity: 0; transform: scale(0.5); }
            10% { opacity: 1; transform: scale(1); }
            80% { opacity: 1; transform: scale(1); }
            100% { top: 110%; opacity: 0; transform: scale(0.8); }
        }

        .waves-right {
            position: fixed;
            right: 10px;
            top: 0;
            width: 80px;
            height: 100%;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }
        .wave-line {
            position: absolute;
            width: 2px;
            height: 100%;
            background: linear-gradient(to bottom, transparent, rgba(168,85,247,0.15), transparent);
            animation: waveMove 8s infinite ease-in-out;
        }
        .wave-line:nth-child(1) { left: 15%; animation-delay: 0s; }
        .wave-line:nth-child(2) { left: 35%; animation-delay: 2s; }
        .wave-line:nth-child(3) { left: 55%; animation-delay: 4s; }
        .wave-line:nth-child(4) { left: 75%; animation-delay: 6s; }

        @keyframes waveMove {
            0% { transform: translateY(-100%) scaleY(0.5); opacity: 0; }
            30% { opacity: 1; }
            70% { opacity: 1; }
            100% { transform: translateY(100%) scaleY(0.5); opacity: 0; }
        }

        .cube-container {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 80px;
            height: 80px;
            z-index: 0;
            pointer-events: none;
            perspective: 300px;
        }
        .cube {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            animation: spin 10s infinite linear;
        }
        .cube-face {
            position: absolute;
            width: 80px;
            height: 80px;
            background: rgba(168,85,247,0.08);
            border: 1px solid rgba(168,85,247,0.15);
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(168,85,247,0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        .cube-face.front  { transform: translateZ(40px); }
        .cube-face.back   { transform: rotateY(180deg) translateZ(40px); }
        .cube-face.right  { transform: rotateY(90deg) translateZ(40px); }
        .cube-face.left   { transform: rotateY(-90deg) translateZ(40px); }
        .cube-face.top    { transform: rotateX(90deg) translateZ(40px); }
        .cube-face.bottom { transform: rotateX(-90deg) translateZ(40px); }

        @keyframes spin {
            0% { transform: rotateX(0deg) rotateY(0deg); }
            100% { transform: rotateX(360deg) rotateY(360deg); }
        }

        .pulse-ring {
            position: fixed;
            bottom: 30px;
            left: 30px;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: 1px solid rgba(0,200,255,0.1);
            z-index: 0;
            pointer-events: none;
            animation: ringPulse 4s infinite ease-in-out;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: rgba(0,200,255,0.15);
            font-weight: 700;
            letter-spacing: 2px;
        }
        .pulse-ring::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 1px solid rgba(0,200,255,0.05);
            animation: ringPulse 4s infinite ease-in-out 0.5s;
        }
        @keyframes ringPulse {
            0% { transform: scale(1); opacity: 0.3; }
            50% { transform: scale(1.3); opacity: 0.05; }
            100% { transform: scale(1); opacity: 0.3; }
        }

        /* ===== ЦЕНТРАЛЬНАЯ КАРТОЧКА ===== */

        .card {
            background: rgba(20, 20, 35, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 32px;
            padding: 60px 50px;
            max-width: 700px;
            width: 90%;
            text-align: center;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.04);
            transition: transform 0.3s ease;
            z-index: 1;
        }
        .card:hover {
            transform: translateY(-4px);
        }

        .logo {
            font-size: 64px;
            margin-bottom: 10px;
            display: inline-block;
            animation: pulse 3s infinite ease-in-out;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        h1 {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #a855f7 0%, #3b82f6 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
        }

        .subtitle {
            color: rgba(255, 255, 255, 0.4);
            font-size: 18px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .divider {
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.4), transparent);
            margin: 16px auto 20px;
        }

        /* ===== ИНТЕРАКТИВНЫЙ ПУТЬ ===== */

        .path-section {
            margin: 12px 0 16px;
            padding: 20px 12px 12px;
            background: rgba(255,255,255,0.02);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.04);
        }

        .path-track {
            display: flex;
            align-items: center;
            gap: 0;
            width: 100%;
            justify-content: center;
            padding-top: 4px;
        }

        .path-point {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            flex-shrink: 0;
            z-index: 2;
        }

        .path-point .point-icon {
            font-size: 28px;
            width: 50px;
            height: 50px;
            background: rgba(255,255,255,0.03);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
        }

        .path-point .point-label {
            font-size: 12px;
            color: rgba(255,255,255,0.25);
            font-weight: 500;
            letter-spacing: 0.5px;
            text-align: center;
            white-space: nowrap;
        }

        .path-point.start .point-icon {
            border-color: rgba(168,85,247,0.2);
            background: rgba(168,85,247,0.05);
        }
        .path-point.start .point-label {
            color: rgba(168,85,247,0.4);
        }

        .path-point.end .point-icon {
            border-color: rgba(0,200,255,0.2);
            background: rgba(0,200,255,0.05);
            animation: glowPulse 2s infinite ease-in-out;
        }
        .path-point.end .point-label {
            color: rgba(0,200,255,0.5);
        }

        @keyframes glowPulse {
            0%, 100% { box-shadow: 0 0 20px rgba(0,200,255,0.05); }
            50% { box-shadow: 0 0 40px rgba(0,200,255,0.15); }
        }

        .path-line {
            flex: 1;
            height: 3px;
            background: rgba(255,255,255,0.06);
            border-radius: 4px;
            position: relative;
            margin: 0 4px;
            min-width: 40px;
            max-width: 120px;
        }

        .path-progress {
            height: 100%;
            background: linear-gradient(90deg, #7c3aed, #06b6d4);
            border-radius: 4px;
            position: relative;
            transition: width 1.5s ease;
        }

        /* ===== РАКЕТА ===== */
        .path-walker {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 32px;
            animation: rocketFly 1.2s infinite ease-in-out;
            filter: drop-shadow(0 0 30px rgba(255, 100, 0, 0.3));
        }

        @keyframes rocketFly {
            0%, 100% { 
                transform: translate(-50%, -50%) scale(1) rotate(-4deg); 
            }
            50% { 
                transform: translate(-50%, -75%) scale(1.1) rotate(4deg); 
            }
        }

        /* ===== ИНДИКАТОР ДЕПЛОЯ ===== */
        .deploy-info {
            margin-top: 16px;
            font-size: 11px;
            color: rgba(255,255,255,0.15);
            letter-spacing: 0.3px;
            border-top: 1px solid rgba(255,255,255,0.04);
            padding-top: 16px;
        }

        .deploy-info .version {
            color: rgba(255,255,255,0.25);
            font-weight: 600;
        }

        .deploy-info .time {
            color: rgba(255,255,255,0.15);
        }

        /* ===== КНОПКИ ===== */

        .buttons {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
            margin-top: 4px;
        }
        .btn {
            padding: 12px 32px;
            border-radius: 50px;
            font-size: 15px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: none;
            cursor: pointer;
        }
        .btn-primary {
            background: linear-gradient(135deg, #7c3aed, #6d28d9);
            color: white;
            box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3);
        }
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(124, 58, 237, 0.4);
        }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.04);
            color: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.08);
            color: white;
            transform: translateY(-3px);
        }

        .status {
            margin-top: 24px;
            color: rgba(255, 255, 255, 0.12);
            font-size: 12px;
            letter-spacing: 1px;
        }
        .status-dot {
            display: inline-block;
            width: 6px;
            height: 6px;
            background: #22c55e;
            border-radius: 50%;
            margin-right: 8px;
            animation: blink 2s infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        /* ===== АДАПТИВ ===== */

        @media (max-width: 600px) {
            .card { padding: 32px 20px; border-radius: 24px; }
            h1 { font-size: 28px; }
            .logo { font-size: 44px; }
            .subtitle { font-size: 14px; }
            .btn { padding: 10px 20px; font-size: 13px; }
            .stars-left, .waves-right { display: none; }
            .cube-container { width: 44px; height: 44px; bottom: 12px; right: 12px; }
            .cube-face { width: 44px; height: 44px; font-size: 14px; }
            .pulse-ring { width: 50px; height: 50px; font-size: 14px; bottom: 12px; left: 12px; }
            .cube-face.front  { transform: translateZ(22px); }
            .cube-face.back   { transform: rotateY(180deg) translateZ(22px); }
            .cube-face.right  { transform: rotateY(90deg) translateZ(22px); }
            .cube-face.left   { transform: rotateY(-90deg) translateZ(22px); }
            .cube-face.top    { transform: rotateX(90deg) translateZ(22px); }
            .cube-face.bottom { transform: rotateX(-90deg) translateZ(22px); }
            .path-point .point-icon {
                font-size: 20px;
                width: 38px;
                height: 38px;
            }
            .path-point .point-label {
                font-size: 10px;
            }
            .path-line {
                min-width: 20px;
                max-width: 60px;
            }
            .path-walker {
                font-size: 24px;
            }
            .path-section {
                padding: 12px 6px 8px;
                margin: 8px 0 12px;
            }
            .divider {
                margin: 12px auto 16px;
            }
            .deploy-info {
                font-size: 9px;
            }
        }
    </style>
</head>
<body>
    <div class="background"></div>
    <div class="orb-1"></div>
    <div class="orb-2"></div>
    <div class="orb-3"></div>

    <!-- ЛЕВАЯ АНИМАЦИЯ: падающие звёзды -->
    <div class="stars-left">
        <div class="star"></div>
        <div class="star"></div>
        <div class="star"></div>
        <div class="star"></div>
        <div class="star"></div>
        <div class="star"></div>
        <div class="star"></div>
        <div class="star"></div>
    </div>

    <!-- ПРАВАЯ АНИМАЦИЯ: волны -->
    <div class="waves-right">
        <div class="wave-line"></div>
        <div class="wave-line"></div>
        <div class="wave-line"></div>
        <div class="wave-line"></div>
    </div>

    <!-- ПРАВЫЙ НИЗ: вращающийся куб -->
    <div class="cube-container">
        <div class="cube">
            <div class="cube-face front">🐍</div>
            <div class="cube-face back">🐳</div>
            <div class="cube-face right">☁️</div>
            <div class="cube-face left">🐧</div>
            <div class="cube-face top">🔷</div>
            <div class="cube-face bottom">🌶️</div>
        </div>
    </div>

    <!-- ЛЕВЫЙ НИЗ: пульсирующее кольцо -->
    <div class="pulse-ring">⚡</div>

    <!-- ЦЕНТРАЛЬНАЯ КАРТОЧКА -->
    <div class="card">
        <div class="logo">🚀</div>
        <h1>IDU B IT</h1>
        <div class="subtitle">From AnyKey to DevOps</div>
        <div class="divider"></div>

        <!-- ИНТЕРАКТИВНЫЙ ПУТЬ -->
        <div class="path-section">
            <div class="path-track">
                <div class="path-point start">
                    <span class="point-icon">🖥️</span>
                    <span class="point-label">AnyKey</span>
                </div>
                <div class="path-line">
                    <div class="path-progress" style="width: 50%;"></div>
                    <div class="path-walker">🚀</div>
                </div>
                <div class="path-point end">
                    <span class="point-icon">☁️</span>
                    <span class="point-label">DevOps</span>
                </div>
            </div>
        </div>

        <div class="divider"></div>

        <div class="buttons">
            <a href="https://github.com/degex26?tab=repositories" target="_blank" class="btn btn-primary">🚀 My Project</a>
            <a href="#" class="btn btn-secondary">📬 Contact</a>
        </div>

        <div class="status">
            <span class="status-dot"></span>
            Status: On the way 🚀
        </div>

        <!-- ===== ИНДИКАТОР ДЕПЛОЯ ===== -->
        <div class="deploy-info">
            <span class="version">v{{ commit }}</span> · 
            <span class="time">deployed at {{ time }}</span>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(
        HTML_TEMPLATE,
        commit=COMMIT_HASH,
        time=DEPLOY_TIME
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)