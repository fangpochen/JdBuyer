# -*- coding: utf-8 -*-
"""
测试获取商品详情接口 ⚠️ 
URL: https://item-soa.jd.com/getWareBusiness
这是最可能出问题的接口！
"""
from base_tester import BaseTester

def test_item_detail():
    tester = BaseTester()
    tester.print_header("测试获取商品详情接口 ⚠️")
    
    print("🔥 注意: 这是最容易出问题的接口，如果失败说明京东已更新此接口")
    print("")
    
    try:
        # 调用获取商品详情接口
        resp = tester.session.getItemDetail(tester.test_skuId, 1, tester.test_areaId)
        
        print(f"📊 详细调试信息:")
        print(f"   状态码: {resp.status_code}")
        print(f"   请求URL: {resp.url}")
        print(f"   Content-Type: {resp.headers.get('Content-Type', 'Unknown')}")
        print(f"   响应大小: {len(resp.text)} 字符")
        print("")
        
        success = resp.status_code == 200
        
        if success:
            try:
                # 尝试解析JSON
                json_data = resp.json()
                
                print("✅ JSON解析成功")
                print(f"   顶级字段: {list(json_data.keys())}")
                
                # 检查关键字段
                checks = {}
                checks['stockInfo'] = 'stockInfo' in json_data
                checks['price'] = 'price' in json_data  # 新接口字段
                checks['wareInfo'] = 'wareInfo' in json_data  # 新接口字段
                checks['itemShopInfo'] = 'itemShopInfo' in json_data  # 新接口字段
                
                for field, exists in checks.items():
                    status = "✅" if exists else "❌"
                    print(f"   {status} {field}: {'存在' if exists else '不存在'}")
                
                # 特别检查库存信息
                if 'stockInfo' in json_data:
                    stock_info = json_data['stockInfo']
                    is_stock = stock_info.get('isStock', False)
                    stock_desc = stock_info.get('stockDesc', '未知')
                    print(f"   📦 库存状态: {is_stock}")
                    print(f"   📦 库存描述: {stock_desc}")
                
                # 检查价格信息
                if 'price' in json_data:
                    price_info = json_data['price']
                    current_price = price_info.get('p', '未知')
                    original_price = price_info.get('op', '未知')
                    print(f"   💰 当前价格: {current_price}")
                    print(f"   💰 原价: {original_price}")
                
                details = f"JSON解析成功，包含字段: {list(json_data.keys())}"
                
            except Exception as json_e:
                success = False
                print("❌ JSON解析失败")
                print(f"   错误: {str(json_e)}")
                print(f"   响应前500字符:")
                print(f"   {resp.text[:500]}")
                print("")
                print("🔍 这通常意味着:")
                print("   1. 接口返回的是HTML而不是JSON")
                print("   2. 接口地址已经更新")
                print("   3. 需要额外的验证参数")
                
                details = f"JSON解析失败: {str(json_e)}, 响应: {resp.text[:200]}"
        else:
            details = f"HTTP错误，状态码: {resp.status_code}, 响应: {resp.text[:200]}"
        
        tester.print_result("获取商品详情", success, details)
        
        # 保存测试结果和响应内容用于分析
        result = {
            "interface": "获取商品详情",
            "url": "https://item-soa.jd.com/getWareBusiness",
            "method": "GET",
            "parameters": {
                "skuId": tester.test_skuId,
                "area": tester.test_areaId,
                "num": 1
            },
            "success": success,
            "status_code": resp.status_code,
            "content_type": resp.headers.get('Content-Type', 'Unknown'),
            "response_size": len(resp.text),
            "response_preview": resp.text[:1000],  # 保存前1000字符用于分析
            "is_json": False,
            "timestamp": "当前时间"
        }
        
        if success:
            try:
                json_data = resp.json()
                result["is_json"] = True
                result["json_fields"] = list(json_data.keys())
                result["has_stock_info"] = 'stockInfo' in json_data
                result["has_shop_info"] = 'shopInfo' in json_data
            except:
                pass
        
        tester.save_result("item_detail_test.json", result)
        
        # 额外保存完整响应用于调试
        with open("api_tests/results/item_detail_full_response.txt", "w", encoding="utf-8") as f:
            f.write(f"URL: {resp.url}\n")
            f.write(f"Status: {resp.status_code}\n")
            f.write(f"Headers: {dict(resp.headers)}\n")
            f.write(f"Content:\n{resp.text}")
        
        print("💾 完整响应已保存到: api_tests/results/item_detail_full_response.txt")
        
    except Exception as e:
        tester.print_result("获取商品详情", False, f"异常: {str(e)}")

if __name__ == "__main__":
    test_item_detail() 