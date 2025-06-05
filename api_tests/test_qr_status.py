# -*- coding: utf-8 -*-
"""
测试检查二维码扫描状态接口
URL: https://qr.m.jd.com/check
"""
from base_tester import BaseTester

def test_qr_status():
    tester = BaseTester()
    tester.print_header("测试检查二维码扫描状态")
    
    try:
        # 先获取二维码以获得必要的cookie
        qr_content = tester.session.getQRcode()
        if not qr_content:
            tester.print_result("前置条件", False, "无法获取二维码，跳过状态检查")
            return
        
        tester.print_result("前置条件", True, "二维码获取成功")
        
        # 检查二维码状态
        ticket = tester.session.getQRcodeTicket()
        
        # 未扫码时ticket应该为None，这是正常的
        success = True  # 只要不报错就算成功
        details = f"Ticket状态: {ticket}"
        
        # 检查必要的cookie
        wlfstk_smdl = tester.session.sess.cookies.get('wlfstk_smdl')
        details += f", wlfstk_smdl Cookie: {wlfstk_smdl}"
        
        if wlfstk_smdl:
            tester.print_result("Cookie检查", True, "wlfstk_smdl cookie存在")
        else:
            tester.print_result("Cookie检查", False, "wlfstk_smdl cookie缺失")
        
        tester.print_result("检查二维码状态", success, details)
        
        # 保存测试结果
        result = {
            "interface": "检查二维码状态",
            "url": "https://qr.m.jd.com/check",
            "method": "GET",
            "parameters": {
                "appid": "133",
                "callback": "jQuery随机数",
                "token": "wlfstk_smdl值",
                "_": "时间戳"
            },
            "success": success,
            "ticket": ticket,
            "has_wlfstk_cookie": wlfstk_smdl is not None,
            "note": "未扫码时ticket为None是正常的",
            "timestamp": "当前时间"
        }
        
        tester.save_result("qr_status_test.json", result)
        
    except Exception as e:
        tester.print_result("检查二维码状态", False, f"异常: {str(e)}")

if __name__ == "__main__":
    test_qr_status() 