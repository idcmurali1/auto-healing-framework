import subprocess
import tempfile
import os

def apply_patch_and_test(patch_content):
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "test_sample.py")
    with open(test_file, "w") as f:
        f.write(patch_content)
    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    return result.stdout