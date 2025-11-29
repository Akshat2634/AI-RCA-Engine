# 🔥 AI-RCA-Engine

An **automated Root Cause Analysis (RCA) system** that transforms raw production logs, alerts, traces, and metrics into comprehensive RCA reports with actionable fixes.

Built with [LangGraph](https://github.com/langchain-ai/langgraph) for **agentic, iterative, and production-grade** incident analysis.

---

## 🎯 What Does It Do?

This engine replicates what SREs and DevOps engineers manually do during incidents — but **automated**:

| Input                             | Output                       |
| --------------------------------- | ---------------------------- |
| Raw logs, metrics, alerts, traces | Structured incident timeline |
| Noisy error messages              | Root cause identification    |
| Multiple data sources             | Actionable remediation steps |

---

## 🧠 Multi-Agent Architecture

The system uses **5 specialized agents** orchestrated via LangGraph:

### 1. 📜 Log Parser Agent

Converts chaos into clarity.

**Input:**

- Raw application/system logs
- Metrics snapshots (CPU, memory, latency)
- Alerts from PagerDuty, NewRelic, Datadog, etc.

**Tasks:**

- Extract errors and exceptions
- Identify anomalies and spikes
- Group events by timestamp
- Detect latency patterns
- Transform noisy logs → structured JSON

---

### 2. 🔍 Context Enricher Agent

Adds depth and understanding to parsed data.

**Tasks:**

- Correlate errors with deployment events
- Link alerts to specific services/pods
- Fetch historical incident data
- Add service dependency context

---

### 3. 🎯 Root Cause Analyzer Agent

The detective of the system.

**Tasks:**

- Identify the probable root cause
- Score confidence levels
- Map error propagation paths
- Distinguish symptoms from causes

---

### 4. 📝 RCA Writer Agent

Generates human-readable reports.

**Output:**

- Executive summary
- Detailed timeline of events
- Root cause explanation
- Evidence and supporting data
- Impact assessment

---

### 5. 🛠️ Remediation Agent

Provides actionable next steps.

**Output:**

- Immediate fixes
- Long-term preventive measures
- Runbook suggestions
- Similar past incidents and resolutions

---

## 🏗️ Project Structure

```
ai_rca_engine/
├── src/
│   ├── main.py                 # Entry point
│   ├── graph/
│   │   ├── rca_graph.py        # LangGraph workflow definition
│   │   └── runner.py           # Graph execution logic
│   ├── agents/
│   │   ├── log_parser.py       # Log parsing agent
│   │   ├── context_enricher.py # Context enrichment agent
│   │   ├── root_cause.py       # Root cause analysis agent
│   │   ├── rca_writer.py       # Report generation agent
│   │   └── remediation.py      # Fix recommendation agent
│   ├── llm/
│   │   ├── client.py           # LLM client wrapper
│   │   ├── utils.py            # LLM utilities
│   │   └── prompts/
│   │       ├── log_parser_prompt.txt
│   │       └── rca_writer_prompt.txt
│   └── models/
│       └── state.py            # State definitions (TypedDict)
├── tests/
│   ├── test_graph.py
│   └── test_parser.py
├── pyproject.toml
└── poetry.lock
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AI-RCA-Engine.git
cd AI-RCA-Engine/ai_rca_engine

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Add your API keys (OpenAI, Anthropic, etc.)
```

### Run the Engine

```bash
# Basic usage
poetry run python src/main.py

# With custom logs
poetry run python src/main.py --input logs/incident_2025_11_29.log
```

---

## ⚙️ Configuration

Create a `.env` file:

```env
# LLM Configuration
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Observability
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=ai-rca-engine
```

---

## 📊 Example Output

**Input:** Raw Kubernetes pod logs with database connection failures

**Output:**

```
╔══════════════════════════════════════════════════════════════╗
║                    ROOT CAUSE ANALYSIS                        ║
╠══════════════════════════════════════════════════════════════╣
║ Incident ID: INC-2025-1129-001                               ║
║ Severity: P1 (Critical)                                       ║
║ Duration: 10:01:05 - 10:15:32 (14 min 27 sec)                ║
╠══════════════════════════════════════════════════════════════╣
║ ROOT CAUSE                                                    ║
║ Database connection pool exhaustion caused by                 ║
║ unclosed connections in payment-service v2.3.1                ║
║ Confidence: 94%                                               ║
╠══════════════════════════════════════════════════════════════╣
║ TIMELINE                                                      ║
║ • 10:01:02 - Deployment of payment-service v2.3.1            ║
║ • 10:01:05 - First DB connection error                        ║
║ • 10:05:00 - Connection pool at 100% capacity                ║
║ • 10:08:00 - Cascading failures to order-service             ║
╠══════════════════════════════════════════════════════════════╣
║ RECOMMENDED FIXES                                             ║
║ 1. Rollback payment-service to v2.3.0                        ║
║ 2. Increase connection pool size (temporary)                  ║
║ 3. Fix: Add connection.close() in PaymentProcessor           ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🔄 LangGraph Workflow

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  START      │────▶│  Log Parser      │────▶│ Context Enricher│
└─────────────┘     └──────────────────┘     └────────┬────────┘
                                                      │
                                                      ▼
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    END      │◀────│  Remediation     │◀────│ Root Cause      │
└─────────────┘     └──────────────────┘     │ Analyzer        │
                            ▲                └────────┬────────┘
                            │                         │
                            │    ┌──────────────┐     │
                            └────│  RCA Writer  │◀────┘
                                 └──────────────┘
```

---

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test
poetry run pytest tests/test_graph.py -v
```

---

## 🛣️ Roadmap

- [x] Basic log parsing
- [x] LangGraph integration
- [ ] Multi-LLM support (OpenAI, Anthropic, local models)
- [ ] Real-time log streaming
- [ ] Slack/PagerDuty integration
- [ ] Vector store for historical incidents
- [ ] Web UI dashboard
- [ ] Kubernetes operator

---

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) - For the amazing agentic framework
- [LangChain](https://github.com/langchain-ai/langchain) - For LLM tooling

---

<p align="center">
  Built with ❤️ for SREs who are tired of 3 AM incidents
</p>
