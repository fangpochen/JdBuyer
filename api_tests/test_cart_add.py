# -*- coding: utf-8 -*-
"""
测试添加商品到购物车接口
URL: https://api.m.jd.com/api
functionId: pcCart_jc_cartAdd
"""
from base_tester import BaseTester

def test_cart_add():
    tester = BaseTester()
    tester.print_header("测试添加商品到购物车")
    
    try:
        # 调用添加商品到购物车接口
        result = tester.session.addCartSku(tester.test_skuId, 1)
        
        print(f"📊 接口调用结果: {result}")
        print(f"   结果类型: {type(result)}")
        
        # addCartSku方法返回的是处理后的boolean结果
        # 我们需要直接测试原始接口来获取更详细信息
        url = 'https://api.m.jd.com/api'
        headers = {
            'User-Agent': tester.session.userAgent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': 'https://cart.jd.com',
            'referer': 'https://cart.jd.com'
        }
        
        data = {
            'functionId': 'pcCart_jc_cartAdd',
            'appid': 'JDC_mall_cart',
            'body': f'{{"operations":[{{"carttype":1,"TheSkus":[{{"Id":"{tester.test_skuId}","num":1}}]}}]}}',
            'loginType': 3
        }
        
        resp = tester.session.sess.post(url=url, headers=headers, data=data)
        
        print(f"📊 详细调试信息:")
        print(f"   状态码: {resp.status_code}")
        print(f"   Content-Type: {resp.headers.get('Content-Type', 'Unknown')}")
        print("")
        
        success = resp.status_code == 200
        
        if success:
            try:
                # 尝试解析JSON
                json_data = resp.json()
                
                print("✅ JSON解析成功")
                print(f"   返回字段: {list(json_data.keys())}")
                
                # 检查关键字段
                if 'success' in json_data:
                    api_success = json_data['success']
                    print(f"   📊 API成功状态: {api_success}")
                    
                    if api_success:
                        print("   ✅ 添加商品成功")
                    else:
                        print("   ❌ 添加商品失败")
                        if 'message' in json_data:
                            print(f"   错误信息: {json_data['message']}")
                        if 'resultCode' in json_data:
                            print(f"   错误代码: {json_data['resultCode']}")
                
                details = f"方法返回: {result}, API success: {json_data.get('success', 'Unknown')}"
                
            except Exception as json_e:
                success = False
                print("❌ JSON解析失败")
                print(f"   错误: {str(json_e)}")
                print(f"   响应内容: {resp.text[:300]}")
                
                details = f"JSON解析失败: {str(json_e)}"
        else:
            details = f"HTTP错误，状态码: {resp.status_code}"
            print(f"❌ HTTP请求失败: {resp.status_code}")
            print(f"   响应内容: {resp.text[:300]}")
        
        tester.print_result("添加商品到购物车", success, details)
        
        # 保存测试结果
        test_result = {
            "interface": "添加商品到购物车",
            "url": "https://api.m.jd.com/api",
            "method": "POST",
            "function_id": "pcCart_jc_cartAdd",
            "parameters": {
                "appid": "JDC_mall_cart",
                "body": f'{{"operations":[{{"carttype":1,"TheSkus":[{{"Id":"{tester.test_skuId}","num":1}}]}}]}}',
                "loginType": 3
            },
            "success": success,
            "method_result": result,
            "status_code": resp.status_code,
            "content_type": resp.headers.get('Content-Type', 'Unknown'),
            "response_preview": resp.text[:500],
            "timestamp": "当前时间"
        }
        
        if success:
            try:
                json_data = resp.json()
                test_result["api_success"] = json_data.get('success', False)
                test_result["error_message"] = json_data.get('message', '')
                test_result["result_code"] = json_data.get('resultCode', '')
            except:
                pass
        
        tester.save_result("cart_add_test.json", test_result)
        
    except Exception as e:
        tester.print_result("添加商品到购物车", False, f"异常: {str(e)}")

if __name__ == "__main__":
    test_cart_add() 