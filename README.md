# Deployment Guide: Flask App on Kubernetes

This guide details the steps to deploy the Flask application and MongoDB database onto a Kubernetes cluster (e.g., Minikube or Killercoda playground).

### Prerequisites

1.  A Kubernetes cluster (`kubectl` installed and configured).
2.  A Docker image available in a container registry (e.g., Docker Hub).

### Step-by-Step Deployment

1.  **Clone the Repository:**
    ```bash
    git clone github.com
    cd flask_app_assignment
    ```

2.  **Update Deployment Image Tag:**
    Open `flask-deployment.yaml` and update the `image:` line to reference *your* container registry username.

3.  **Apply All Manifests:**
    Use `kubectl` to deploy all the services and resources defined in the YAML files:
    ```bash
    kubectl apply -f .
    ```

4.  **Monitor Deployment Status:**
    Wait for all pods to reach the `Running` status (this may take a minute as images are downloaded):
    ```bash
    kubectl get all
    kubectl get pvc
    ```

5.  **Access the Application:**
    If using Minikube, find the exposed IP and Port:
    ```bash
    minikube service flask-service --url
    ```
    If using a cloud playground, use the provided port/IP to access `http://<IP_ADDRESS>:<PORT>/`.
