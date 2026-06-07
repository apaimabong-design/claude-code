import os
import re

print("="*60)
print("TOKEN SCANNER")
print("="*60)

# Check root status
print(f"\n[ROOT STATUS]")
print(f"EUID: {os.geteuid()}")
print(f"USER: {os.environ.get('USER', 'unknown')}")

if os.geteuid() != 0:
    print("Not running as root. Scan limited to current directory.")
    search_paths = ['.']
else:
    print("Running as root! Scanning entire filesystem.")
    search_paths = ['/']

# Patterns to search
patterns = {
    'Kaggle_API': r'CfDJ8[A-Za-z0-9]{50,}',
    'Kaggle_JWT': r'eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
    'OpenAI': r'sk-[a-zA-Z0-9]{48}',
    'Anthropic': r'sk-ant-[a-zA-Z0-9_-]{40,}',
    'AWS_Access': r'AKIA[0-9A-Z]{16}',
    'GitHub_Token': r'ghp_[a-zA-Z0-9]{36}',
    'JWT': r'eyJ[a-zA-Z0-9_-]{50,}\.[a-zA-Z0-9_-]{50,}\.[a-zA-Z0-9_-]{50,}',
}

found_tokens = {}
file_count = 0

def scan_file(filepath):
    global file_count
    try:
        size = os.path.getsize(filepath)
        if size > 1024 * 1024:
            return
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(50000)
        
        for name, pattern in patterns.items():
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ''
                if match and len(match) > 10:
                    if 'EXAMPLE' not in match and 'example' not in match:
                        if name not in found_tokens:
                            found_tokens[name] = []
                        if match not in found_tokens[name]:
                            found_tokens[name].append(match[:100])
                            print(f"  FOUND {name} in {filepath}")
                            return
    except:
        pass

print(f"\n[SCANNING]")
for search_path in search_paths:
    print(f"Searching in: {search_path}")
    
    for root, dirs, files in os.walk(search_path):
        if '.git' in root or 'node_modules' in root or '.cache' in root:
            continue
        
        for file in files:
            if file.endswith(('.json', '.yaml', '.yml', '.conf', '.config', '.env', '.txt', '.py', '.ini', '.pem', '.key')):
                file_count += 1
                scan_file(os.path.join(root, file))
                
                if file_count % 100 == 0:
                    print(f"  Scanned {file_count} files...")

print(f"\n[SCAN COMPLETE]")
print(f"Files scanned: {file_count}")
print(f"Tokens found: {len(found_tokens)}")

for name, tokens in found_tokens.items():
    print(f"\n{name}:")
    for t in tokens[:3]:
        print(f"  {t[:80]}")

if not found_tokens:
    print("\nNo tokens found")

# Environment variables
print(f"\n[ENVIRONMENT VARIABLES]")
for key, value in os.environ.items():
    if any(x in key.upper() for x in ['TOKEN', 'KEY', 'SECRET']):
        print(f"  {key}: {value[:20]}...")
