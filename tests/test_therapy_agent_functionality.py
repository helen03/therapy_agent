#!/usr/bin/env python3
"""
全面测试Therapy Agent应用功能的测试脚本
测试覆盖用户登录、会话交互、语音生成、文档上传等核心功能
"""

import requests
import json
import tempfile
import os
import time

class TherapyAgentTest:
    def __init__(self):
        # 设置API基础URL
        self.base_url = "http://localhost:5000"
        # 测试用户凭据
        self.test_user = {
            "username": "guest",
            "password": "guest"
        }
        # 存储会话信息
        self.user_id = None
        self.session_id = None
        # 测试文档路径
        self.test_doc_path = self._create_test_document()

    def _create_test_document(self):
        """创建一个临时测试文档用于上传测试"""
        # 创建一个临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        # 写入测试内容
        temp_file.write("心理健康的重要性\n\n心理健康对每个人都至关重要，它影响着我们的思考、感受和行为方式。\n通过适当的治疗和支持，大多数心理健康问题都可以得到有效管理。\n保持积极的心态、建立良好的社交关系和定期锻炼都是维护心理健康的重要方式。".encode('utf-8'))
        temp_file.close()
        return temp_file.name

    def test_login(self):
        """测试用户登录功能"""
        print("\n===== 测试用户登录功能 =====")
        try:
            response = requests.post(
                f"{self.base_url}/api/login",
                json={"user_info": self.test_user}
            )
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {result}")
            
            # 验证登录成功
            if result.get("validID") and result.get("userID") and result.get("sessionID"):
                self.user_id = result["userID"]
                self.session_id = result["sessionID"]
                print(f"✅ 登录成功! 用户ID: {self.user_id}, 会话ID: {self.session_id}")
                print(f"初始提示: {result.get('model_prompt')}")
                print(f"可选选项: {result.get('choices')}")
                return True
            else:
                print("❌ 登录失败: 响应不包含有效用户ID或会话ID")
                return False
        except Exception as e:
            print(f"❌ 登录测试异常: {e}")
            return False

    def test_update_session(self):
        """测试会话更新功能"""
        print("\n===== 测试会话更新功能 =====")
        if not self.user_id or not self.session_id:
            print("⚠️ 请先成功登录")
            return False
            
        try:
            # 模拟用户选择一个选项
            choice_info = {
                "user_id": self.user_id,
                "session_id": self.session_id,
                "input_type": "emotional_state",
                "user_choice": "有些焦虑"
            }
            
            response = requests.post(
                f"{self.base_url}/api/update_session",
                json={"choice_info": choice_info}
            )
            
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {result}")
            
            # 验证响应包含正确的字段
            if "chatbot_response" in result and "user_options" in result:
                print(f"✅ 会话更新成功!")
                print(f"聊天机器人回复: {result['chatbot_response']}")
                print(f"用户可选选项: {result['user_options']}")
                return True
            else:
                print("❌ 会话更新失败: 响应不完整")
                return False
        except Exception as e:
            print(f"❌ 会话更新测试异常: {e}")
            return False

    def test_generate_speech(self):
        """测试语音生成功能"""
        print("\n===== 测试语音生成功能 =====")
        try:
            response = requests.post(
                f"{self.base_url}/api/generate_speech",
                json={
                    "text": "你好，我是你的心理支持助手。无论你现在感觉如何，我都在这里陪伴你。",
                    "user_emotion": "anxious"
                }
            )
            
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {result}")
            
            # 验证语音生成成功
            if result.get("success") and result.get("audio_file"):
                print(f"✅ 语音生成成功! 音频文件: {result['audio_file']}")
                return True
            else:
                print(f"❌ 语音生成失败: {result.get('error', '未知错误')}")
                return False
        except Exception as e:
            print(f"❌ 语音生成测试异常: {e}")
            return False

    def test_user_insights(self):
        """测试用户洞察功能"""
        print("\n===== 测试用户洞察功能 =====")
        if not self.user_id:
            print("⚠️ 请先成功登录")
            return False
            
        try:
            response = requests.get(
                f"{self.base_url}/api/user_insights?user_id={self.user_id}"
            )
            
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {result}")
            
            # 验证洞察获取成功
            if result.get("success") and result.get("insights"):
                print(f"✅ 用户洞察获取成功!")
                print(f"洞察内容: {result['insights']}")
                return True
            else:
                print(f"❌ 用户洞察获取失败: {result.get('error', '未知错误')}")
                return False
        except Exception as e:
            print(f"❌ 用户洞察测试异常: {e}")
            return False

    def test_upload_document(self):
        """测试文档上传功能"""
        print("\n===== 测试文档上传功能 =====")
        if not self.user_id:
            print("⚠️ 请先成功登录")
            return False
            
        try:
            # 准备文件上传
            with open(self.test_doc_path, 'rb') as file:
                response = requests.post(
                    f"{self.base_url}/api/upload_document",
                    files={'file': file},
                    data={
                        'user_id': str(self.user_id),
                        'title': '测试心理健康文档'
                    }
                )
            
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {result}")
            
            # 验证文档上传成功
            if result.get("success") and result.get("doc_id"):
                print(f"✅ 文档上传成功! 文档ID: {result['doc_id']}")
                return True
            else:
                print(f"❌ 文档上传失败: {result.get('error', '未知错误')}")
                return False
        except Exception as e:
            print(f"❌ 文档上传测试异常: {e}")
            return False
    
    def test_daily_checkin(self):
        """测试每日签到功能"""
        print("\n===== 测试每日签到功能 =====")
        if not self.user_id:
            print("⚠️ 请先成功登录")
            return False
            
        try:
            response = requests.get(
                f"{self.base_url}/api/daily_checkin?user_id={self.user_id}"
            )
            
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {result}")
            
            # 验证签到成功
            if result.get("success") and result.get("message"):
                print(f"✅ 每日签到成功!")
                print(f"签到消息: {result['message']}")
                return True
            else:
                print(f"❌ 每日签到失败: {result.get('error', '未知错误')}")
                return False
        except Exception as e:
            print(f"❌ 每日签到测试异常: {e}")
            return False

    def run_all_tests(self):
        """运行所有测试"""
        print("\n========= 开始Therapy Agent功能测试 =========")
        
        # 测试结果统计
        results = {
            "login": False,
            "update_session": False,
            "generate_speech": False,
            "user_insights": False,
            "upload_document": False,
            "daily_checkin": False
        }
        
        # 运行测试
        results["login"] = self.test_login()
        if results["login"]:
            # 登录成功后再运行其他测试
            results["update_session"] = self.test_update_session()
            # 等待1秒，避免请求过于频繁
            time.sleep(1)
            results["generate_speech"] = self.test_generate_speech()
            time.sleep(1)
            results["user_insights"] = self.test_user_insights()
            time.sleep(1)
            results["upload_document"] = self.test_upload_document()
            time.sleep(1)
            results["daily_checkin"] = self.test_daily_checkin()
        
        # 清理临时文件
        if os.path.exists(self.test_doc_path):
            os.unlink(self.test_doc_path)
        
        # 显示测试结果摘要
        print("\n========= 测试结果摘要 =========")
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        
        for test_name, success in results.items():
            status = "✅ 通过" if success else "❌ 失败"
            print(f"{test_name}: {status}")
            
        print(f"\n总测试数: {total_tests}, 通过数: {passed_tests}, 通过率: {passed_tests/total_tests*100:.1f}%")
        print("================================\n")

if __name__ == "__main__":
    print("Therapy Agent功能测试工具")
    print("注意：请确保后端服务已在 http://localhost:5000 启动")
    print("3秒后开始测试...")
    time.sleep(3)
    
    tester = TherapyAgentTest()
    tester.run_all_tests()