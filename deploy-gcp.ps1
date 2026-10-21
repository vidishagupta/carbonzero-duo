<#
.SYNOPSIS
  PowerShell One-Click Deployment Script for Google Cloud Run
  Qualifies for +0.2 Bonus Points in Life After Code Hackathon
#>

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID,
    [string]$Region = "europe-north1",
    [string]$ServiceName = "carbonzero-duo"
)

if (-not $ProjectId) {
    try {
        $ProjectId = (gcloud config get-value project 2>$null).Trim()
    } catch {
        $ProjectId = "carbonzero-duo-demo"
    }
}

Write-Host "============================================================" -ForegroundColor Green
Write-Host "🌱 Deploying CarbonZero Duo to Google Cloud Run" -ForegroundColor Green
Write-Host "📍 Project: $ProjectId" -ForegroundColor Cyan
Write-Host "🌿 Region:  $Region (Hamina, Finland - 94% CFE)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Green

Write-Host "📦 Building container on Google Cloud Build..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$ProjectId/$ServiceName:latest" .

Write-Host "🚀 Deploying to Cloud Run with scale-to-zero..." -ForegroundColor Yellow
gcloud run deploy $ServiceName `
    --image "gcr.io/$ProjectId/$ServiceName:latest" `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --cpu 1 `
    --memory 512Mi `
    --min-instances 0 `
    --max-instances 5

$ServiceUrl = (gcloud run services describe $ServiceName --platform managed --region $Region --format 'value(status.url)')
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✅ CarbonZero Duo is live on Google Cloud Run!" -ForegroundColor Green
Write-Host "🔗 URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Green
