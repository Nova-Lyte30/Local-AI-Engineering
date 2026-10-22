# Cosmos-Reason2-8B 图片输入核验

> 2026-10-21。区分本次独立 API 实测与用户提供的历史会话记录。新增的两份 `llama-export` JSONL 将八张实际上传图片、提示词、模型 ID 和回复关联起来；原件留在用户资料夹，[脱敏核验摘要](../tests/evidence/llama-export-audit-2026-10-21.md)记录其哈希与范围。历史输出已具备图文对照依据，但不是本轮重新推理或正式准确率测评。

## 本次可复核的图片 API 短测

使用项目内明确标为合成测试图的 [geometry-layout.png](../tests/fixtures/geometry-layout.png)：白底，左侧蓝色正方形、右侧红色圆形、下方绿色三角形。以本机已安装的 `llama-server.exe` 加载 Cosmos Q8_0 及其 mmproj，参数为 `--host 127.0.0.1 --port 18080 --ctx-size 16384 --gpu-layers 0 --no-mmproj-offload --parallel 1 --threads 8 --reasoning off --no-webui`。服务日志出现 `loaded multimodal model`、`n_ctx_slot = 16384`、`model loaded`。

通过本机 `/v1/chat/completions` 发送文字与 `data:image/png;base64,...` 图片。问题为“请根据图片，仅用一句中文说明左、右、下方三个图形的颜色与形状。不要猜测。”实际可见答复为：

> 左侧是蓝色正方形，右侧是红色圆形，下方是绿色三角形。

API 记录 `prompt_tokens = 273`、`completion_tokens = 18`、`finish_reason = stop`。本例的颜色、形状和方位均与测试图一致，证明该配置下图片输入链路和一个简单空间识别任务可用。该次独立测试未测视频或长时稳定性。复现时使用 [multimodal-test.ps1](../scripts/multimodal-test.ps1) 和自己从 `/v1/models` 取得的模型 ID；原始响应保存在本机不跟踪的 `test-output/` 中，摘录见[先前 API 证据](../tests/evidence/local-api-2026-10-21.md)。

## 原始启动器的静态图片复测

本轮用原始 `start.bat` 启动 Cosmos，加载 mmproj 后再次问合成几何图，回答“左侧为蓝色正方形，右侧为红色圆形，下方为绿色三角形。”，与图一致。随后对历史会话的三张实际静态图片附件给出新问题：绿色苹果计数得到 `3`、黄色苹果颜色得到 `黄色`、木球图中猫/雨伞/直升机是否存在得到 `没有`，且没有虚构坐标。四个受控图片检查均与预先记录的可见答案一致；原图留在不跟踪的本机测试目录。请求、token 用量与限制见[原始启动器复测](../tests/evidence/start-bat-e2e-2026-10-21.md)。

这些新问题比历史原题短，不能据此抹去历史错误或估算通用多模态准确率。没有人工标注的定位框，也没有运行视频测试；视频按用户要求跳过。

## 用户提供的历史会话与截图

《Cosmos多模态能力测试.md》描述了八类提示词。两份[会话导出](../tests/evidence/llama-export-audit-2026-10-21.md)中的八条用户消息各附一张图片，后续助手消息记录 `Cosmos-Reason2-8B.Q8_0` 的完整文字回复；这补上了截图缺少实际输入的问题。本机参考资料夹中的[八张同场景图片](../tests/evidence/cosmos-input-inventory-2026-10-21.md)与会话附件的尺寸、哈希不同，尤其时序参考图裁掉了实际附件顶部的英文动作标签。下表以导出中的**实际附件**为对照对象，输出截图供直观查看。

| 场景 | 输出截图 | 能确认的范围与缺口 |
| --- | --- | --- |
| 基础视觉识别 | [截图](../assets/screenshots/cosmos-multimodal/visual-recognition.jpg) | 实际附件有木桌、水杯、苹果、橙子、柠檬和香蕉。回复识别主要类别；图中可见三颗绿色苹果，回复只列两颗，计数不准确。 |
| 空间关系 | [截图](../assets/screenshots/cosmos-multimodal/spatial-relations.jpg) | 实际附件中是**黄色**苹果，回复沿用提示词中的“红色苹果”错误前提；还把“蓝色杯子本身位于木制桌面上”放进杯子后方列表。 |
| 物理常识 | [截图](../assets/screenshots/cosmos-multimodal/physical-reasoning.jpg) | 实际附件是靠近桌边的玩具车。回复把静态画面断言为“静止”，并称其确定保持静止；单张照片不足以证明运动状态或未来结果。 |
| 交通场景 | [截图](../assets/screenshots/cosmos-multimodal/traffic-scene.jpg) | 实际附件可见车辆、过街行人、绿色车灯与行人灯；主体识别大体相符。具体车型、速度、距离及安全策略执行无法据静态图或文字回复确认。 |
| 动作时序 | [截图一](../assets/screenshots/cosmos-multimodal/temporal-reasoning-1.jpg)、[截图二](../assets/screenshots/cosmos-multimodal/temporal-reasoning-2.jpg) | 实际附件是**带英文动作标签的静态多行拼图**，顶部明确写有抓杯、拿起、移动、放下和释放杯子。回复的动作顺序有图中文字依据；0–5 秒时间戳没有图像或视频时间轴依据。此项证明读取了带标注图片中的动作信息，不能证明视频时序理解。 |
| 机器人具身推理 | [截图一](../assets/screenshots/cosmos-multimodal/embodied-reasoning-1.jpg)、[截图二](../assets/screenshots/cosmos-multimodal/embodied-reasoning-2.jpg) | 实际附件显示承载纸箱的移动机器人、蓝色料箱和黄色手动托盘车；回复识别主要场景，但自行设定“安全移动并卸载纸箱”为任务目标。传感器、路径和动作完成情况没有实测。 |
| 物体定位 | [截图](../assets/screenshots/cosmos-multimodal/grounding.jpg) | 实际附件可见红柄螺丝刀、黑色钳子及其他工具。两条回复给出相同坐标，但“绿色手柄的扳手”与可见工具不符；缺人工标注与框叠加，不能称定位准确。 |
| 抗幻觉 | [截图](../assets/screenshots/cosmos-multimodal/uncertainty.jpg) | 实际附件仅见木球与木块。回复正确说所问的猫、雨伞和直升机未发现，却仍给三个不存在目标 `[0, 0, 1000, 1000]` 全图框与中心点；结论和定位信息矛盾。 |

导出记录已把实际上传输入、提示词和完整文字回复绑定为同一会话；仍缺用于历史整组测试的客观评分标签，不能给出正式准确率。导出本身不含服务器日志或 GPU 证据；本轮原始启动器的 GPU 证据另见端到端记录。第三方图片使用许可尚未核对，本项目不复制 JSONL 与附件；本地项目只保留用户提供的输出截图和自行生成的合成测试图。
