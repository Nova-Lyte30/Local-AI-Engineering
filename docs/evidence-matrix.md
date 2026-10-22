# 简历主张与证据对应表

> 更新：2026-10-21。状态仅针对当前已取得的资料，后续测试须追加原始记录和时间。

| 简历主张 | 已找到的证据 | 核验状态 | 发布前缺口 |
| --- | --- | --- | --- |
| Windows、NVIDIA GPU 与 llama.cpp 环境 | 本机 `nvidia-smi` 识别 RTX 4060 Laptop 8188 MiB；`llama-server.exe --version` 返回 build 11461 | 本次实测：硬件识别与程序版本 | Windows 展示版本、运行器下载来源 |
| 部署 Qwen IQ2_M 并完成加载与推理 | [原始启动器复测](../tests/evidence/start-bat-e2e-2026-10-21.md)：加载、短答、5 次顺序请求、近 16K 检索通过 | `start.bat` 本机 HTTP POST 通过；边界有截断标记 | 自然长文档与长期稳定性未测 |
| 部署 Cosmos-Reason2-8B 并完成加载与推理 | [原始启动器复测](../tests/evidence/start-bat-e2e-2026-10-21.md)：短答、合成图及三张历史静态图定向复测、近 16K 检索；[历史会话导出](../tests/evidence/llama-export-audit-2026-10-21.md)保留旧结果 | `start.bat` 本机图文推理通过；历史复杂图片仍有已记录错误 | 大样本图片准确率、长期稳定性未测 |
| 按显存选量化、配置上下文并排错 | 启动器含显存档位、GPU/KV 配置；两模型 `n_ctx_slot = 16384`；运行与退出时显存各下降约 5 GiB；[Qwen 思考模式复测](model-troubleshooting.md) | 上下文、显存使用和参数修正有实测 | 无准确 GPU 卸载层数、最佳参数或量化性能对比 |
| Cursor 辅助编写和调整自动化脚本 | 现存脚本和 INI；用户提供的[对话截图](launcher-audit.md)显示模型切换与参数管理需求 | 脚本与历史对话存在；截图未显示编辑器身份或代码差异 | 具体 Cursor 代码贡献需编辑记录或版本差异 |
| 切换模型启动配置和管理推理参数 | [原始启动器审计](launcher-audit.md)与本轮两次 `-Model` / `-Ctx` / `-Predict` / `-Thinking` / `-PortPref` 实际启动 | 两个模型依次从原始入口加载并验证；测试后恢复原配置 | 本轮没有测试同一 router 会话内的网页热切换 |
| 测试 16384 Token 上下文 | 两模型 `n_ctx_slot = 16384`；各有输入 16,365 + 输出 19 = 16,384 tokens 的正确答案和 `truncated = 1` 日志 | 配置边界已触及；不能称无截断 16K 通过 | 无截断上限与自然长文档质量仍未知 |
| 无需外部推理 API 的模型调用 | 本机 `127.0.0.1:18080` 的 `/health`、`/v1/models`、两模型 HTTP POST 与响应，[原始启动器证据](../tests/evidence/start-bat-e2e-2026-10-21.md) | 本地推理链路通过 | 不代表其他工具、素材或下载过程完全离线 |

模型名称与量化标识按本地文件名记录；用户确认 Cosmos 主模型来自 mradermacher 仓库，先前提供的 mmproj 链接哈希与本地匹配，本地主模型与该仓库的主文件尚未完成哈希比对。发布页面、许可差异与来源缺口见[来源核对](sources.md)。历史口述结果不会自动升级为“本次实测”。测试记录模板见[测试报告](../tests/model-test-report.md)。
