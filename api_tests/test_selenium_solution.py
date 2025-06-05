# -*- coding: utf-8 -*-
"""
Selenium解决方案：绕过JS加密获取商品信息
使用浏览器环境执行JS代码，获取真实的加密参数
"""
import json
import time
from base_tester import BaseTester

def test_selenium_approach():
    """测试Selenium方案"""
    print("🌐 Selenium方案测试")
    print("=" * 60)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        
        print("✅ Selenium依赖检查通过")
    except ImportError as e:
        print("❌ Selenium未安装，请先安装:")
        print("   pip install selenium")
        print("   下载ChromeDriver: https://chromedriver.chromium.org/")
        return False
    
    # Chrome配置
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    try:
        print("🚀 启动Chrome浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # 访问商品页面
        test_sku_id = "10122586394356"
        url = f"https://item.jd.com/{test_sku_id}.html"
        print(f"📄 访问商品页面: {url}")
        
        driver.get(url)
        time.sleep(3)  # 等待页面加载
        
        # 检查页面是否正常加载
        title = driver.title
        print(f"📄 页面标题: {title[:50]}...")
        
        # 执行JS获取商品信息
        js_code = """
        // 尝试获取页面中的商品数据
        var result = {};
        
        // 1. 尝试从window对象获取
        if (window.pageConfig && window.pageConfig.product) {
            result.pageConfig = window.pageConfig.product;
        }
        
        // 2. 尝试从全局变量获取
        if (window.cat) result.cat = window.cat;
        if (window.venderId) result.venderId = window.venderId;
        if (window.shopId) result.shopId = window.shopId;
        
        // 3. 尝试获取库存信息
        var stockElement = document.querySelector('#stock');
        if (stockElement) {
            result.stockText = stockElement.textContent;
        }
        
        // 4. 获取价格信息
        var priceElement = document.querySelector('.price');
        if (priceElement) {
            result.priceText = priceElement.textContent;
        }
        
        return JSON.stringify(result);
        """
        
        print("🔧 执行JS获取数据...")
        js_result = driver.execute_script(js_code)
        
        if js_result:
            try:
                data = json.loads(js_result)
                print("✅ JS执行成功，获取数据:")
                for key, value in data.items():
                    print(f"   {key}: {str(value)[:100]}...")
            except:
                print(f"📄 JS结果: {js_result[:200]}...")
        
        # 尝试拦截网络请求
        print("🕷️ 监控网络请求...")
        
        # 启用Performance日志
        driver.execute_cdp_cmd('Network.enable', {})
        
        # 模拟用户操作触发网络请求
        try:
            # 滚动页面可能触发懒加载
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # 获取网络日志
            logs = driver.get_log('performance')
            api_requests = []
            
            for log in logs:
                message = json.loads(log['message'])
                if message['message']['method'] == 'Network.responseReceived':
                    url = message['message']['params']['response']['url']
                    if 'api.m.jd.com' in url:
                        api_requests.append(url)
            
            if api_requests:
                print("🎯 发现API请求:")
                for req in api_requests[:5]:  # 显示前5个
                    print(f"   {req}")
            else:
                print("❌ 未发现相关API请求")
                
        except Exception as e:
            print(f"⚠️ 网络监控失败: {str(e)}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Selenium方案失败: {str(e)}")
        print("💡 可能原因:")
        print("   1. ChromeDriver未安装或版本不匹配")
        print("   2. Chrome浏览器未安装")
        print("   3. 网络连接问题")
        return False

def create_manual_instructions():
    """创建手动获取参数的说明"""
    print("📋 手动获取加密参数说明")
    print("=" * 60)
    
    instructions = """
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
"""
    
    print(instructions)
    
    # 保存说明到文件
    with open("api_tests/results/manual_instructions.md", "w", encoding="utf-8") as f:
        f.write("# 手动获取京东API加密参数说明\n\n")
        f.write(instructions)
    
    print("💾 详细说明已保存到: api_tests/results/manual_instructions.md")

def suggest_alternative_solutions():
    """建议替代解决方案"""
    print("🔄 替代解决方案")
    print("=" * 60)
    
    solutions = """
📋 可行的替代方案:

1. 🎭 使用代理服务
   - 购买专业的爬虫代理服务
   - 使用已破解的API服务
   - 成本较高但效果稳定

2. 🤖 使用Puppeteer/Playwright
   - 比Selenium更轻量的浏览器自动化
   - 更好的网络请求拦截功能
   - 可以执行复杂的JS逆向

3. 🔍 寻找旧版本接口
   - 京东可能保留了兼容性接口
   - 手机版H5接口通常加密较少
   - 小程序API可能有不同的验证方式

4. 📱 移动端接口
   - app.jd.com 的移动接口
   - 微信小程序接口
   - 通常验证较为宽松

5. 🎯 静态数据方案
   - 如果只需要基本信息，可以解析HTML
   - 商品标题、价格等在页面源码中
   - 库存信息可能需要额外请求

🎯 当前最可行的方案:
1. 先尝试解析HTML获取基本信息
2. 对于库存等动态信息，使用定时爬虫
3. 长期考虑投资专业的API解决方案
"""
    
    print(solutions)
    
    # 保存方案到文件
    with open("api_tests/results/alternative_solutions.md", "w", encoding="utf-8") as f:
        f.write("# 京东API替代解决方案\n\n")
        f.write(solutions)
    
    print("💾 替代方案已保存到: api_tests/results/alternative_solutions.md")

def main():
    print("🛠️ 京东新接口解决方案测试")
    print("=" * 80)
    
    # 1. 测试Selenium方案
    selenium_success = test_selenium_approach()
    
    print("\n")
    
    # 2. 创建手动说明
    create_manual_instructions()
    
    print("\n")
    
    # 3. 建议替代方案
    suggest_alternative_solutions()
    
    print("\n")
    print("📋 总结:")
    if selenium_success:
        print("✅ Selenium方案可用，建议进一步开发")
    else:
        print("❌ Selenium方案需要环境配置")
    print("📚 已生成详细的手动操作说明")
    print("🎯 已提供多种替代解决方案")

if __name__ == "__main__":
    main() 