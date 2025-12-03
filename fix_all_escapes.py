import re

with open(r'c:/Users/CHINMOY ROY/Desktop/k/english is power by kumu 2/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all literal \n occurrences in the JavaScript section
# This is more aggressive but should catch all instances
content = re.sub(r'\\n\\n\s+//', '\n\n        //', content)
content = re.sub(r'\\n\\n\s+const', '\n\n        const', content)

with open(r'c:/Users/CHINMOY ROY/Desktop/k/english is power by kumu 2/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all literal escape sequences")
