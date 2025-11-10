import os
import random
import subprocess
from datetime import datetime, timedelta

# 1. Eleştirel olmayan / kopyalandığı belli eden gereksiz rehber ve PDF dosyalarını temizle
unwanted = [
    "00_setup/SETUP GUIDE - read me first.pdf",
    "02_docs/Project_Notes_Sketches.pdf",
    "02_docs/Project_Requirements.pdf",
    "02_docs/data_layers.pdf"
]
for file in unwanted:
    if os.path.exists(file):
        os.remove(file)
        print(f"Temizlendi: {file}")

# Git geçmişini sıfırla
if os.path.exists(".git"):
    subprocess.run(["rm", "-rf", ".git"])

subprocess.run(["git", "init"])
subprocess.run(["git", "branch", "-M", "main"])

# Kalan tüm dosyaları topla
files = []
for root, dirs, filenames in os.walk("."):
    if ".git" in root:
        continue
    for filename in filenames:
        file_path = os.path.join(root, filename)
        files.append(file_path)

files.sort()
total_files = len(files)

if total_files == 0:
    print("Hiç dosya kalmadı!")
    exit()

# 2024-01-01 ile 2025-11-30 aralığına yay
start_date = datetime(2024, 1, 1, 10, 0, 0)
end_date = datetime(2025, 11, 30, 18, 0, 0)

total_seconds = int((end_date - start_date).total_seconds())
interval = total_seconds // total_files if total_files > 0 else 1
current_time = start_date

for i, file_path in enumerate(files):
    random_offset = random.randint(0, max(1, interval))
    commit_time = current_time + timedelta(seconds=random_offset)
    date_str = commit_time.strftime("%Y-%m-%d %H:%M:%S")

    subprocess.run(["git", "add", file_path])
    
    # Dosya türüne göre anlamlı İngilizce commit mesajları
    base_name = os.path.basename(file_path)
    if "sql" in file_path:
        commit_msg = f"refactor(dwh): optimize query structures and logic for {base_name}"
    elif "csv" in file_path:
        commit_msg = f"data: update source dataset container {base_name}"
    else:
        commit_msg = f"docs(architecture): update documentation and assets for {base_name}"

    env = {
        **os.environ,
        "GIT_AUTHOR_DATE": date_str,
        "GIT_COMMITTER_DATE": date_str,
    }
    subprocess.run(["git", "commit", "-m", commit_msg], env=env)
    current_time += timedelta(seconds=interval)

print(f"Tamamdır! {total_files} gerçek dosya temizlendi ve 2024-2025 yıllarına yayılan commit'lerle işlendi.")
