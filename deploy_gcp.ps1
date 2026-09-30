# AegisSurge: Google Cloud Run Deployment Script (PowerShell)
param(
    [string]$ProjectId = $env:GCP_PROJECT,
    [string]$Region = "asia-south1",
    [string]$ServiceName = "aegissurge-core"
)

if (-not $ProjectId) {
    Write-Host "Error: GCP Project ID not specified." -ForegroundColor Red
    Write-Host "Usage: .\deploy_gcp.ps1 -ProjectId YOUR_GCP_PROJECT_ID" -ForegroundColor Yellow
    exit 1
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   Deploying AegisSurge to Google Cloud Run ($Region)" -ForegroundColor Cyan
Write-Host "   Project: $ProjectId" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Build and Submit Container Image to Google Container Registry
$ImageUri = "gcr.io/$ProjectId/${ServiceName}:latest"
Write-Host "[1/3] Building container image via Google Cloud Build..." -ForegroundColor Yellow
gcloud builds submit --project $ProjectId --tag $ImageUri .

# 2. Deploy to Cloud Run
Write-Host "[2/3] Deploying service to Google Cloud Run ($Region)..." -ForegroundColor Yellow
gcloud run deploy $ServiceName `
    --project $ProjectId `
    --image $ImageUri `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 1Gi `
    --cpu 1 `
    --min-instances 0 `
    --max-instances 10

# 3. Retrieve Deployed Service URL
Write-Host "[3/3] Retrieving Cloud Run public endpoint..." -ForegroundColor Green
$ServiceUrl = gcloud run services describe $ServiceName --project $ProjectId --region $Region --format 'value(status.url)'

Write-Host ""
Write-Host "=================================================================" -ForegroundColor Green
Write-Host "   AegisSurge Backend Successfully Deployed to Google Cloud Run! " -ForegroundColor Green
Write-Host "   Public API Endpoint: $ServiceUrl" -ForegroundColor Cyan
Write-Host "   Swagger Docs:        $ServiceUrl/docs" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Green
