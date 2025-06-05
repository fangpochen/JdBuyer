# -*- coding: utf-8 -*-
"""
接口测试基础工具类
"""
import requests
import json
import time
import os
import sys

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from JdSession import Session

class BaseTester:
    def __init__(self):
        self.session = Session()
        self.test_skuId = '100015253059'  # 测试用商品ID
        self.test_areaId = '1_2901_55554_0'  # 测试用地区ID
    
    def print_header(self, title):
        """打印测试标题"""
        print("=" * 60)
        print(f"🧪 {title}")
        print("=" * 60)
    
    def print_result(self, test_name, success, details):
        """打印测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        print(f"详情: {details}")
        if not success:
            print("💡 建议: 检查接口是否已更新，使用浏览器F12抓包对比")
        print("-" * 50)
        return success
    
    def test_response(self, resp, test_name):
        """通用响应测试"""
        try:
            success = resp.status_code == 200
            details = f"状态码: {resp.status_code}, URL: {resp.url}"
            details += f", Content-Type: {resp.headers.get('Content-Type', 'Unknown')}"
            
            if success:
                # 尝试解析JSON
                try:
                    json_data = resp.json()
                    details += f", JSON字段: {list(json_data.keys())[:5]}"  # 只显示前5个字段
                except:
                    details += f", 响应长度: {len(resp.text)}, 前100字符: {resp.text[:100]}"
            else:
                details += f", 错误响应: {resp.text[:200]}"
            
            return self.print_result(test_name, success, details)
        except Exception as e:
            return self.print_result(test_name, False, f"异常: {str(e)}")
    
    def save_result(self, filename, result_data):
        """保存测试结果"""
        try:
            with open(f"api_tests/results/{filename}", "w", encoding="utf-8") as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            print(f"💾 结果已保存到: api_tests/results/{filename}")
        except Exception as e:
            print(f"保存失败: {e}")

# 创建结果目录
os.makedirs("api_tests/results", exist_ok=True) 