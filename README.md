# MNIST Image Classification API

A simple image classification API using a PyTorch-trained MNIST model. The backend is built with FastAPI, containerized with Docker, and deployed to Google Cloud Run (GCP).

---

## Features

- Classifies hand-written digits (0–9) from base64-encoded images
- `/predict` API endpoint for inference
- Fully containerized with Docker
- Deployed to GCP Cloud Run (serverless)

---

## Getting Started

Use python virtual environment to make sure that the local environment would be clean.  

### 1. Start python virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train Model

```bash
python -m train.train_model
```

### 4. Run the API locally (Optional)

```bash
uvicorn app.main:app --reload
```

Open the Swagger UI for interactive testing:  
👉 http://127.0.0.1:8000/docs

---

## Example Usage

### POST `/predict`

**Input JSON:**

```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAA6ElEQVR4nGNgGMyAWUhIqK5jvdSy/9/rQXwWmIQcm5WNQDCI9WRS4OeLB0EsRqic4V5+KOtf0leGZ+9vIpsodPsvCBzb9v0jFvsC5mT//XuWm0F7FjbX8DHO+huFKsQEZ336/5EhBcFFB9z7/rrh9qfyx4cLcmDuxwCBH/7+LZfEJau76+/fadK4ZAVi//zdjdvin39/OkCZLKgyeiGmLAzXDmHTpD7l6d+/f39twyIlUXQXFLwn/TClxJ2ugkM+EDOQhFaDY+VwACeGlPmaRyCpL63cqOJg1wYGMjBc3/y35wNuD1ITAABFF16AbmkxawAAAABJRU5ErkJggg=="
}
```

**Response:**

```json
{
  "prediction": 5
}
```

---

## Docker Deployment

### 1. Install Docker Desktop

Official Website: https://www.docker.com/products/docker-desktop/

### 2. Create Dockerfile and .dockignore

There are already a Dickerfile and .dockignore in the repositery.

### 3. Build Docker Image

```bash
docker build -t mnist-api .
```

### 4. Run Docker Locally (Optional)

```bash
docker run -p 8080:8080 mnist-api
```

---

## Deploy to Google Cloud Run

### 1. Install gcloud CLI (Google Cloud SDK)

Office Website: https://cloud.google.com/sdk/docs/install

### 2. Prerequisite
```bash
gcloud auth login

gcloud init

gcloud config set project mnist-api-469005
gcloud config set run/region asia-east1

gcloud services enable run.googleapis.com artifactregistry.googleapis.com
```

### 3. Verify if login and project setup are successful (Optional)

```bash
gcloud auth list
gcloud config list project
```

### 4. Deployment

```bash
gcloud artifacts repositories create mnist-repo --repository-format=docker --location=asia-east1 --project=mnist-api-469005 --description="MNIST API Repo"

gcloud auth configure-docker asia-east1-docker.pkg.dev

gcloud builds submit --tag asia-east1-docker.pkg.dev/mnist-api-469005/mnist-repo/mnist-api

gcloud run deploy mnist-api --image=asia-east1-docker.pkg.dev/mnist-api-469005/mnist-repo/mnist-api --platform=managed --region=asia-east1 --allow-unauthenticated --project=mnist-api-469005 --memory=1Gi
```

Once deployed, you’ll get a public endpoint like:

```
https://mnist-api-xxxxx.a.run.app/predict
```

### 5. Test

#### Method 1
Use Swagger UI.  
The URL would be https://mnist-api-xxxxx.a.run.app/predict/docs
Use the previous Example Usage for input.

#### Method 2
Use Windows cmd line.  
```bash
curl -X POST https://mnist-api-xxxxx.a.run.app/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"image_base64\": \"iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAA6ElEQVR4nGNgGMyAWUhIqK5jvdSy/9/rQXwWmIQcm5WNQDCI9WRS4OeLB0EsRqic4V5+KOtf0leGZ+9vIpsodPsvCBzb9v0jFvsC5mT//XuWm0F7FjbX8DHO+huFKsQEZ336/5EhBcFFB9z7/rrh9qfyx4cLcmDuxwCBH/7+LZfEJau76+/fadK4ZAVi//zdjdvin39/OkCZLKgyeiGmLAzXDmHTpD7l6d+/f39twyIlUXQXFLwn/TClxJ2ugkM+EDOQhFaDY+VwACeGlPmaRyCpL63cqOJg1wYGMjBc3/y35wNuD1ITAABFF16AbmkxawAAAABJRU5ErkJggg==\"}"
```
The answer is 5.  

---

## Project Structure

```
mnist-api/
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── model.py         # Load model
│   ├── predict.py       # Inference logic
│   └── utils.py         # Base64 to tensor
├── train/
│   └── train_model.py   # Train model
├── data/
│   └── MNIST            # Dataset
├── model/
│   └── mnist_cnn.pt     # Pre-trained PyTorch model
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## Notes

- The image input must be 28x28 grayscale (or will be auto-resized)
- Base64-encoded image is required in request

---

## Future Improvements

- Add frontend for UI upload
- Convert to REST + Web UI hybrid
- Add GitHub Actions for CI/CD
- Deploy multiple models (e.g., CIFAR, fashion-MNIST)

---

Here is my blog, there are more details about this project:  
https://myblog-alpha-umber.vercel.app/blog/mnist_api