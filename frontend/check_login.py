#!/usr/bin/env python3
"""
简单的登录页面功能检查脚本
"""
import os
import subprocess
import sys

def check_file_structure():
    """检查文件结构是否正确"""
    print("📁 检查文件结构...")
    
    required_files = [
        'src/LoginSimple.js',
        'src/LoginSimple.css',
        'src/App.js',
        'src/config.js',
        'src/ActionProvider.js',
        'src/MessageParser.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少以下文件:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ 所有必需文件都存在")
        return True

def check_node_dependencies():
    """检查Node.js依赖"""
    print("\n📦 检查Node.js依赖...")
    
    if not os.path.exists('package.json'):
        print("❌ 不在正确的目录中，请确保在frontend目录下运行")
        return False
    
    if not os.path.exists('node_modules'):
        print("⚠️  node_modules目录不存在，运行 'npm install'")
        return False
    
    print("✅ Node.js依赖已安装")
    return True

def check_imports():
    """检查导入语句"""
    print("\n🔍 检查导入语句...")
    
    try:
        with open('src/LoginSimple.js', 'r') as f:
            content = f.read()
            
        # 检查关键导入
        if 'import React' in content:
            print("✅ React导入正确")
        else:
            print("❌ React导入缺失")
            return False
            
        if 'import axios' in content:
            print("✅ axios导入正确")
        else:
            print("❌ axios导入缺失")
            return False
            
        if "from './LoginSimple.css'" in content:
            print("✅ CSS导入正确")
        else:
            print("❌ CSS导入缺失")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 检查导入失败: {e}")
        return False

def check_app_js():
    """检查App.js中的Login导入"""
    print("\n📱 检查App.js...")
    
    try:
        with open('src/App.js', 'r') as f:
            content = f.read()
            
        if 'import Login from "./LoginSimple"' in content:
            print("✅ App.js中正确导入LoginSimple")
            return True
        else:
            print("❌ App.js中没有正确导入LoginSimple")
            return False
            
    except Exception as e:
        print(f"❌ 检查App.js失败: {e}")
        return False

def check_syntax():
    """检查JavaScript语法"""
    print("\n🔧 检查JavaScript语法...")
    
    try:
        # 检查LoginSimple.js语法
        result = subprocess.run(['node', '-c', 'src/LoginSimple.js'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ LoginSimple.js语法正确")
        else:
            print("❌ LoginSimple.js语法错误")
            print(f"错误: {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 语法检查失败: {e}")
        return False

def main():
    """主检查函数"""
    print("🚀 开始检查登录页面...")
    print("=" * 50)
    
    # 检查文件结构
    files_ok = check_file_structure()
    
    # 检查Node.js依赖
    deps_ok = check_node_dependencies()
    
    # 检查导入语句
    imports_ok = check_imports()
    
    # 检查App.js
    app_ok = check_app_js()
    
    # 检查语法
    syntax_ok = check_syntax()
    
    print("\n" + "=" * 50)
    print("📋 检查结果总结:")
    print(f"📁 文件结构: {'✅ 通过' if files_ok else '❌ 失败'}")
    print(f"📦 依赖安装: {'✅ 通过' if deps_ok else '❌ 失败'}")
    print(f"🔍 导入语句: {'✅ 通过' if imports_ok else '❌ 失败'}")
    print(f"📱 App.js配置: {'✅ 通过' if app_ok else '❌ 失败'}")
    print(f"🔧 语法检查: {'✅ 通过' if syntax_ok else '❌ 失败'}")
    
    if files_ok and deps_ok and imports_ok and app_ok and syntax_ok:
        print("\n🎉 所有检查通过！登录页面应该正常工作。")
        print("💡 运行 'npm start' 来启动前端应用")
        print("🌐 访问 http://localhost:3000 查看登录页面")
    else:
        print("\n⚠️  存在一些问题，请根据上述信息进行修复。")

if __name__ == "__main__":
    main()