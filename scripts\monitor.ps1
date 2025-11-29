# Simple HF Space health checker
# Usage: .\monitor.ps1 -Url 'https://YOUR_SPACE.hf.space/healthz' -Interval 10
param(
    [string]$Url = 'https://DS22F2001348-llm-quiz-solver.hf.space/healthz',
    [int]$Interval = 10
)

Write-Host "Starting HF monitor for $Url (interval ${Interval}s)"
while ($true) {
    try {
        $r = Invoke-WebRequest -Uri $Url -Method GET -UseBasicParsing -TimeoutSec 10
        $status = $r.StatusCode
        $content = $r.Content
        Write-Host "$(Get-Date -Format o) Status: $status - $content"
    } catch {
        Write-Host "$(Get-Date -Format o) ERROR: $($_.Exception.Message)"
    }
    Start-Sleep -Seconds $Interval
}
