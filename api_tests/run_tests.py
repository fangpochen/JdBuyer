# -*- coding: utf-8 -*-
"""
快速运行API测试脚本
"""
import os
import sys

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_all_apis import main

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 京东API接口测试工具")
    print("=" * 60)
    print("📝 测试说明:")
    print("1. 此工具将测试所有京东接口的可用性")
    print("2. 不需要登录，仅测试接口连通性和返回格式")
    print("3. 测试结果将保存到 api_tests/test_results.json")
    print("4. 如果需要查看详细接口信息，请查看 api_tests/interface_urls.md")
    print("")
    
    input("按回车键开始测试...")
    main() 