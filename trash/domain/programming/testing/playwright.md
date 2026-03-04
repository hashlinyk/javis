# Playwright E2E 测试

使用 Playwright 进行端到端自动化测试。

## 安装

```bash
npm install -D @playwright/test
npx playwright install
```

## 配置文件

### playwright.config.js

```javascript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  reporter: [
    ['html', { outputFolder: 'tests/playwright-report' }],
    ['json', { outputFile: 'tests/test-results.json' }]
  ],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:5000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
    viewport: { width: 1280, height: 720 },
  },

  webServer: {
    command: 'python -m src.main web',
    url: 'http://localhost:5000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## 基础测试

### 页面加载测试

```javascript
const { test, expect } = require('@playwright/test');

test('页面加载验证', async ({ page }) => {
  await page.goto('http://localhost:5000');

  // 验证标题
  await expect(page).toHaveTitle(/A股交易/);

  // 验证元素存在
  await expect(page.locator('h1')).toBeVisible();
  await expect(page.locator('.header')).toBeVisible();
});
```

### API 测试

```javascript
test('API接口测试', async ({ request }) => {
  const response = await request.get('http://localhost:5000/api/status');

  expect(response.status()).toBe(200);

  const data = await response.json();
  expect(data).toHaveProperty('status', 'running');
});
```

### 交互测试

```javascript
test('按钮点击测试', async ({ page }) => {
  await page.goto('http://localhost:5000');

  // 点击按钮
  await page.click('.refresh-btn');

  // 验证状态变化
  await expect(page.locator('text=加载中')).toBeVisible();

  // 等待完成
  await page.waitForSelector('text=刷新数据', { state: 'visible' });
});
```

## 高级测试

### 数据加载测试

```javascript
test('数据加载验证', async ({ page }) => {
  await page.goto('http://localhost:5000');

  // 等待数据加载
  await page.waitForSelector('.data-item', { timeout: 10000 });

  // 验证数据存在
  const items = await page.locator('.data-item').count();
  expect(items).toBeGreaterThan(0);
});
```

### 自动刷新测试

```javascript
test('自动刷新功能', async ({ page }) => {
  await page.goto('http://localhost:5000');

  // 获取初始时间
  const initialTime = await page.locator('.update-time').textContent();

  // 等待刷新周期
  await page.waitForTimeout(35000);

  // 验证时间已更新
  const newTime = await page.locator('.update-time').textContent();
  expect(newTime).not.toBe(initialTime);
});
```

### 性能测试

```javascript
test('页面加载性能', async ({ page }) => {
  const startTime = Date.now();

  await page.goto('http://localhost:5000');
  await page.waitForLoadState('networkidle');

  const loadTime = Date.now() - startTime;

  expect(loadTime).toBeLessThan(5000);
});
```

### 视觉测试

```javascript
test('界面截图', async ({ page }) => {
  await page.goto('http://localhost:5000');

  // 完整页面截图
  await page.screenshot({
    path: 'tests/screenshots/homepage.png',
    fullPage: true
  });

  // 元素截图
  await page.locator('.card').first().screenshot({
    path: 'tests/screenshots/card.png'
  });
});
```

### 响应式测试

```javascript
test('移动端适配', async ({ page }) => {
  // 设置移动端视口
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('http://localhost:5000');

  // 验证布局
  const card = page.locator('.card').first();
  const box = await card.boundingBox();

  expect(box.width).toBeLessThanOrEqual(375);
});
```

## 测试组织

### 测试套件

```javascript
test.describe('功能模块A', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/page-a');
  });

  test('测试1', async ({ page }) => {
    // ...
  });

  test('测试2', async ({ page }) => {
    // ...
  });
});
```

### 参数化测试

```javascript
const testCases = [
  { name: 'Chrome', use: devices['Desktop Chrome'] },
  { name: 'Firefox', use: devices['Desktop Firefox'] },
  { name: 'Safari', use: devices['Desktop Safari'] }
];

for (const { name, use } of testCases) {
  test(`${name} 浏览器测试`, async ({ page }) => {
    // 测试代码
  });
}
```

## 辅助函数

### 等待API

```javascript
async function waitForApi(request, endpoint, timeout = 5000) {
  const startTime = Date.now();

  while (Date.now() - startTime < timeout) {
    const response = await request.get(endpoint);
    if (response.status() === 200) {
      return await response.json();
    }
    await new Promise(r => setTimeout(r, 500));
  }

  throw new Error(`API ${endpoint} 超时`);
}
```

### 元素操作

```javascript
// 等待元素
await page.waitForSelector('.my-element');

// 检查元素存在
const exists = await page.locator('.my-element').count() > 0;

// 获取文本
const text = await page.locator('.my-element').textContent();

// 获取属性
const href = await page.locator('a').getAttribute('href');
```

## 运行测试

```bash
# 运行所有测试
npx playwright test

# 有头模式
npx playwright test --headed

# UI 模式
npx playwright test --ui

# 调试模式
npx playwright test --debug

# 特定文件
npx playwright test example.spec.js

# 特定浏览器
npx playwright test --project=chromium
```

## CI/CD 集成

### GitHub Actions

```yaml
- name: 运行 E2E 测试
  run: |
    npm install
    npx playwright install --with-deps
    npm test

- uses: actions/upload-artifact@v3
  if: always()
  with:
    name: playwright-report
    path: tests/playwright-report/
```

## 相关项目

- stock-trader: A股交易决策辅助系统
  - 完整的 Playwright 测试套件
  - 位置: `javis_projects/active/stock-trader/tests`
