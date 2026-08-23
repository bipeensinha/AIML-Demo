import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from transformers import pipeline


# ============================================================
# LOAD LOCAL AI MODEL
# ============================================================

print("\nLoading local AI model...")

ai = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

print("Model ready!")


# ============================================================
# ORCHESTRATOR
# ============================================================

def orchestrator(customer_request):

    prompt = f"""
You are a routing agent for Vodafone customer service.

Your ONLY job is to choose the best specialist.

SPECIALISTS:

BILLING
Use for:
- High bill
- Unexpected charges
- Payment problems
- Plan charges

ROAMING
Use for:
- Travel abroad
- International usage
- Roaming charges

TECHNICAL
Use for:
- 4G or 5G problems
- Mobile internet not working
- Network problems
- SIM problems
- Phone connectivity problems

Here are examples:

Customer: My bill is £95 instead of £40.
Answer: BILLING

Customer: I travelled to Dubai and received roaming charges.
Answer: ROAMING

Customer: My 5G internet is not working.
Answer: TECHNICAL

Customer: My mobile network keeps disconnecting.
Answer: TECHNICAL

Customer: I was charged extra for my data.
Answer: BILLING

Now classify this customer request:

Customer:
{customer_request}

Answer with ONLY ONE WORD:
BILLING
ROAMING
TECHNICAL
"""

    messages = [
        {
            "role": "system",
            "content": "You are a routing agent. Return only one category."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = ai(
        messages,
        max_new_tokens=5,
        do_sample=False
    )

    decision = response[0]["generated_text"][-1]["content"].strip().upper()

    print(f"   Orchestrator decision: {decision}")

    # Clean up the AI output
    if "TECHNICAL" in decision:
        return "TECHNICAL"

    if "ROAMING" in decision:
        return "ROAMING"

    if "BILLING" in decision:
        return "BILLING"

    # Fallback
    return "BILLING"

# ============================================================
# SPECIALIST AGENTS
# ============================================================

def billing_agent(request):

    prompt = f"""
You are the Vodafone Billing Specialist.

Customer request:
{request}

Explain the likely billing issue and suggest
what the customer should check.

Give only 2-3 short sentences.
"""

    return call_agent(prompt)


def roaming_agent(request):

    prompt = f"""
You are the Vodafone Roaming Specialist.

Customer request:
{request}

Analyze the possible roaming issue and explain
what the customer should check.

Give only 2-3 short sentences.
"""

    return call_agent(prompt)


def technical_agent(request):

    prompt = f"""
You are the Vodafone Technical Support Specialist.

Customer request:
{request}

Analyze the technical problem and suggest
simple troubleshooting steps.

Give only 2-3 short sentences.
"""

    return call_agent(prompt)


# ============================================================
# COMMON AGENT FUNCTION
# ============================================================

def call_agent(prompt):

    messages = [
        {
            "role": "system",
            "content": "You are a helpful Vodafone specialist."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = ai(
        messages,
        max_new_tokens=70
    )

    return response[0]["generated_text"][-1]["content"].strip()


# ============================================================
# MAIN PROGRAM
# ============================================================

print("\n==============================================")
print("       VODAFONE MULTI-AGENT SYSTEM")
print("==============================================")

print("\nEnter customer request:")
customer_request = input("Customer: ")


# ============================================================
# ORCHESTRATOR DECIDES
# ============================================================

print("\n🤖 ORCHESTRATOR AGENT")
print("----------------------------------------------")
print("Analyzing request...")

selected_agent = orchestrator(customer_request)

print(f"Decision: {selected_agent} AGENT")


# ============================================================
# ROUTE REQUEST
# ============================================================

print("\n➡️ Routing request...")

if selected_agent == "BILLING":

    print("📋 BILLING AGENT")

    answer = billing_agent(customer_request)

elif selected_agent == "ROAMING":

    print("🌍 ROAMING AGENT")

    answer = roaming_agent(customer_request)

else:

    print("📱 TECHNICAL AGENT")

    answer = technical_agent(customer_request)


# ============================================================
# FINAL RESPONSE
# ============================================================

print("\n==============================================")
print("              FINAL RESPONSE")
print("==============================================")

print(answer)

print("\n==============================================")
print("                 COMPLETE")
print("==============================================")