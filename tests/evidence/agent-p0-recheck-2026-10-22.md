# P0：Cline 文件任务复验与受限修复（2026-10-22）

> 设备：Windows 本机；Cline Desktop v0.0.45，模型 Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ2_M；本地 llama.cpp 接口。Cline GUI 的真实任务由 UI 自动化触发，独立验证/修复通过 Remote Desktop Commander 在宿主机执行。**两者不混同**。

## 范围与防护

- Cline 工作区：`D:\AI-Workspace\Sandbox`，本轮唯一目标文件位于 `Agent-P0-2026-10-22\probe.py`。不改正式项目、原有失败样例或模型服务配置。
- 每个 Cline 测试使用新会话，提示词指定**绝对路径**、原生文件工具、不得用终端生成文件。要求 UTF-8 无 BOM，源码精确匹配且以 **一个 LF** 结束。
- 通过标准：Cline 工具调用与文件存在只是中间条件；还须独立检查实际路径、逐字节内容以及 Python 运行结果。

## 第一轮：文件创建

| 检查 | 实际结果 |
| --- | --- |
| Cline 创建的目标 | 指定绝对路径下的 `probe.py` 确实存在；GUI 显示创建及读取工具调用 |
| 实际文件 | `print("AGENT_P0_OK")`；20 字节；UTF-8 无 BOM，**无末尾 LF** |
| SHA-256 | `2E82FD432ECC7ADD5BED8E0C1B6B6B85F276EA36C1FFEFE9138E80CC3C03D320` |
| 独立运行 | `python -B probe.py` 输出 `AGENT_P0_OK`，退出码 0 |
| 判定 | 绝对路径与 Python 运行通过；**精确字节要求未通过** |

Cline 的成功总结与独立字节校验不一致，不据此更新既有第 04 项为完全通过。

## 第二轮：读取与编辑

- Cline 新会话先请求读取既有 `probe.py`，再使用文件编辑工具将代码改为 `print("AGENT_P0_EDIT_OK")`，要求保留一个 LF。
- 独立读取到 25 字节源码 `print("AGENT_P0_EDIT_OK")`，末尾仍无 LF；SHA-256：`1FA9DE4B8AD84409980873BBE44E8A7774CC9E4A74498E669F938020911A14CF`。
- GUI 期间出现多次重复调用读取工具；实际已编辑代码正文，但**未满足精确内容**。因此既有第 05 项仍为“需修正”。
- 两轮文件工具未能实现最终精确字节，不应宣称 Cline 已解决所有文件编码/换行问题。

## 独立防护工具与实际修复

新增 [`scripts/agent-file-guard.py`](../../scripts/agent-file-guard.py)：只接受隔离工作区范围内现存的 `.py` 文件；默认只读校验。启用 `--normalize-newline` 时，只有在**源码正文与预期完全一致，仅 BOM/末尾换行不同**的情况下才会写回标准的 UTF-8 无 BOM、一个 LF；否则拒绝覆盖。

```powershell
$root = 'D:\AI-Workspace\Sandbox\Agent-P0-2026-10-22'
$file = Join-Path $root 'probe.py'
$guard = '.\scripts\agent-file-guard.py'

# 在本仓库根目录执行：
python -B $guard --root $root --file $file --expected-print AGENT_P0_EDIT_OK
# 检查失败：退出码 1，实际 25 字节，预期 26 字节

python -B $guard --root $root --file $file --expected-print AGENT_P0_EDIT_OK --normalize-newline
# 受限修复通过：退出码 0

python -B $guard --root $root --file $file --expected-print AGENT_P0_EDIT_OK
python -B $file
# 二次检查退出码 0；Python 输出 AGENT_P0_EDIT_OK
```

| 验证 | 实际结果 |
| --- | --- |
| 只读初检 | 失败（exit 1），实际 25 字节 |
| 受限换行规范化 | 成功（exit 0），26 字节 |
| 修复后 SHA-256 | `7D0E9B336C6B934D47FD3ABCB4D687DC1497A8D4B8842AB6F7EDAA5787C02238` |
| 修复后二次校验 | `after_exact=true`，exit 0 |
| 修复后独立 Python 运行 | `AGENT_P0_EDIT_OK`，exit 0 |
| 错误预期内容 + 修复参数 | 拒绝覆盖，exit 1；文件 SHA 不变 |
| 工作区外文件 + 修复参数 | 拒绝访问，exit 2；文件 SHA 不变 |

**归属声明：** 本次规范化命令由 Remote Desktop Commander 独立执行，**不是 Cline 自主调用修复脚本**。Cline 原生文件创建/编辑在严格字节标准下仍未通过；这里验证的是可重复的外部质量门禁和受限修复流程，不是 Agent 自动化整体可靠性。

## 回归测试

在仓库根目录执行 `python -B -m unittest discover -s tests -p 'test_agent_file_guard.py' -v`，2026-10-22 本机实测 **5/5 通过**、退出码 0；覆盖精确文件、缺少 LF、内容不匹配拒绝覆盖、工作区外路径拒绝访问、UTF-8 BOM 规范化。`git diff --check` 同次检查退出码 0。

## 后续验收门槛

1. Cline 在全新隔离任务中先完成文件创建、读取与修改；独立工具验证文件绝对路径、预期文本和末尾 LF。不能只看聊天总结。
2. 如果 Cline 未满足字节精度，可在**人工核对目标路径与源码正文后**调用本工具修复；保留“Agent 未通过 / 独立修复通过”两个状态。
3. 不将此复测自动升级为多文件、Git、安全审批或长任务恢复的验收证明；相应项目仍按[11 项报告](../agent-acceptance-report.md)判定。

注意：Windows PowerShell 5.1 向 Python 传递带嵌套双引号的 `--expected-line` 可能改变参数内容，本报告使用无内嵌引号的 `--expected-print`，由工具生成预期源码，避免命令行引号被吞掉。
