# Formal Agent: Multi-Agent Workflow for Lean Proofs

A LangGraph-based multi-agent system for automatically generating and verifying formal mathematical proofs in Lean 4.

## Architecture

This project implements a multi-agent workflow using LangChain and LangGraph:

```
┌─────────────┐
│   Planner   │  Generate proof strategy
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Prover    │  Write Lean 4 proof
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Verifier   │  Check proof with Lean
└──────┬──────┘
       │
       ├─── Success ──→ END
       │
       └─── Failure ──→ ┌─────────────┐
                        │   Critic    │  Provide feedback
                        └──────┬──────┘
                               │
                               └──→ Back to Prover
```

## Project Structure

```
formal_agent/
├── README.md                 # This file
├── data/                     # Problem datasets
│   └── putnam_1981_a1.json
├── lean_workspace/           # Lean 4 workspace
│   ├── lean-toolchain
│   ├── Main.lean
│   └── TmpCheck.lean         # Temporary verification file
├── agents/                   # Agent implementations
│   ├── planner_agent.py      # Generates proof plans
│   ├── prover_agent.py       # Writes Lean proofs
│   ├── verifier.py           # Verifies proofs
│   └── critic_agent.py       # Provides feedback
├── tools/                    # Agent tools (placeholder implementations)
│   ├── planner_tools.py      # Tools for planner agent
│   ├── prover_tools.py       # Tools for prover agent
│   └── critic_tools.py       # Tools for critic agent
├── schemas/                  # Pydantic schemas
│   ├── planner_schemas.py    # Planner tool input schemas
│   ├── prover_schemas.py     # Prover tool input schemas
│   ├── critic_schemas.py     # Critic tool input schemas
│   └── agent_outputs.py      # Agent output schemas (for JSON parsing)
├── workflow/                 # LangGraph workflow
│   ├── orchestrator_graph.py # Main workflow graph
│   └── nodes/                # Workflow node implementations
│       ├── planner_node.py
│       ├── prover_node.py
│       ├── verifier_node.py
│       └── critic_node.py
├── config/                   # Configuration
│   ├── model_config.yaml     # LLM model settings
│   └── paths.yaml            # File paths
├── utils/                    # Utilities
│   ├── io_utils.py           # I/O operations
│   ├── prompt_templates.py   # Prompt templates
│   └── types.py              # Type definitions
└── test_run.py               # Test script
```

## Installation

1. **Install Python dependencies:**

```bash
pip install langchain langchain-openai langgraph pyyaml python-dotenv
```

2. **Install Lean 4:**

Follow instructions at https://leanprover.github.io/lean4/doc/setup.html

3. **Set up environment variables:**

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

The agents will automatically load the API key from this file using `python-dotenv`.

## Usage

Run the test script on the sample problem:

```bash
cd formal_agent
python test_run.py
```

## How It Works

### State Flow

The workflow maintains a state dictionary with the following fields:

- `informal_statement`: The informal mathematical problem
- `lean4_statement`: The Lean 4 theorem formalization
- `plan_hint`: Strategic guidance from the planner
- `lean_candidate`: The generated Lean 4 proof code
- `verify_success`: Boolean indicating if verification passed
- `verify_log`: Output from the Lean verifier
- `critic_hint`: Feedback from the critic on failed attempts

**State Management Pattern:**

Each node in the workflow:

1. **Receives** the full state as `Dict[str, Any]`
2. **Processes** the relevant fields
3. **Returns** only the updated fields (partial state)
4. LangGraph **automatically merges** the partial update into the full state

Example:

```python
def my_node(state: Dict[str, Any]) -> Dict[str, Any]:
    result = process(state["input_field"])
    # Return only what changed
    return {"output_field": result}
```

This pattern ensures:

- Clear separation of concerns (each node only updates its output)
- No accidental state mutations
- Easy to track what each node modifies

### Agent Responsibilities

All agents are implemented using **LangChain's `create_agent` API** with specialized tools and structured output:

1. **Planner Agent**:

   - Analyzes the problem and generates a high-level proof strategy
   - **Tools**: `planner_tool_example` (placeholder - replace with actual tools)
   - **Output**: JSON format `{"plan": "..."}`

2. **Prover Agent**:

   - Writes complete Lean 4 proof code based on the plan and any critic feedback
   - **Tools**: `prover_tool_example` (placeholder - replace with actual tools)
   - **Output**: JSON format `{"lean_code": "..."}`

3. **Verifier**:

   - Runs Lean on the proof candidate and captures the result
   - No tools (pure subprocess execution)
   - **Output**: Updates state with `verify_success` and `verify_log`

4. **Critic Agent**:

   - Analyzes verification failures and provides actionable feedback
   - **Tools**: `critic_tool_example` (placeholder - replace with actual tools)
   - **Output**: JSON format `{"critique": "..."}`

**Structured Output:**

All agents use `ToolStrategy` with Pydantic models for structured output:

- Uses artificial tool calling for reliable structured output
- Works with any tool-capable LLM model
- Automatic validation against Pydantic schemas
- Built-in retry logic and error handling

### Workflow Logic

1. The **planner_node** generates an initial proof plan
2. The **prover_node** writes a Lean 4 proof
3. The **verifier_node** checks if the proof compiles
4. If successful → workflow ends
5. If failed → **critic_node** analyzes the error and provides feedback
6. Loop back to prover with critic feedback (max iterations applies)

## Configuration

### Model Configuration (`config/model_config.yaml`)

Configure different LLM models for each agent:

```yaml
planner:
  model_name: 'gpt-4'
  temperature: 0.3
  max_tokens: 2000
```

### Path Configuration (`config/paths.yaml`)

Configure file paths for the workspace:

```yaml
lean_workspace: 'lean_workspace'
tmp_check_file: 'lean_workspace/TmpCheck.lean'
```

## Extending the System

### Adding New Problems

Add JSON files to the `data/` directory with this format:

```json
{
  "problem_id": "unique_id",
  "informal_statement": "Problem description",
  "lean4_statement": "theorem ... := by sorry"
}
```

### Customizing Prompts

Edit the prompt templates in `utils/prompt_templates.py`:

- `PLANNER_SYSTEM_PROMPT`: Planning instructions
- `PROVER_SYSTEM_PROMPT`: Proof generation instructions
- `CRITIC_SYSTEM_PROMPT`: Critique instructions

All prompts are simple string templates formatted with Python's `.format()` method.

### Adding New Tools

**Note:** Current tool implementations are placeholders. Replace with actual implementations as needed.

To add new tools for an agent:

1. **Create the tool function** with the `@tool` decorator in `tools/*_tools.py`:

   ```python
   from langchain.tools import tool

   @tool
   def your_tool_name(input_param: str) -> str:
       """Tool description that will be used by the LLM.

       Args:
           input_param: Parameter description
       """
       # TODO: Implement actual logic here
       return f"Actual output for {input_param}"
   ```

2. **Add to agent** in `agents/*_agent.py`:

   ```python
   from formal_agent.tools.your_tools import your_tool_name

   tools = [planner_tool_example, your_tool_name]

   self.agent = create_agent(
       model=model,
       tools=tools,
       response_format=ToolStrategy(PlannerOutput)
   )
   ```

**Tool Implementation Status:**

- ⚠️ All tools currently return example/placeholder outputs
- ✅ Structure and integration are ready
- 🔧 Replace tool logic in `tools/*.py` files when ready

### Using Different LLM Providers

Modify the agent files to use different LangChain LLM classes (e.g., `ChatAnthropic`, `ChatOllama`).

## Requirements

- Python 3.8+
- LangChain
- LangGraph
- Lean 4
- OpenAI API key (or other LLM provider)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key
cp .env.example .env
# Edit .env and add your OpenAI API key

# 3. Run the test
python -m formal_agent.test_run
```

For detailed setup instructions, see [SETUP_GUIDE.md](../SETUP_GUIDE.md).
