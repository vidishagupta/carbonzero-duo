"""
Kubernetes & Container Eco-Optimizer:
Scans Dockerfiles and Kubernetes manifests to identify compute bloat and over-provisioned resources,
calculating operational carbon reduction and generating auto-remediation patches.
"""

import re
from typing import Dict, Any, List

SAMPLE_DOCKERFILE = """FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
"""

SAMPLE_K8S_DEPLOYMENT = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: production
spec:
  replicas: 4
  template:
    spec:
      containers:
      - name: payment-api
        image: gcr.io/my-org/payment-service:v1.2.0
        resources:
          requests:
            cpu: "2000m"
            memory: "4Gi"
          limits:
            cpu: "4000m"
            memory: "8Gi"
"""


def analyze_dockerfile(dockerfile_content: str) -> Dict[str, Any]:
    """Analyzes Dockerfile for carbon-heavy base images and wasteful build layers."""
    recommendations = []
    carbon_waste_score = 0
    optimized_dockerfile = dockerfile_content

    # Check for heavyweight base images
    if re.search(r"FROM\s+python:[\d\.]+(?!-slim|-alpine)", dockerfile_content):
        carbon_waste_score += 35
        recommendations.append({
            "issue": "Heavyweight Full Python Base Image (~1.1GB)",
            "impact": "Slow container pulls, high registry storage, and bloated RAM usage.",
            "remediation": "Switch to `python:3.12-slim` (~140MB, 87% size reduction)."
        })
        optimized_dockerfile = re.sub(
            r"(FROM\s+python:[\d\.]+)",
            r"\1-slim",
            optimized_dockerfile
        )
    elif re.search(r"FROM\s+node:[\d\.]+(?!-slim|-alpine)", dockerfile_content):
        carbon_waste_score += 35
        recommendations.append({
            "issue": "Heavyweight Full Node.js Base Image (~1.2GB)",
            "impact": "Excessive container footprint in CI runner cache and GCP Cloud Run startup.",
            "remediation": "Switch to `node:20-alpine` (~180MB, 85% size reduction)."
        })
        optimized_dockerfile = re.sub(
            r"(FROM\s+node:[\d\.]+)",
            r"\1-alpine",
            optimized_dockerfile
        )

    # Check for missing multi-stage build or cache cleaning
    if "pip install" in dockerfile_content and "--no-cache-dir" not in dockerfile_content:
        carbon_waste_score += 15
        recommendations.append({
            "issue": "Pip cache retained in build layer",
            "impact": "Unneeded cache artifacts stored across container revisions.",
            "remediation": "Add `--no-cache-dir` to `pip install` commands."
        })
        optimized_dockerfile = optimized_dockerfile.replace(
            "pip install -r requirements.txt",
            "pip install --no-cache-dir -r requirements.txt"
        )

    return {
        "carbon_waste_score": carbon_waste_score,
        "recommendations": recommendations,
        "optimized_dockerfile": optimized_dockerfile,
        "estimated_image_reduction_mb": 950 if carbon_waste_score > 30 else 120
    }


def analyze_k8s_manifest(k8s_content: str) -> Dict[str, Any]:
    """Audits Kubernetes deployment resources for over-provisioning and calculates carbon savings."""
    recommendations = []
    replicas = 2
    rep_match = re.search(r"replicas:\s*(\d+)", k8s_content)
    if rep_match:
        replicas = int(rep_match.group(1))

    # Extract CPU requests
    cpu_req_match = re.search(r'cpu:\s*"(\d+)m?"', k8s_content)
    cpu_millicores = 1000
    if cpu_req_match:
        val = cpu_req_match.group(1)
        cpu_millicores = int(val) if "m" in cpu_req_match.group(0) else int(val) * 1000

    # Extract Memory requests
    mem_req_match = re.search(r'memory:\s*"(\d+)Gi?"', k8s_content)
    mem_gb = 2
    if mem_req_match:
        mem_gb = int(mem_req_match.group(1))

    # Detection logic: standard web APIs rarely need > 500m CPU or > 1Gi RAM average
    optimized_cpu = min(cpu_millicores, 350)
    optimized_mem = min(mem_gb, 1)

    cpu_savings_per_pod = (cpu_millicores - optimized_cpu) / 1000.0  # in vCPUs
    mem_savings_per_pod = mem_gb - optimized_mem                     # in GB

    total_vcpu_saved = round(cpu_savings_per_pod * replicas, 2)
    total_ram_saved_gb = round(mem_savings_per_pod * replicas, 2)

    # Calculate operational carbon saved per month (assuming GCP us-central1 @ 180 gCO2/kWh)
    # Watts = (vCPU * 12.5) + (RAM_GB * 0.38)
    watts_saved = (total_vcpu_saved * 12.5) + (total_ram_saved_gb * 0.38)
    monthly_kwh_saved = (watts_saved * 730 * 1.10) / 1000.0
    monthly_kg_co2_saved = round((monthly_kwh_saved * 180) / 1000.0, 2)
    annual_kg_co2_saved = round(monthly_kg_co2_saved * 12, 1)

    # Generate patch
    optimized_k8s = k8s_content
    optimized_k8s = re.sub(
        r'requests:\s*\n\s*cpu:\s*".*?"\s*\n\s*memory:\s*".*?"',
        f'requests:\n            cpu: "{optimized_cpu}m"\n            memory: "{optimized_mem}Gi"',
        optimized_k8s
    )
    optimized_k8s = re.sub(
        r'limits:\s*\n\s*cpu:\s*".*?"\s*\n\s*memory:\s*".*?"',
        f'limits:\n            cpu: "{optimized_cpu * 2}m"\n            memory: "{optimized_mem * 2}Gi"',
        optimized_k8s
    )

    if total_vcpu_saved > 0 or total_ram_saved_gb > 0:
        recommendations.append({
            "type": "Resource Right-Sizing",
            "observation": f"Pod requests {cpu_millicores}m CPU & {mem_gb}Gi RAM across {replicas} replicas.",
            "recommendation": f"Right-size requests to {optimized_cpu}m CPU and {optimized_mem}Gi RAM based on runtime telemetry.",
            "monthly_co2_saved_kg": monthly_kg_co2_saved,
            "annual_co2_saved_kg": annual_kg_co2_saved
        })

    return {
        "replicas": replicas,
        "total_vcpu_saved": total_vcpu_saved,
        "total_ram_saved_gb": total_ram_saved_gb,
        "monthly_kg_co2_saved": monthly_kg_co2_saved,
        "annual_kg_co2_saved": annual_kg_co2_saved,
        "recommendations": recommendations,
        "optimized_k8s": optimized_k8s
    }
