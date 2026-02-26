# Flask Web 开发

使用 Flask 开发 RESTful API 和 Web 应用的实践经验。

## Flask 快速开始

### 基本应用结构

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用跨域支持

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    data = {'key': 'value'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### RESTful API 设计

```python
# 获取单个资源
@app.route('/api/quote/<symbol>', methods=['GET'])
def get_quote(symbol):
    data = data_source.get_realtime_quote(symbol)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': f'未找到股票 {symbol}'}), 404

# 获取列表
@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    stocks = data_source.get_watchlist_quotes(symbols)
    return jsonify({'stocks': stocks, 'timestamp': now()})

# 带查询参数
@app.route('/api/historical/<symbol>', methods=['GET'])
def get_historical(symbol):
    count = request.args.get('count', 100, type=int)
    data = data_source.get_historical_data(symbol, count=count)
    return jsonify({'symbol': symbol, 'data': data})
```

### CORS 跨域配置

```python
from flask_cors import CORS

# 全局启用
CORS(app)

# 仅特定域名
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# 支持凭证
CORS(app, supports_credentials=True)
```

## 前端集成

### Axios 请求示例

```javascript
import axios from 'axios';

const API_BASE = '';  // 相对路径

// GET 请求
async function loadIndices() {
    const response = await axios.get(`${API_BASE}/api/indices`);
    return response.data;
}

// 带参数的 GET 请求
async function loadNews(limit = 20) {
    const response = await axios.get(`${API_BASE}/api/news`, {
        params: { limit }
    });
    return response.data;
}

// POST 请求
async function updateConfig(config) {
    const response = await axios.post(`${API_BASE}/api/config`, config);
    return response.data;
}
```

### 自动刷新实现

```javascript
// 定时刷新
setInterval(() => {
    refreshAll();
}, 30000);  // 30秒

// 手动刷新
async function refreshAll() {
    const btn = document.querySelector('.refresh-btn');
    btn.disabled = true;
    btn.textContent = '⏳ 加载中...';

    await Promise.all([
        loadIndices(),
        loadWatchlist(),
        loadSignals(),
        loadNews()
    ]);

    btn.disabled = false;
    btn.textContent = '🔄 刷新数据';
    updateLastUpdate();
}
```

## ECharts 图表

### K线图配置

```javascript
const chart = echarts.init(document.getElementById('chart'));

const option = {
    backgroundColor: 'transparent',
    tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' }
    },
    legend: {
        data: ['K线', 'MA5', 'MA10', 'MA20'],
        textStyle: { color: '#9ca3af' }
    },
    grid: {
        left: '3%',
        right: '3%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        data: dates,
        axisLine: { lineStyle: { color: '#374151' } },
        axisLabel: { color: '#9ca3af' }
    },
    yAxis: {
        scale: true,
        axisLine: { lineStyle: { color: '#374151' } },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
    },
    series: [
        {
            name: 'K线',
            type: 'candlestick',
            data: [[open, close, low, high], ...],
            itemStyle: {
                color: '#ef4444',      // 上涨
                color0: '#22c55e',     // 下跌
                borderColor: '#ef4444',
                borderColor0: '#22c55e'
            }
        },
        {
            name: 'MA5',
            type: 'line',
            data: ma5Data,
            smooth: true,
            lineStyle: { color: '#f59e0b', width: 1 },
            symbol: 'none'
        }
    ]
};

chart.setOption(option);

// 响应式
window.addEventListener('resize', () => chart.resize());
```

## 常见问题

### 1. 模板路径问题

```python
# 正确方式
@app.route('/')
def index():
    return render_template('index.html')  # Flask 自动在 templates/ 目录查找

# 模板位置
project/
├── app.py
└── templates/
    └── index.html
```

### 2. 静态文件访问

```python
# Flask 默认处理 static/ 目录
project/
├── app.py
├── static/
│   ├── css/
│   ├── js/
│   └── img/
└── templates/

# HTML 中引用
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

### 3. 开发 vs 生产环境

```python
# 开发环境
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

# 生产环境（使用 gunicorn）
# $ gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 4. 代理问题（Nginx）

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 相关项目

- stock-trader: A股交易决策辅助系统
  - Flask RESTful API 示例
  - 位置: `javis_projects/active/stock-trader/src/web`
  - 仓库: https://github.com/hashlinyk/stock-trader
