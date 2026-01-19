import json

with open('my_github_catalog_*.json') as f:
    data = json.load(f)

print("# My Projects\n")
categories = {
    "Syntax Diagrams": [],
    "Security Tools": [],
    "Infrastructure": [],
    "Web Development": [],
    "Graphics & Games": [],
}

for repo in data['analyses']:
    name = repo['name']
    desc = repo['suggested_description']
    if 'syntax' in name.lower():
        categories["Syntax Diagrams"].append(f"- [{name}](https://github.com/Notoriousjayy/{name}) - {desc}")
    # Add more categorization...

for category, repos in categories.items():
    if repos:
        print(f"\n## {category}\n")
        print("\n".join(repos))
