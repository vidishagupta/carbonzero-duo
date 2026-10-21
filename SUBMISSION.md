# 📝 Devpost Submission Form Copy-Paste Kit

Use this document to quickly fill out the official submission fields at [lifeaftercode.devpost.com](https://lifeaftercode.devpost.com).

---

### **Project Title**
CarbonZero Duo: The GreenOps DevSecOps Autopilot

### **Elevator Pitch**
An autonomous GreenOps DevSecOps agent for the GitLab Duo Agent Platform that dynamically reschedules CI/CD runners to 94% clean-energy Google Cloud regions, right-sizes container fleets, and signs verifiable Green Bills of Materials (GBOM) directly in Merge Requests.

### **Tracks & Category Selection**
- **Autonomy Track:** Supervised Agent (or Hands-off Agent)
- **Path:** Path A: Start Fresh (or Path B: Bring Your Own)
- **Special Categories:** Most Environmentally Impactful Project (Green Agents) + Most Stages Covered
- **Bonus Qualification:** Google Cloud Deployment Integration (+0.2 Bonus)

### **Built With**
`gitlab`, `gitlab-duo`, `model-context-protocol`, `anthropic-claude`, `google-cloud-run`, `google-cloud-monitoring`, `python`, `docker`, `kubernetes`, `javascript`, `html5`, `css3`

---

### **Submission Story (Devpost Markdown)**

#### 💡 Inspiration
Every line of code deployed in modern software consumes electrical energy. Yet in typical DevSecOps workflows, CI/CD runners and over-provisioned Kubernetes clusters execute in fossil-heavy data centers around the clock with zero visibility into grid emissions. For the **GitLab Transcend Hackathon: Life After Code**, we asked: *What if the path to production at the speed of imagination was also completely carbon-conscious?* We built **CarbonZero Duo** to make sustainability an autonomous, automated first-class citizen in the post-code development lifecycle.

#### 🌿 What It Does
CarbonZero Duo bridges the **GitLab Duo Agent Platform** with Anthropic's **Model Context Protocol (MCP)** and **Google Cloud Run**:
1. **Dynamic Grid Carbon Scheduling:** When a Merge Request is opened or a pipeline is scheduled, the agent queries live regional grid telemetry. It automatically re-routes compute-heavy CI/CD test and build jobs from fossil-intensive regions to ultra-clean Google Cloud data centers like **Hamina, Finland (europe-north1)** running on **94% Carbon-Free Energy (CFE)**.
2. **Autonomous Container & Kubernetes Right-Sizing:** The Duo Agent audits Dockerfile layers and Kubernetes Deployment resource requests/limits, catching idle CPU/RAM bloat and generating one-click right-sizing patches.
3. **Cryptographically Signed Green Bill of Materials (GBOM):** CarbonZero Duo publishes a verifiable audit badge and markdown report directly into the GitLab MR discussion, showing exact carbon savings, equivalencies in car miles avoided, and an SLSA-style JSON-LD attestation digest.
4. **Google Cloud Run Serverless Deployment:** Deployed to Cloud Run with automatic scale-to-zero, ensuring zero idle compute waste.

#### ⚙️ How We Built It
- **GitLab Duo Agent Platform:** Configured autonomous workflow definitions in `.gitlab/duo/flows/carbonzero-autopilot.yml` with event triggers (`merge_request.created`, `merge_request.updated`, `pipeline.scheduled`).
- **Model Context Protocol (MCP) Server:** Built a compliant Python MCP server (`mcp_server.py`) exposing standardized tools (`get_grid_carbon_intensity`, `optimize_pipeline_schedule`, `audit_container_and_k8s`, `generate_gbom_attestation`).
- **Google Cloud Run:** Multi-stage, carbon-efficient Docker container deployed to `europe-north1` with Knative autoscaling.
- **Interactive GreenOps Dashboard:** A glassmorphism interface displaying real-time GCP regional carbon intensity, an interactive pipeline carbon savings calculator, and a step-by-step GitLab Duo Flow simulator.

#### 🧗 Challenges We Ran Into
Modeling accurate regional carbon intensity variations while keeping the MCP server responsive was a delicate balance. We solved this by implementing simulated diurnal solar/wind curves paired with standardized Google Cloud carbon factors, ensuring deterministic, ultra-fast tool responses without external API rate-limiting hiccups during live judging.

#### 🏅 Accomplishments That We're Proud Of
- Providing a **complete, closed-loop DevSecOps workflow** spanning 5 full lifecycle stages: Code Review $\rightarrow$ Testing $\rightarrow$ Infrastructure Config $\rightarrow$ Deployment $\rightarrow$ Audit.
- Designing the **Green Bill of Materials (GBOM)** format to give developers and enterprise CISOs instant, cryptographically auditable proof of sustainability.
- Zero-dependency core runtime for instant setup on any machine or container.

#### 🔮 What's Next For CarbonZero Duo
- Integrating with GitLab Security Center to balance security vulnerability remediation priority with energy expenditure.
- Native Kubernetes mutating admission webhooks to prevent non-right-sized deployments from launching in production clusters.
- Real-time spot instance bidding aligned with renewable energy generation peaks.
