# Batch Issue Reproduction Design

**Date:** 2026-06-14

## Goal

为一批指定的 `langchain`、`crewai` 和现有 `codex` issue 生成独立、可审计、尽量可运行的复现目录，并严格遵循仓库 [prompt.md](/Users/guoyiheng/Documents/大学/UROP%20SUMMER/urop_agent_bug_reproduce/prompt.md) 规定的两阶段流程。

## Scope

本次范围包含：

- `langchain-ai/langchain` issues: `11408`, `12077`, `17352`, `19699`, `21482`
- `crewAIInc/crewAI` issues: `3821`, `3843`, `3873`, `3889`, `3915`, `3925`
- `codex/` 目录下已有 issue 复现目录的重做

不包含：

- 对上游项目提交修复
- 自动申请或填入任何真实 API key
- 构建超出复现所需的额外测试框架

## Constraints

- 必须先执行阶段 A，再执行阶段 B；禁止跳过 `normalized_issue_summary.md`
- 阶段 B 只能基于阶段 A 的规范化结果生成
- 对需要 LLM API key 的场景，只保留空白占位和说明
- 不编造缺失信息；缺失条件必须在摘要和 README 中明确标注
- 尽量沿用仓库现有目录命名与 README 风格

## Output Structure

每个 issue 目录默认包含：

- `normalized_issue_summary.md`
- `README.md`
- `reproduce.py`

按需补充：

- `requirements.txt`
- `requirements-*.txt`
- `package.json`
- 其他运行所需最小依赖声明文件

目录命名规则：

- `langchain-issue-<id>`
- `crewai-issue-<id>`
- `codex/codex-issue-<id>` 保持原目录位置，重写内部内容

## Reproduction Strategy

### Stage A

对每个 issue 提取并规范化以下关键信息：

- 项目、issue URL、标题
- 预期行为、实际行为、主错误
- 版本、运行时、系统、provider、外部服务依赖
- 最小代码片段、复现步骤、错误信息
- `minimal` 或 `real_dependency` 预判

结果保存为 `normalized_issue_summary.md`，严格遵循 [prompt.md](/Users/guoyiheng/Documents/大学/UROP%20SUMMER/urop_agent_bug_reproduce/prompt.md) 的固定字段结构。

### Stage B

基于阶段 A 摘要生成最小复现：

- `minimal`：优先本地逻辑、协议、参数处理或状态机级别复现
- `real_dependency`：使用真实库或真实调用路径，但尽量减少外部环境需求

README 必须包含：

- 复现类型说明
- 环境准备
- 安装命令
- 运行命令
- 预期结果
- 实际结果
- 缺失信息与限制

## Codex Rebuild Rules

`codex/` 下已有 issue 不沿用旧内容，而是按本次统一标准重做：

- 补齐阶段 A 摘要
- 重写 README 为明确的 step-by-step 复现说明
- 重写主脚本以最小方式触发问题
- 若依赖 API key，环境变量值留空

## Quality Bar

- 每个目录应该能让阅读者一眼看出“这是什么 bug、怎么运行、会看到什么”
- `reproduce.py` 只保留触发 bug 所需逻辑
- 不把未验证的推测写成事实
- 对无法完全可靠复现的 issue，明确说明“最小近似复现”的边界

## Risks

- 某些 issue 页面或评论中的关键信息可能缺失
- 某些 bug 高度依赖上游在线服务、账号权限或特定历史版本
- 批量处理 issue 时需要保证目录结构和文档格式一致，避免个别目录偏离仓库标准

## Execution Notes

优先顺序：

1. 读取现有仓库模式与 `codex/` 目录内容
2. 批量抓取 issue 信息并产出阶段 A 摘要
3. 按 issue 逐个生成阶段 B 复现目录
4. 运行最小验证命令，确认脚本至少可执行到预期阶段
