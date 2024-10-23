# app.py
import psutil
import platform
from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>System Monitor</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .metric {
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        .refresh-btn {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .refresh-btn:hover {
            background-color: #0056b3;
        }
    </style>
    <script>
        function refreshMetrics() {
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('cpu').textContent = `CPU Usage: ${data.cpu_percent}%`;
                    document.getElementById('memory').textContent = `Memory Usage: ${data.memory_percent}%`;
                    document.getElementById('disk').textContent = `Disk Usage: ${data.disk_percent}%`;
                    document.getElementById('updated').textContent = `Last Updated: ${data.timestamp}`;
                });
        }
        // Автоматичне оновлення кожні 5 секунд
        setInterval(refreshMetrics, 5000);
    </script>
</head>
<body>
    <div class="container">
        <h1>System Monitor</h1>
        <div class="metric" id="cpu">CPU Usage: {{ metrics.cpu_percent }}%</div>
        <div class="metric" id="memory">Memory Usage: {{ metrics.memory_percent }}%</div>
        <div class="metric" id="disk">Disk Usage: {{ metrics.disk_percent }}%</div>
        <div class="metric" id="system">System: {{ metrics.system_info }}</div>
        <div class="metric" id="updated">Last Updated: {{ metrics.timestamp }}</div>
        <button class="refresh-btn" onclick="refreshMetrics()">Refresh Metrics</button>
    </div>
</body>
</html>
"""

def get_system_metrics():
    """Get current system metrics"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'system_info': f"{platform.system()} {platform.release()}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def home():
    """Render main page with system metrics"""
    return render_template_string(HTML_TEMPLATE, metrics=get_system_metrics())

@app.route('/api/metrics')
def metrics():
    """API endpoint for system metrics"""
    return jsonify(get_system_metrics())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
