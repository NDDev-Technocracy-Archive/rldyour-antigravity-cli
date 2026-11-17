"""Check Python grammar and shell syntax without executing the adapter."""
import ast
from pathlib import Path
import subprocess

files = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
python_files = [Path(name) for name in files if name.endswith(".py")]
shell_files = [name for name in files if name.endswith(".sh")]
for path in python_files:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path), feature_version=(3, 13))
for name in shell_files:
    subprocess.run(["bash", "-n", name], check=True)
subprocess.run(["git", "diff", "--check"], check=True)
print(f"Checked {len(python_files)} Python files and {len(shell_files)} shell files.")
