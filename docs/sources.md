# 模型与运行器来源核对

> 核对日期：2026-10-21。以下链接指向模型发布方或运行器维护方的页面。本机已计算项目范围内四个 GGUF 文件的 SHA-256，并与名称相符的发布页比较。本仓库不分发模型权重。

| 本地对象 | 可核对的发布页面 | 本次判断 |
| --- | --- | --- |
| `llama-server.exe` | [llama.cpp 官方仓库](https://github.com/ggml-org/llama.cpp)、[server 文档](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) | 本机程序能返回版本并加载模型；安装包下载地址与完整构建来源尚未找到。 |
| Qwen3.6 35B-A3B Aggressive 的 IQ2_M 与 mmproj | [HauhauCS 模型页](https://huggingface.co/HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive)、[Qwen 原始模型页](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | 两个本地文件的 SHA-256 均与 HauhauCS 同名发布文件一致；可确认字节内容相同。此模型是社区改版，不应简称为 Qwen 官方权重。 |
| Cosmos-Reason2-8B 的 Q8_0 与 mmproj | [NVIDIA 原始模型页](https://huggingface.co/nvidia/Cosmos-Reason2-8B)、[mradermacher GGUF 仓库](https://huggingface.co/mradermacher/Cosmos-Reason2-8B-GGUF/tree/main)、[此前核对的 prithivMLmods 仓库](https://huggingface.co/prithivMLmods/Cosmos-Reason2-8B-GGUF) | 用户在 2026-10-21 的对话中确认主 Q8_0 来自 mradermacher 同一仓库，这是**用户提供的下载来源记录**。最初提供的 `Cosmos-Reason2-8B.mmproj-Q8_0.gguf` 链接指向视觉投影器，其发布页哈希与本地 mmproj 一致；mradermacher 主模型文件哈希本轮未取得，尚未独立验证主模型字节一致性。本地主模型与 prithivMLmods 同名文件不一致。NVIDIA 与 mradermacher 页面标注 `nvidia-open-model-license`，prithivMLmods 页标注 `apache-2.0`。 |

## 文件哈希对照

| 本地文件 | 本机 SHA-256 | 发布页 SHA-256 | 对照 |
| --- | --- | --- | --- |
| `Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ2_M.gguf` | `BA3A1D47A604F17EF74D913F9A9D9A2B456ACC6925E7B168BFA2E6527246011C` | [同值](https://huggingface.co/HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive/blob/main/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ2_M.gguf) | 一致 |
| `mmproj-Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf` | `C8E702344A81F8C226A914AA980ED6E1F604BCE9374F1FED8E65C896908AF414` | [同值](https://huggingface.co/HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive/blob/main/mmproj-Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf) | 一致 |
| `Cosmos-Reason2-8B.Q8_0.gguf` | `BF1846411C279B3957945119566580646D678FE4C0DC46CD4B08F2DCCE2D226F` | [prithivMLmods 文件](https://huggingface.co/prithivMLmods/Cosmos-Reason2-8B-GGUF/blob/main/Cosmos-Reason2-8B.Q8_0.gguf)：`0CD7DC26CB43A9E0A549372647C50923E72C2C95C8C00318D69D1C9765E9E868`；[mradermacher 文件](https://huggingface.co/mradermacher/Cosmos-Reason2-8B-GGUF/blob/main/Cosmos-Reason2-8B.Q8_0.gguf)：本轮未取得哈希 | 与前者不一致；用户确认来自后者，字节一致性未独立核实 |
| `mmproj-Cosmos-Reason2-8B-Q8_0.gguf` | `4AA321B682336D5EF39A9B86272C88DF22590F0DDECA6EFAB8BE1A0AC4453D32` | [用户提供的 mradermacher 文件](https://huggingface.co/mradermacher/Cosmos-Reason2-8B-GGUF/blob/main/Cosmos-Reason2-8B.mmproj-Q8_0.gguf)：同值；[prithivMLmods 文件](https://huggingface.co/prithivMLmods/Cosmos-Reason2-8B-GGUF/blob/main/Cosmos-Reason2-8B.mmproj-q8_0.gguf)：同值 | 字节内容一致；本机文件名已重命名 |

SHA-256 相同证明内容一致，不证明实际下载路径或作者历史。Cosmos 主模型的下载仓库现有用户确认；还需 mradermacher 主模型文件页的哈希来独立验证本地文件字节一致性。用户最初给出的 mmproj 链接不能充当主模型的文件哈希证据。模型页面给出的能力和推荐参数不能当作本机实测结果。
