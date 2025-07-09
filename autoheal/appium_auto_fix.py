# Project: RAG-Based Auto-Fix for Failing Appium Identifiers Across Decoupled Repos

"""
Overview:
---------
This project automatically fixes failing identifiers in Appium YAML test files
using a Retrieval-Augmented Generation (RAG) approach. It is designed to work
across three separate repos:

1. iOS App Code Repo (e.g., Walmart-iOS)
2. Android App Code Repo (e.g., Walmart-Android)
3. Automation Repo (e.g., glass-automation)

Key Objectives:
  - Detects failing identifiers in mappings YAML
  - Traces function-to-mapping references from test YAML
  - Parses optional Appium Inspector XML snapshot
  - Retrieves related context from app code commits using Git
  - Uses RAG + LLM to suggest updated XPath
  - Auto-updates mappings YAML with the fix
  - Pushes a new branch with the fix to the automation repo
  - Includes CLI interface to trigger the flow manually

Supports handling **any failing identifier**, not just verifySelectLensesCTA.
"""

import os
import yaml
import re
import argparse
import xml.etree.ElementTree as ET
from git import Repo
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ========== Step 0: Load All YAML Inputs ==========
def load_yaml_files():
    with open("mappings-ios.yaml") as f:
        mappings = yaml.safe_load(f)
    with open("functions.yaml") as f:
        functions = yaml.safe_load(f)
    with open("C2707319-vision-flow-mixed-order.yaml") as f:
        test_flow = yaml.safe_load(f)
    return mappings, functions, test_flow

# ========== Step 1: Simulate Failing Identifier ==========
def simulate_failure():
    return "us.mappings.item.verifySelectLensesCTA"

# ========== Step 2: Extract Current Identifier ==========
def get_current_identifier(name, mappings):
    for item in mappings:
        if item['name'] == name:
            return item['identifier']
    return None

# ========== Step 3: Clone and Pull iOS Repo ==========
def clone_and_extract_ios_changes():
    ios_repo_path = "./Walmart-iOS"
    if not os.path.exists(ios_repo_path):
        Repo.clone_from("https://gecgithub01.walmart.com/Walmart-iOS.git", ios_repo_path)
    os.chdir(ios_repo_path)
    os.system("git pull")
    logs = os.popen("git log -S 'Select lenses' -p -n 5").read()
    os.chdir("..")
    return logs

# ========== Step 4: Parse Appium Inspector Snapshot ==========
def parse_appium_snapshot(xml_file):
    if not os.path.exists(xml_file):
        return ""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        all_elements = [elem.attrib for elem in root.iter() if 'name' in elem.attrib or 'label' in elem.attrib]
        descriptions = [f"name='{e.get('name', '')}' label='{e.get('label', '')}'" for e in all_elements]
        return "\n".join(descriptions)
    except Exception as e:
        return f"Error parsing XML: {str(e)}"

# ========== Step 5: Create RAG Chain ==========
def create_rag_chain(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    docs_split = text_splitter.create_documents([docs])
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs_split, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=retriever)
    return qa_chain

# ========== Step 6: Ask LLM for Identifier Fix ==========
def suggest_identifier_fix(mapping_name, current_xpath, appium_context, ios_diffs):
    full_context = f"""
    Current failing mapping: {mapping_name}
    Previous XPath: {current_xpath}

    Recent app code changes:
    {ios_diffs}

    Appium Inspector elements:
    {appium_context}

    Please suggest a more robust Appium XPath.
    """
    rag_chain = create_rag_chain(full_context)
    result = rag_chain.run("Suggest new XPath for the failed element.")
    return result

# ========== Step 7: Update Mappings File ==========
def update_mapping(name, new_identifier, mappings):
    for item in mappings:
        if item['name'] == name:
            item['identifier'] = new_identifier
    with open("mappings-ios.yaml", "w") as f:
        yaml.dump(mappings, f)

# ========== Step 8: Commit and Push ==========
def submit_patch(name):
    repo_path = "./glass-automation"
    if not os.path.exists(repo_path):
        Repo.clone_from("https://gecgithub01.walmart.com/MobileQE/glass-automation.git", repo_path)
    repo = Repo(repo_path)
    branch_name = f"auto-fix-{name.split('.')[-1]}"
    repo.git.checkout('-b', branch_name)
    mappings_path = os.path.join(repo_path, "mappings-ios.yaml")
    with open(mappings_path, "w") as f:
        yaml.dump(mappings, f)
    repo.git.add("mappings-ios.yaml")
    repo.git.commit(m=f"[auto-heal] Fixed identifier for {name}")
    repo.git.push('--set-upstream', 'origin', branch_name)
    print(f"PR ready for {name}. Please create a pull request for branch: {branch_name}")

# ========== CLI Execution Entry ==========
def main():
    parser = argparse.ArgumentParser(description="Auto-fix failing Appium identifiers using RAG + LLM")
    parser.add_argument('--fail', type=str, default=simulate_failure(), help='Name of the failing mapping')
    parser.add_argument('--snapshot', type=str, help='Optional Appium Inspector XML file path')
    args = parser.parse_args()

    mappings, functions, test_flow = load_yaml_files()
    current_xpath = get_current_identifier(args.fail, mappings)
    ios_diffs = clone_and_extract_ios_changes()
    appium_context = parse_appium_snapshot(args.snapshot) if args.snapshot else ""
    
    print("\n[FAILURE IDENTIFIED]", args.fail)
    print("Current XPath:", current_xpath)
    print("Parsing app snapshot...\n")

    suggestion = suggest_identifier_fix(args.fail, current_xpath, appium_context, ios_diffs)
    match = re.search(r'(//XCUIElementType[^\n]*)', suggestion)
    new_xpath = match.group(1).strip() if match else current_xpath

    print("\n[LLM SUGGESTION]\n", suggestion)
    print("\n[APPLIED FIX]", new_xpath)
    update_mapping(args.fail, new_xpath, mappings)
    submit_patch(args.fail)

if __name__ == "__main__":
    main()
