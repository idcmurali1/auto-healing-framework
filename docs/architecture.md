# System Architecture – Auto-Healing Test Framework

This framework detects test failures, retrieves similar context, generates a patch using an LLM, and validates it—all locally.

## 🧠 Architecture Workflow

1. **Failure Detection**  
   Triggered by simulated CI failure (can be extended with webhook integrations).

2. **Context Retrieval (Retriever Module)**  
   Uses FAISS + Sentence-BERT to find the most relevant prior failures.

3. **Prompt Construction (Prompt Builder)**  
   Formats the failure + context into a system/user JSON prompt for GPT-4.

4. **Patch Generation (LLM Generator)**  
   Uses OpenAI ChatCompletion API to suggest the fix.

5. **Validation (Sandbox Runner)**  
   Applies the patch to a temp file and validates via `pytest`.

6. **Result Orchestration**  
   Logs result, prints diff, and reports pass/fail summary.

## 🔁 Data Flow Diagram

```plaintext
[Test Failure] --> [Retriever] --> [Prompt Builder] --> [GPT-4 Patch Generator] --> [Validator] --> [Output]
```

## 🔒 Security

No test code or logs are stored. All patch generation is stateless, using in-memory prompts.

## 📌 Future Enhancements

- GitHub Actions webhook for real-time CI integration
- Support for multi-language test frameworks
- Secure token detection & masking in generated patches
