from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END, START


class IncidentState(TypedDict,total=False):
    raw_logs:str
    parsed_summary:str
    rca_report:str


def log_parser_node(state: IncidentState) -> dict:
    raw_logs = state.get("raw_logs", "")
    # For now, super naive: just count "ERROR" and lines
    lines = raw_logs.strip().splitlines()
    error_lines = [l for l in lines if "ERROR" in l or "Error" in l]

    summary = (
        f"Total lines: {len(lines)}. "
        f"Error lines: {len(error_lines)}. "
        f"Sample error: {error_lines[0] if error_lines else 'None'}"
    )

    return {"parsed_summary": summary}



def rca_writer_node(state: IncidentState) -> dict:
    parsed_summary = state.get("parsed_summary", "")
    raw_logs = state.get("raw_logs", "")

    # Super simplified "RCA":
    report = f"""
        Root Cause Analysis (Draft)

        1. Summary of Logs
        {parsed_summary}

        2. Probable Root Cause
        Based on the presence of errors in the logs, the issue is likely related to a failing component.
        More advanced logic will refine this.

        3. Evidence
        Sample logs:
        {raw_logs[:500]}  # truncate to avoid huge output
        """

    return {"rca_report": report}


workflow = StateGraph(IncidentState)

workflow.add_node("log_parser", log_parser_node)
workflow.add_node("rca_writer", rca_writer_node)

workflow.add_edge(START, "log_parser")
workflow.add_edge("log_parser", "rca_writer")
workflow.add_edge("rca_writer", END)

app = workflow.compile()


if __name__ == "__main__":
    sample_logs = """
    2025-11-27 10:01:02 INFO Starting service api-gateway
    2025-11-27 10:01:05 ERROR Failed to connect to database
    2025-11-27 10:01:06 ERROR Retry attempt 1 failed
    2025-11-27 10:01:07 WARN Falling back to read-only mode
    """

    initial_state: IncidentState = {
        "raw_logs": sample_logs
    }

    final_state = app.invoke(initial_state)

    print("=== Parsed Summary ===")
    print(final_state["parsed_summary"])

    print("\n=== RCA Report ===")
    print(final_state["rca_report"])