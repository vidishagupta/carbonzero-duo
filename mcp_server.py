#!/usr/bin/env python3
"""
CarbonZero Model Context Protocol (MCP) Server:
Standardized tool provider for GitLab Duo Agent Platform and Anthropic Claude.
Complies with Model Context Protocol (JSON-RPC 2.0 stdio / HTTP).
"""

import sys
import json
from typing import Dict, Any, List

from src.carbon_engine import (
    get_current_intensity,
    get_all_regions_summary,
    find_cleanest_gcp_region,
    calculate_pipeline_emissions
)
from src.k8s_optimizer import (
    analyze_dockerfile,
    analyze_k8s_manifest,
    SAMPLE_DOCKERFILE,
    SAMPLE_K8S_DEPLOYMENT
)
from src.gbom_generator import generate_gbom_markdown

TOOLS = [
    {
        "name": "get_grid_carbon_intensity",
        "description": "Retrieves real-time carbon intensity (gCO2eq/kWh) and Carbon Free Energy percentage (CFE%) for a specified Google Cloud deployment region.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "Google Cloud region code (e.g. 'us-central1', 'europe-north1', 'europe-west1', 'asia-east1')",
                    "default": "us-central1"
                },
                "hour_offset": {
                    "type": "integer",
                    "description": "Hours ahead to forecast (0-24)",
                    "default": 0
                }
            },
            "required": ["region"]
        }
    },
    {
        "name": "list_all_gcp_regions_carbon",
        "description": "Returns a ranked list of all major Google Cloud regions sorted from lowest to highest carbon intensity.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "optimize_pipeline_schedule",
        "description": "Calculates the exact carbon emissions of a GitLab CI/CD pipeline and recommends optimal clean-energy GCP runner regions and time windows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "duration_minutes": {
                    "type": "number",
                    "description": "Duration of pipeline run in minutes",
                    "default": 18.5
                },
                "vcpus": {
                    "type": "integer",
                    "description": "Number of vCPUs allocated to CI runner",
                    "default": 4
                },
                "ram_gb": {
                    "type": "integer",
                    "description": "Memory in GB allocated to CI runner",
                    "default": 16
                },
                "current_region": {
                    "type": "string",
                    "description": "Current region where CI runner operates",
                    "default": "us-central1"
                }
            },
            "required": ["duration_minutes"]
        }
    },
    {
        "name": "audit_container_and_k8s",
        "description": "Audits Dockerfile base images and Kubernetes deployment resource requests/limits, providing right-sizing recommendations and auto-generated patch.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dockerfile_content": {
                    "type": "string",
                    "description": "Dockerfile text content. If empty, uses standard repository sample.",
                    "default": ""
                },
                "k8s_manifest": {
                    "type": "string",
                    "description": "Kubernetes Deployment YAML text content. If empty, uses standard repository sample.",
                    "default": ""
                }
            }
        }
    },
    {
        "name": "generate_gbom_attestation",
        "description": "Generates a certified Green Bill of Materials (GBOM) markdown report and cryptographic attestation for GitLab Merge Requests and Release Notes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "default": "production-payment-service"
                },
                "commit_sha": {
                    "type": "string",
                    "default": "7f8b91a0c4"
                }
            }
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Executes the requested tool and returns the response payload."""
    if name == "get_grid_carbon_intensity":
        region = arguments.get("region", "us-central1")
        offset = arguments.get("hour_offset", 0)
        return get_current_intensity(region, offset)

    elif name == "list_all_gcp_regions_carbon":
        return {"regions": get_all_regions_summary()}

    elif name == "optimize_pipeline_schedule":
        dur = float(arguments.get("duration_minutes", 18.5))
        vcpus = int(arguments.get("vcpus", 4))
        ram = int(arguments.get("ram_gb", 16))
        reg = arguments.get("current_region", "us-central1")
        return calculate_pipeline_emissions(dur, vcpus, ram, reg)

    elif name == "audit_container_and_k8s":
        df_content = arguments.get("dockerfile_content") or SAMPLE_DOCKERFILE
        k8s_content = arguments.get("k8s_manifest") or SAMPLE_K8S_DEPLOYMENT
        df_result = analyze_dockerfile(df_content)
        k8s_result = analyze_k8s_manifest(k8s_content)
        return {
            "dockerfile_audit": df_result,
            "k8s_audit": k8s_result
        }

    elif name == "generate_gbom_attestation":
        project = arguments.get("project_name", "production-payment-service")
        sha = arguments.get("commit_sha", "7f8b91a0c4")
        pipe = calculate_pipeline_emissions(18.5, 4, 16, "us-central1")
        k8s = analyze_k8s_manifest(SAMPLE_K8S_DEPLOYMENT)
        df = analyze_dockerfile(SAMPLE_DOCKERFILE)
        markdown = generate_gbom_markdown(project, sha, pipe, k8s, df)
        return {
            "project": project,
            "commit_sha": sha,
            "gbom_markdown": markdown
        }

    else:
        raise ValueError(f"Unknown tool: {name}")


def run_stdio_server():
    """Runs standard JSON-RPC 2.0 loop over stdin/stdout for MCP clients."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = handle_tool_call(tool_name, arguments)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            elif method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {
                            "name": "carbonzero-mcp-server",
                            "version": "1.0.0"
                        },
                        "capabilities": {
                            "tools": {}
                        }
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method {method} not found"}
                }
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(err_resp), flush=True)


if __name__ == "__main__":
    run_stdio_server()
