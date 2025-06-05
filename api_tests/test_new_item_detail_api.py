# -*- coding: utf-8 -*-
"""
测试新版商品详情接口分析
URL: https://api.m.jd.com/
需要JS逆向的参数：h5st、x-api-eid-token、uuid
"""
import json
import time
import urllib.parse
from base_tester import BaseTester

def analyze_new_api_url():
    """分析新接口URL中的加密参数"""
    print("🔍 分析新版商品详情接口")
    print("=" * 60)
    
    # 你提供的完整URL
    original_url = """https://api.m.jd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc&clientVersion=1.0.0&t=1749128085783&body=%7B%22skuId%22%3A10122586394356%2C%22cat%22%3A%226233%2C6264%2C21638%22%2C%22area%22%3A%2216_1303_3483_59783%22%2C%22shopId%22%3A%2210179889%22%2C%22venderId%22%3A10315111%2C%22paramJson%22%3A%22%7B%5C%22platform2%5C%22%3A%5C%221%5C%22%2C%5C%22colType%5C%22%3A100%2C%5C%22specialAttrStr%5C%22%3A%5C%22p0ppppppppp2pppppppppppppppp%5C%22%2C%5C%22skuMarkStr%5C%22%3A%5C%2200%5C%22%7D%22%2C%22num%22%3A1%2C%22bbTraffic%22%3A%22%22%2C%22canvasType%22%3A1%2C%22giftServiceIsSelected%22%3A%22%22%2C%22customInfoId%22%3A%220%22%7D&h5st=20250605205450817%3Baazd9wgdi02w20m2%3Bfb5df%3Btk03w874f1bcd18nvLDMgbZRGl2FWPFNCI3nJFi2it3Z1OvpLBVX92D4ahKyDwtJrCeLCoSNqvDYh8zCmPAqRFeGsOZX%3Ba49d083be07040c0479d7904c6f4ea39ab39a96b80b425afdaf16c45aa334479%3B5.1%3B1749128085817%3Bri_uxFOm22ciAuLmOGLm9aHWMusmk_Mm86oi8SHi_KoVHRXgKFXWNlsm0msSIlsmOGuj6mrm0mMTLhImOuMsCmcWLpbh3urV_KbV1moi6abW8WbhMJLh3WoV4OLh7Sbh2msm0msSo94VMZ4RMusmk_MmJVIVLRrhMhbV5qoh9WLh7aLV7qbg8aIW8i7h5a7iJhLmOGLm7pIRAp4WMusmk_siOGLm6aHWMusmk_Mm52ciAaLRPZoTFV4X5OImOGLm4lsmOGujMaZYelIi7GIU3msm0mcT-dITNlHmOuMsCmMi72YUXlsm0mMV_lsmOGujxtsmkirm0mci9aHWMusmOuMsCqbiOGLm_qbRMlsmOusmk_sgBuMgMmbi5lImOusmOGujMmJcbJ6Tfx5W76IhBmsm0mcT-dITNlHmOusmOGuj_uMgMObRMlsmOusmk_siOGLm3aHWMusmOuMsCKLiOGLm4aHWMusmOuMsCurm0mch5lImOusmOGuj_uMgMebRMlsmOusmk_Mi_qrm0m8i5lImOusmOGujMKLj92siMuMgMqbRMlsmOusmk_siOGLmDRHmOusmOGuj5uMgMinTMusmOuMsCurm0msTMusmOuMsCurm0msV3lsmOusmkCnm0msVAZoR2ZImOuMsC6nmOGOmbIF1sAG1GIF16s01MuMgMmrSMusmOuMsztMgMunSMusmk_Mm6WrQOCrh42YUXt8g_2si9usZgt8S3xoVAJ4ZMuMgMqYR7lsmOG_Q%3Ba52ca00da5bb04423076fe1971fc3b4177cbd7b9d4dbd2f805cc4afcaed183d6%3BtenjKJKT-JoRL1YRI9MT-J4S8ZIZ61YVF94WCeHTJJoTL9cQKxIWCeYU_tXW&x-api-eid-token=jdd03WFLCZKZUHSR5PPN3K4I4MAICNBVC3XY7PMUUHFRW6HDDMQ72G7O22T3TJJYPDSBAAOMOI52SSPZWIUVNAOWUDPHOTIAAAAMXIAUFL2IAAAAACHPSIZNFAPSOBYX&loginType=3&scval=10122586394356&uuid=181111935.17490280250701527595118.1749028025.1749119733.1749126886.6"""
    
    # 解析URL参数
    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(original_url)
    params = parse_qs(parsed.query)
    
    print("📊 URL参数分析:")
    print(f"   基础URL: {parsed.scheme}://{parsed.netloc}{parsed.path}")
    print("")
    
    print("🔧 基础参数:")
    basic_params = ['appid', 'functionId', 'client', 'clientVersion', 't', 'loginType', 'scval']
    for param in basic_params:
        if param in params:
            print(f"   {param}: {params[param][0]}")
    print("")
    
    print("📦 body参数 (URL解码后):")
    if 'body' in params:
        body_decoded = urllib.parse.unquote(params['body'][0])
        print(f"   {body_decoded}")
        
        # 解析body中的JSON
        try:
            body_json = json.loads(body_decoded)
            print("   📋 body JSON结构:")
            for key, value in body_json.items():
                print(f"      {key}: {value}")
        except:
            print("   ❌ body JSON解析失败")
    print("")
    
    print("🔐 加密参数分析:")
    
    # h5st参数分析
    if 'h5st' in params:
        h5st = urllib.parse.unquote(params['h5st'][0])
        h5st_parts = h5st.split(';')
        print(f"   🔑 h5st参数: {len(h5st)} 字符")
        print(f"      分段数量: {len(h5st_parts)}")
        for i, part in enumerate(h5st_parts[:5]):  # 只显示前5段
            print(f"      段{i+1}: {part[:50]}{'...' if len(part) > 50 else ''}")
        if len(h5st_parts) > 5:
            print(f"      ... 还有 {len(h5st_parts) - 5} 段")
    
    # x-api-eid-token参数分析
    if 'x-api-eid-token' in params:
        eid_token = params['x-api-eid-token'][0]
        print(f"   🎫 x-api-eid-token: {len(eid_token)} 字符")
        print(f"      {eid_token}")
    
    # uuid参数分析
    if 'uuid' in params:
        uuid = params['uuid'][0]
        print(f"   🆔 uuid: {uuid}")
        uuid_parts = uuid.split('.')
        if len(uuid_parts) >= 5:
            print(f"      用户ID: {uuid_parts[0]}")
            print(f"      时间戳们: {uuid_parts[1:]}")
    
    print("")
    return params

def test_simplified_request():
    """测试简化版请求（去掉加密参数）"""
    print("🧪 测试简化版请求")
    print("=" * 60)
    
    tester = BaseTester()
    url = 'https://api.m.jd.com/'
    
    # 基础参数（无加密）
    payload = {
        'appid': 'pc-item-soa',
        'functionId': 'pc_detailpage_wareBusiness',
        'client': 'pc',
        'clientVersion': '1.0.0',
        't': str(int(time.time() * 1000)),
        'body': json.dumps({
            "skuId": str(tester.test_skuId),
            "cat": "",
            "area": str(tester.test_areaId),
            "num": 1
        }),
        'loginType': '3',
        'scval': str(tester.test_skuId)
    }
    
    headers = {
        'User-Agent': tester.session.userAgent,
        'Referer': f'https://item.jd.com/{tester.test_skuId}.html',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    
    print("📤 发送简化请求...")
    resp = tester.session.sess.post(url, data=payload, headers=headers)
    
    print(f"📊 响应信息:")
    print(f"   状态码: {resp.status_code}")
    print(f"   Content-Type: {resp.headers.get('Content-Type', 'Unknown')}")
    print(f"   响应大小: {len(resp.text)} 字符")
    print(f"   响应前200字符: {resp.text[:200]}")
    
    return resp

def test_original_request(params):
    """使用原始参数测试请求"""
    print("🧪 测试原始请求参数")
    print("=" * 60)
    
    tester = BaseTester()
    url = 'https://api.m.jd.com/'
    
    # 构建完整参数
    payload = {}
    for key, value_list in params.items():
        payload[key] = value_list[0]
    
    headers = {
        'User-Agent': tester.session.userAgent,
        'Referer': 'https://item.jd.com/10122586394356.html',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    
    print("📤 发送原始参数请求...")
    resp = tester.session.sess.post(url, data=payload, headers=headers)
    
    print(f"📊 响应信息:")
    print(f"   状态码: {resp.status_code}")
    print(f"   Content-Type: {resp.headers.get('Content-Type', 'Unknown')}")
    print(f"   响应大小: {len(resp.text)} 字符")
    
    if resp.status_code == 200:
        try:
            json_data = resp.json()
            print("✅ JSON解析成功!")
            print(f"   顶级字段: {list(json_data.keys())[:10]}...")  # 显示前10个字段
            
            # 检查关键字段
            if 'stockInfo' in json_data:
                stock_info = json_data['stockInfo']
                print(f"   📦 库存状态: {stock_info.get('isStock', 'Unknown')}")
                print(f"   📦 库存描述: {stock_info.get('stockDesc', 'Unknown')}")
        except Exception as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"   响应前500字符: {resp.text[:500]}")
    
    return resp

def generate_js_reverse_tips():
    """生成JS逆向提示"""
    print("💡 JS逆向分析提示")
    print("=" * 60)
    
    print("🔍 关键加密参数:")
    print("   1. h5st: 签名参数，通常由时间戳+设备信息+请求参数生成")
    print("   2. x-api-eid-token: 设备指纹token，可能需要浏览器环境生成")
    print("   3. uuid: 用户唯一标识，包含多个时间戳")
    print("")
    
    print("🛠️ 逆向步骤建议:")
    print("   1. 在浏览器F12中搜索 'h5st' 关键字")
    print("   2. 找到生成h5st的JS函数")
    print("   3. 分析函数的输入参数和算法")
    print("   4. 用Python重新实现算法")
    print("")
    
    print("🔧 可能的JS文件位置:")
    print("   - item.jd.com 页面的内联JS")
    print("   - static.360buyimg.com 的JS文件")
    print("   - 搜索关键字: h5st, eid, uuid, sign")
    print("")
    
    print("📋 临时解决方案:")
    print("   1. 使用selenium模拟浏览器获取参数")
    print("   2. 寻找不需要加密的替代接口")
    print("   3. 使用代理/爬虫服务")

def save_analysis_result(params, simple_resp, original_resp):
    """保存分析结果"""
    result = {
        "interface_analysis": "新版商品详情接口分析",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url_params": {key: value[0] for key, value in params.items()},
        "simple_request": {
            "status_code": simple_resp.status_code,
            "content_type": simple_resp.headers.get('Content-Type', 'Unknown'),
            "response_size": len(simple_resp.text),
            "success": simple_resp.status_code == 200,
            "headers": dict(simple_resp.headers),
            "response_text": simple_resp.text[:2000] if simple_resp.text else "",  # 保存前2000字符
            "response_full": simple_resp.text  # 保存完整响应
        },
        "original_request": {
            "status_code": original_resp.status_code,
            "content_type": original_resp.headers.get('Content-Type', 'Unknown'),
            "response_size": len(original_resp.text),
            "success": original_resp.status_code == 200,
            "headers": dict(original_resp.headers),
            "response_text": original_resp.text[:2000] if original_resp.text else "",  # 保存前2000字符
            "response_full": original_resp.text  # 保存完整响应
        },
        "conclusion": {
            "requires_encryption": True,
            "key_params": ["h5st", "x-api-eid-token", "uuid"],
            "next_steps": "需要JS逆向分析h5st生成算法"
        }
    }
    
    # 保存结果
    with open("api_tests/results/new_api_analysis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("💾 分析结果已保存到: api_tests/results/new_api_analysis.json")

def main():
    print("🔬 新版商品详情接口深度分析")
    print("=" * 80)
    
    # 1. 分析URL参数
    params = analyze_new_api_url()
    
    print("\n")
    
    # 2. 测试简化请求
    simple_resp = test_simplified_request()
    
    print("\n")
    
    # 3. 测试原始请求
    original_resp = test_original_request(params)
    
    print("\n")
    
    # 4. 生成逆向提示
    generate_js_reverse_tips()
    
    print("\n")
    
    # 5. 保存分析结果
    save_analysis_result(params, simple_resp, original_resp)

if __name__ == "__main__":
    main() 