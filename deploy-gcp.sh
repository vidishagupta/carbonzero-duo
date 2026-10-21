#!/usr/bin/env bash
# ==============================================================================
# One-Click Deploy Script to Google Cloud Run
# Qualifies for +0.2 Bonus Points in Life After Code Hackathon
# ==============================================================================

set -e

PROJECT_ID=${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo "carbonzero-duo-demo")}
REGION=${GCP_REGION:-"europe-north1"} # Hamina, Finland (94% Carbon-Free Energy)
SERVICE_NAME="carbonzero-duo"

echo "============================================================"
echo "🌱 Deploying CarbonZero Duo to Google Cloud Run"
echo "📍 Project: $PROJECT_ID"
echo "🌿 Ultra-Clean Region: $REGION (94% Carbon-Free Energy)"
echo "============================================================"

# Build and submit image to Google Artifact Registry / GCR
echo "📦 Building container with Google Cloud Build..."
gcloud builds submit --tag "gcr.io/$PROJECT_ID/$SERVICE_NAME:latest" .

# Deploy to Cloud Run with scale-to-zero (zero idle carbon)
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "gcr.io/$PROJECT_ID/$SERVICE_NAME:latest" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --cpu 1 \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 5

URL=$(gcloud run services describe "$SERVICE_NAME" --platform managed --region "$REGION" --format 'value(status.url)')
echo "============================================================"
echo "✅ CarbonZero Duo is live on Google Cloud Run!"
echo "🔗 URL: $URL"
echo "============================================================"
