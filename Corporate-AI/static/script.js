async function submitProblem() {

    const problem =
        document.getElementById("problem").value.trim();


    if (!problem) {

        alert("Please describe the IT problem.");

        return;
    }


    // Reset UI

    resetAgents();


    // Show request in memory

    document.getElementById(
        "memory-request"
    ).innerText = problem;


    addActivity(
        "👤",
        "Employee",
        "Submitted IT request"
    );


    // Orchestrator

    setAgent(
        "orchestrator",
        "running",
        "Analyzing request..."
    );


    addActivity(
        "🤖",
        "Orchestrator Agent",
        "Analyzing the issue..."
    );


    try {

        const response = await fetch(
            "/api/solve",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    problem: problem
                })

            }
        );


        if (!response.ok) {

            throw new Error(
                "Backend request failed"
            );

        }


        const data =
            await response.json();


        // -------------------------
        // ORCHESTRATOR
        // -------------------------

        setAgent(
            "orchestrator",
            "completed",
            "Decision completed"
        );


        document.getElementById(
            "memory-decision"
        ).innerText =
            data.selected_agents.join(", ");


        addActivity(
            "🤖",
            "Orchestrator Agent",
            "Selected: " +
            data.selected_agents.join(", ")
        );


        // -------------------------
        // SPECIALISTS
        // -------------------------

        for (
            const agentName
            of data.selected_agents
        ) {

            const agentId =
                agentName.toLowerCase()
                + "-agent";


            setAgent(
                agentId,
                "running",
                "Investigating..."
            );


            addActivity(
                getAgentIcon(agentName),
                agentName + " Agent",
                "Investigation started..."
            );


            // Small visual delay
            // so students can see agents
            // working

            await sleep(800);


            const finding =
                data.findings[agentName];


            setAgent(
                agentId,
                "completed",
                finding
            );


            addActivity(
                "✅",
                agentName + " Agent",
                "Investigation completed"
            );

        }


        // -------------------------
        // MEMORY
        // -------------------------

        document.getElementById(
            "memory-findings"
        ).innerText =
            "Specialist findings collected";


        // -------------------------
        // RESOLUTION
        // -------------------------

        setAgent(
            "resolution",
            "running",
            "Analyzing all findings..."
        );


        addActivity(
            "🎯",
            "Resolution Agent",
            "Creating final resolution..."
        );


        await sleep(800);


        setAgent(
            "resolution",
            "completed",
            "Resolution generated"
        );


        document.getElementById(
            "final-answer"
        ).innerText =
            data.final_answer;


        addActivity(
            "✅",
            "Resolution Agent",
            "Final resolution completed"
        );

    }


    catch (error) {

        console.error(error);

        document.getElementById(
            "final-answer"
        ).innerText =
            "Unable to connect to the AI backend.";

    }

}


/* -----------------------------------
   SET AGENT STATUS
----------------------------------- */

function setAgent(
    agent,
    status,
    text
) {

    const element =
        document.getElementById(
            agent + "-agent"
        );


    if (!element) return;


    const badge =
        document.getElementById(
            agent + "-status"
        );


    element.classList.remove(
        "active-agent"
    );


    if (status === "running") {

        badge.innerText = "RUNNING";

        badge.className =
            "badge running";

        element.classList.add(
            "active-agent"
        );

    }


    else if (status === "completed") {

        badge.innerText = "COMPLETED";

        badge.className =
            "badge completed";

    }


    else {

        badge.innerText = "WAITING";

        badge.className =
            "badge waiting";

    }


    const textElement =
        document.getElementById(
            agent + "-text"
        );


    if (textElement) {

        textElement.innerText = text;

    }

}


/* -----------------------------------
   ACTIVITY FEED
----------------------------------- */

function addActivity(
    icon,
    agent,
    message
) {

    const activity =
        document.getElementById(
            "activity"
        );


    const item =
        document.createElement("div");


    item.className =
        "activity-item";


    item.innerHTML = `

        <span>${icon}</span>

        <div>

            <strong>${agent}</strong>

            <p>${message}</p>

        </div>

    `;


    activity.prepend(item);

}


/* -----------------------------------
   AGENT ICON
----------------------------------- */

function getAgentIcon(agent) {

    if (agent === "IDENTITY")
        return "👤";

    if (agent === "NETWORK")
        return "🌐";

    if (agent === "ENDPOINT")
        return "💻";

    return "🤖";
}


/* -----------------------------------
   RESET
----------------------------------- */

function resetAgents() {

    const agents = [
        "orchestrator",
        "identity",
        "network",
        "endpoint",
        "resolution"
    ];


    agents.forEach(
        agent => {

            const status =
                document.getElementById(
                    agent + "-status"
                );


            if (status) {

                status.innerText =
                    "WAITING";

                status.className =
                    "badge waiting";

            }

        }
    );


    document.getElementById(
        "activity"
    ).innerHTML = "";

}


/* -----------------------------------
   DELAY
----------------------------------- */

function sleep(ms) {

    return new Promise(
        resolve =>
            setTimeout(resolve, ms)
    );

}