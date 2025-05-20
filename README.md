# CS436-Project
# CloudRate – A Scalable Song Rating Platform on GCP

CloudRate is a cloud-native application built using React, FastAPI, Docker, Kubernetes, and Firestore. It allows users to rate songs, browse artists and albums, and view system-generated analytics — all deployed and orchestrated through Google Cloud Platform.

## 🌐 Live Endpoints

- **Frontend (React via GKE LoadBalancer)**: http://34.67.59.39
- **Backend (FastAPI via GKE LoadBalancer)**: http://35.188.156.109

## 📁 Repository Structure

├── backend/
│ ├── logic/ # FastAPI backend source code
│ ├── Dockerfile # Backend Dockerfile
│ ├── deployment.yaml # Kubernetes deployment for backend
│ ├── service.yaml # Kubernetes service for backend
│
├── frontend/
│ ├── src/ # React source code
│ ├── Dockerfile # Frontend Dockerfile
│ ├── cloudrate-frontend-deployment.yaml # Frontend deployment
│ ├── cloudrate-frontend-service.yaml # Frontend service
│
├── locust/
│ ├── locustfile.py # Load testing script


---

## 🚀 Deployment Guide

### ✅ Prerequisites

- GCP project with billing enabled
- Docker, `kubectl`, and `gcloud` installed
- A GKE cluster created and configured

---

### Deployment Guide
 Build and Push Docker Images:
```bash
# Backend
docker build -t gcr.io/YOUR_PROJECT_ID/music-backend:latest ./backend
docker push gcr.io/YOUR_PROJECT_ID/music-backend:latest

# Frontend
docker build -t gcr.io/YOUR_PROJECT_ID/cloudrate-frontend:latest ./frontend
docker push gcr.io/YOUR_PROJECT_ID/cloudrate-frontend:latest

 Deploy to Kubernetes:
# Backend
kubectl apply -f backend/deployment.yaml
kubectl apply -f backend/service.yaml

# Frontend
kubectl apply -f frontend/cloudrate-frontend-deployment.yaml
kubectl apply -f frontend/cloudrate-frontend-service.yaml

Create Compute Engine VMs:
gcloud compute instances create seeder-vm --zone=us-central1-a --scopes=cloud-platform
gcloud compute instances create scraper-vm --zone=us-central1-a --scopes=cloud-platform
gcloud compute instances create analytics-vm --zone=us-central1-a --scopes=cloud-platform

Each VM runs the following:
seeder-vm: seed_users_and_logs.py
scraper-vm: spotify_importer.py
analytics-vm: log_top_rated.py

 Deploy Cloud Functions:
# log_review - HTTP triggered
gcloud functions deploy log_review \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point log_review \
  --region=us-central1

# generate_daily_summary - triggered via Pub/Sub
gcloud functions deploy generate_daily_summary \
  --runtime python310 \
  --trigger-topic=daily-summary \
  --entry-point generate_daily_summary \
  --region=us-central1

Set Up Cloud Scheduler with Pub/Sub:
 gcloud scheduler jobs create pubsub daily-summary-job \
  --schedule="0 2 * * *" \
  --time-zone="UTC" \
  --topic=daily-summary \
  --message-body="trigger" \
  --location=us-central1

Locust was used to simulate traffic:
locust -f locust/locustfile.py --host=http://35.188.156.109

👨‍💻 Authors
Irmak Küçükoba
Ahmet Doğaç Altın
