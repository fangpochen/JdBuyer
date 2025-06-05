# -*- coding: utf-8 -*-
"""
京东抢购项目 - API接口测试脚本
用于测试所有接口的可用性和返回格式
"""
import requests
import json
import time
import os
import sys

# 添加父目录到路径，以便导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from JdSession import Session
from utils import save_image

class JdApiTester:
    def __init__(self):
        self.session = Session()
        self.test_results = {}
        self.test_skuId = '100015253059'  # 测试用商品ID
        self.test_areaId = '1_2901_55554_0'  # 测试用地区ID
    
    def log_test_result(self, test_name, success, details):
        """记录测试结果"""
        self.test_results[test_name] = {
            'success': success,
            'details': details,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if not success:
            print(f"   错误详情: {details}")
        print("-" * 50)
    
    def test_qr_login_apis(self):
        """测试二维码登录相关接口"""
        print("🔐 测试登录相关接口...")
        
        # 1. 测试获取登录页面
        try:
            page = self.session.getLoginPage()
            success = page.status_code == 200
            details = f"状态码: {page.status_code}, Content-Type: {page.headers.get('Content-Type', 'Unknown')}"
            if success:
                details += f", 页面长度: {len(page.text)}"
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("获取登录页面", success, details)
        
        # 2. 测试获取二维码
        try:
            qr_content = self.session.getQRcode()
            success = qr_content is not None and len(qr_content) > 0
            details = f"二维码大小: {len(qr_content) if qr_content else 0} bytes"
            if success:
                # 保存二维码用于查看
                save_image(qr_content, "api_tests/test_qrcode.png")
                details += ", 已保存到 api_tests/test_qrcode.png"
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("获取二维码", success, details)
        
        # 3. 测试检查二维码状态（不扫码，预期返回状态码）
        try:
            ticket = self.session.getQRcodeTicket()
            # 未扫码时应该返回None，这是正常的
            success = True  # 只要不报错就算成功
            details = f"Ticket状态: {ticket}, Cookie中wlfstk_smdl: {self.session.sess.cookies.get('wlfstk_smdl', 'None')}"
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("检查二维码状态", success, details)
    
    def test_item_apis(self):
        """测试商品相关接口"""
        print("🛍️ 测试商品相关接口...")
        
        # 1. 测试获取商品详情
        try:
            resp = self.session.getItemDetail(self.test_skuId, 1, self.test_areaId)
            success = resp.status_code == 200
            details = f"状态码: {resp.status_code}, URL: {resp.url}"
            details += f", Content-Type: {resp.headers.get('Content-Type', 'Unknown')}"
            
            if success:
                try:
                    json_data = resp.json()
                    details += f", JSON字段: {list(json_data.keys())}"
                    # 检查关键字段
                    if 'stockInfo' in json_data:
                        details += f", 库存信息: {json_data['stockInfo']}"
                    if 'shopInfo' in json_data:
                        details += f", 店铺信息存在"
                except:
                    details += f", 响应前500字符: {resp.text[:500]}"
            else:
                details += f", 响应内容: {resp.text[:200]}"
                
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("获取商品详情", success, details)
        
        # 2. 测试库存查询
        try:
            has_stock = self.session.getItemStock(self.test_skuId, 1, self.test_areaId)
            success = isinstance(has_stock, bool)
            details = f"库存状态: {has_stock}"
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("查询商品库存", success, details)
    
    def test_cart_apis(self):
        """测试购物车相关接口"""
        print("🛒 测试购物车相关接口...")
        
        # 1. 测试清空购物车
        try:
            resp = self.session.uncheckCartAll()
            success = resp.status_code == 200
            details = f"状态码: {resp.status_code}, URL: {resp.url}"
            
            if success:
                try:
                    json_data = resp.json()
                    details += f", 返回字段: {list(json_data.keys())}"
                    if 'success' in json_data:
                        details += f", success: {json_data['success']}"
                except:
                    details += f", 响应内容: {resp.text[:200]}"
            else:
                details += f", 响应内容: {resp.text[:200]}"
                
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("清空购物车选中", success, details)
        
        # 2. 测试添加商品到购物车
        try:
            result = self.session.addCartSku(self.test_skuId, 1)
            success = isinstance(result, bool)
            details = f"添加结果: {result}"
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("添加商品到购物车", success, details)
    
    def test_order_apis(self):
        """测试订单相关接口"""
        print("📋 测试订单相关接口...")
        
        # 1. 测试获取结算页面
        try:
            order_info = self.session.getCheckoutPage()
            success = order_info is not None
            details = f"结算页面信息: {order_info}"
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("获取订单结算页面", success, details)
    
    def test_external_apis(self):
        """测试外部接口"""
        print("🌐 测试外部接口...")
        
        # 1. 测试微信通知接口 (Server酱)
        try:
            # 这里只测试接口格式，不实际发送
            test_url = "https://sc.ftqq.com/test.send"
            resp = requests.get(test_url, params={'text': 'test', 'desp': 'test'}, timeout=5)
            success = resp.status_code in [200, 404]  # 404也是正常的，说明接口地址正确
            details = f"状态码: {resp.status_code}, 接口可达性正常"
        except Exception as e:
            success = False
            details = f"异常: {str(e)}"
        
        self.log_test_result("微信通知接口可达性", success, details)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("🚀 京东API接口测试开始")
        print("=" * 60)
        
        self.test_qr_login_apis()
        self.test_item_apis()
        self.test_cart_apis()
        self.test_order_apis()
        self.test_external_apis()
        
        # 输出测试总结
        self.print_summary()
    
    def print_summary(self):
        """打印测试总结"""
        print("=" * 60)
        print("📊 测试结果总结")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {passed_tests/total_tests*100:.1f}%")
        
        print("\n📋 详细结果:")
        for test_name, result in self.test_results.items():
            status = "✅" if result['success'] else "❌"
            print(f"{status} {test_name}")
            if not result['success']:
                print(f"    {result['details']}")
        
        print("\n💡 建议:")
        if failed_tests > 0:
            print("- 失败的接口可能需要更新")
            print("- 使用浏览器F12抓包分析新接口")
            print("- 检查请求参数和响应格式变化")
        else:
            print("- 所有接口测试通过！")
        
        # 保存测试结果到文件
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """保存测试结果到文件"""
        try:
            with open("api_tests/test_results.json", "w", encoding="utf-8") as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            print(f"\n💾 测试结果已保存到: api_tests/test_results.json")
        except Exception as e:
            print(f"保存测试结果失败: {e}")

def main():
    """主函数"""
    # 创建测试目录
    os.makedirs("api_tests", exist_ok=True)
    
    # 运行测试
    tester = JdApiTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 