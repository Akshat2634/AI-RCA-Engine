from typing import TypedDict, Optional

class IncidentState(TypedDict,total=False):
    raw_logs:str
    parsed_summary:str
    rca_report:str


