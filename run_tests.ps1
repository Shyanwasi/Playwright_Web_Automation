param (
    [string]$Env = "qa",
    [string]$Marker = ""
)

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host " Running Playwright Tests on Environment: $Env" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

$cmd = "pytest --env=$Env"

if ($Marker -ne "") {
    $cmd += " -m $Marker"
}

Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nTests completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nTest execution failed." -ForegroundColor Red
}