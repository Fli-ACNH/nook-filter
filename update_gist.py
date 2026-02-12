import os, json, requests

token = os.getenv('GIST_TOKEN')
gist_id = "570cf10db5dd7418cb7ea428782ed417"
# Handle the toJson() string from GitHub Actions
raw_entry = os.getenv('NEW_ENTRY')
new_entry = json.loads(raw_entry)

# 1. Fetch current Gist
res = requests.get(f"https://api.github.com/gists/{gist_id}")
gist_data = res.json()

if 'files' not in gist_data:
    print(f"Error fetching Gist: {gist_data.get('message')}")
    exit(1)

# 2. Extract content from 'links.json'
file_name = 'links.json'
if file_name not in gist_data['files']:
    print(f"Error: {file_name} not found in Gist. Available files: {list(gist_data['files'].keys())}")
    exit(1)

content = json.loads(gist_data['files'][file_name]['content'])

t = new_entry['type']
val = new_entry['url'].lower()

# 3. Add to the correct list
if t == 'BAN':
    if val not in content['instantBanLinks']:
        content['instantBanLinks'].append(val)
elif t == 'BLOCK':
    if val not in content['blockedLinks']:
        content['blockedLinks'].append(val)
else:
    if not any(e['url'] == val for e in content['links']):
        content['links'].append({"url": val, "global": True, "channels": []})

# 4. Push update back to GitHub
payload = {"files": {file_name: {"content": json.dumps(content, indent=2)}}}
update_res = requests.patch(
    f"https://api.github.com/gists/{gist_id}", 
    headers={"Authorization": f"token {token}"}, 
    json=payload
)

if update_res.status_code == 200:
    print(f"Successfully added {val} to {t}")
else:
    print(f"Failed to update Gist: {update_res.status_code} - {update_res.text}")
