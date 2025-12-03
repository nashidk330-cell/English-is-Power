with open(r'c:/Users/CHINMOY ROY/Desktop/k/english is power by kumu 2/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the literal \n\n on line 981
content = content.replace('\\n\\n        const root', '\n\n        const root')

with open(r'c:/Users/CHINMOY ROY/Desktop/k/english is power by kumu 2/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed literal escape sequences in index.html")
