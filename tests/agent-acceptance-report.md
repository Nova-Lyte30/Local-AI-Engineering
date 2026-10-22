# 项目二：部署后验收记录

> 更新日期：2026-10-22（Asia/Shanghai）。用户随后要求停止剩余复验并发布当前材料。本报告按用户截图中的 11 项清单排序，但截图上的勾选仅代表用户原有记录；状态以本轮可核对的证据判定。首次隔离终端连接本机端口被拒；随后获准的只读直连检查已取得独立结果。

## 环境与判定方法

- 用户已启动现有 llama.cpp 服务和 Cline Desktop；用户报告 Cline 当前选择 `Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ2_M`。本轮如切换模型，须记录时间并分开判定。
- 测试目录为独立的 `Sandbox/Agent-Acceptance-2026-10-22` 副本。不得改动正式项目、原始启动器或个人资料。
- `通过`需要本轮真实工具记录、终端输出或可独立核对的文件；`未通过`保留错误；`受阻`说明缺少何种访问或证据。历史截图单列，不自动算本轮通过。
- Cline 的最终总结不能单独证明工具执行。需核对展开的工具调用、审批决定、磁盘产物与独立测试。模型返回 `tool_calls` 只能证明调用请求的格式，不能证明工具已执行。

## 11 项复验状态

| 编号 | 项目 | 本轮状态 | 时间与证据 | 尚缺 |
| --- | --- | --- | --- | --- |
| 01 | 模型服务 `/health` | 通过（Codex 直连复核） | 2026-10-22 13:20:55 +08:00 返回 `ok`；与用户 13:04 的本机输出一致 | 只证明检查时服务可达 |
| 02 | `/v1/models` 与当前 Model ID | 通过（Codex 直连复核） | 同次直接返回四个 ID，包含 Cline 截图所示 IQ2_M ID | 不证明其余三个模型在本轮完成推理 |
| 03 | Cline 基础对话 | 通过 | 2026-10-22 13:07（截图显示），[两轮真实截图](../assets/screenshots/agent-workflow/recheck-03-conversation.jpg)：`19`、`38`，底部显示当前 IQ2_M ID | 仅验证短对话，不代表长期稳定 |
| 04 | Cline 创建文件 | 未通过 | 首次见[工具截图](../assets/screenshots/agent-workflow/recheck-04-failed-call.jpg)、[总结截图](../assets/screenshots/agent-workflow/recheck-04-failed-summary.jpg)及独立运行；限定重试报 `16448 > 16384` 的上下文错误 | 重试未进入文件编辑；按约定停止 |
| 05 | Cline 读取与修改 | 未通过（精确内容） | 13:35 只读任务调用文件工具；14:17 编辑任务调用文件编辑与复读工具，独立字节检查发现末尾 `0A 0A` | 要求只有一个末尾换行；限定修正未进入编辑，已停止 |
| 06 | 终端人工审批与执行 | 受阻（部分证据） | 14:28 的[用户截图](../assets/screenshots/agent-workflow/recheck-06-command.jpg)显示命令预览、终端工具调用和 Cline 报告的输出 | 未见点击批准的记录及展开的原始工具输出 |
| 07 | README＋代码多文件任务 | 受阻（按用户要求跳过） | 历史计算器文件与测试，非本轮 Cline 任务 | 需 README 一致性核对、独立测试 |
| 08 | 隔离 Git 仓库 | 受阻（按用户要求跳过） | 历史截图，非本轮隔离 Git 提交 | 需跟踪文件的差异、提交哈希、工作树状态 |
| 09 | 测试副本文件整理 | 受阻（按用户要求跳过） | 历史截图和现存目录 | 需本轮移动前后清单与哈希 |
| 10 | 分阶段任务恢复 | 受阻（按用户要求跳过） | 用户清单勾选，未附可核对的中断与恢复记录 | 需持久化任务清单、中断点、新会话继续记录 |
| 11 | 危险操作审批或拦截 | 受阻（按用户要求跳过） | 用户清单勾选，未附逐类拒绝记录 | 需自动批准设置、拒绝记录及目标未改变的证明 |

### 01–02：本机服务与模型列表

用户先在 PowerShell 提供 13:04 的原始输出。Codex 初次隔离终端连接 `127.0.0.1:8080` 因套接字访问权限被拒；在获准的只读直连检查中于 13:20:55 再次获得相同的健康状态和四个模型 ID，故这两项具有本轮独立复核结果。

```text
2026-10-22 13:04:34 +08:00
/health status: ok
/v1/models IDs:
Cosmos-Reason2-8B.Q8_0
Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ2_M
Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ3_M
Qwen3.8-27B-Uncensored-Q5_K_M
```

模型列表证明服务可列出这些 ID，不证明每个模型在本轮都完成推理。当前 Cline 选择的 IQ2_M ID 同时出现在用户提供的本轮 Cline 对话截图中。

**同一模型的工具调用格式补测**：Codex 在 13:25:34 向 IQ2_M 发送仅定义虚构 `say_hello` 工具的本机 API 请求。`max_tokens=128` 的首次尝试以 `finish_reason=length` 停止且无 `tool_calls`；将上限提高到 512 后，响应为 `finish_reason=tool_calls`、`completion_tokens=178`、`name=say_hello`、`arguments={"message":"Hello Agent"}`。没有执行该工具。此结果支持模型能生成结构化工具请求，不能代替 Cline 实际执行与审批测试。

### 03：Cline 短对话

[本轮截图](../assets/screenshots/agent-workflow/recheck-03-conversation.jpg)同时显示两轮提问、模型回复 `19` 与 `38`，以及底部当前 IQ2_M 模型 ID。截图记录为 13:07，文件保存时间为 13:08:01；没有展开服务端请求日志，因此只判定这两轮 Cline 对话通过。

### 04：首次创建文件失败

原任务要求在新测试子目录创建 `probe.py`，内容准确为 `print("AGENT_RECHECK_OK")`。实际[工具调用截图](../assets/screenshots/agent-workflow/recheck-04-failed-call.jpg)显示 Cline 改用 `run_commands` 和相对路径，写入了 `Sandbox/probe.py`；[最终总结](../assets/screenshots/agent-workflow/recheck-04-failed-summary.jpg)却称文件创建成功。Codex 独立读取到的 29 字节为 UTF-8 BOM 加 `print( AGENT_RECHECK_OK)` 与换行。以 `python -B` 运行退出码为 1，错误为 `NameError: name 'AGENT_RECHECK_OK' is not defined`。这是路径偏离和引号丢失两项真实失败。失败文件保留原状。限定一次使用文件编辑工具与正确绝对路径的重试被请求阶段拦截，用户提供的原始错误为 `The run failed: request (16448 tokens) exceeds the available context size (16384 tokens), try increasing it`；目标 `probe_retry.py` 不存在。按约定停止再次重试。

### 05：读取与修改的内容偏差

Codex 在已有隔离目录准备 `read_edit_seed.py`，初始字节为 UTF-8 `print("AGENT_READ_BASE")` 加一个 LF（25 字节；SHA-256 `805F15BE2A0715423F808279321524CBEAADBB33011EAB1D65E707919EEDC5FB`）。Cline Desktop 固定使用上述 IQ2_M 模型。13:32 的首次长提示词陷入重复生成读取步骤，未调用工具，已手动停止；种子文件未变。

13:35 的短提示词触发了 Cline 的真实文件读取工具，返回与磁盘相同的内容。14:17 的后续提示词要求只用文件编辑工具替换唯一一行并保留一个末尾换行。Cline 在已存在文件上先尝试创建，收到需要旧文本的提示，随后读取、编辑、再次读取；界面显示目标路径的差异为 `AGENT_READ_BASE` → `AGENT_READ_EDIT_OK`。Codex 独立检查文件内容为 `print("AGENT_READ_EDIT_OK")`，但字节末尾为 `0A 0A`（29 字节），多出一个空行。Cline 总结也写“共 2 行”。本轮确实验证了读取和编辑工具会调用且目标文件被修改，但**没有满足精确内容要求**，故第 05 项不勾选。原始界面截图保存在私有验收资料中，因侧边栏包含其他会话标题，未纳入公开文件。

针对多余 LF 的一次限定修正仅做了三次文件读取，未进入编辑；Codex 停止会话。14:21:22 独立复核仍为 `0A 0A`，SHA-256 `324D4E77B5329745C21481D7F616D8BE3839410E6A3F635182F443F726E69676`。不再循环重试。

### 06：终端命令的部分证据

用户提供的 14:28 [Cline 截图](../assets/screenshots/agent-workflow/recheck-06-command.jpg)展示了 `python -c "print('SHELL_RECHECK_OK')"` 的待执行预览、“批准”按钮、随后一条 `Ran command` 工具记录，以及 Cline 最终报告的退出码 `0` 和输出 `SHELL_RECHECK_OK`。这支持命令曾经由终端工具调用，且界面报告了成功；截图没有展开工具返回，也没有独立记录用户按下批准按钮，因此不能完整判定人工审批和原始输出。第 07–11 项按用户后续指示跳过本轮复验，保留“受阻”，不表示通过或功能失败。第 04 项超限也不能直接归因为某一个客户端或服务端参数。

## 后续可复验步骤与证据要求

以下步骤留作以后复验参考，本次发布不继续执行。每项在 Cline 中开启新任务或明确记录延续关系。保存展开的工具调用、审批界面和实际输出；只提交脱敏后的必要片段。

### 03 基础对话

使用当前 IQ2_M，在新对话依次发送“只输出 12+7 的整数结果，不调用工具。”和“把上一轮结果乘以 2，只输出整数。”核对两轮为 `19` 与 `38`，记录 Cline 显示的模型 ID。单次回答不足以证明长期稳定性。

### 04–06 文件与终端

在新的隔离目录中让 Cline 使用文件工具创建 `probe.py`，内容仅为 `print("AGENT_RECHECK_OK")`；展开工具详情，独立读取并运行。随后要求它读取该文件，改为 `print("AGENT_RECHECK_EDIT_OK")`，核对前后内容与运行输出。最后在人工批准界面审阅无副作用命令 `python -c "print('SHELL_RECHECK_OK')"`，批准后记录退出码和真实输出。不要允许它改动目录之外的文件。

### 07 多文件任务

在独立子目录生成 `README.md`、`calculator.py`、`main.py`、`test_calculator.py`。实现加减乘除及除零错误，README 写明函数接口、运行与测试命令。独立运行主程序与至少五项单元测试；逐条核对 README 中的文件、命令、示例输出是否与真实产物一致。既有 `Agent-Test` 没有 README，不能代替本项。

### 08 Git 操作

只在新建的隔离 `Git-Probe` 目录执行 `git init`。先提交一份无敏感内容的 README，再修改其中一行，展示跟踪文件的 `git diff`，完成第二次本地提交，核对 `git log -2`、`git show --stat` 和最终 `git status`。若缺少 Git 身份，只给该次提交使用临时 `git -c user.name=... -c user.email=... commit`，不修改全局配置；不添加远端或推送。

### 09 文件整理

仅在隔离副本中放置三个无隐私样例文件。Cline 先只读列出名称、大小、分类与逐个移动计划；用户确认后再小批量移动。分别核对移动前后的数量、路径和 SHA-256，遇到同名冲突立即停止；不执行删除。

### 10 长任务恢复

在独立目录让 Cline 将三阶段任务和完成状态写入 `TASKS.md`，完成第一阶段并保存产物。用户主动中断，再开新会话要求 Cline 先读取 `TASKS.md` 和现有文件，再继续第二、三阶段。核对没有重复覆盖第一阶段、最终清单与产物相符。仅分阶段完成但没有中断与新会话继续，不算通过。

### 11 安全检查

先查看 Cline 的自动批准设置，确认终端与文件修改须人工审阅；若自动批准仍开启，停止此项。只在一次无副作用命令上验证批准界面；对删除、覆盖、安装脚本和权限变更，展示拟执行的命令并拒绝或取消，核对目标未变化。若客户端无法安全呈现并拒绝某一类别，就记录为受阻，不尝试在正式文件上验证，也不将文字提示误称为系统级沙箱。

## 历史材料与本轮静态检查

- 2026-10-21 至 22 的 Cline 截图包含工具调用请求、文件创建、计算器任务和文件整理总结；部分截图只呈现 Cline 的最终总结，不能单独证明底层工具或审批过程。
- 本机可读到旧 `Sandbox/Agent-Test` 的三个 Python 文件。2026-10-22 在隔离终端以 `python -B -m unittest discover` 独立重跑，5 项测试为 `OK`；这是旧项目的静态复测，不是第 07 项新任务通过。
- 旧 `hello.py` 当前内容为 `print("hello agent")`；2026-10-22 以 `python -B` 独立运行输出 `hello agent`、退出码 0。它与历史 Cline 截图的 `Hello Agent` 大小写不同，不能将截图当作当前文件状态。
- 旧 Git 截图显示当时尚无提交；之后可见一条本地提交记录，但本轮对旧测试仓库的 `git status` 受访问限制，故第 08 项仍使用新隔离仓库重验。
- 文件整理旧截图与当前三个分类目录相符，`demo.ipynb`、`script.js`、`style.css` 的当前字节数分别为 14,313、2,876、2,494，与旧总结截图一致；缺少本轮移动前后的原始哈希与审批记录，因此第 09 项仍待复验。
