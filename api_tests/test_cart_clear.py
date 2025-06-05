# -*- coding: utf-8 -*-
"""
测试清空购物车选中商品接口
URL: https://api.m.jd.com/api
functionId: pcCart_jc_cartUnCheckAll
"""
from base_tester import BaseTester

def test_cart_clear():
    tester = BaseTester()
    tester.print_header("测试清空购物车选中商品")
    
    try:
        # 调用清空购物车接口
        resp = tester.session.uncheckCartAll()
        
        print(f"📊 详细调试信息:")
        print(f"   状态码: {resp.status_code}")
        print(f"   请求URL: {resp.url}")
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
                        print("   ✅ 购物车操作成功")
                    else:
                        print("   ❌ 购物车操作失败")
                        if 'message' in json_data:
                            print(f"   错误信息: {json_data['message']}")
                
                # 检查购物车信息
                if 'resultData' in json_data:
                    result_data = json_data['resultData']
                    print(f"   📦 结果数据: {type(result_data)}")
                    if isinstance(result_data, dict) and 'cartInfo' in result_data:
                        cart_info = result_data['cartInfo']
                        print(f"   🛒 购物车信息: {type(cart_info)}")
                
                details = f"JSON解析成功，API success: {json_data.get('success', 'Unknown')}"
                
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
        
        tester.print_result("清空购物车选中", success, details)
        
        # 保存测试结果
        result = {
            "interface": "清空购物车选中商品",
            "url": "https://api.m.jd.com/api",
            "method": "POST",
            "function_id": "pcCart_jc_cartUnCheckAll",
            "parameters": {
                "appid": "JDC_mall_cart",
                "body": '{"serInfo":{"area":"","user-key":""}}',
                "loginType": 3
            },
            "success": success,
            "status_code": resp.status_code,
            "content_type": resp.headers.get('Content-Type', 'Unknown'),
            "response_preview": resp.text[:500],
            "timestamp": "当前时间"
        }
        
        if success:
            try:
                json_data = resp.json()
                result["api_success"] = json_data.get('success', False)
                result["has_cart_info"] = 'resultData' in json_data and 'cartInfo' in json_data.get('resultData', {})
            except:
                pass
        
        tester.save_result("cart_clear_test.json", result)
        
    except Exception as e:
        tester.print_result("清空购物车选中", False, f"异常: {str(e)}")

if __name__ == "__main__":
    test_cart_clear() 