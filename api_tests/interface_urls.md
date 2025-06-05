# 京东抢购项目 - 接口清单

## 🔐 登录认证相关接口

### 1. 获取登录页面
- **URL**: `https://passport.jd.com/new/login.aspx`
- **方法**: GET
- **用途**: 获取京东登录页面，建立初始会话
- **返回**: HTML页面

### 2. 获取登录二维码
- **URL**: `https://qr.m.jd.com/show`
- **方法**: GET
- **参数**:
  - `appid`: 133
  - `size`: 147
  - `t`: 时间戳(毫秒)
- **请求头**:
  - `Referer`: `https://passport.jd.com/new/login.aspx`
- **用途**: 获取登录二维码图片
- **返回**: PNG图片二进制数据

### 3. 检查二维码扫描状态
- **URL**: `https://qr.m.jd.com/check`
- **方法**: GET
- **参数**:
  - `appid`: 133
  - `callback`: jQuery随机数
  - `token`: wlfstk_smdl cookie值
  - `_`: 时间戳
- **请求头**:
  - `Referer`: `https://passport.jd.com/new/login.aspx`
- **用途**: 轮询检查二维码扫描状态，获取ticket
- **返回**: JSONP格式响应

### 4. 验证登录凭证
- **URL**: `https://passport.jd.com/uc/qrCodeTicketValidation`
- **方法**: GET
- **参数**:
  - `t`: ticket值
- **请求头**:
  - `Referer`: `https://passport.jd.com/uc/login?ltype=logout`
- **用途**: 验证ticket有效性，完成登录
- **返回**: JSON格式

### 5. 验证登录状态
- **URL**: `https://order.jd.com/center/list.action`
- **方法**: GET
- **参数**:
  - `rid`: 时间戳
- **用途**: 验证cookie是否有效，判断登录状态
- **返回**: 302重定向(未登录) 或 200(已登录)

## 🛍️ 商品信息相关接口

### 1. 获取商品详情和库存 ⚠️ 
- **URL**: `https://item-soa.jd.com/getWareBusiness`
- **方法**: GET
- **参数**:
  - `skuId`: 商品ID
  - `area`: 地区ID
  - `num`: 商品数量
- **请求头**:
  - `Referer`: `https://item.jd.com/{skuId}.html`
- **用途**: 获取商品详情、库存状态、店铺信息
- **返回**: JSON格式
- **关键字段**:
  - `stockInfo.isStock`: 是否有库存
  - `shopInfo.shop.shopId`: 店铺ID
  - `YuShouInfo`: 预售信息
  - `miaoshaInfo`: 秒杀信息

## 🛒 购物车操作接口

### 基础信息
- **基础URL**: `https://api.m.jd.com/api`
- **方法**: POST
- **Content-Type**: `application/x-www-form-urlencoded`
- **请求头**:
  - `origin`: `https://cart.jd.com`
  - `referer`: `https://cart.jd.com`

### 1. 清空购物车选中商品
- **functionId**: `pcCart_jc_cartUnCheckAll`
- **appid**: `JDC_mall_cart`
- **body**: `{"serInfo":{"area":"","user-key":""}}`
- **loginType**: 3

### 2. 添加商品到购物车
- **functionId**: `pcCart_jc_cartAdd`
- **appid**: `JDC_mall_cart`
- **body**: `{"operations":[{"carttype":1,"TheSkus":[{"Id":"商品ID","num":数量}]}]}`
- **loginType**: 3

### 3. 修改购物车商品数量
- **functionId**: `pcCart_jc_changeSkuNum`
- **appid**: `JDC_mall_cart`
- **body**: `{"operations":[{"TheSkus":[{"Id":"商品ID","num":数量,"skuUuid":"UUID","useUuid":false}]}],"serInfo":{"area":"地区ID"}}`
- **loginType**: 3

## 📋 订单相关接口

### 1. 普通商品结算页面
- **URL**: `http://trade.jd.com/shopping/order/getOrderInfo.action`
- **方法**: GET
- **参数**:
  - `rid`: 时间戳
- **请求头**:
  - `Referer`: `https://cart.jd.com/cart`
- **用途**: 获取结算页面，提取风控参数
- **返回**: HTML页面
- **提取参数**:
  - `eid`: 设备指纹
  - `fp`: 指纹参数
  - `riskControl`: 风控参数
  - `TrackID`: 追踪ID

### 2. 预售商品结算页面
- **URL**: `https://cart.jd.com/cart/dynamic/gateForSubFlow.action`
- **方法**: GET
- **参数**:
  - `wids`: 商品ID
  - `nums`: 数量
  - `subType`: 32
- **请求头**:
  - `Referer`: `https://cart.jd.com/cart`
- **用途**: 预售商品结算页面

### 3. 提交订单 ⚠️
- **URL**: `https://trade.jd.com/shopping/order/submitOrder.action`
- **方法**: POST
- **请求头**:
  - `Host`: `trade.jd.com`
  - `Referer`: `http://trade.jd.com/shopping/order/getOrderInfo.action`
- **数据参数**:
  - `overseaPurchaseCookies`: 空
  - `vendorRemarks`: []
  - `submitOrderParam.sopNotPutInvoice`: false
  - `submitOrderParam.trackID`: TestTrackId
  - `submitOrderParam.ignorePriceChange`: 0
  - `submitOrderParam.btSupport`: 0
  - `riskControl`: 风控参数
  - `submitOrderParam.isBestCoupon`: 1
  - `submitOrderParam.jxj`: 1
  - `submitOrderParam.trackId`: 追踪ID
  - `submitOrderParam.eid`: 设备指纹
  - `submitOrderParam.fp`: 指纹参数
  - `submitOrderParam.needCheck`: 1
  - `submitOrderParam.payPassword`: 支付密码(可选)
- **预售特殊参数**:
  - `preSalePaymentTypeInOptional`: 2
  - `submitOrderParam.payType4YuShou`: 2

### 4. 保存发票信息
- **URL**: `https://trade.jd.com/shopping/dynamic/invoice/saveInvoice.action`
- **方法**: POST
- **用途**: 切换发票类型重试下单

## 🌐 外部接口

### 1. 微信通知 (Server酱)
- **URL**: `https://sc.ftqq.com/{sckey}.send`
- **方法**: GET
- **参数**:
  - `text`: 消息标题
  - `desp`: 消息内容
- **用途**: 发送微信通知

## ⚠️ 状态说明

- ✅ **正常**: 接口通常工作正常
- ⚠️ **可能过时**: 接口可能已被京东更新，需要验证
- 🔥 **高频使用**: 核心功能接口，优先测试

## 🔧 测试建议

1. **优先测试标记为⚠️的接口**
2. **使用浏览器F12开发者工具抓包对比**
3. **关注返回格式的变化**
4. **检查新增的验证参数**
5. **测试不同商品ID的兼容性** 