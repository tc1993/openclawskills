---
name: create-feishu-doc
description: "Use this skill whenever the user wants to create, generate, write to, or organize content into a Feishu document. Triggers include: any mention of 'Feishu doc', 'Feishu document', or requests to produce structured or complete documents within Feishu. This applies to scenarios requiring fully formatted documents, including but not limited to: technical documentation, PRDs, project plans, reports, notes, articles, or novels. Use this skill whenever content needs to be compiled, structured, and delivered as a Feishu document."
---

# Universal Feishu Document Creation Skill

## Overview

This skill provides universal Feishu document creation functionality, creating documents based on any content provided by the user. It supports various document types: novels, technical documentation, project plans, reports, notes, articles, etc. 

**⚠️ 重要提示：由于飞书文档API对单次写入操作的长度有限制，写入飞书文档时必须使用分段写入策略！**

### 为什么必须分段写入？
1. **API限制**：飞书文档API对单次请求的内容长度有严格限制
2. **稳定性**：长内容一次性写入容易导致超时或失败
3. **可靠性**：分段写入可以确保即使部分失败也能保留已写入内容
4. **性能**：分段写入可以更好地处理网络波动和服务器响应

### 分段写入原则：
- **每段300-500字**：避免单次写入内容过长
- **按逻辑分段**：按章节、段落或主题自然分割
- **保持完整性**：不在句子中间切断内容
- **适当等待**：段与段之间等待1-2秒，确保文档稳定

## Core Workflow

### Step 1: Create Blank Document
1. Call the `feishu_doc` tool's `create` operation
2. Pass in the document title and initial content (usually just the title)
3. Record the returned `document_id` and document URL

### Step 2: Wait for Document Initialization
1. Wait 2 seconds to ensure the document is fully initialized on the Feishu server
2. This is a critical step to avoid write operations before the document is ready

### Step 3: Append Content in Batches (必须分段写入！)
**重要：这是整个流程中最关键的步骤，必须严格遵守分段写入原则！**

1. **内容分段策略**：
   - 将完整内容按逻辑分割成多个小段
   - **每段建议300-500字**，绝对不能超过1000字
   - 按自然段落、章节或主题进行分割
   - 避免在句子中间切断内容

2. **分段写入操作**：
   - 对每个内容段调用 `feishu_doc` 工具的 `append` 操作
   - 使用上一步获取的 `document_id`
   - **每段写入后等待1-2秒**，确保文档稳定

3. **分段建议**：
   - 小说：按章节分段
   - 技术文档：按主题或小节分段
   - 报告：按章节或主要部分分段
   - 长文章：按逻辑段落分段

**⚠️ 警告：不要尝试一次性写入过长内容，这会导致API失败！**

### Step 4: Error Handling and Retry
1. If the `append` operation fails (returns 400 error):
   - Wait 2 seconds and retry
   - Maximum of 3 retries
   - If still failing, record the error and continue with the next segment
2. When retrying, consider:
   - Reducing content length
   - Simplifying format (removing complex Markdown)
   - Checking network connection

## Best Practices

### 内容分段策略 (必须遵守！)
- **小段优先原则**：每段300-500字，避免API限制
- **逻辑完整性**：按章节或主题分段，不在句子中间切断
- **格式简化**：使用飞书支持的简单格式（纯文本、简单列表）
- **进度跟踪**：记录已写入段数和总段数

### 分段写入检查清单：
1. ✅ 内容是否已按逻辑分段？
2. ✅ 每段是否不超过500字？
3. ✅ 是否避免了在句子中间切断？
4. ✅ 段与段之间是否有适当等待时间？
5. ✅ 是否记录了写入进度？

### Error Handling Strategy
- **Immediate retry**: Wait 2 seconds and retry after first failure
- **Graceful degradation**: Simplify content format when retry fails
- **Skip and continue**: Failure of a single segment doesn't affect overall progress
- **Final verification**: Read the document to verify completeness after all segments are written

### Performance Optimization
- **Parallel writing**: Can process multiple documents simultaneously
- **Batch operations**: Similar content can be merged and written together
- **Cache utilization**: Repeated content can be cached to avoid regeneration
- **Progress saving**: Supports resumable transmission, records completed segments

## Usage Examples

### Example 1: Creating Novel Chapter Documents
```python
# Pseudo-code example
1. create_doc("Sword Coming Chapter 1")
2. wait(2)
3. append_content("Section 1: Town Youth...")
4. wait(1)
5. append_content("Section 2: Market Adventure...")
6. wait(1)
7. append_content("Section 3: Mysterious Prophecy...")
8. Verify document completeness
```

### Example 2: Creating Technical Documentation
```python
# Pseudo-code example
1. create_doc("Python Programming Guide")
2. wait(2)
3. append_content("Chapter 1: Python Basics...")
4. wait(1)
5. append_content("Chapter 2: Functions and Modules...")
6. wait(1)
7. append_content("Chapter 3: Object-Oriented Programming...")
8. Verify document completeness
```

### Example 3: Universal Document Creation Process
```python
# Pseudo-code example
1. Get document title and content from user input
2. Create blank document
3. Wait for document initialization
4. Intelligently segment the content
5. Write all segments in batches
6. Handle errors and retries
7. Verify document completeness
8. Return document link and creation results
```

## Common Problem Solving

### 问题1: API返回400错误
**原因**：内容过长或格式不支持
**解决方案**：
1. **减少单次写入内容长度**（这是最常见原因！）
2. 移除复杂的Markdown格式
3. 使用纯文本格式重试

### 分段写入失败排查：
1. **检查分段大小**：是否超过500字？
2. **检查等待时间**：段与段之间是否等待了足够时间？
3. **检查内容格式**：是否包含飞书不支持的格式？
4. **检查网络连接**：网络是否稳定？

### Problem 2: Document Content Loss
**Cause**: Write operation unsuccessful but not detected
**Solution**:
1. Verify return status after each write
2. Record write status for each segment
3. Finally read the document to verify completeness

### Problem 3: Slow Write Speed
**Cause**: Wait time too long or network latency
**Solution**:
1. Optimize wait time (1-2 seconds is usually sufficient)
2. Consider parallel writing of multiple segments
3. Use local cache to reduce repeated generation

## 重要提醒

### 分段写入是必须的！
**每次使用此技能时，请务必记住：**
1. 飞书文档API有严格的单次写入长度限制
2. 长内容必须分段写入（每段300-500字）
3. 段与段之间需要适当等待（1-2秒）
4. 按逻辑分段，保持内容完整性

### references/feishu_api_guide.md
飞书API使用指南，包含常见错误代码和解决方案。

**Skill Features**:
- **High versatility**: Supports various types of document content creation
- **Intelligent segmentation**: Automatically segments intelligently based on content type
- **Error handling**: Intelligent retry and format simplification mechanisms
- **Progress tracking**: Real-time display of write progress and success rate
- **Completeness verification**: Verify document completeness after creation
- **User-friendly**: Simple interface and detailed status reports