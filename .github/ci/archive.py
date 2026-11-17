"""Keep the existing source archive hygiene gate behind the build command."""
from pathlib import Path
import subprocess
import zipfile

dist = Path("dist")
dist.mkdir(exist_ok=True)
archive = dist / "rldyour-antigravity-cli-source.zip"
subprocess.run(
    ["git", "archive", "--format=zip", "--prefix=rldyour-antigravity-cli/", "-o", str(archive), "HEAD"],
    check=True,
)
forbidden = (".git/", "__MACOSX/", ".venv/", ".pytest_cache/", ".serena/cache/", "__pycache__/", "node_modules/")
with zipfile.ZipFile(archive) as source:
    hits = [name for name in source.namelist() if any(part in name for part in forbidden)]
if hits:
    raise SystemExit(f"Forbidden archive entries: {hits[:20]}")
print("Source archive hygiene passed.")
