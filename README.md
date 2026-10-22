# Local AI Engineering

本仓库展示开源模型本地部署与推理环境配置项目，仅涵盖 Qwen IQ2_M 与 Cosmos-Reason2-8B。

## 项目一：开源模型本地部署与推理环境配置

在 Windows 与 NVIDIA GPU 设备的机器上，使用 llama.cpp 管理本地 GGUF 模型、配置推理参数，并通过本机 OpenAI 兼容接口调用。2026-10-21 用原始 `start.bat` 依次启动 Qwen IQ2_M 与 Cosmos-Reason2-8B；两模型在 `n_ctx_slot = 16384` 下完成短答、近 16K 索引记录检索和各 5 次顺序请求。两次合计 16,384 tokens 的边界请求均得到正确答案，但服务日志标记了截断，不能称无截断通过。Cosmos 以 mmproj 正确回答合成图和三张历史静态图的定向问题；测试进程运行和退出时的显存变化支持 GPU 实际使用，准确卸载层数未取得。

- [部署过程与技术说明](docs/model-deployment.md)
- [简历主张与证据对应表](docs/evidence-matrix.md)
- [原始启动器审计](docs/launcher-audit.md)
- [问题记录](docs/model-troubleshooting.md)
- [测试计划与结果](tests/model-test-report.md)
- [本机 API 原始结果摘录](tests/evidence/local-api-2026-10-21.md)
- [原始 start.bat 端到端复测](tests/evidence/start-bat-e2e-2026-10-21.md)
- [Cosmos 图片输入核验与历史会话审阅](docs/cosmos-multimodal-audit.md)
- [历史会话导出证据摘要](tests/evidence/llama-export-audit-2026-10-21.md)
- [模型来源与许可核对](docs/sources.md)
- [安全复现示例](scripts/llama-oneclick.example.ps1)

## 阅读说明

文档将证据区分为“本次静态核验”“本次实测”“历史记录”“待验证”。早先 CPU 模式 14.8K 测试与后续原始启动器的 GPU 显存、16K 边界测试分别记录；合成检索任务不推广为自然长文档准确率或长期稳定性。示例脚本是基于现有配置整理的公开复现版本，不冒充原始开发历史。用户提供的 `llama-export` 会话已将八张实际图片、提示词、Cosmos 模型 ID 与回复关联；其历史结果与本轮独立 API 请求分别标注。

本仓库不会收录 GGUF 权重、llama.cpp 二进制程序、密钥、完整个人日志或未经脱敏的截图。模型及运行器应由读者依据各自来源和许可自行获取。
