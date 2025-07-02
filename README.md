# Auto-Healing Test Framework

A local self-healing system powered by OpenAI's GPT models and vector-based context retrieval.

## Key Modules
- **Retriever**: FAISS-based failure similarity search
- **Prompt Builder**: Converts logs into GPT prompts
- **LLM Patch Generator**: Calls OpenAI API to generate fixes
- **Validator**: Runs patch in isolated test environment
- **CI Orchestrator**: Kicks off pipeline on failure

## Setup
1. Set `OPENAI_API_KEY` in `.env`
2. Run `pip install -r requirements.txt`
3. Trigger via `python orchestrator/ci_listener.py`

MIT License.
