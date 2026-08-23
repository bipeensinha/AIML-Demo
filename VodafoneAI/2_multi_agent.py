import os

# Suppress Transformers messages
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from transformers import pipeline


# ---------------------------------------------
# Load local AI model
# ---------------------------------------------

ai = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)


# ---------------------------------------------
# Agent function
# ---------------------------------------------

def run_agent(agent_name, instruction, context):

    prompt = f"""
You are {agent_name}.

Task:
{instruction}

Shared context:
{context}

Give only 2-3 short sentences.
Do not repeat the entire context.
"""

    messages = [
        {
            "role": "system",
            "content": f"You are {agent_name}."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = ai(
        messages,
        max_new_tokens=60
    )

    return response[0]["generated_text"][-1]["content"]


# ---------------------------------------------
# Customer request
# ---------------------------------------------

customer_request = """
A Vodafone customer normally pays £40,
but this month the bill is £95.
The customer wants to know why.
"""


# ---------------------------------------------
# Shared Context
# ---------------------------------------------

shared_context = f"""
Customer Request:
{customer_request}
"""


print("\n======================================")
print("       VODAFONE MULTI-AGENT DEMO")
print("======================================")


# =============================================
# AGENT 1
# =============================================

print("\n🤖 AGENT 1 — CUSTOMER ANALYST")
print("--------------------------------------")

agent1 = run_agent(
    "Customer Analyst",
    """
Identify the customer's problem and
what should be investigated.
""",
    shared_context
)

print(agent1)

shared_context += f"""

Agent 1 Analysis:
{agent1}
"""


print("\n➡️ Context passed to Agent 2...")


# =============================================
# AGENT 2
# =============================================

print("\n🤖 AGENT 2 — BILLING SPECIALIST")
print("--------------------------------------")

agent2 = run_agent(
    "Billing Specialist",
    """
Identify likely billing causes such as
extra data, roaming or additional services.
Use Agent 1's analysis.
""",
    shared_context
)

print(agent2)

shared_context += f"""

Agent 2 Analysis:
{agent2}
"""


print("\n➡️ Context passed to Agent 3...")


# =============================================
# AGENT 3
# =============================================

print("\n🤖 AGENT 3 — RESOLUTION AGENT")
print("--------------------------------------")

agent3 = run_agent(
    "Customer Resolution Specialist",
    """
Review the previous analysis and give
the best recommendation for the customer.
""",
    shared_context
)

print(agent3)


# =============================================
# END
# =============================================

print("\n======================================")
print("             DEMO COMPLETE")
print("======================================\n")