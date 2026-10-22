param(
    [ValidateRange(1, 65535)]
    [int]$Port = 8080
)

$ErrorActionPreference = 'Stop'
$baseUrl = "http://127.0.0.1:$Port"
$localRequest = @{}
if ((Get-Command Invoke-RestMethod).Parameters.ContainsKey('NoProxy')) { $localRequest.NoProxy = $true }
try {
    $health = Invoke-RestMethod @localRequest -Uri "$baseUrl/health" -TimeoutSec 10
    $models = Invoke-RestMethod @localRequest -Uri "$baseUrl/v1/models" -TimeoutSec 10
    Write-Host 'HEALTH:'
    $health | ConvertTo-Json -Depth 5
    Write-Host 'MODELS:'
    $models | ConvertTo-Json -Depth 8
} catch {
    Write-Error "本地服务检查失败：$($_.Exception.Message)"
    exit 1
}
