from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# =========================================================
# IMPORT MULTI-AGENT SYSTEM
# =========================================================

from Corporate_user_helpdesk import (
    orchestrator,
    identity_agent,
    network_agent,
    endpoint_agent,
    resolution_agent
)


# =========================================================
# CREATE FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Enterprise AI Service Desk",
    description="Multi-Agent IT Helpdesk using Local Qwen AI",
    version="1.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# REQUEST MODEL
# =========================================================

class ProblemRequest(BaseModel):

    problem: str


# =========================================================
# MAIN MULTI-AGENT API
# =========================================================

@app.post("/api/solve")
def solve_problem(request: ProblemRequest):

    problem = request.problem.strip()

    # -----------------------------------------------------
    # Validate request
    # -----------------------------------------------------

    if not problem:

        return {
            "selected_agents": [],
            "findings": {},
            "final_answer": "Please enter an IT problem."
        }


    # =====================================================
    # 1. ORCHESTRATOR AGENT
    # =====================================================

    selected_agents = orchestrator(problem)


    # =====================================================
    # 2. CREATE SHARED CONTEXT
    # =====================================================

    context = f"""
Employee Request:

{problem}

Selected Specialist Agents:

{selected_agents}
"""


    # =====================================================
    # 3. RUN SPECIALIST AGENTS
    # =====================================================

    findings = {}


    # -----------------------------------------------------
    # Identity Agent
    # -----------------------------------------------------

    if "IDENTITY" in selected_agents:

        findings["IDENTITY"] = identity_agent(
            context
        )


    # -----------------------------------------------------
    # Network Agent
    # -----------------------------------------------------

    if "NETWORK" in selected_agents:

        findings["NETWORK"] = network_agent(
            context
        )


    # -----------------------------------------------------
    # Endpoint Agent
    # -----------------------------------------------------

    if "ENDPOINT" in selected_agents:

        findings["ENDPOINT"] = endpoint_agent(
            context
        )


    # =====================================================
    # 4. BUILD SHORT-TERM MEMORY
    # =====================================================

    memory = {

        "employee_request": problem,

        "orchestrator_decision": selected_agents,

        "agent_findings": [

            {
                "agent": agent,

                "finding": finding
            }

            for agent, finding
            in findings.items()

        ]
    }


    # =====================================================
    # 5. RESOLUTION AGENT
    # =====================================================

    final_answer = resolution_agent(
        memory
    )


    # =====================================================
    # 6. RETURN RESULT TO FRONTEND
    # =====================================================

    return {

        "employee_request": problem,

        "selected_agents": selected_agents,

        "findings": findings,

        "memory": memory,

        "final_answer": final_answer

    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/api/health")
def health():

    return {
        "status": "online",
        "service": "Enterprise AI Service Desk",
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "agents": [
            "Orchestrator",
            "Identity",
            "Network",
            "Endpoint",
            "Resolution"
        ]
    }


# =========================================================
# SERVE FRONTEND
# =========================================================
#
# Folder structure:
#
# enterprise-ai-helpdesk/
#
# ├── app.py
# ├── Corporate_user_helpdesk.py
# │
# └── static/
#     ├── index.html
#     ├── style.css
#     └── script.js
#
# =========================================================

app.mount(
    "/",
    StaticFiles(
        directory="static",
        html=True
    ),
    name="static"
)