# 项目二：本地 AI Agent 工作流搭建与应用

> 个人项目｜Windows、Cline Desktop、llama.cpp、GGUF、PowerShell、Git

## 项目目标与个人工作

在已有的[本地模型推理环境](model-deployment.md)上，将 Cline Desktop 连接到本机 OpenAI 兼容接口，验证从用户任务、模型响应到 Cline 工具执行的完整链路。重点是文件读写、终端运行、简单代码任务、人工审批，以及出错后的可复核记录。

本人配置了本机模型连接与测试工作区，设计了隔离测试任务，记录了文件编码、PowerShell 引号与上下文参数引发的问题，并按[部署后验收报告](../tests/agent-acceptance-report.md)重新核对已有结论。本文将历史截图、独立文件检查和本轮端到端验收分别标明。

| 简历中的能力描述 | 当前可指向的材料与限度 |
| --- | --- |
| Cline 与 llama.cpp 的本地架构 | 配置步骤、Codex 直接复核的 `/health`／`/v1/models` 输出，以及本轮 Cline 两轮短对话 |
| 文件读取、创建及代码辅助 | 历史 Cline 截图、现存测试文件及旧项目五项测试；本轮文件创建和精确修改未通过，多文件 README 一致性仍待核对 |
| Token 超限排查与配置调整 | 参数区别、故障现象和排查方法有记录；尚无“长任务问题已修复”的通过证据 |
| 可重复使用的工作流 | 有小规模历史任务记录与现存文件，可按验收报告复测；任务恢复、安全审批和复杂任务可靠性仍按逐项状态表述 |

## 架构与工作流程

![本地 AI Agent 架构示意：用户任务经 Cline、llama-server 和 GGUF 模型，再进入工具与工作区](../assets/diagrams/agent-architecture.png)

![本地 AI Agent 工作流程示意：任务、推理、工具请求、审批与结果](../assets/diagrams/agent-workflow.png)

> 这两张图是用户提供的架构与可能流程示意。模型通常在服务启动阶段加载，并非每次 API 请求都重新加载；工具执行、人工审批及 Git 写入由具体任务和客户端设置决定。图中的 Git 提交／恢复及审批节点不代表本轮已全部验收通过，实际状态以[11 项验收报告](../tests/agent-acceptance-report.md)为准。

### 安全边界

模型返回 `tool_calls` 只是工具执行请求；必须继续查看 Cline 的工具调用、用户审批、工具返回和磁盘产物，才能确认工作流完成。任务约束与 Git 都不是操作系统沙箱。推理接口指向 `127.0.0.1`；Cline 的更新、外部工具或用户主动上传行为须分别核查，不能概括为“所有数据绝不出站”。

## 配置与最小复现

1. 在 Windows 上启动已有的 llama.cpp 服务，并确认它只监听预期的本机接口。运行器、模型与量化文件由使用者根据各自来源和许可获取；本仓库不分发权重或二进制程序。
2. 在 PowerShell 中检查服务和模型 ID：

   ```powershell
   (Invoke-RestMethod 'http://127.0.0.1:8080/health').status
   (Invoke-RestMethod 'http://127.0.0.1:8080/v1/models').data | Select-Object -ExpandProperty id
   ```

3. 在 Cline Desktop 选择自定义 OpenAI 兼容提供商，Base URL 使用 `http://127.0.0.1:8080/v1`，Model ID 使用 `/v1/models` 的实际返回值。若服务没有启用认证，客户端要求填写的占位字符串不构成安全验证。
4. 在隔离工作区先测试无副作用对话和小文件任务，保留展开的工具详情；人工审阅命令，再执行。完整的 11 项流程与判定标准见[验收报告](../tests/agent-acceptance-report.md)。

服务端 `--ctx-size`、Cline 的 Context Window 和 Max Output Tokens 是不同设置。配置值不能证明长上下文不截断或长任务可恢复。遇到 Token 超限，应同时检查输入、历史、工具返回、输出上限和服务端日志，并分阶段复测。

## 已有证据及其限度

| 证据 | 可支持的结论 | 不能据此宣称 |
| --- | --- | --- |
| [本地 API 工具调用历史截图](../assets/screenshots/agent-workflow/historical-tool-call.jpg)与[本轮 IQ2_M 补测](../tests/agent-acceptance-report.md) | 历史模型和本轮 IQ2_M 分别返回了结构化 `say_hello` 调用请求 | Cline 已执行任意工具 |
| [Cline 文件创建总结](../assets/screenshots/agent-workflow/historical-cline-write.jpg)与本机文件 | 历史任务中报告了文件工具调用，旧文件目前存在且可读 | 所有文件操作均稳定或无审批风险 |
| [计算器任务总结](../assets/screenshots/agent-workflow/historical-cline-calculator.jpg)与[主程序输出](../assets/screenshots/agent-workflow/historical-calculator-output.jpg) | 小规模多文件 Python 项目曾运行，旧项目五项单元测试本轮独立重跑为 `OK` | README 一致性、复杂项目或长任务已通过 |
| [文件整理建议](../assets/screenshots/agent-workflow/historical-file-organizer-plan.jpg)与[移动总结](../assets/screenshots/agent-workflow/historical-file-organizer-result.jpg) | 历史截图呈现先建议后移动，当前可见相应分类目录 | 本轮审批、哈希一致性或任意批量整理已通过 |

上述六张图片均为用户此前的真实截图，且只截取了局部界面；它们是**历史记录**。[本轮 Cline 短对话截图](../assets/screenshots/agent-workflow/recheck-03-conversation.jpg)显示 IQ2_M 的两轮回复为 `19` 与 `38`。本轮的其他 Cline 任务和文件／Git 产物以[验收报告](../tests/agent-acceptance-report.md)中的逐项状态为准。`2026-10-22 13:20:55 +08:00` 的 `/health` 与 `/v1/models` 已由 Codex 在获准的本机只读连接中直接复核。

## 故障排查与改进

- **编码与引号**：旧 `hello.py` 曾出现非 UTF-8 字节、字面量 `\n` 和未闭合字符串。先读取实际字节与文件内容，再用文件工具写入 UTF-8，运行 `python -m py_compile` 和主程序；不要用多层 `python -c` 引号拼接生成源码。
- **仅有成功总结**：展开 Cline 工具详情并在独立终端核对文件、退出码和输出；模型生成的文字与实际执行分开记录。
- **本轮失败案例**：一次文件创建任务要求写入隔离子目录，但 Cline 用 PowerShell 相对路径写到了上级目录，且丢失字符串引号；它仍给出“成功”总结。独立运行发现 `NameError`。限定重试又在请求阶段触发 `16448 > 16384` 的上下文错误，没有生成目标文件，详见[验收记录](../tests/agent-acceptance-report.md)。
- **Git 差异为空**：未跟踪文件不会出现在普通 `git diff` 中；测试仓库应先建立基线提交，再修改已跟踪文件，检查差异和第二次提交。
- **长任务中断**：把阶段、产物和完成状态写入磁盘；在新会话读取记录后继续。该流程在本轮验收通过前仅是待验证方法。

## 适用范围与参考

本项目展示本机 Agent 的配置、基础工具链和可复核测试方法。它不证明长期稳定性、工作区外访问被系统阻断、自动故障恢复，或所有外部网络行为被禁止。危险操作保持人工审批；不在正式项目或私人文件上做破坏性测试。

- [Cline 官方文档](https://docs.cline.bot/)
- [llama.cpp Server 文档](https://github.com/ggml-org/llama.cpp/tree/master/tools/server)
- [llama.cpp Function Calling 文档](https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md)
