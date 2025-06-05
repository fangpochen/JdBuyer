# 京东API接口单独测试工具

## 📁 更新后的目录结构

```
api_tests/
├── README.md                    # 原始说明文档
├── README_individual.md         # 本文档 - 单独测试说明
├── base_tester.py              # 基础测试工具类
├── run_all_individual_tests.py # 运行所有单独测试的主脚本
├── results/                    # 测试结果目录
│   ├── *.json                  # 各接口测试结果
│   ├── *.png                   # 二维码图片
│   ├── *.txt                   # 原始响应内容
│   └── *.html                  # HTML响应页面
└── 单独接口测试脚本:
    ├── test_login_page.py      # 测试获取登录页面
    ├── test_qrcode.py          # 测试获取二维码
    ├── test_qr_status.py       # 测试检查二维码状态
    ├── test_item_detail.py     # 测试获取商品详情 ⚠️
    ├── test_cart_clear.py      # 测试清空购物车
    ├── test_cart_add.py        # 测试添加商品到购物车
    └── test_checkout_page.py   # 测试获取订单结算页面
```

## 🚀 使用方法

### 方法1: 运行所有单独测试
```bash
cd api_tests
python run_all_individual_tests.py
```

### 方法2: 运行单个接口测试
```bash
cd api_tests
python test_item_detail.py      # 测试商品详情接口
python test_qrcode.py           # 测试二维码接口
python test_cart_clear.py       # 测试购物车接口
```

## 📋 各个测试脚本详情

### 🔐 登录相关测试

#### `test_login_page.py`
- **功能**: 测试获取京东登录页面
- **检查**: 页面状态码、内容类型、是否包含登录元素
- **输出**: `results/login_page_test.json`

#### `test_qrcode.py`
- **功能**: 测试获取登录二维码
- **检查**: 二维码大小、PNG格式验证
- **输出**: `results/qrcode_test.json`, `results/test_qrcode.png`

#### `test_qr_status.py`
- **功能**: 测试检查二维码扫描状态
- **检查**: Cookie状态、ticket获取
- **输出**: `results/qr_status_test.json`

### 🛍️ 商品相关测试

#### `test_item_detail.py` ⚠️ **重点关注**
- **功能**: 测试获取商品详情接口
- **检查**: JSON解析、关键字段存在性、库存信息
- **输出**: `results/item_detail_test.json`, `results/item_detail_full_response.txt`
- **注意**: 这是最容易出问题的接口！

### 🛒 购物车相关测试

#### `test_cart_clear.py`
- **功能**: 测试清空购物车选中商品
- **检查**: API调用成功状态、购物车信息
- **输出**: `results/cart_clear_test.json`

#### `test_cart_add.py`
- **功能**: 测试添加商品到购物车
- **检查**: 添加结果、错误信息
- **输出**: `results/cart_add_test.json`

### 📋 订单相关测试

#### `test_checkout_page.py`
- **功能**: 测试获取订单结算页面
- **检查**: HTML页面、风控参数提取
- **输出**: `results/checkout_page_test.json`, `results/checkout_page_full_response.html`

## 📊 测试结果分析

### ✅ 正常情况
- 接口返回200状态码
- 返回预期的数据格式
- 关键字段存在

### ❌ 异常情况及解决方案

#### 1. 商品详情接口失败
**症状**: JSON解析错误、返回HTML而非JSON
**解决**:
1. 查看 `results/item_detail_full_response.txt`
2. 使用浏览器访问京东商品页面抓包分析
3. 对比新旧接口差异

#### 2. 购物车接口需要登录
**症状**: 返回登录相关错误
**解决**:
1. 确保在主程序中先完成登录
2. 这些接口测试主要验证格式和可达性

#### 3. 结算页面重定向
**症状**: 返回登录页面而非结算页面
**解决**:
1. 需要先添加商品到购物车
2. 需要完整的登录状态

## 🔧 自定义测试

### 修改测试商品
编辑 `base_tester.py`:
```python
self.test_skuId = '你的商品ID'
self.test_areaId = '你的地区ID'
```

### 添加新的接口测试
1. 复制现有测试脚本作为模板
2. 修改接口URL和参数
3. 更新检查逻辑
4. 添加到 `run_all_individual_tests.py`

## 💡 重要提示

1. **单独测试的优势**:
   - 快速定位具体问题接口
   - 详细的调试输出
   - 独立的结果文件
   - 便于逐个修复

2. **测试限制**:
   - 不测试完整业务流程
   - 部分接口需要登录状态
   - 主要验证接口可达性和格式

3. **优先级建议**:
   - 先测试 `test_item_detail.py`
   - 其次测试购物车相关接口
   - 登录相关接口通常较稳定

方总牛逼 