from fabric import task, Connection

# 2026 BMB Hybrid Pipeline Configuration
# Host 'dgx-spark' must be defined in your ~/.ssh/config
REMOTE_HOST = "dgx-spark"
REMOTE_DIR = "~/projects/2026_BMB"

@task
def sync(c):
    """[Local -> DGX] rsync local files to the DGX server."""
    print(f"🚀 Syncing 2026_BMB to {REMOTE_HOST}...")
    # Excluding .git and local large datasets to save time
    c.local(f"rsync -avz --exclude='.git' --exclude='node_modules' ./ {REMOTE_HOST}:{REMOTE_DIR}")
    print("✅ Sync complete.")

@task
def remote_test(c):
    """[DGX] Run a quick test on the DGX server to verify GPU visibility."""
    sync(c)
    print("🔍 Testing DGX Environment...")
    with c.cd(REMOTE_DIR):
        c.run("nvidia-smi")
        c.run("python3 --version")

@task
def build_rag(c):
    """[Hybrid] Sync local data and build RAG index on DGX GPU."""
    sync(c)
    print("🧠 Starting RAG indexing on DGX (GPU enabled)...")
    with c.cd(REMOTE_DIR):
        # Assumes scripts/build_rag.py exists on remote
        c.run("python3 scripts/build_rag.py")
    
    print("📥 Pulling processed Vector DB back to local Mac...")
    c.get(f"{REMOTE_DIR}/data/vector_db.index", local="./data/remote_index.db")
    print("✨ Hybrid RAG build completed.")
