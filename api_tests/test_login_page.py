# -*- coding: utf-8 -*-
"""
测试获取京东登录页面接口
URL: https://passport.jd.com/new/login.aspx
"""
from base_tester import BaseTester

def test_login_page():
    tester = BaseTester()
    tester.print_header("测试获取京东登录页面")
    
    try:
        # 调用获取登录页面接口
        page = tester.session.getLoginPage()
        
        # 测试响应
        success = tester.test_response(page, "获取登录页面")
        
        if success:
            # 检查页面内容是否包含登录相关元素
            if "登录" in page.text or "login" in page.text.lower():
                tester.print_result("页面内容检查", True, "页面包含登录相关内容")
            else:
                tester.print_result("页面内容检查", False, "页面不包含登录相关内容")
        
        # 保存测试结果
        result = {
            "interface": "获取登录页面",
            "url": "https://passport.jd.com/new/login.aspx",
            "method": "GET",
            "status_code": page.status_code,
            "success": success,
            "content_type": page.headers.get('Content-Type', 'Unknown'),
            "response_size": len(page.text),
            "timestamp": tester.session._Session__time_str() if hasattr(tester.session, '_Session__time_str') else "N/A"
        }
        
        tester.save_result("login_page_test.json", result)
        
    except Exception as e:
        tester.print_result("获取登录页面", False, f"异常: {str(e)}")

if __name__ == "__main__":
    test_login_page() 