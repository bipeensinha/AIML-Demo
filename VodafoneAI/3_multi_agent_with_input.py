import os

# Keep the terminal clean by suppressing Transformers warnings/info
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from transformers import pipeline


# ------------------------------------------------
# Load ONE local AI model
# ------------------------------------------------

print("\nLoading local AI model...")

ai = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

print("Model ready!")


# ------------------------------------------------
# Function used by each agent
# ------------------------------------------------

def run_agent(agent_name, instruction, context):

    prompt = f"""
You are {agent_name}.

Your task:
{instruction}

Shared context from the customer and other agents:
{context}

Give only 2-3 short sentences.
Do not repeat the entire context.
Focus only on your assigned task.
"""

    messages = [
        {
            "role": "system",
            "content": f"You are {agent_name}. Be concise and practical."
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

    return response[0]["generated_text"][-1]["content"].strip()


# ------------------------------------------------
# Get customer request from the user
# ------------------------------------------------

print("\n======================================")
print("       VODAFONE MULTI-AGENT DEMO")
print("======================================")

print("\nEnter the customer request.")
print("Type END when you have finished.\n")

lines = []

while True:
    line = input()

    if line.strip().upper() == "END":
        break

    lines.append(line)

customer_request = "\n".join(lines).strip()

if not customer_request:
    print("\nNo customer request entered. Exiting.")
    raise SystemExit


# ------------------------------------------------
# Shared context
# ------------------------------------------------

shared_context = f"""
Customer Request:
{customer_request}
"""


# ------------------------------------------------
# AGENT 1
# ------------------------------------------------

print("\n🤖 AGENT 1 — CUSTOMER ANALYST")
print("--------------------------------------")

agent1 = run_agent(
    "Customer Analyst",
    """
Understand the customer's problem.
Identify the important facts and what should
be investigated.
""",
    shared_context
)

print(agent1)

shared_context += f"""

Agent 1 - Customer Analyst:
{agent1}
"""

print("\n➡️ Context passed to Agent 2...")


# ------------------------------------------------
# AGENT 2
# ------------------------------------------------

print("\n🤖 AGENT 2 — BILLING SPECIALIST")
print("--------------------------------------")

agent2 = run_agent(
    "Billing Specialist",
    """
Analyze the possible billing causes.
Consider data usage, roaming, additional services,
plan limits, or unexpected charges.
Use the original request and Agent 1's analysis.
""",
    shared_context
)

print(agent2)

shared_context += f"""

Agent 2 - Billing Specialist:
{agent2}
"""

print("\n➡️ Context passed to Agent 3...")


# ------------------------------------------------
# AGENT 3
# ------------------------------------------------

print("\n🤖 AGENT 3 — RESOLUTION AGENT")
print("--------------------------------------")

agent3 = run_agent(
    "Customer Resolution Specialist",
    """
Review the customer's problem and the analysis
from the other agents.
Recommend the best next step and provide a
short, customer-friendly response.
""",
    shared_context
)

print(agent3)


# ------------------------------------------------
# Demonstrate the shared context
# ------------------------------------------------

print("\n======================================")
print("          CONTEXT FLOW")
print("======================================")

print("""
Customer Request
       ↓
   Agent 1
       ↓
  Shared Context
       ↓
   Agent 2
       ↓
  Shared Context
       ↓
   Agent 3
       ↓
  Final Response
""")


print("======================================")
print("             DEMO COMPLETE")
print("======================================\n")