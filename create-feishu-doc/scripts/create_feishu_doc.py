#!/usr/bin/env python3
"""
飞书文档创建工具
用于创建飞书文档并分批次填充完整内容
解决飞书API对单次写入内容长度的限制问题
"""

import time
import json
import sys
from typing import List, Dict, Tuple, Optional

class FeishuDocCreator:
    """飞书文档创建器"""
    
    def __init__(self, title: str, initial_content: str = None):
        """
        初始化文档创建器
        
        Args:
            title: 文档标题
            initial_content: 初始内容（通常只包含标题）
        """
        self.title = title
        self.initial_content = initial_content or f"# {title}"
        self.document_id = None
        self.document_url = None
        self.content_segments = []
        
    def create_document(self) -> Tuple[bool, str]:
        """
        创建空白文档
        
        Returns:
            (成功状态, 消息)
        """
        try:
            # 这里应该调用实际的飞书API
            # 伪代码：feishu_doc.create(title=self.title, content=self.initial_content)
            print(f"📄 创建文档: {self.title}")
            print(f"📝 初始内容: {self.initial_content[:50]}...")
            
            # 模拟API调用
            time.sleep(0.5)  # 模拟网络延迟
            
            # 模拟返回结果
            self.document_id = f"doc_{int(time.time())}"
            self.document_url = f"https://feishu.cn/docx/{self.document_id}"
            
            print(f"✅ 文档创建成功")
            print(f"📋 文档ID: {self.document_id}")
            print(f"🔗 文档链接: {self.document_url}")
            
            return True, f"文档创建成功，ID: {self.document_id}"
            
        except Exception as e:
            error_msg = f"文档创建失败: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def wait_for_initialization(self, seconds: int = 2):
        """
        等待文档初始化完成
        
        Args:
            seconds: 等待秒数
        """
        print(f"⏳ 等待文档初始化 ({seconds}秒)...")
        time.sleep(seconds)
        print("✅ 文档初始化完成")
    
    def split_content(self, full_content: str, max_segment_length: int = 500) -> List[str]:
        """
        将完整内容分割成多个段落
        
        Args:
            full_content: 完整内容
            max_segment_length: 每个段落的最大长度
            
        Returns:
            内容段落列表
        """
        print(f"📊 分割内容，最大段落长度: {max_segment_length}字符")
        
        # 按章节分割（## 标题）
        segments = []
        lines = full_content.split('\n')
        current_segment = []
        current_length = 0
        
        for line in lines:
            line_length = len(line)
            
            # 如果是章节标题，开始新段落
            if line.startswith('## ') and current_segment:
                if current_segment:
                    segments.append('\n'.join(current_segment))
                current_segment = [line]
                current_length = line_length
            # 如果当前段落太长，开始新段落
            elif current_length + line_length > max_segment_length and current_segment:
                segments.append('\n'.join(current_segment))
                current_segment = [line]
                current_length = line_length
            else:
                current_segment.append(line)
                current_length += line_length
        
        # 添加最后一个段落
        if current_segment:
            segments.append('\n'.join(current_segment))
        
        self.content_segments = segments
        print(f"📋 内容分割完成，共{len(segments)}个段落")
        
        # 显示段落统计
        for i, segment in enumerate(segments[:3]):  # 只显示前3个段落预览
            print(f"  段落{i+1}: {segment[:50]}...")
        if len(segments) > 3:
            print(f"  ... 还有{len(segments)-3}个段落")
        
        return segments
    
    def append_segment(self, segment: str, segment_index: int, max_retries: int = 3) -> Tuple[bool, str]:
        """
        追加一个内容段落
        
        Args:
            segment: 内容段落
            segment_index: 段落索引
            max_retries: 最大重试次数
            
        Returns:
            (成功状态, 消息)
        """
        if not self.document_id:
            return False, "文档ID未设置，请先创建文档"
        
        print(f"📝 写入段落 {segment_index + 1}/{len(self.content_segments)}")
        print(f"  长度: {len(segment)}字符")
        print(f"  内容预览: {segment[:50]}...")
        
        for retry in range(max_retries):
            try:
                # 这里应该调用实际的飞书API
                # 伪代码：feishu_doc.append(doc_token=self.document_id, content=segment)
                time.sleep(0.3)  # 模拟网络延迟
                
                # 模拟API响应
                if len(segment) > 1000 and retry == 0:
                    # 模拟第一次失败（内容太长）
                    raise Exception("Request failed with status code 400")
                
                print(f"✅ 段落 {segment_index + 1} 写入成功")
                return True, f"段落 {segment_index + 1} 写入成功"
                
            except Exception as e:
                error_msg = str(e)
                if retry < max_retries - 1:
                    wait_time = 2  # 重试等待时间
                    print(f"⚠️  段落 {segment_index + 1} 写入失败，{error_msg}")
                    print(f"🔄 第{retry + 1}次重试，等待{wait_time}秒...")
                    time.sleep(wait_time)
                    
                    # 简化内容格式重试
                    if "400" in error_msg:
                        print("🔄 简化内容格式重试...")
                        # 移除复杂格式重试
                        simplified_segment = self.simplify_content(segment)
                        segment = simplified_segment
                else:
                    print(f"❌ 段落 {segment_index + 1} 写入失败，已达到最大重试次数")
                    return False, f"段落 {segment_index + 1} 写入失败: {error_msg}"
        
        return False, "未知错误"
    
    def simplify_content(self, content: str) -> str:
        """
        简化内容格式，提高API兼容性
        
        Args:
            content: 原始内容
            
        Returns:
            简化后的内容
        """
        # 移除复杂的Markdown格式
        simplified = content
        
        # 替换三级标题为加粗文本
        simplified = simplified.replace('### ', '**')
        simplified = simplified.replace('\n###', '\n**')
        
        # 移除代码块标记
        simplified = simplified.replace('```', '')
        
        # 确保每行不要太长
        lines = simplified.split('\n')
        simplified_lines = []
        for line in lines:
            if len(line) > 100:
                # 长行分割
                words = line.split()
                current_line = []
                current_length = 0
                for word in words:
                    if current_length + len(word) + 1 > 100:
                        simplified_lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)
                    else:
                        current_line.append(word)
                        current_length += len(word) + 1
                if current_line:
                    simplified_lines.append(' '.join(current_line))
            else:
                simplified_lines.append(line)
        
        return '\n'.join(simplified_lines)
    
    def append_all_segments(self, wait_between_segments: int = 1) -> Dict:
        """
        追加所有内容段落
        
        Args:
            wait_between_segments: 段落间等待秒数
            
        Returns:
            执行结果统计
        """
        if not self.content_segments:
            return {"success": False, "message": "没有内容段落需要写入"}
        
        print(f"🚀 开始写入所有段落，共{len(self.content_segments)}个")
        
        results = {
            "total_segments": len(self.content_segments),
            "successful_segments": 0,
            "failed_segments": 0,
            "failed_details": []
        }
        
        for i, segment in enumerate(self.content_segments):
            success, message = self.append_segment(segment, i)
            
            if success:
                results["successful_segments"] += 1
            else:
                results["failed_segments"] += 1
                results["failed_details"].append({
                    "segment_index": i,
                    "error": message
                })
            
            # 段落间等待
            if i < len(self.content_segments) - 1:
                print(f"⏳ 等待{wait_between_segments}秒后继续...")
                time.sleep(wait_between_segments)
        
        # 生成总结报告
        success_rate = (results["successful_segments"] / results["total_segments"]) * 100
        results["success_rate"] = round(success_rate, 2)
        
        print("\n" + "="*50)
        print("📊 执行结果总结")
        print("="*50)
        print(f"📋 总段落数: {results['total_segments']}")
        print(f"✅ 成功段落: {results['successful_segments']}")
        print(f"❌ 失败段落: {results['failed_segments']}")
        print(f"📈 成功率: {results['success_rate']}%")
        
        if results['failed_details']:
            print("\n⚠️  失败详情:")
            for detail in results['failed_details']:
                print(f"  段落{detail['segment_index']+1}: {detail['error']}")
        
        if results['success_rate'] >= 90:
            print("\n🎉 文档创建基本成功，可以手动补充失败段落")
        elif results['success_rate'] >= 50:
            print("\n⚠️  文档创建部分成功，建议检查失败段落")
        else:
            print("\n❌ 文档创建失败较多，建议重新尝试")
        
        return results
    
    def verify_document(self) -> Tuple[bool, str]:
        """
        验证文档完整性
        
        Returns:
            (验证状态, 消息)
        """
        if not self.document_id:
            return False, "文档ID未设置"
        
        print("🔍 验证文档完整性...")
        
        try:
            # 这里应该调用实际的飞书API读取文档
            # 伪代码：feishu_doc.read(doc_token=self.document_id)
            time.sleep(0.5)  # 模拟网络延迟
            
            # 模拟验证结果
            print("✅ 文档验证完成")
            print(f"🔗 文档链接: {self.document_url}")
            
            return True, f"文档验证完成，链接: {self.document_url}"
            
        except Exception as e:
            error_msg = f"文档验证失败: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def create_complete_document(self, full_content: str) -> Dict:
        """
        完整流程：创建文档并填充内容
        
        Args:
            full_content: 完整内容
            
        Returns:
            完整执行结果
        """
        print("="*50)
        print("🚀 开始创建飞书文档完整流程")
        print("="*50)
        
        # 步骤1：创建文档
        success, message = self.create_document()
        if not success:
            return {"success": False, "message": message, "step": "create_document"}
        
        # 步骤2：等待初始化
        self.wait_for_initialization()
        
        # 步骤3：分割内容
        segments = self.split_content(full_content)
        
        # 步骤4：追加所有段落
        append_results = self.append_all_segments()
        
        # 步骤5：验证文档
        verify_success, verify_message = self.verify_document()
        
        # 整合结果
        final_result = {
            "success": append_results["success_rate"] >= 80 and verify_success,
            "document_id": self.document_id,
            "document_url": self.document_url,
            "append_results": append_results,
            "verify_success": verify_success,
            "verify_message": verify_message,
            "total_steps": 5,
            "completed_steps": 5
        }
        
        print("\n" + "="*50)
        print("🎯 流程完成总结")
        print("="*50)
        print(f"📄 文档标题: {self.title}")
        print(f"📋 文档ID: {self.document_id}")
        print(f"🔗 文档链接: {self.document_url}")
        print(f"📊 内容写入成功率: {append_results['success_rate']}%")
        print(f"✅ 文档验证: {'成功' if verify_success else '失败'}")
        
        if final_result["success"]:
            print("🎉 文档创建流程成功完成！")
        else:
            print("⚠️  文档创建流程部分完成，请检查失败部分")
        
        return final_result


def main():
    """主函数，示例用法"""
    
    # 示例内容
    example_title = "iOS闹钟App PRD文档"
    
    example_content = """# iOS闹钟App PRD文档

## 产品概述

### 产品愿景
打造一款简洁、优雅、功能完善的iOS原生闹钟应用，为用户提供可靠的起床提醒和日程管理工具。

### 目标用户
1. 学生群体 (18-25岁)
   - 需要规律作息
   - 对界面美观度要求高
   - 喜欢个性化设置

2. 上班族 (25-45岁)
   - 需要准时起床
   - 重视可靠性和稳定性
   - 需要工作日/周末不同设置

3. 中老年用户 (45岁以上)
   - 需要大字体显示
   - 操作简单直观
   - 铃声清晰响亮

### 核心价值主张
- 可靠性：100%准时响铃，绝不漏闹
- 简洁性：界面直观，3步完成闹钟设置
- 个性化：丰富的铃声和主题选择
- 智能化：智能跳过节假日，自动调整

## 核心功能需求

### 基础功能模块
1. 闹钟设置与管理
2. 重复周期设置
3. 贪睡功能
4. 铃声系统

### 高级功能模块
1. 主题与个性化
2. 智能功能
3. 快捷操作

### 辅助功能
- 震动模式
- 无障碍支持
- 语音报时

## 技术实现方案

### 技术栈
- 开发语言：Swift 6.0+
- UI框架：SwiftUI
- 架构模式：MVVM + Combine
- 最低支持：iOS 18+

### 核心组件
- 本地通知系统
- 数据持久化
- 音频播放系统

## 项目时间规划

### 开发阶段（9周）
- 阶段一：基础框架（2周）
- 阶段二：核心功能（3周）
- 阶段三：高级功能（2周）
- 阶段四：测试优化（2周）

### 里程碑
1. M1：基础框架完成
2. M2：核心功能完成
3. M3：高级功能完成
4. M4：准备上架

## 成功指标

### 产品指标
- App Store评分 > 4.5星
- 日活跃用户 > 10,000
- 7日留存率 > 40%
- 崩溃率 < 0.1%

## 风险与应对

### 技术风险
- 风险：iOS通知限制
- 应对：精确触发、后台任务

### 产品风险
- 风险：与系统闹钟重叠
- 应对：突出个性化、强化智能

### 市场风险
- 风险：竞争激烈
- 应对：专注iOS优化、口碑推荐

## 后续计划

### 版本规划
- v1.0：基础闹钟功能
- v1.1：睡眠分析统计
- v1.2：健康数据集成
- v2.0：社交智能场景

---
文档创建时间：2026年3月20日
产品经理：OpenClaw助手"""
    
    # 创建文档
    creator = FeishuDocCreator(example_title)
    result = creator.create_complete_document(example_content)
    
    # 输出结果
    print("\n" + "="*50)
    print("📋 最终结果")
    print("="*50)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result


if __name__ == "__main__":
    main()