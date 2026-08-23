# ============================================================
# ENTERPRISE AI SERVICE DESK
# MULTI-AGENT SYSTEM
#
# Demonstrates:
# 1. AI Agent
# 2. Orchestrator Agent
# 3. Multiple Specialist Agents
# 4. Context Passing
# 5. Short-Term Memory
# 6. Resolution Agent
#
# Local model:
# Qwen/Qwen2.5-0.5B-Instruct
#
# Can be used by:
# 1. FastAPI Web UI
# 2. Standalone Terminal Demo
# ============================================================


import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from transformers import pipeline


# ============================================================
# 1. LOAD LOCAL AI MODEL
# ============================================================

print("\nLoading local AI model...")

ai = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

print("AI model ready!")


# ============================================================
# 2. SHORT-TERM MEMORY
# ============================================================

short_term_memory = {

    "employee_request": "",

    "orchestrator_decision": [],

    "agent_findings": []
}


# ============================================================
# 3. GENERIC AI FUNCTION
# ============================================================

def call_ai(system_message, user_message):

    messages = [

        {
            "role": "system",
            "content": system_message
        },

        {
            "role": "user",
            "content": user_message
        }

    ]

    response = ai(
        messages,
        max_new_tokens=100
    )

    return response[0]["generated_text"][-1]["content"].strip()


# ============================================================
# 4. ORCHESTRATOR AGENT
# ============================================================
#
# The Orchestrator does NOT solve the problem.
#
# Its job is:
#
# "Which specialist agents should investigate?"
#
# ============================================================

def orchestrator(employee_request):

    prompt = f"""
You are an Enterprise IT Orchestrator Agent.

Employee request:

{employee_request}

Available specialist agents:

IDENTITY
- Account
- Password
- MFA
- Access
- User authentication

NETWORK
- VPN
- Wi-Fi
- Internet
- DNS
- Firewall
- Network connectivity

ENDPOINT
- Laptop
- Desktop
- Device
- VPN client
- Certificate
- Software
- Local configuration

Decide which specialist agents should investigate
this problem.

Return ONLY the agent names separated by commas.

Example:
IDENTITY, NETWORK

or:

ENDPOINT
"""

    decision = call_ai(
        "You are an enterprise IT Orchestrator.",
        prompt
    ).upper()

    selected_agents = []

    if "IDENTITY" in decision:
        selected_agents.append("IDENTITY")

    if "NETWORK" in decision:
        selected_agents.append("NETWORK")

    if "ENDPOINT" in decision:
        selected_agents.append("ENDPOINT")

    # Safety fallback
    if not selected_agents:
        selected_agents.append("ENDPOINT")

    return selected_agents


# ============================================================
# 5. IDENTITY AGENT
# ============================================================

def identity_agent(context):

    prompt = f"""
Here is the current incident context:

{context}

You are the Identity Specialist Agent.

Investigate possible identity and access problems.

Check conceptually for:

- Account status
- Password
- MFA
- User access
- Permissions

Give a short finding.

Do not provide a long explanation.
"""

    return call_ai(
        "You are an Enterprise Identity Specialist.",
        prompt
    )


# ============================================================
# 6. NETWORK AGENT
# ============================================================

def network_agent(context):

    prompt = f"""
Here is the current incident context:

{context}

You are the Network Specialist Agent.

Investigate possible network problems.

Consider:

- VPN
- Wi-Fi
- Internet
- DNS
- Firewall
- Network availability

Give a short finding.

Do not provide a long explanation.
"""

    return call_ai(
        "You are an Enterprise Network Specialist.",
        prompt
    )


# ============================================================
# 7. ENDPOINT AGENT
# ============================================================

def endpoint_agent(context):

    prompt = f"""
Here is the current incident context:

{context}

You are the Endpoint Specialist Agent.

Investigate possible device-side problems.

Consider:

- Laptop
- VPN client
- Software
- Device configuration
- Certificate
- Local firewall

Give a short finding.

Do not provide a long explanation.
"""

    return call_ai(
        "You are an Enterprise Endpoint Specialist.",
        prompt
    )


# ============================================================
# 8. RESOLUTION AGENT
# ============================================================
#
# Receives:
#
# Employee Request
#       +
# Orchestrator Decision
#       +
# Specialist Findings
#
# ============================================================

def resolution_agent(memory):

    prompt = f"""
You are an Enterprise IT Resolution Agent.

Here is the accumulated incident information:

{memory}

Analyze all available information.

Provide:

1. Most likely root cause
2. What the employee should check
3. Recommended next step

Keep the answer short and easy to understand.

Do not invent specific facts that are not supported
by the investigation.
"""

    return call_ai(
        "You are an Enterprise IT Resolution Specialist.",
        prompt
    )


# ============================================================
# 9. RUN COMPLETE MULTI-AGENT WORKFLOW
# ============================================================
#
# This function is useful for:
#
# - FastAPI
# - Web UI
# - Testing
# - Future applications
#
# It keeps the complete workflow in one place.
#
# ============================================================

def solve_problem(employee_request):

    employee_request = employee_request.strip()

    if not employee_request:

        return {
            "employee_request": "",
            "selected_agents": [],
            "findings": {},
            "memory": {},
            "final_answer": "Please enter an IT problem."
        }


    # --------------------------------------------------------
    # Reset short-term memory
    # --------------------------------------------------------

    memory = {

        "employee_request": employee_request,

        "orchestrator_decision": [],

        "agent_findings": []
    }


    # --------------------------------------------------------
    # ORCHESTRATOR
    # --------------------------------------------------------

    selected_agents = orchestrator(
        employee_request
    )

    memory["orchestrator_decision"] = selected_agents


    # --------------------------------------------------------
    # SHARED CONTEXT
    # --------------------------------------------------------

    context = f"""
Employee Request:

{employee_request}

Orchestrator Decision:

{selected_agents}
"""


    # --------------------------------------------------------
    # SPECIALIST AGENTS
    # --------------------------------------------------------

    findings = {}


    if "IDENTITY" in selected_agents:

        findings["IDENTITY"] = identity_agent(
            context
        )


    if "NETWORK" in selected_agents:

        findings["NETWORK"] = network_agent(
            context
        )


    if "ENDPOINT" in selected_agents:

        findings["ENDPOINT"] = endpoint_agent(
            context
        )


    # --------------------------------------------------------
    # STORE FINDINGS IN MEMORY
    # --------------------------------------------------------

    for agent, finding in findings.items():

        memory["agent_findings"].append(
            {
                "agent": agent,
                "finding": finding
            }
        )


    # --------------------------------------------------------
    # RESOLUTION AGENT
    # --------------------------------------------------------

    final_answer = resolution_agent(
        memory
    )


    # --------------------------------------------------------
    # RETURN COMPLETE RESULT
    # --------------------------------------------------------

    return {

        "employee_request":
            employee_request,

        "selected_agents":
            selected_agents,

        "findings":
            findings,

        "memory":
            memory,

        "final_answer":
            final_answer
    }


# ============================================================
# 10. TERMINAL DEMO
# ============================================================
#
# IMPORTANT:
#
# This section only runs when this file is executed directly:
#
#     python Corporate_user_helpdesk.py
#
# It will NOT run when FastAPI imports this file.
#
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("          ENTERPRISE AI SERVICE DESK")
    print("             MULTI-AGENT DEMO")
    print("=" * 60)

    print("\nEnter the employee IT problem.")
    print("Type END when finished.\n")


    lines = []


    while True:

        line = input()

        if line.strip().upper() == "END":

            break

        lines.append(line)


    employee_request = "\n".join(
        lines
    ).strip()


    # --------------------------------------------------------
    # Run Multi-Agent System
    # --------------------------------------------------------

    result = solve_problem(
        employee_request
    )


    # --------------------------------------------------------
    # Display Short-Term Memory
    # --------------------------------------------------------

    print("\n")
    print("-" * 60)
    print("🧠 SHORT-TERM MEMORY")
    print("-" * 60)

    print("\nEmployee Request:")

    print(
        result["memory"]["employee_request"]
    )


    print("\nOrchestrator Decision:")

    print(
        result["memory"]["orchestrator_decision"]
    )


    # --------------------------------------------------------
    # Display Specialist Findings
    # --------------------------------------------------------

    print("\nSpecialist Findings:")


    for finding in result["memory"]["agent_findings"]:

        print(
            f"\n[{finding['agent']}]"
        )

        print(
            finding["finding"]
        )


    # --------------------------------------------------------
    # Display Resolution
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("              🎯 RESOLUTION AGENT")
    print("=" * 60)


    print("\n")
    print(
        result["final_answer"]
    )


    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("                DEMO COMPLETE")
    print("=" * 60)