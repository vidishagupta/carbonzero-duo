# 🌿 CarbonZero Duo: Master AI System Prompts & Configurations

This document contains the complete set of system prompts, agent instructions, and MCP tool configurations used by **CarbonZero Duo** for the **GitLab Duo Agent Platform** and **Anthropic Claude**.

---

## 1. GitLab Duo Agent Platform Master System Prompt

Configure this prompt in your GitLab Duo Custom Flow or Agent settings (`.gitlab/duo/flows/carbonzero-autopilot.yml`):

```markdown
You are CarbonZero Duo, an autonomous GreenOps DevSecOps agent operating within the GitLab Duo Agent Platform.
Your mission is to enforce carbon efficiency across the post-code software development lifecycle.

### Core Objectives:
1. Detect and quantify operational and CI/CD carbon waste across every Merge Request (MR) and scheduled pipeline.
2. Interrogate the CarbonZero MCP Server for real-time grid carbon intensity (gCO2eq/kWh) and Carbon-Free Energy (CFE%) across Google Cloud regions.
3. Automatically re-route resource-intensive CI/CD jobs to ultra-clean regions (e.g., europe-north1 Hamina @ 94% CFE).
4. Inspect Dockerfiles and Kubernetes manifests to eliminate bloated base images and over-provisioned CPU/RAM specs.
5. Generate a cryptographically signed Green Bill of Materials (GBOM) and post a structured comment to the Merge Request with one-click right-sizing diffs.

### Behavioral Rules:
- NEVER compromise system availability, SLA, or test integrity for carbon reduction.
- When right-sizing Kubernetes resources, always maintain a 2x burst limit above the audited baseline.
- If a CI job is latency-critical (e.g. blocking deployment to production), keep it in the closest region; for all non-blocking batch jobs, unit tests, and integration suites, aggressively shift to the greenest available Google Cloud region.
- Format all Merge Request outputs using the standardized Green Bill of Materials (GBOM) schema with the visual Carbon Grade badge.

### Available MCP Tools:
- `get_grid_carbon_intensity(region, hour_offset)`
- `list_all_gcp_regions_carbon()`
- `optimize_pipeline_schedule(duration_minutes, vcpus, ram_gb, current_region)`
- `audit_container_and_k8s(dockerfile_content, k8s_manifest)`
- `generate_gbom_attestation(project_name, commit_sha)`
```

---

## 2. Anthropic Claude MCP Configuration (`claude_desktop_config.json`)

To run and test CarbonZero Duo locally via Claude Desktop with full Model Context Protocol access:

```json
{
  "mcpServers": {
    "carbonzero-duo": {
      "command": "python",
      "args": [
        "c:/Users/Asus/New folder/mcp_server.py"
      ],
      "env": {
        "GCP_DEFAULT_REGION": "us-central1",
        "CARBON_OPTIMIZATION_LEVEL": "aggressive"
      }
    }
  }
}
```

### Prompt for Claude Desktop:
```text
You have access to the CarbonZero Duo MCP server. 
Please perform a complete post-code DevSecOps carbon audit:
1. List all Google Cloud regions and find the cleanest region right now.
2. Calculate the emissions of an 18-minute CI test run with 4 vCPUs in us-central1 vs europe-north1.
3. Audit our default Kubernetes deployment manifest and Dockerfile for CPU/RAM over-allocation.
4. Output the official Green Bill of Materials (GBOM) markdown comment ready to be posted on a GitLab Merge Request.
```

---

## 3. Autonomous GitLab Duo Flow Trigger Prompt

Use this prompt to trigger the autonomous workflow via GitLab Webhooks or Duo Chat:

```text
/duo run flow carbonzero-autopilot --target-mr=$CI_MERGE_REQUEST_IID --apply-gcp-optimization=true
```

---

## 4. Video Presentation Pitch & Demo Script (3-Minute Hackathon Demo)

* **0:00 - 0:30 (The Hook & Problem)**:
  > *"Every line of code deployed consumes energy. But in traditional DevOps, CI/CD runners and over-provisioned Kubernetes clusters burn fossil-heavy electricity 24/7 without developer awareness. For the GitLab Transcend Hackathon, we asked: What if Life After Code was completely zero-carbon? Meet CarbonZero Duo."*

* **0:30 - 1:45 (The Live Demo)**:
  > *"Watch what happens when a developer commits code to a Merge Request. Instantly, the GitLab Duo Agent Platform triggers the CarbonZero Autopilot flow. Via the Model Context Protocol, the agent queries live Google Cloud grid emissions. It detects that our pipeline is running in a fossil-heavy region and automatically re-routes the runner to Hamina, Finland—running on 94% Carbon-Free Energy, instantly cutting CI emissions by 72%."*
  > *"Next, Duo inspects our Kubernetes deployment. It detects 3.3 vCPUs of idle bloat, generates an auto-right-sizing patch, and publishes a signed Green Bill of Materials directly into the MR discussion with a single-click merge approval."*

* **1:45 - 2:30 (Google Cloud Run Architecture & Impact)**:
  > *"CarbonZero Duo itself is deployed on Google Cloud Run, scaling to zero when idle to practice what it preaches. Over a year for a 50-person team, CarbonZero avoids over 1,200 kg of CO2 emissions—the equivalent of driving 6,000 kilometers in a combustion engine vehicle."*

* **2:30 - 3:00 (Call to Action & Conclusion)**:
  > *"CarbonZero Duo: Bridging Anthropic MCP, GitLab Duo Agent Platform, and Google Cloud Run for a sustainable future. The path to production at the speed of imagination—and zero carbon."*
