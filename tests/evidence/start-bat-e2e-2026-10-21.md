# 原始 `start.bat` 端到端复测

> 2026-10-21，本机 Windows。仅测试 Qwen IQ2_M 与 Cosmos Q8_0。用户要求跳过视频、来源细节和 GitHub 交付。以下为本轮实际请求与服务日志摘录；数值只代表这次运行。

## 启动与配置

先备份 `launcher.ini` 与 `presets.generated.ini`，记录脚本哈希及 GGUF 文件清单。安装目录下的模型均已在各自子目录，启动器的整理分支没有移动模型文件。首次在受限沙箱调用 `start.bat` 时，`Get-CimInstance Win32_ComputerSystem` 被系统拒绝，服务尚未启动；在宿主机权限下重试成功。两次使用同一个原始入口，依次启动并停止，避免同时加载测试模型：

```powershell
& 'D:\Program App\llama\start.bat' -Auto -Model 'Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ2_M' -Ctx 16384 -Predict 512 -Thinking off -PortPref 18080
& 'D:\Program App\llama\start.bat' -Auto -Model 'Cosmos-Reason2-8B.Q8_0' -Ctx 16384 -Predict 512 -Thinking off -PortPref 18080
```

两个服务均绑定 `127.0.0.1:18080`。启动器生成 `--models-dir`、`--models-preset`、`-c 16384`、`--cache-type-k q8_0`、`--cache-type-v q8_0`、`--flash-attn on`、`--fit on --fit-target 1024` 与 `--mmproj-offload`；子进程日志均出现 `model loaded` 和 `n_ctx_slot = 16384`。Qwen 运行时 `/health` 返回 `{"status":"ok"}`；两次 `/v1/models` 均显示本轮目标模型为 loaded，且两者 API 实际推理成功。脚本扫描了其他目录并列出名称，但没有测试其他模型。

## 推理结果

| 模型与场景 | API 实际结果 | 判断 |
| --- | --- | --- |
| Qwen IQ2_M 短答 | `Qwen 启动器测试通过。`；输入 31、输出 9 tokens；`finish_reason=stop` | 通过 |
| Qwen IQ2_M 连续 5 次短答 | `OK1` 至 `OK5`，每次均为 `stop`，预期文本全匹配 | 5/5；仅代表短时重复调用 |
| Cosmos 短答 | `Cosmos 启动器测试通过。`；输入 21、输出 10 tokens；`stop` | 通过 |
| Cosmos 合成几何图 | `左侧为蓝色正方形，右侧为红色圆形，下方为绿色三角形。`；输入 273、输出 18 tokens；`stop` | 颜色、形状、方位正确 |
| Cosmos 连续 5 次短答 | `OK1` 至 `OK5`，每次均为 `stop`，预期文本全匹配 | 5/5；仅代表短时重复调用 |

图片请求使用 [multimodal-test.ps1](../../scripts/multimodal-test.ps1) 与项目自行生成的 [geometry-layout.png](../fixtures/geometry-layout.png)。

### 近 16K 与边界测试

用 [context-boundary-test.py](../../scripts/context-boundary-test.py) 生成 250 条带不同索引和值的记录，并在中间加入确定长度的填充段。任务要求只返回 R001、R125、R250 三处值：`K07936 K89892 K79767`。脚本通过本机 `/tokenize` 校准文本 token 数，然后用 `/v1/chat/completions` 请求。该任务检验长输入中多处记录找回；填充段大量重复，不能等同真实复杂文档测评。

| 模型 | 文本 token 数 | API 输入 + 输出 | 服务端截断标记 | 答案 |
| --- | ---: | ---: | --- | --- |
| Qwen IQ2_M，近上限 | 16,180 | 16,192 + 19 = 16,211 | 本次未单独留存该请求的标记 | 三值精确匹配；`stop` |
| Qwen IQ2_M，边界 | 16,353 | 16,365 + 19 = 16,384 | `truncated = 1` | 三值精确匹配；`stop` |
| Cosmos，近上限 | 16,180 | 16,188 + 19 = 16,207 | `truncated = 0` | 三值精确匹配；`stop` |
| Cosmos，边界 | 16,357 | 16,365 + 19 = 16,384 | `truncated = 1` | 三值精确匹配；`stop` |

`16,384` 是这两次边界请求的 API 输入与输出用量之和。日志同时标记 `truncated = 1`，因此不能宣称 16,384 token **无截断**通过；两次可见答案仍正确。Qwen 另一次 16,364 + 19 = 16,383 tokens 请求也返回相同准确答案，但没有留存对应截断标记。

### 历史静态图片定向复测

使用用户 `llama-export` 中的三张**实际会话附件**，经新提示词重发至本轮 Cosmos 服务。图片只保存在不跟踪的本机 `test-output/`，不纳入项目文件；本轮提示词与历史会话不相同。

| 图片与本轮问题 | 预期 | 实际 | 结果 |
| --- | --- | --- | --- |
| 水果图：绿色苹果有几个？ | `3` | `3`；输入 2,773、输出 2 tokens | 通过 |
| 杯子、香蕉、苹果图：苹果是什么颜色？ | `黄色` | `黄色`；输入 2,710、输出 2 tokens | 通过 |
| 木球图：猫、雨伞或直升机是否存在？ | `没有` | `没有`；输入 1,251、输出 2 tokens，无虚构坐标 | 通过 |

这三项加上合成几何图是四个已定义答案的图片检查，均通过。它们不是无提示的历史原题复现，也不构成通用多模态准确率。用户历史记录中的错误仍保留在[图片审阅](../../docs/cosmos-multimodal-audit.md)。

## GPU 与收尾

两次启动均识别 `CUDA0: NVIDIA GeForce RTX 4060 Laptop GPU`，且 `--fit on` 自动选择资源分配。Qwen 运行期间 `nvidia-smi` 显存占用约 7,696 MiB，关闭本轮 Qwen 服务后为约 2,351 MiB，差约 5,345 MiB。Cosmos 退出前为约 7,325 MiB，退出后为约 2,233 MiB，差约 5,092 MiB；Cosmos 退出日志还出现 `CUDA0 compute buffer`。这些前后变化支持两个测试进程实际使用 GPU 显存，但本轮没有取得准确的 GPU 卸载层数，也不据此比较量化性能或最佳参数。用户此前在 8080 端口运行的 router 和 Cosmos 进程始终保留，没有中断。

测试实例均正常清理，退出后只剩原有 8080 服务。模型文件清单的路径与大小前后无差异；`start.bat`、`llama-oneclick.ps1` 和 `presets.ini` 未改动。两次启动重写的 `launcher.ini` 与 `presets.generated.ini` 已由测试前备份恢复，恢复后的 SHA-256 与原文件相同。测试备份、哈希快照保存在不跟踪的 `test-output/start-bat-2026-10-21/`。

短时 5 次调用不能证明数小时或数天的持续稳定性。GPU 卸载层数、真正长篇自然语言文档准确率和大样本图片准确率仍无证据。视频能力按用户要求跳过。
