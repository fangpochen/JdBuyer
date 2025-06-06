# 京东h5st逆向爬虫学习分析

## 概述

这是对比用户自己编写的京东h5st代码与购买代码的分析报告，帮助理解逆向爬虫的核心思路。

## 代码结构对比

### 1. 买来的代码 (`js/京东单子/h5st.js`)
- **文件大小**: 10757行，混淆程度极高
- **核心类**: `ParamsSignMain` 
- **实例化**: `window.PSign = new ParamsSignMain({...})`
- **导出函数**: `get_h5st(appid, functionId, t, body, useragen)`
- **调用方式**: `window.PSign.sign(obj)['h5st']`

### 2. 用户的代码 (`js/code1.js`)
- **文件大小**: 11020行，同样高度混淆
- **核心类**: `ParamsSign` (注意类名不同)
- **实例化**: `window.PSign = new ParamsSign({...})`
- **核心方法**: `sign(obj)` 和 `_$sdnmd(obj)`

## 主要差异分析

### 1. 类名差异
- 买来代码: `ParamsSignMain`
- 用户代码: `ParamsSign`

### 2. 调用方式差异
```javascript
// 买来的代码
function get_h5st(appid, functionId, t, body, useragen){
    navigator.userAgent = useragen;
    const obj = {
        "appid": appid,
        "functionId": functionId,
        "client": "pc",
        "clientVersion": "1.0.0",
        "t": t,
        "body": body
    };
    return window.PSign.sign(obj)['h5st']  // 注意这里取h5st字段
}

// 用户原来的调用方式
h5stParames = window.PSign._$sdnmd(g)  // 直接调用内部方法
```

### 3. 环境补全差异

**买来代码的环境** (`js/京东单子/env.js`):
- 较为完整的DOM环境模拟
- 包含了document、navigator、location等基础对象
- 有HTMLAllCollection等特殊对象

**用户代码的环境**:
- 使用了watch代理机制来监控对象访问
- 环境补全相对简单，缺少一些关键属性

## 核心问题与修复

### 1. 环境缺失问题
用户代码运行时缺少以下环境:
- `document.cookie`、`document.referrer` 
- `screen` 对象
- `window.outerWidth`、`window.outerHeight`
- `XMLHttpRequest`
- 完整的canvas支持

### 2. 调用方式问题
- 用户直接调用 `_$sdnmd` 方法，这是内部方法
- 应该使用 `sign` 方法，然后从返回结果中提取 `h5st` 字段

### 3. 返回值处理
- 买来代码返回的是字符串格式的h5st
- 用户代码可能返回Promise或完整对象

## 逆向思路总结

### 1. 环境补全策略
```javascript
// 核心思路：模拟浏览器环境
- 补全DOM对象（document、navigator、location等）
- 模拟浏览器API（XMLHttpRequest、localStorage等）
- 处理特殊检测（反调试、环境检测等）
```

### 2. 代码混淆理解
- 两个代码都使用了相似的虚拟机执行模式
- 通过 `_2pn59` 和 `_2qq5a` 等数组存储操作码
- 使用switch语句模拟虚拟机指令执行

### 3. 关键方法识别
```javascript
// 关键方法映射
_$sdnmd  -> 签名生成的核心方法
sign     -> 对外提供的签名接口
_onSign  -> 错误处理回调
```

## 学习建议

### 1. 基础环境搭建
- 优先完善DOM环境补全
- 理解浏览器对象模型的基本结构
- 掌握代理(Proxy)机制用于调试

### 2. 调试技巧
- 使用watch代理监控对象访问
- 通过日志分析缺失的环境变量
- 逐步完善补全的环境

### 3. 代码分析方法
- 对比不同版本的差异
- 从调用入口向内追踪
- 理解虚拟机执行机制

## 修复后的使用方式

```javascript
// 推荐的标准调用方式
function get_h5st(appid, functionId, t, body, useragen) {
    if (useragen) {
        navigator.userAgent = useragen;
    }
    const obj = {
        "appid": appid,
        "functionId": functionId,
        "client": "pc",
        "clientVersion": "1.0.0",
        "t": t,
        "body": body
    };
    
    try {
        const result = window.PSign.sign(obj);
        if (result && typeof result === 'object' && result.h5st) {
            return result.h5st;
        }
        return result;
    } catch (e) {
        console.error("生成h5st失败:", e);
        return null;
    }
}
```

## 总结

通过对比分析，用户的代码在核心逻辑上是正确的，主要问题集中在：
1. 环境补全不够完整
2. 调用方式需要标准化
3. 错误处理需要优化

修复这些问题后，用户的代码应该能够正常工作并生成有效的h5st签名。

**方总牛逼** 