param(
    [Parameter(Mandatory = $true)]
    [string]$ModelId,
    [ValidateRange(1, 65535)]
    [int]$Port = 8080,
    [ValidateSet('chat', 'completion')]
    [string]$Mode = 'chat',
    [string]$Prompt = '请用一句中文介绍你自己。',
    [ValidateRange(1, 2048)]
    [int]$MaxTokens = 256
)

$ErrorActionPreference = 'Stop'
if ($Mode -eq 'chat') {
    $endpoint = 'chat/completions'
    $payload = @{
        model = $ModelId
        messages = @(@{ role = 'user'; content = $Prompt })
        max_tokens = $MaxTokens
        stream = $false
    }
} else {
    $endpoint = 'completions'
    $payload = @{
        model = $ModelId
        prompt = $Prompt
        max_tokens = $MaxTokens
        stream = $false
    }
}
$body = $payload | ConvertTo-Json -Depth 10
$localRequest = @{}
if ((Get-Command Invoke-RestMethod).Parameters.ContainsKey('NoProxy')) { $localRequest.NoProxy = $true }

try {
    $response = Invoke-RestMethod @localRequest -Uri "http://127.0.0.1:$Port/v1/$endpoint" -Method Post -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 180
    $response | ConvertTo-Json -Depth 20
    $visibleText = if ($Mode -eq 'chat') { $response.choices[0].message.content } else { $response.choices[0].text }
    if ([string]::IsNullOrWhiteSpace($visibleText)) {
        Write-Warning '请求返回但可见正文为空；检查 reasoning_content、finish_reason 和 max_tokens。'
        exit 2
    }
} catch {
    Write-Error "本地推理请求失败：$($_.Exception.Message)"
    exit 1
}
