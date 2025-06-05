# -*- coding: utf-8 -*-
"""
测试获取京东登录二维码接口
URL: https://qr.m.jd.com/show
"""
from base_tester import BaseTester
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import save_image

def test_qrcode():
    tester = BaseTester()
    tester.print_header("测试获取京东登录二维码")
    
    try:
        # 调用获取二维码接口
        qr_content = tester.session.getQRcode()
        
        if qr_content and len(qr_content) > 0:
            success = True
            details = f"二维码大小: {len(qr_content)} bytes"
            
            # 保存二维码图片
            try:
                save_image(qr_content, "api_tests/results/test_qrcode.png")
                details += ", 已保存到 api_tests/results/test_qrcode.png"
            except Exception as e:
                details += f", 保存图片失败: {str(e)}"
                
            tester.print_result("获取二维码", success, details)
            
            # 检查文件头是否为PNG格式
            if qr_content.startswith(b'\x89PNG'):
                tester.print_result("二维码格式检查", True, "确认为PNG格式")
            else:
                tester.print_result("二维码格式检查", False, f"非PNG格式，文件头: {qr_content[:10]}")
                
        else:
            success = False
            tester.print_result("获取二维码", success, "二维码内容为空")
        
        # 保存测试结果
        result = {
            "interface": "获取登录二维码",
            "url": "https://qr.m.jd.com/show",
            "method": "GET",
            "parameters": {
                "appid": 133,
                "size": 147,
                "t": "动态时间戳"
            },
            "success": success,
            "qr_size": len(qr_content) if qr_content else 0,
            "is_png": qr_content.startswith(b'\x89PNG') if qr_content else False,
            "timestamp": "当前时间"
        }
        
        tester.save_result("qrcode_test.json", result)
        
    except Exception as e:
        tester.print_result("获取二维码", False, f"异常: {str(e)}")

if __name__ == "__main__":
    test_qrcode() 