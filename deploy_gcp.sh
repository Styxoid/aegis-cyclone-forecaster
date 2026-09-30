#!/usr/bin/env bash
# AegisSurge: Google Cloud Run Deployment Script (Bash)
set -eo pipefail

PROJECT_ID="${1:-$GCP_PROJECT}"
REGION="${2:-asia-south1}"
SERVICE_NAME="aegissurge-core"

if [ -z "$PROJECT_ID" ]; then
    echo "Error: GCP Project ID not specified."
    echo "Usage: ./deploy_gcp.sh <PROJECT_ID> [REGION]"
    exit 1
fi

echo "================================================================="
echo "   Deploying AegisSurge to Google Cloud Run ($REGION)"
echo "   Project: $PROJECT_ID"
echo "================================================================="

IMAGE_URI="gcr.io/$PROJECT_ID/${SERVICE_NAME}:latest"

echo "[1/3] Building container image via Google Cloud Build..."
gcloud builds submit --project "$PROJECT_ID" --tag "$IMAGE_URI" .

echo "[2/3] Deploying service to Google Cloud Run ($REGION)..."
gcloud run deploy "$SERVICE_NAME" \
    --project "$PROJECT_ID" \
    --image "$IMAGE_URI" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10

echo "[3/3] Retrieving Cloud Run public endpoint..."
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --project "$PROJECT_ID" --region "$REGION" --format 'value(status.url)')

echo ""
echo "================================================================="
echo "   AegisSurge Backend Successfully Deployed to Google Cloud Run!"
echo "   Public API Endpoint: $SERVICE_URL"
echo "   Swagger Docs:        $SERVICE_URL/docs"
echo "================================================================="
