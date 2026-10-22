# 公开复现示例：只启动明确指定的本地模型，不整理模型目录或改写配置。
# 使用前请阅读源代码。此文件创建于本项目整理阶段，不代表原始脚本历史。
param(
    [Parameter(Mandatory = $true)]
    [string]$ServerExe,
    [Parameter(Mandatory = $true)]
    [string]$ModelPath,
    [string]$MmprojPath,
    [ValidateRange(512, 131072)]
    [int]$Ctx = 8192,
    [ValidateRange(0, 999)]
    [int]$GpuLayers = 0,
    [ValidateRange(1, 65535)]
    [int]$Port = 8080,
    [ValidateRange(1, 32768)]
    [int]$Predict = 4096,
    [ValidateSet('auto', 'on', 'off')]
    [string]$Reasoning = 'auto'
)

$ErrorActionPreference = 'Stop'
$serverFile = (Resolve-Path -LiteralPath $ServerExe -ErrorAction Stop).Path
$modelFile = (Resolve-Path -LiteralPath $ModelPath -ErrorAction Stop).Path
if (-not (Test-Path -LiteralPath $serverFile -PathType Leaf)) { throw "运行器不是文件：$serverFile" }
if (-not (Test-Path -LiteralPath $modelFile -PathType Leaf)) { throw "模型不是文件：$modelFile" }
if ($MmprojPath) {
    $mmprojFile = (Resolve-Path -LiteralPath $MmprojPath -ErrorAction Stop).Path
    if (-not (Test-Path -LiteralPath $mmprojFile -PathType Leaf)) { throw "mmproj 不是文件：$mmprojFile" }
}

$serverArgs = @(
    '--model', $modelFile,
    '--host', '127.0.0.1',
    '--port', "$Port",
    '--ctx-size', "$Ctx",
    '--gpu-layers', "$GpuLayers",
    '--predict', "$Predict"
)
if ($MmprojPath) {
    $serverArgs += @('--mmproj', $mmprojFile)
    if ($GpuLayers -eq 0) { $serverArgs += '--no-mmproj-offload' }
}
if ($Reasoning -ne 'auto') { $serverArgs += @('--reasoning', $Reasoning) }

Write-Host "启动本地服务：127.0.0.1:$Port；模型：$modelFile；上下文：$Ctx；GPU 层数：$GpuLayers"
& $serverFile @serverArgs
exit $LASTEXITCODE
