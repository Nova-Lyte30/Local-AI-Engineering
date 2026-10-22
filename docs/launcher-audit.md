# 原始启动器审计

> 2026-10-21 先进行本机只读审计，随后按用户要求实际运行原始 `start.bat`。原始文件仍在 llama.cpp 安装目录，未复制到本项目；运行结果见[端到端复测](../tests/evidence/start-bat-e2e-2026-10-21.md)。

| 本机文件 | SHA-256 | 审计结论 |
| --- | --- | --- |
| `start.bat` | `80CABE003F2F7C10BBC5A91300B9FD7BA6D46D3806E8BCD218D1E9D365093EB7` | 切换到脚本目录，优先调用 `pwsh`，否则调用 Windows PowerShell，入口指向 `llama-oneclick.ps1`。 |
| `llama-oneclick.ps1` | `1783F8E2312BFB3570F2FB41F11DD88A7E7BF707345043759F053BC190FDCA5C` | 参数包括模型名、上下文、输出长度、温度、Top-P、端口和思考模式；PowerShell 语法解析无错误。 |

PowerShell 脚本会检测 GPU 与内存，扫描模型目录，选择模型和参数档位，生成 router 预设，并用 `--models-dir`、`--models-preset`、`--host 127.0.0.1` 等参数启动 `llama-server`。它的 8 GB 显存自动档位设为 8192 上下文；已有 `launcher.ini` 的 16384 配置会覆盖该自动值。是否成功加载 16384 上下文应看运行日志。

脚本具有实际文件与系统副作用：可能移动根目录的 GGUF、创建硬链接或复制 mmproj、重写 `launcher.ini` 和 `presets.generated.ini`；若找不到 `llama-server`，还有 `winget` 安装及远端安装脚本的分支。最初的隔离加载复核使用[无整理动作示例](../scripts/llama-oneclick.example.ps1)。后续实际运行原始入口前备份了两个 INI 并记录模型目录；本机已有运行器，未进入安装分支，模型文件清单无变化，两个 INI 在测试后恢复原哈希。

## 用户补充的历史截图

用户提供两张[辅助编写交流截图](../assets/screenshots/provenance/cursor-conversation-1.jpg)（[续图](../assets/screenshots/provenance/cursor-conversation-2.jpg)）：能看到围绕多模型启动、模型切换与输出长度调整提出需求，随后出现对 `llama-oneclick.ps1` 和配置的说明。这支持“曾使用辅助编写工具讨论和调整启动脚本”的经历；截图没有编辑器标识、代码差异或提交记录，不能独立确认每段现存代码由 Cursor 生成。

用户另提供 `start.bat` 的历史运行截图：[入口与参数菜单](../assets/screenshots/provenance/start-bat-menu.jpg)、[Qwen IQ2_M 16K 加载日志](../assets/screenshots/provenance/start-bat-qwen-load.jpg)、[Cosmos Q8_0 16K 加载日志](../assets/screenshots/provenance/start-bat-cosmos-load.jpg)。截图中可见原始入口进入启动器、写入配置、生成预设、启动 router；两模型的子进程日志分别出现 `n_ctx_slot = 16384` 与 `model loaded`。历史截图未附完整连续终端日志和录屏；本轮的实际运行、API 和边界测试另行记录，不用历史截图代替。

SHA-256 用于识别本次审计的脚本版本，不证明作者或 Cursor 参与过程；用户截图作为历史材料单独标识，不与本次独立 API 实测混同。
