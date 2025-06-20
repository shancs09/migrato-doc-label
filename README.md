
# 🧠 Multi-PDF Document Classifier using watsonx

This project provides a full-stack AI-powered document classification system using **Watsonx**. It enables batch uploading of PDF files, intelligent LLM-based labeling, and an interactive UI to view results.

---
## Demo:

<img width="1054" alt="Screenshot 2025-05-08 at 13 30 16" src="https://github.com/user-attachments/assets/d5ceabc9-a60f-401f-b303-3125af7c53bd" />
<img width="1021" alt="Screenshot 2025-05-08 at 13 30 31" src="https://github.com/user-attachments/assets/26b58436-f948-45e9-ae9e-ca63b9c89707" />

## 🗂️ Project Structure

```
.
├── fastapi
│   ├── Dockerfile
│   ├── env_sample
│   ├── main.py
│   ├── previews/
│   ├── requirements.txt
│   └── utils/
│       ├── pdf_parser.py
│       └── watsonx_utils.py
├── llm_instruction.yaml
└── streamlit
    ├── Dockerfile
    ├── env_sample
    ├── requirements.txt
    └── st_main.py
```

---

## 🚀 Features

- 🔍 **Multi-language document classification**
- 📎 **Multi-PDF uploads with bulk classification**
- 📄 **Preview PDFs in-browser**
- 🌐 **FastAPI backend with multithreaded processing**
- 🖥️ **Streamlit frontend with progress feedback**
- ☁️ **Deployable on IBM Cloud Code Engine**

---

## 📦 Setup

### 1. Environment Variables

Copy the sample `.env_sample` in both `fastapi/` and `streamlit/` directories and rename as `.env`.

```bash
cp env_sample .env
```

### 2. FastAPI Requirements

```bash
cd fastapi
pip install -r requirements.txt
```

### 3. Streamlit Requirements

```bash
cd streamlit
pip install -r requirements.txt
```

---

## 🐳 Dockerized Deployment

Steps to build, test, push, and deploy a Dockerized FastAPI app (`migrato_fastapi`) to IBM Cloud Code Engine, along with an optional UI component.

---

## 🏗️ Build Docker Image(https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/)

```bash
# FastAPI
cd fastapi
# Build the Docker image locally
docker build -t migrato_fastapi .
```
---

## 🚀 Run & Test Locally

```bash
# Run the app on localhost
docker run -p 8080:8080 migrato_fastapi
```

Open your browser at: [http://localhost:8080](http://localhost:8080)

---

## 🍿 Tag and Push Image to IBM Cloud Container Registry (ICR)

```bash
# Tag the image for IBM Cloud Container Registry
docker tag migrato_fastapi uk.icr.io/llm-lang/migrato_fastapi:latest

# Push the image to ICR
docker push uk.icr.io/llm-lang/migrato_fastapi:latest
```

> 🔐 Make sure you're logged into IBM Cloud CLI before pushing to the registry.

Repeat same steps from streamlit-ui app directory as well

---

## ☁️ IBM Cloud CLI Commands (https://cloud.ibm.com/docs/cli?topic=cli-getting-started)

### 1. 🔐 Login to IBM Cloud

```bash
ibmcloud login --sso
```

* Enter the one-time passcode from your email.
* Select the appropriate account (e.g., `Ibm Migrato**`).
* Target the default resource group:

```bash
ibmcloud target -g Default
```

---

### 2. 📁 Create & Select a Code Engine Project

```bash
# List available projects
ibmcloud ce project list

# Create a new project
ibmcloud ce project create --name migrato-doc-label

# Select the project
ibmcloud ce project select --name migrato-doc-label
```

---

### 3. 🔐 Create a Registry Secret

```bash
ibmcloud ce registry create \
  --name migrato-registry \
  --server uk.icr.io \
  --username iamapikey \
  --password <YOUR_IBM_CLOUD_API_KEY>
```

---

### 4. 🚢 Deploy FastAPI App

```bash
ibmcloud ce app create \
  --name mg-doc-label \
  --image uk.icr.io/llm-labeling/migrato_fastapi@sha256:<digest> \
  --registry-secret migrato-registry \
  --port 8080
```

---

### 5. 🎨 Deploy Frontend UI (Optional)

```bash
ibmcloud ce app create \
  --name mg-doc-label-ui \
  --image uk.icr.io/llm-labeling/migrato_ui@sha256:<digest> \
  --registry-secret migrato-registry \
  --port 8501 \
  --env FAST_API_URL=https://mg-doc-label.1v4xjh38ru11.eu-gb.codeengine.appdomain.cloud
```

---

## 💻 Alternative: IBM Cloud Console

> 🛍️ All the above steps — from project creation to app deployment — can also be performed using the **IBM Cloud Console UI**:

1. Navigate to [IBM Cloud Code Engine](https://cloud.ibm.com/codeengine)
2. Create a new project
3. Connect container registry & deploy your application
4. Configure environment variables, secrets, and ports as needed

---

## 📁 Watsonx Prompt Template

The prompt used for classification is defined in `llm_instruction.yaml` and supports auto-detecting languages and JSON-only responses.

---

## 🔧 API Endpoints

- `POST /label`: Classify and store preview
- `POST /label_nopreview`: Classify without storing file
- `GET /preview/{filename}`: Stream preview PDF

<img width="1457" alt="Screenshot 2025-05-08 at 13 29 58" src="https://github.com/user-attachments/assets/0f62fc33-d347-4245-b644-91c418bbd05a" />

---

## 🧼 Housekeeping

Temporary files stored in `fastapi/previews` are cleaned up at runtime to avoid cluttering the filesystem.

---

## 📬 Contact

For issues, please open an [issue on GitHub](https://github.com/your-repo-url/issues).
