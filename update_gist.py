import os, json, requests

# Get secrets from GitHub Environment
token = os.getenv('GIST_TOKEN')
gist_id = "570cf10db5dd7418cb7ea428782ed417" # Your Link Gist ID
new_entry = json.loads(os.getenv('NEW_ENTRY')) # Data from the website

# 1. Fetch current Gist data
res = requests.get(f"https://api.github.com/gists/{gist_id}")
gist_data = res.json()
content = json.loads(gist_data['files']['links.json']['content'])

# 2. Add the new entry based on type
t = new_entry['type']
val = new_entry['url']

if t == 'BAN': content['instantBanLinks'].append(val)
elif t == 'BLOCK': content['blockedLinks'].append(val)
else: content['links'].append({"url": val, "global": True, "channels": []})

# 3. Push back to GitHub
payload = {"files": {"links.json": {"content": json.dumps(content, indent=2)}}}
requests.patch(f"https://api.github.com/gists/{gist_id}", 
               headers={"Authorization": f"token {token}"}, 
               json=payload)
