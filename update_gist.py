import os, json, requests

token = os.getenv('GIST_TOKEN')
gist_id = "570cf10db5dd7418cb7ea428782ed417"
new_entry = json.loads(os.getenv('NEW_ENTRY'))

# 1. Fetch current Gist
res = requests.get(f"https://api.github.com/gists/{gist_id}")
gist_data = res.json()
# Ensure we target 'links.json' exactly
content = json.loads(gist_data['files']['links.json']['content'])

t = new_entry['type']
val = new_entry['url'].lower() # Keep it lowercase for the bot

# 2. Add to the correct list
if t == 'BAN':
    if val not in content['instantBanLinks']:
        content['instantBanLinks'].append(val)
elif t == 'BLOCK':
    if val not in content['blockedLinks']:
        content['blockedLinks'].append(val)
else:
    # For whitelists, check if already exists
    if not any(e['url'] == val for e in content['links']):
        content['links'].append({"url": val, "global": True, "channels": []})

# 3. Push update
payload = {"files": {"links.json": {"content": json.dumps(content, indent=2)}}}
requests.patch(f"https://api.github.com/gists/{gist_id}", 
               headers={"Authorization": f"token {token}"}, 
               json=payload)
