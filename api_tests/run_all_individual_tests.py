# -*- coding: utf-8 -*-
"""
运行所有单独的接口测试脚本
"""
import os
import sys
import subprocess
import time

def run_test_script(script_name, description):
    """运行单个测试脚本"""
    print(f"\n{'='*60}")
    print(f"🧪 运行测试: {description}")
    print(f"脚本: {script_name}")
    print(f"{'='*60}")
    
    try:
        # 使用subprocess运行Python脚本
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, 
                              text=True, 
                              cwd="api_tests")
        
        # 输出结果
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("❌ 错误输出:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 运行脚本失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 京东API接口单独测试工具")
    print("="*60)
    print("📝 说明: 将依次运行每个接口的单独测试脚本")
    print("")
    
    # 定义测试脚本列表
    test_scripts = [
        ("test_login_page.py", "测试获取登录页面"),
        ("test_qrcode.py", "测试获取二维码"),
        ("test_qr_status.py", "测试检查二维码状态"),
        ("test_item_detail.py", "测试获取商品详情 ⚠️"),
        ("test_cart_clear.py", "测试清空购物车"),
        ("test_cart_add.py", "测试添加商品到购物车"),
        ("test_checkout_page.py", "测试获取订单结算页面"),
    ]
    
    # 确保结果目录存在
    os.makedirs("api_tests/results", exist_ok=True)
    
    # 记录开始时间
    start_time = time.time()
    success_count = 0
    total_count = len(test_scripts)
    
    # 逐个运行测试
    for script_name, description in test_scripts:
        success = run_test_script(script_name, description)
        if success:
            success_count += 1
        
        # 等待1秒再运行下一个测试
        time.sleep(1)
    
    # 输出总结
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    print(f"总测试脚本数: {total_count}")
    print(f"成功运行: {success_count} ✅")
    print(f"运行失败: {total_count - success_count} ❌")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    print(f"总耗时: {duration:.2f} 秒")
    print("")
    print("📁 测试结果已保存到: api_tests/results/")
    print("")
    print("💡 建议:")
    if success_count == total_count:
        print("   - 所有测试脚本运行成功！")
        print("   - 检查各个结果文件了解接口状态")
    else:
        print("   - 部分脚本运行失败，请检查错误信息")
        print("   - 确保当前目录包含所有必要的文件")
    
    print("\n🔍 重点关注:")
    print("   - test_item_detail.py: 商品详情接口最容易过时")
    print("   - 购物车相关接口可能需要登录状态")
    print("   - 查看 api_tests/results/ 目录下的详细结果")

if __name__ == "__main__":
    main() 