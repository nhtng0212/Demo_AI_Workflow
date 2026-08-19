import subprocess
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

# file .env
load_dotenv()

# Path
SCRIPT_PATH = Path(__file__).parent.resolve() / "auto_push.sh"


# State
class AgentState(TypedDict):
    user_request: str
    intent: str
    final_answer: str


# Node
def classify_node(state: AgentState):
    """
    Node: Classifier
    Calls Gemini to classify the user's intent based on their request.
    """
    print(f"-> @@@ [Classifier Node] Analyzing: '{state['user_request']}'")

    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest", temperature=0, max_retries=3
    )

    # Define the prompt messages
    messages = [
        SystemMessage(
            content="You are a classification system. Read the user request. If the request is about pushing code to git, return exactly 'git_push'. For any other request, return exactly 'unknown'. DO NOT EXPLAIN."
        ),
        HumanMessage(content=state["user_request"]),
    ]

    # Call the LLM and clean result
    response = llm.invoke(messages)

    # Handle response
    raw_content = response.content

    if isinstance(raw_content, list):
        text_content = ""
        for item in raw_content:
            if isinstance(item, dict) and "text" in item:
                text_content += item["text"]
            elif isinstance(item, str):
                text_content += item

        ai_result = text_content.strip().lower()
    else:
        ai_result = str(raw_content).strip().lower()

    return {"intent": ai_result}


def run_git_node(state: AgentState):
    """
    Node: Git Executor
    Executes the auto_push.sh bash script using subprocess.
    """
    print(f"-> @@@ [Git Node] Executing script: {SCRIPT_PATH}")

    try:
        result = subprocess.run(
            ["bash", "auto_push.sh"], capture_output=True, text=True, check=True
        )

        # Check
        if result.returncode == 0:
            final_result = f"Git push successful!\nLog:\n{result.stdout}"
        else:
            final_result = f"Error during git push:\n{result.stderr}"
    except FileNotFoundError:
        final_result = f"File not found: {"auto_push.sh"}. Did you create it?"
    except Exception as e:  # noqa: BLE001
        final_result = f"Unexpected system error: {e}"

    return {"final_answer": final_result}


def not_supported_node(state: AgentState):
    """
    Node: Fallback
    Handles request that are out of scope.
    """
    print("-> [Fallback Node] Feature not supported.")
    return {"final_answer": "Xin lỗi. Chưa có chức năng này!"}


def route_request(state: AgentState) -> str:
    """
    Router: Decides the next node based on the intent.
    """
    if state["intent"] == "git_push":
        return "GitPush"
    else:
        return "NotSupported"


def main():
    # Initialize Graph
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("Classifier", classify_node)
    workflow.add_node("GitPush", run_git_node)
    workflow.add_node("NotSupported", not_supported_node)

    # Start Node
    workflow.set_entry_point("Classifier")

    # Set conditional edges
    workflow.add_conditional_edges(
        "Classifier",
        route_request,
        {"GitPush": "GitPush", "NotSupported": "NotSupported"},
    )

    # Set ending points
    workflow.add_edge("GitPush", END)
    workflow.add_edge("NotSupported", END)

    # Compile the graph
    app = workflow.compile()

    while True:
        print("\n\n\n")
        input_text = input("[INPUT] Nhập yêu cầu của bạn:")

        # Run a test case
        print("\n STARTING WORKFLOW")
        initial_state = {
            "user_request": input_text,
            "intent": "",
            "final_answer": "",
        }

        result = app.invoke(initial_state)

        print("\n FINAL RESULT")
        print(result["final_answer"])


if __name__ == "__main__":
    main()
