$ErrorActionPreference = "Stop"

$toolsDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path + "\.tools"
New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null

$target = Join-Path $toolsDir "cloudflared.exe"
$url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"

Write-Host "Downloading cloudflared to $target"
Invoke-WebRequest -Uri $url -OutFile $target
Write-Host "Done. Use: $target"
