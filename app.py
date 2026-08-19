from flask import Flask, render_template_string, request, redirect, url_for
import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# ============================================
# ПОДКЛЮЧЕНИЕ К БД (через DATABASE_URL)
# ============================================
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://devops:devops123@localhost:5432/projects')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                tech VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Таблица projects готова")
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")

# Инициализируем БД при старте
init_db()

# Информация о версии
COMMIT_HASH = "v1.0.0"
DEPLOY_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============================================
# ГЛАВНАЯ СТРАНИЦА
# ============================================
HTML_INDEX = '''
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

        /* ===== НАВИГАЦИЯ ===== */
        .nav-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 12px;
        }

        .nav-links a {
            color: rgba(255,255,255,0.3);
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: rgba(255,255,255,0.8);
        }

        .nav-links a.active {
            color: #a855f7;
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

        <!-- НАВИГАЦИЯ -->
        <div class="nav-links">
            <a href="/" class="active">🏠 Главная</a>
            <a href="/about">📖 Обо мне</a>
            <a href="/projects">📁 Проекты</a>
        </div>

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
            <a href="/about" class="btn btn-secondary">📖 Обо мне</a>
            <a href="/projects" class="btn btn-secondary">📁 Проекты</a>
        </div>

        <div class="status">
            <span class="status-dot"></span>
            Status: On the way 🚀
        </div>

        <!-- ===== ИНДИКАТОР ДЕПЛОЯ ===== -->
        <div class="deploy-info">
            <span class="version">{{ commit }}</span> · 
            <span class="time">deployed at {{ time }}</span>
        </div>
    </div>
</body>
</html>
'''

# ============================================
# СТРАНИЦА /ABOUT
# ============================================
HTML_ABOUT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About — IDU B IT</title>
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
            font-size: 48px;
            margin-bottom: 10px;
            display: inline-block;
            animation: pulse 3s infinite ease-in-out;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        h1 {
            font-size: 38px;
            font-weight: 800;
            background: linear-gradient(135deg, #a855f7 0%, #3b82f6 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }

        .subtitle {
            color: rgba(255, 255, 255, 0.3);
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        .divider {
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.4), transparent);
            margin: 12px auto 20px;
        }

        .nav-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .nav-links a {
            color: rgba(255,255,255,0.3);
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: rgba(255,255,255,0.8);
        }

        .nav-links a.active {
            color: #a855f7;
        }

        .about-text {
            color: rgba(255,255,255,0.6);
            font-size: 16px;
            line-height: 1.8;
            text-align: left;
            margin: 12px 0 20px;
        }

        .about-text strong {
            color: rgba(255,255,255,0.85);
        }

        .about-text .highlight {
            color: #a855f7;
            font-weight: 600;
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

        .deploy-info {
            margin-top: 20px;
            font-size: 11px;
            color: rgba(255,255,255,0.12);
            letter-spacing: 0.3px;
            border-top: 1px solid rgba(255,255,255,0.04);
            padding-top: 16px;
        }

        .deploy-info .version {
            color: rgba(255,255,255,0.2);
            font-weight: 600;
        }

        .deploy-info .time {
            color: rgba(255,255,255,0.1);
        }

        @media (max-width: 600px) {
            .card { padding: 32px 20px; border-radius: 24px; }
            h1 { font-size: 28px; }
            .logo { font-size: 36px; }
            .about-text { font-size: 14px; }
            .stars-left, .waves-right { display: none; }
            .deploy-info { font-size: 9px; }
        }
    </style>
</head>
<body>
    <div class="background"></div>
    <div class="orb-1"></div>
    <div class="orb-2"></div>
    <div class="orb-3"></div>

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

    <div class="waves-right">
        <div class="wave-line"></div>
        <div class="wave-line"></div>
        <div class="wave-line"></div>
        <div class="wave-line"></div>
    </div>

    <div class="card">
        <div class="logo">👨‍💻</div>
        <h1>About Me</h1>
        <div class="subtitle">From AnyKey to DevOps</div>
        <div class="divider"></div>

        <div class="nav-links">
            <a href="/">🏠 Главная</a>
            <a href="/about" class="active">📖 Обо мне</a>
            <a href="/projects">📁 Проекты</a>
        </div>

        <div class="about-text">
            <p><strong>Привет! Я Daniel (degex26).</strong></p>
            <br>
            <p>Я начинал как <span class="highlight">системный администратор (AnyKey)</span> — чинил серверы, настраивал сети, работал с железом.</p>
            <br>
            <p>Сейчас я активно учусь и двигаюсь в сторону <span class="highlight">DevOps</span>. Этот проект — мой первый шаг в мире контейнеризации, CI/CD и автоматизации.</p>
            <br>
            <p><strong>Мой стек:</strong><br>
            🐍 Python · 🌶️ Flask · 🐳 Docker · 🐧 Ubuntu · 🔷 Git · ☁️ VMware</p>
            <br>
            <p><strong>Цель:</strong> Стать инженером, который умеет не только настраивать инфраструктуру, но и писать код для её автоматизации.</p>
        </div>

        <div class="divider"></div>

        <a href="/" class="btn btn-secondary">🏠 Вернуться на главную</a>

        <div class="deploy-info">
            <span class="version">{{ commit }}</span> · 
            <span class="time">deployed at {{ time }}</span>
        </div>
    </div>
</body>
</html>
'''

# ============================================
# СТРАНИЦА /PROJECTS
# ============================================
HTML_PROJECTS = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projects — IDU B IT</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
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
        .orb-1 { width: 400px; height: 400px; background: #6c00ff; top: -100px; left: -100px; }
        .orb-2 { width: 300px; height: 300px; background: #00ccff; bottom: -80px; right: -80px; animation-delay: -4s; }
        .orb-3 { width: 200px; height: 200px; background: #ff00aa; top: 50%; left: 50%; transform: translate(-50%, -50%); animation-delay: -8s; }
        @keyframes float {
            0% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(50px, -30px) scale(1.1); }
            66% { transform: translate(-30px, 40px) scale(0.9); }
            100% { transform: translate(0, 0) scale(1); }
        }

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
        .card:hover { transform: translateY(-4px); }

        .logo { font-size: 48px; margin-bottom: 10px; display: inline-block; animation: pulse 3s infinite ease-in-out; }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        h1 {
            font-size: 38px;
            font-weight: 800;
            background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }

        .subtitle {
            color: rgba(255, 255, 255, 0.3);
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        .divider {
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.4), transparent);
            margin: 12px auto 20px;
        }

        .nav-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .nav-links a {
            color: rgba(255,255,255,0.3);
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: rgba(255,255,255,0.8);
        }

        .nav-links a.active {
            color: #10b981;
        }

        .project-form {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }

        .project-form input,
        .project-form textarea {
            padding: 12px;
            border-radius: 12px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            color: rgba(255,255,255,0.8);
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.3s ease;
        }

        .project-form input:focus,
        .project-form textarea:focus {
            outline: none;
            border-color: rgba(16, 185, 129, 0.4);
        }

        .project-form textarea {
            resize: vertical;
            min-height: 60px;
        }

        .project-form .btn-submit {
            padding: 10px;
            border-radius: 12px;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .project-form .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(16, 185, 129, 0.3);
        }

        .project-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin: 20px 0;
            text-align: left;
        }

        .project-item {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 12px;
            padding: 16px 20px;
            transition: all 0.3s ease;
        }

        .project-item:hover {
            background: rgba(255,255,255,0.04);
            border-color: rgba(16, 185, 129, 0.2);
        }

        .project-item .name {
            font-size: 16px;
            font-weight: 600;
            color: rgba(255,255,255,0.85);
        }

        .project-item .description {
            font-size: 14px;
            color: rgba(255,255,255,0.5);
            margin-top: 4px;
        }

        .project-item .tech {
            font-size: 12px;
            color: rgba(16, 185, 129, 0.5);
            margin-top: 6px;
            display: inline-block;
            background: rgba(16, 185, 129, 0.06);
            padding: 2px 12px;
            border-radius: 50px;
        }

        .project-item .delete-btn {
            float: right;
            background: none;
            border: none;
            color: rgba(255,255,255,0.15);
            font-size: 16px;
            cursor: pointer;
            transition: color 0.3s ease;
        }

        .project-item .delete-btn:hover {
            color: #ef4444;
        }

        .empty-msg {
            color: rgba(255,255,255,0.2);
            font-size: 14px;
            text-align: center;
            padding: 20px 0;
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

        .deploy-info {
            margin-top: 20px;
            font-size: 11px;
            color: rgba(255,255,255,0.12);
            letter-spacing: 0.3px;
            border-top: 1px solid rgba(255,255,255,0.04);
            padding-top: 16px;
        }

        .deploy-info .version {
            color: rgba(255,255,255,0.2);
            font-weight: 600;
        }

        .deploy-info .time {
            color: rgba(255,255,255,0.1);
        }

        .flash {
            padding: 10px 16px;
            border-radius: 10px;
            margin-bottom: 16px;
            font-size: 14px;
        }
        .flash-success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: rgba(16, 185, 129, 0.8);
        }
        .flash-error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: rgba(239, 68, 68, 0.8);
        }

        @media (max-width: 600px) {
            .card { padding: 32px 20px; border-radius: 24px; }
            h1 { font-size: 28px; }
            .logo { font-size: 36px; }
            .stars-left, .waves-right { display: none; }
            .deploy-info { font-size: 9px; }
            .project-item {
                padding: 12px 16px;
            }
        }
    </style>
</head>
<body>
    <div class="background"></div>
    <div class="orb-1"></div>
    <div class="orb-2"></div>
    <div class="orb-3"></div>

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

    <div class="waves-right">
        <div class="wave-line"></div>
        <div class="wave-line"></div>
        <div class="wave-line"></div>
        <div class="wave-line"></div>
    </div>

    <div class="card">
        <div class="logo">📁</div>
        <h1>Мои проекты</h1>
        <div class="subtitle">Добавляй и отслеживай свои проекты</div>
        <div class="divider"></div>

        <div class="nav-links">
            <a href="/">🏠 Главная</a>
            <a href="/about">📖 Обо мне</a>
            <a href="/projects" class="active">📁 Проекты</a>
        </div>

        {% if message %}
        <div class="flash flash-{{ message_type }}">{{ message }}</div>
        {% endif %}

        <form method="POST" class="project-form">
            <input type="text" name="name" placeholder="Название проекта" required>
            <input type="text" name="tech" placeholder="Технологии (Python, Docker, etc.)">
            <textarea name="description" placeholder="Описание проекта"></textarea>
            <button type="submit" class="btn-submit">➕ Добавить проект</button>
        </form>

        <div class="divider"></div>

        <div class="project-list">
            {% if projects %}
                {% for p in projects %}
                <div class="project-item">
                    <span class="name">{{ p.name }}</span>
                    <a href="{{ url_for('delete_project', project_id=p.id) }}" 
                       class="delete-btn" 
                       onclick="return confirm('Удалить проект?')">✕</a>
                    <div class="description">{{ p.description }}</div>
                    {% if p.tech %}
                    <span class="tech">{{ p.tech }}</span>
                    {% endif %}
                </div>
                {% endfor %}
            {% else %}
                <div class="empty-msg">📭 Пока нет проектов. Добавь первый!</div>
            {% endif %}
        </div>

        <div class="divider"></div>

        <a href="/" class="btn btn-secondary">🏠 Вернуться на главную</a>

        <div class="deploy-info">
            <span class="version">{{ commit }}</span> · 
            <span class="time">deployed at {{ time }}</span>
        </div>
    </div>
</body>
</html>
'''

# ============================================
# РОУТЫ
# ============================================
@app.route('/')
def home():
    return render_template_string(
        HTML_INDEX,
        commit=COMMIT_HASH,
        time=DEPLOY_TIME
    )

@app.route('/about')
def about():
    return render_template_string(
        HTML_ABOUT,
        commit=COMMIT_HASH,
        time=DEPLOY_TIME
    )

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    message = None
    message_type = None

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            tech = request.form.get('tech', '').strip()

            if name:
                cur.execute(
                    "INSERT INTO projects (name, description, tech) VALUES (%s, %s, %s)",
                    (name, description, tech)
                )
                conn.commit()
                message = f"✅ Проект '{name}' добавлен!"
                message_type = "success"
            else:
                message = "❌ Название проекта обязательно"
                message_type = "error"

        # Получаем список проектов
        cur.execute("SELECT id, name, description, tech FROM projects ORDER BY created_at DESC")
        projects_list = cur.fetchall()

        cur.close()
        conn.close()

        return render_template_string(
            HTML_PROJECTS,
            projects=projects_list,
            commit=COMMIT_HASH,
            time=DEPLOY_TIME,
            message=message,
            message_type=message_type
        )

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return render_template_string(
            HTML_PROJECTS,
            projects=[],
            commit=COMMIT_HASH,
            time=DEPLOY_TIME,
            message=f"❌ Ошибка подключения к БД: {e}",
            message_type="error"
        )

@app.route('/delete/<int:project_id>')
def delete_project(project_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка удаления: {e}")
    return redirect(url_for('projects'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)