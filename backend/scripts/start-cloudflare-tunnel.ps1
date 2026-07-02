param(
  [string]$Origin = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

function Get-CloudflaredPath {
  $localTool = Join-Path (Resolve-Path (Join-Path $PSScriptRoot "..")).Path ".tools\cloudflared.exe"
  if (Test-Path $localTool) {
    return $localTool
  }

  $command = Get-Command cloudflared -ErrorAction SilentlyContinue
  if ($command) {
    return $command.Source
  }

  throw "cloudflared is not installed. Run install-cloudflared.ps1 first."
}

Write-Host "Starting Cloudflare Tunnel for $Origin"
& (Get-CloudflaredPath) tunnel --url $Origin
