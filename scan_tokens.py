import os
import re

print("="*60)
print("TOKEN SCANNER")
print("="*60)

print(f"\nEUID: {os.geteuid()}")
print(f"USER: {os.environ.get('USER', 'unknown')}")

patterns = {
    'Kaggle': r'CfDJ8[A-Za-z0-9]{50,}',
    'OpenAI': r'sk-[a-zA-Z0-9]{48}',
    'Anthropic': r'sk-ant-[a-zA-Z0-9_-]{40,}',
    'AWS': r'AKIA[0-9A-Z]{16}',
    'GitHub': r'ghp_[a-zA-Z0-9]{36}',
}

found = []
file_count = 0

for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith(('.py', '.json', '.yaml', '.yml', '.txt', '.md', '.env')):
            file_count += 1
            try:
                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    content = f.read()
                for name, pattern in patterns.items():
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if 'EXAMPLE' not in match:
                            found.append(f"{name}: {match[:50]} in {file}")
            except:
                pass

print(f"\nFiles scanned: {file_count}")
print(f"Tokens found: {len(found)}")
for f in found[:10]:
    print(f"  {f}")
if not found:
    print("  None found")
