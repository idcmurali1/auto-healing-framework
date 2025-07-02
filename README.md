# Auto-Healing Test Framework

This is a fully functional, local framework for autonomous test case healing using OpenAI's GPT models and a vector similarity retriever.

## 🔧 Components

- **Retriever** – Encodes and stores historical failure logs using `sentence-transformers` and searches with FAISS.
- **Prompt Builder** – Assembles failure info and retrieved context into a structured prompt.
- **LLM Patch Generator** – Calls OpenAI's GPT-4 to generate code fixes and rationale.
- **Validator** – Applies the fix to a test file and re-runs tests using `pytest`.
- **CI Orchestrator** – Simulates CI failure trigger and manages full repair workflow.

## 🚀 How It Works

```bash
# Setup
pip install -r requirements.txt
export OPENAI_API_KEY=your-key-here

# Run Orchestrator
python orchestrator/ci_listener.py
```

## 📂 Directory Structure

```
auto-healing-framework/
├── retriever/              # FAISS-based semantic retriever
├── prompt_builder/         # Prompt constructor for LLM input
├── llm_patch_generator/    # GPT-4 integration
├── validator/              # Test execution and validation
├── orchestrator/           # Entry point and control flow
├── examples/               # Sample test failures (future)
├── tests/                  # Unit tests for components
├── config/                 # Future prompt and config templates
└── docs/                   # Architecture and documentation
```

## 🛡 License

MIT License

© 2025 idcmurali1
