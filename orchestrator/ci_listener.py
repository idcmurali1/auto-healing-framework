from retriever.vector_search import Retriever
from prompt_builder.builder import build_prompt
from llm_patch_generator.patcher import generate_patch
from validator.sandbox_runner import apply_patch_and_test

def main():
    r = Retriever()
    r.add_documents(["Selector changed on login button", "API schema mismatch on user profile"])
    context = r.query("Test failed on login screen")

    prompt = build_prompt("Login button not found", context)
    patch = generate_patch(prompt)

    print("Generated Patch:")
    print(patch)

    result = apply_patch_and_test(patch)
    print("Validation Result:")
    print(result)

if __name__ == "__main__":
    main()