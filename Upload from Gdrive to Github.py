# ============================================
# ⚠️ FILL IN THESE 3 DETAILS ONLY!
# ============================================

GITHUB_USERNAME = ""         # Your GitHub username
GITHUB_TOKEN = ""      # Paste your generated token
REPO_NAME = ""              # Repository name on GitHub



# ✅ Already set correctly - DON'T CHANGE:
SOURCE_FOLDER = "Path to the Gdrive Folder"
BRANCH = "main"

# ============================================
# UPLOADS EVERYTHING AS-IS IN YOUR FOLDER
# ============================================

import os
import shutil
import time
import subprocess
from google.colab import drive
from IPython.display import clear_output

print("=" * 70)
print("🚀 UPLOAD EVERYTHING AS-IS")
print("=" * 70)

# Mount Google Drive
print("\n📂 Mounting Google Drive...")
drive.mount('/content/drive')
print("✅ Mounted!")

# Check source
if not os.path.exists(SOURCE_FOLDER):
    print(f"❌ Folder not found: {SOURCE_FOLDER}")
    raise SystemExit

# Count total files
print("\n🔍 Scanning files...")
total_files = 0
total_size = 0
for root, dirs, files in os.walk(SOURCE_FOLDER):
    total_files += len(files)
    for file in files:
        total_size += os.path.getsize(os.path.join(root, file))

total_size_gb = total_size / (1024**3)
print(f"📁 Files: {total_files}")
print(f"💾 Size: {total_size_gb:.2f} GB")

# Setup Git
print("\n🔧 Setting up Git...")
!apt-get update -qq 2>/dev/null
!apt-get install -qq git-lfs 2>/dev/null
!git lfs install --skip-smudge
!git config --global user.email "colab@github.com"
!git config --global user.name "Colab Upload"
!git config --global http.postBuffer 1572864000
!git config --global core.compression 0
print("✅ Done!")

# Clone repo
print(f"\n📥 Cloning repository...")
repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
!rm -rf {REPO_NAME}
!git clone {repo_url}
%cd {REPO_NAME}
print("✅ Cloned!")

# COPY EVERYTHING AS-IS
print(f"\n📁 Copying ALL files (preserving everything)...")
print("=" * 70)

copied = 0
start_time = time.time()

for root, dirs, files in os.walk(SOURCE_FOLDER):
    for file in files:
        src = os.path.join(root, file)
        rel_path = os.path.relpath(src, SOURCE_FOLDER)
        dst = os.path.join(os.getcwd(), rel_path)
        
        # Create subdirectories
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        # Copy file
        shutil.copy2(src, dst)
        copied += 1
        
        # Live progress every 10 files
        if copied % 10 == 0 or copied == total_files:
            elapsed = time.time() - start_time
            pct = (copied / total_files) * 100
            eta = (elapsed / copied) * (total_files - copied) if copied > 0 else 0
            
            clear_output(wait=True)
            print("=" * 70)
            print("📁 COPYING EVERYTHING")
            print("=" * 70)
            print(f"Progress: {copied}/{total_files} files ({pct:.1f}%)")
            print(f"Elapsed: {int(elapsed)}s | ETA: {int(eta)}s")
            print(f"Current: {rel_path[:80]}")
            print("=" * 70)

print(f"\n✅ All {copied} files copied!")

# ADD EVERYTHING TO GIT
print("\n📦 Adding everything to Git...")
!git add .
print("✅ Added!")

# COMMIT EVERYTHING
print("\n💾 Committing everything...")
!git commit -m "Upload complete project - all files"
print("✅ Committed!")

# PUSH EVERYTHING
print("\n🚀 Pushing everything to GitHub...")
print("(This may take a while for large files)")
print("=" * 70)

push_success = False
for attempt in range(1, 6):
    print(f"\n📤 Push attempt {attempt}/5...")
    
    try:
        result = subprocess.run(
            ['git', 'push', '-u', 'origin', BRANCH],
            capture_output=True,
            text=True,
            timeout=1800
        )
        
        if result.returncode == 0:
            push_success = True
            print("✅ PUSH SUCCESSFUL!")
            break
        else:
            print("❌ Push failed, retrying...")
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout, retrying...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    if attempt < 5:
        time.sleep(30)

# FINAL RESULT
clear_output(wait=True)
print("=" * 70)
if push_success:
    print("✅ SUCCESS! EVERYTHING UPLOADED!")
else:
    print("⚠️  Push incomplete - run manually:")
    print(f"   %cd {REPO_NAME}")
    print(f"   !git push -u origin {BRANCH}")
print("=" * 70)
print(f"📁 Files: {total_files}")
print(f"💾 Size: {total_size_gb:.2f} GB")
print(f"🔗 https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
print("=" * 70)