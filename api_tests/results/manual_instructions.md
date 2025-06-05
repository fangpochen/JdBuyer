# 手动获取京东API加密参数说明


🔧 手动获取步骤:

1. 打开Chrome浏览器，访问商品页面
   https://item.jd.com/10122586394356.html

2. 按F12打开开发者工具，切换到Network标签

3. 刷新页面，在Network中搜索 "api.m.jd.com"

4. 找到 pc_detailpage_wareBusiness 请求

5. 右键点击请求 -> Copy -> Copy as cURL

6. 将cURL命令保存到文件中供分析

7. 提取关键参数:
   - h5st: 签名参数
   - x-api-eid-token: 设备token
   - uuid: 用户标识
   - body: 请求体JSON

8. 分析h5st生成规律:
   - 在Console中搜索全局函数
   - 查找h5st相关的JS代码
   - 尝试复现生成算法

🎯 关键文件位置:
- 搜索关键字: h5st, sign, token
- 常见文件: item.jd.com/xxx.js
- 内联script标签中可能包含生成函数

💾 建议工具:
- Charles/Fiddler: 抓包分析
- Chrome扩展: Header Editor
- Python: requests-html库
