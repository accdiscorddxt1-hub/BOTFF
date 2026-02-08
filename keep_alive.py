from flask import Flask, render_template_string
from threading import Thread
import datetime

app = Flask(__name__)

# Biến toàn cục
start_time = datetime.datetime.now()

def calculate_uptime():
    """Tính thời gian đã chạy"""
    now = datetime.datetime.now()
    delta = now - start_time
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    if days > 0:
        return f"{days} ngày {hours} giờ"
    elif hours > 0:
        return f"{hours} giờ {minutes} phút"
    else:
        return f"{minutes} phút"

# HTML Template giới thiệu bản thân
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>👨‍💻 Giới Thiệu - XUANTHANG</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 50px;
            max-width: 1000px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
        }

        .avatar {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            margin: 0 auto 20px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        }

        .name {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .title {
            font-size: 1.4rem;
            color: #aaa;
            margin-bottom: 25px;
        }

        .status-badge {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 12px 30px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            box-shadow: 0 5px 20px rgba(76, 175, 80, 0.4);
        }

        .content {
            margin: 40px 0;
        }

        .section {
            margin-bottom: 35px;
        }

        .section-title {
            font-size: 1.8rem;
            color: #4ecdc4;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-content {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #ff6b6b;
        }

        .skill-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }

        .skill-item {
            background: rgba(255, 255, 255, 0.08);
            padding: 12px 20px;
            border-radius: 10px;
            text-align: center;
            transition: all 0.3s;
        }

        .skill-item:hover {
            background: rgba(78, 205, 196, 0.2);
            transform: translateY(-3px);
        }

        .contact-list {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
        }

        .contact-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px 25px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            transition: all 0.3s;
            text-decoration: none;
            color: white;
        }

        .contact-item:hover {
            background: rgba(255, 107, 107, 0.2);
            transform: translateY(-3px);
        }

        .icon {
            font-size: 1.5rem;
            color: #4ecdc4;
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #888;
            font-size: 0.9rem;
        }

        .uptime {
            font-size: 1.1rem;
            color: #ff6b6b;
            font-weight: 600;
            margin-top: 10px;
        }

        @media (max-width: 768px) {
            .container {
                padding: 30px 20px;
            }
            .name {
                font-size: 2.2rem;
            }
            .avatar {
                width: 140px;
                height: 140px;
                font-size: 3rem;
            }
        }

        .glow {
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #4ecdc4; }
            to { text-shadow: 0 0 15px #fff, 0 0 25px #4ecdc4, 0 0 35px #ff6b6b; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header với avatar và tên -->
        <div class="header">
            <div class="avatar">
                <i class="fas fa-user-secret"></i>
            </div>
            <h1 class="name glow">XTHANG</h1>
            <p class="title">🎯 Discord Bot Developer & Automation Specialist</p>
            <div class="status-badge">
                <i class="fas fa-circle" style="color: #4CAF50;"></i> 
                BOT ĐANG HOẠT ĐỘNG
            </div>
            <div class="uptime">
                <i class="fas fa-clock"></i> Đã chạy: {{ uptime }}
            </div>
        </div>

        <!-- Nội dung chính -->
        <div class="content">
            <!-- Giới thiệu -->
            <div class="section">
                <h2 class="section-title"><i class="fas fa-user"></i> GIỚI THIỆU</h2>
                <div class="section-content">
                    <p>Xin chào! Tôi là <strong>XTHANG</strong>, một lập trình viên đam mê phát triển các công cụ tự động hóa và bot Discord.</p>
                    <p>Với kinh nghiệm trong việc tạo các hệ thống tự động hóa cho Messenger và Discord, tôi luôn tìm kiếm những giải pháp sáng tạo để giải quyết vấn đề.</p>
                    <p>Đam mê của tôi là tạo ra những công cụ hữu ích, tiết kiệm thời gian và nâng cao hiệu quả công việc.</p>
                </div>
            </div>

            <!-- Kỹ năng -->
            <div class="section">
                <h2 class="section-title"><i class="fas fa-code"></i> KỸ NĂNG</h2>
                <div class="section-content">
                    <p>Chuyên môn của tôi bao gồm:</p>
                    <div class="skill-list">
                        <div class="skill-item">Python</div>
                        <div class="skill-item">Discord Bot</div>
                        <div class="skill-item">Automation</div>
                        <div class="skill-item">Web Scraping</div>
                        <div class="skill-item">API Integration</div>
                        <div class="skill-item">Database</div>
                        <div class="skill-item">Flask</div>
                        <div class="skill-item">JavaScript</div>
                    </div>
                </div>
            </div>

            <!-- Dự án -->
            <div class="section">
                <h2 class="section-title"><i class="fas fa-project-diagram"></i> DỰ ÁN NỔI BẬT</h2>
                <div class="section-content">
                    <p><strong>🤖 XTHANG BOT</strong></p>
                    <p>• Bot Discord đa năng với tính năng tự động hóa Messenger</p>
                    <p>• Hệ thống treo tin nhắn, reo tag tự động</p>
                    <p>• Quản lý admin với phân quyền chi tiết</p>
                    <p>• Chạy 24/7 với Flask server</p>

                    <p style="margin-top: 15px;"><strong>🌐 Các dự án khác</strong></p>
                    <p>• Automation tools cho Facebook/Messenger</p>
                    <p>• Web dashboard quản lý bot</p>
                    <p>• API services cho cộng đồng</p>
                </div>
            </div>

            <!-- Liên hệ -->
            <div class="section">
                <h2 class="section-title"><i class="fas fa-envelope"></i> LIÊN HỆ</h2>
                <div class="section-content">
                    <p>Hãy kết nối với tôi qua:</p>
                    <div class="contact-list">
                        <a href="https://discord.gg/" class="contact-item" target="_blank">
                            <i class="fab fa-discord icon"></i>
                            <span>Discord Server</span>
                        </a>
                        <a href="https://github.com/" class="contact-item" target="_blank">
                            <i class="fab fa-github icon"></i>
                            <span>GitHub</span>
                        </a>
                        <a href="https://facebook.com/" class="contact-item" target="_blank">
                            <i class="fab fa-facebook icon"></i>
                            <span>Facebook</span>
                        </a>
                        <a href="mailto:contact@example.com" class="contact-item">
                            <i class="fas fa-envelope icon"></i>
                            <span>Email</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>© 2024 XTHANG. Tất cả các quyền được bảo lưu.</p>
            <p>📍 "Không có gì là không thể với đam mê và sự kiên trì"</p>
            <div class="uptime">
                <i class="fas fa-server"></i> Server Uptime: {{ uptime }}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Trang chủ giới thiệu bản thân"""
    uptime = calculate_uptime()
    return render_template_string(HTML_TEMPLATE, uptime=uptime)

@app.route('/health')
def health():
    """API kiểm tra sức khỏe"""
    return {
        "status": "healthy",
        "service": "XTHANG Bot",
        "uptime": calculate_uptime(),
        "timestamp": datetime.datetime.now().isoformat()
    }

def run():
    """Chạy Flask server"""
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Khởi động server trong thread riêng"""
    print("🚀 Khởi động web server...")
    print("🌐 Truy cập: http://localhost:8080")
    print("📊 Health check: http://localhost:8080/health")

    t = Thread(target=run)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    keep_alive()
    print("✅ Web server đã khởi động!")

    # Giữ chương trình chạy
    import time
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n👋 Tắt server...")
