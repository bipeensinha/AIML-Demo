# ============================================================
# VODAFONE MULTI-AGENT SYSTEM
#
# Demonstrates:
#
# 1. AI Agent
# 2. Orchestrator Agent
# 3. Context Passing
# 4. Short-Term Memory
# 5. Multiple Specialist Agents
#
# Everything runs locally using Qwen.
# No cloud / API / Azure required.
# ============================================================


import os

# ------------------------------------------------------------
# Keep the terminal output clean
# ------------------------------------------------------------

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"


from transformers import pipeline


# ============================================================
# 1. LOAD THE LOCAL AI MODEL
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
#
# This dictionary represents our simple SHORT-TERM MEMORY.
#
# It stores information generated during the CURRENT session.
#
# It is NOT a database.
# It is NOT long-term memory.
#
# When the program stops, this memory disappears.
#
# Think of it as:
#
#        "What does the system currently know?"
#
# ============================================================

short_term_memory = {

    # Original customer request
    "customer_request": "",

    # Decision made by the orchestrator
    "orchestrator_decision": "",

    # Findings produced by specialist agents
    "agent_findings": []
}


# ============================================================
# 3. GENERIC AI FUNCTION
# ============================================================
#
# All our agents use the SAME underlying AI model.
#
# What makes them different?
#
# Their ROLE and INSTRUCTION.
#
# ------------------------------------------------------------
#
# Agent 1 = Orchestrator
# Agent 2 = Billing Specialist
# Agent 3 = Roaming Specialist
# Agent 4 = Resolution Agent
#
# Same AI model
# Different instructions
#
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
        max_new_tokens=80
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
#       "Who should handle this request?"
#
# This is the decision-making part of our
# Multi-Agent System.
#
# ============================================================

def orchestrator(customer_request):

    prompt = f"""
Customer request:

{customer_request}

Available specialist agents:

BILLING
- High bill
- Unexpected charges
- Payments
- Plan charges

ROAMING
- International travel
- Roaming
- Overseas usage

TECHNICAL
- Network
- Internet
- 4G / 5G
- SIM problems

Decide which specialist should handle the
customer request.

Return ONLY:

BILLING
ROAMING
or
TECHNICAL
"""

    decision = call_ai(
        "You are the Vodafone Orchestrator Agent.",
        prompt
    ).upper()

    # --------------------------------------------------------
    # Convert the AI response into a reliable decision.
    # --------------------------------------------------------

    if "ROAMING" in decision:
        return "ROAMING"

    if "TECHNICAL" in decision:
        return "TECHNICAL"

    return "BILLING"


# ============================================================
# 5. BILLING AGENT
# ============================================================
#
# IMPORTANT:
#
# The Billing Agent receives CONTEXT.
#
# It doesn't just receive the latest question.
#
# We pass the customer request + information already
# discovered by other agents.
#
# This is CONTEXT PASSING.
#
# ============================================================

def billing_agent(context):

    prompt = f"""
Here is the current customer context:

{context}

You are the Vodafone Billing Specialist.

Analyze the possible reasons for the high bill.

Consider:
- Extra data
- Additional services
- Plan limits
- Unexpected charges

Give 2-3 short sentences.
"""

    return call_ai(
        "You are a Vodafone Billing Specialist.",
        prompt
    )


# ============================================================
# 6. ROAMING AGENT
# ============================================================
#
# This agent receives the SAME SHARED CONTEXT.
#
# It specializes in roaming.
#
# ============================================================

def roaming_agent(context):

    prompt = f"""
Here is the current customer context:

{context}

You are the Vodafone Roaming Specialist.

Analyze whether international travel or roaming
could explain the customer's problem.

Give 2-3 short sentences.
"""

    return call_ai(
        "You are a Vodafone Roaming Specialist.",
        prompt
    )


# ============================================================
# 7. TECHNICAL AGENT
# ============================================================

def technical_agent(context):

    prompt = f"""
Here is the current customer context:

{context}

You are the Vodafone Technical Specialist.

Look for possible network, SIM, 4G or 5G issues.

Give 2-3 short sentences.
"""

    return call_ai(
        "You are a Vodafone Technical Specialist.",
        prompt
    )


# ============================================================
# 8. RESOLUTION AGENT
# ============================================================
#
# This agent receives the accumulated SHORT-TERM MEMORY.
#
# It sees:
#
#   Customer request
#   +
#   Orchestrator decision
#   +
#   Specialist findings
#
# It then creates the final response.
#
# ============================================================

def resolution_agent(memory):

    prompt = f"""
You are the Vodafone Customer Resolution Agent.

Here is the current short-term memory:

{memory}

Review all available information.

Create a simple customer-friendly answer.

Give:
1. Most likely explanation
2. What the customer should check
3. Recommended next step

Keep it short.
"""

    return call_ai(
        "You are a Vodafone Customer Resolution Specialist.",
        prompt
    )


# ============================================================
# 9. GET CUSTOMER REQUEST
# ============================================================

print("\n==========================================")
print("      VODAFONE MULTI-AGENT SYSTEM")
print("==========================================")

print("\nEnter the customer request.")
print("Type END when finished.\n")


lines = []

while True:

    line = input()

    if line.strip().upper() == "END":
        break

    lines.append(line)


customer_request = "\n".join(lines).strip()


# ============================================================
# 10. STORE CUSTOMER REQUEST IN SHORT-TERM MEMORY
# ============================================================
#
# The first piece of information entering our system
# is stored in memory.
#
# ============================================================

short_term_memory["customer_request"] = customer_request


print("\n------------------------------------------")
print("SHORT-TERM MEMORY")
print("------------------------------------------")

print("Customer request stored ✓")


# ============================================================
# 11. ORCHESTRATOR MAKES A DECISION
# ============================================================

print("\n🤖 ORCHESTRATOR AGENT")
print("------------------------------------------")

selected_agent = orchestrator(customer_request)

print("Decision:", selected_agent)


# ============================================================
# 12. STORE ORCHESTRATOR DECISION IN MEMORY
# ============================================================
#
# Now our short-term memory contains TWO pieces
# of information:
#
#   1. Customer request
#   2. Orchestrator decision
#
# ============================================================

short_term_memory["orchestrator_decision"] = selected_agent


print("\n🧠 SHORT-TERM MEMORY UPDATED")
print("------------------------------------------")

print("Customer request ✓")
print("Orchestrator decision ✓")


# ============================================================
# 13. CREATE CONTEXT FOR THE SPECIALIST
# ============================================================
#
# Here we demonstrate CONTEXT PASSING.
#
# We take information from memory and send it
# to the specialist agent.
#
# ============================================================

context = f"""
Customer Request:
{short_term_memory["customer_request"]}

Orchestrator Decision:
{short_term_memory["orchestrator_decision"]}
"""


# ============================================================
# 14. SEND REQUEST TO SPECIALIST
# ============================================================

print("\n➡️ ROUTING TO", selected_agent, "AGENT")


if selected_agent == "BILLING":

    specialist_result = billing_agent(context)

elif selected_agent == "ROAMING":

    specialist_result = roaming_agent(context)

else:

    specialist_result = technical_agent(context)


# ============================================================
# 15. STORE SPECIALIST RESULT IN MEMORY
# ============================================================
#
# This is VERY important.
#
# The specialist has produced NEW INFORMATION.
#
# We store that information in short-term memory.
#
# Now another agent can use it.
#
# ============================================================

short_term_memory["agent_findings"].append(
    {
        "agent": selected_agent,
        "finding": specialist_result
    }
)


print("\n🤖", selected_agent, "AGENT")
print("------------------------------------------")

print(specialist_result)


print("\n🧠 SHORT-TERM MEMORY UPDATED")
print("------------------------------------------")

print("Customer request ✓")
print("Orchestrator decision ✓")
print("Specialist finding ✓")


# ============================================================
# 16. SHOW THE MEMORY
# ============================================================
#
# This is a great point to pause during your class.
#
# Show students:
#
# "This is what the system currently remembers."
#
# ============================================================

print("\n==========================================")
print("       CURRENT SHORT-TERM MEMORY")
print("==========================================")

print("\nCustomer:")
print(short_term_memory["customer_request"])

print("\nOrchestrator:")
print(short_term_memory["orchestrator_decision"])

print("\nAgent Findings:")

for finding in short_term_memory["agent_findings"]:

    print(
        f"- {finding['agent']}: "
        f"{finding['finding']}"
    )


# ============================================================
# 17. PASS MEMORY TO RESOLUTION AGENT
# ============================================================
#
# The Resolution Agent receives the accumulated
# short-term memory.
#
# This demonstrates BOTH:
#
#       CONTEXT PASSING
#
# and
#
#       SHORT-TERM MEMORY
#
# ============================================================

print("\n🤖 RESOLUTION AGENT")
print("------------------------------------------")

final_answer = resolution_agent(
    short_term_memory
)


# ============================================================
# 18. FINAL RESPONSE
# ============================================================

print("\n==========================================")
print("             FINAL RESPONSE")
print("==========================================")

print(final_answer)


print("\n==========================================")
print("              DEMO COMPLETE")
print("==========================================")