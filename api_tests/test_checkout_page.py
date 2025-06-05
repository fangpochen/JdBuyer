# -*- coding: utf-8 -*-
"""
测试获取订单结算页面接口
URL: http://trade.jd.com/shopping/order/getOrderInfo.action
用于提取风控参数：eid、fp、riskControl、trackId
"""
from base_tester import BaseTester

def test_checkout_page():
    tester = BaseTester()
    tester.print_header("测试获取订单结算页面")
    
    try:
        # 调用获取结算页面接口
        order_info = tester.session.getCheckoutPage()
        
        print(f"📊 结算页面信息: {order_info}")
        print(f"   信息类型: {type(order_info)}")
        print("")
        
        # 同时直接测试原始接口
        url = 'http://trade.jd.com/shopping/order/getOrderInfo.action'
        payload = {
            'rid': str(int(tester.session.sess.time.time() * 1000)) if hasattr(tester.session.sess, 'time') else "123456789"
        }
        headers = {
            'User-Agent': tester.session.userAgent,
            'Referer': 'https://cart.jd.com/cart',
        }
        
        import time
        payload['rid'] = str(int(time.time() * 1000))
        
        resp = tester.session.sess.get(url=url, params=payload, headers=headers)
        
        print(f"📊 详细调试信息:")
        print(f"   状态码: {resp.status_code}")
        print(f"   请求URL: {resp.url}")
        print(f"   Content-Type: {resp.headers.get('Content-Type', 'Unknown')}")
        print(f"   响应大小: {len(resp.text)} 字符")
        print("")
        
        success = resp.status_code == 200
        
        if success:
            # 检查是否是HTML页面
            if 'text/html' in resp.headers.get('Content-Type', ''):
                print("✅ 返回HTML页面")
                
                # 尝试提取风控参数
                from lxml import etree
                try:
                    html = etree.HTML(resp.text)
                    
                    # 提取风控参数
                    params = {}
                    params['eid'] = html.xpath("//input[@id='eid']/@value")
                    params['fp'] = html.xpath("//input[@id='fp']/@value")
                    params['riskControl'] = html.xpath("//input[@id='riskControl']/@value")
                    params['trackId'] = html.xpath("//input[@id='TrackID']/@value")
                    
                    print("🔍 风控参数提取结果:")
                    for param_name, param_value in params.items():
                        if param_value:
                            print(f"   ✅ {param_name}: {param_value[0][:20]}..." if len(param_value[0]) > 20 else f"   ✅ {param_name}: {param_value[0]}")
                        else:
                            print(f"   ❌ {param_name}: 未找到")
                    
                    # 检查页面内容
                    if "订单" in resp.text or "结算" in resp.text:
                        print("   ✅ 页面包含订单相关内容")
                    elif "登录" in resp.text or "login" in resp.text.lower():
                        print("   ⚠️  页面似乎重定向到登录页面")
                    else:
                        print("   ❓ 页面内容未知")
                    
                    details = f"HTML页面，风控参数: {len([p for p in params.values() if p])}/4 个"
                    
                except Exception as parse_e:
                    print(f"❌ HTML解析失败: {str(parse_e)}")
                    details = f"HTML页面，但解析失败: {str(parse_e)}"
            else:
                print("❌ 非HTML响应")
                details = f"非HTML响应，Content-Type: {resp.headers.get('Content-Type', 'Unknown')}"
                print(f"   响应前300字符: {resp.text[:300]}")
        else:
            details = f"HTTP错误，状态码: {resp.status_code}"
            print(f"❌ HTTP请求失败: {resp.status_code}")
            print(f"   响应内容: {resp.text[:300]}")
        
        tester.print_result("获取订单结算页面", success, details)
        
        # 保存测试结果
        result = {
            "interface": "获取订单结算页面",
            "url": "http://trade.jd.com/shopping/order/getOrderInfo.action",
            "method": "GET",
            "parameters": {
                "rid": "动态时间戳"
            },
            "success": success,
            "method_result": order_info,
            "status_code": resp.status_code,
            "content_type": resp.headers.get('Content-Type', 'Unknown'),
            "response_size": len(resp.text),
            "is_html": 'text/html' in resp.headers.get('Content-Type', ''),
            "timestamp": "当前时间"
        }
        
        # 保存完整响应用于分析
        with open("api_tests/results/checkout_page_full_response.html", "w", encoding="utf-8") as f:
            f.write(f"<!-- URL: {resp.url} -->\n")
            f.write(f"<!-- Status: {resp.status_code} -->\n")
            f.write(f"<!-- Headers: {dict(resp.headers)} -->\n")
            f.write(resp.text)
        
        print("💾 完整HTML响应已保存到: api_tests/results/checkout_page_full_response.html")
        
        tester.save_result("checkout_page_test.json", result)
        
    except Exception as e:
        tester.print_result("获取订单结算页面", False, f"异常: {str(e)}")

if __name__ == "__main__":
    test_checkout_page() 