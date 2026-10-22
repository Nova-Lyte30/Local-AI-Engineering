# 将指定本地图片发送到本机 llama-server；不上传到公网。
param(
    [Parameter(Mandatory = $true)]
    [string]$ModelId,
    [Parameter(Mandatory = $true)]
    [string]$ImagePath,
    [ValidateRange(1, 65535)]
    [int]$Port = 8080,
    [string]$Prompt = '请根据图片，仅用一句中文说明左、右、下方三个图形的颜色与形状。不要猜测。',
    [ValidateRange(1, 2048)]
    [int]$MaxTokens = 128
)

$ErrorActionPreference = 'Stop'
$imageFile = (Resolve-Path -LiteralPath $ImagePath -ErrorAction Stop).Path
$extension = [IO.Path]::GetExtension($imageFile).ToLowerInvariant()
$mime = switch ($extension) {
    '.png' { 'image/png' }
    '.jpg' { 'image/jpeg' }
    '.jpeg' { 'image/jpeg' }
    default { throw '仅支持 PNG 和 JPEG 图片。' }
}
$imageData = [Convert]::ToBase64String([IO.File]::ReadAllBytes($imageFile))
$payload = @{
    model = $ModelId
    messages = @(@{
        role = 'user'
        content = @(
            @{ type = 'text'; text = $Prompt },
            @{ type = 'image_url'; image_url = @{ url = "data:$mime;base64,$imageData" } }
        )
    })
    max_tokens = $MaxTokens
    stream = $false
}
$body = $payload | ConvertTo-Json -Depth 20
$localRequest = @{}
if ((Get-Command Invoke-RestMethod).Parameters.ContainsKey('NoProxy')) { $localRequest.NoProxy = $true }
$response = Invoke-RestMethod @localRequest -Uri "http://127.0.0.1:$Port/v1/chat/completions" -Method Post -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 180
$response | ConvertTo-Json -Depth 20
if ([string]::IsNullOrWhiteSpace($response.choices[0].message.content)) { exit 2 }
