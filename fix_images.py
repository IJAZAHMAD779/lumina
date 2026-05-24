import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has getImageUrl
    if 'getImageUrl' in content:
        return False
    
    # Skip if no image paths
    if '"/images/' not in content and "`/images/" not in content:
        return False
    
    # Add import after other imports
    if content.startswith('import '):
        lines = content.split('\n')
        import_end = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('export '):
                import_end = i + 1
            else:
                break
        
        # Add import and const after imports
        insert_point = import_end
        lines.insert(insert_point, 'import { getImageUrl } from "../utils/imageUrl";')
        lines.insert(insert_point + 1, 'const img = (path) => getImageUrl(path);')
        lines.insert(insert_point + 2, '')
        
        content = '\n'.join(lines)
    
    # Fix simple string paths
    content = re.sub(r'src="(/images/[^"]*)"', r'src={img("\1")}', content)
    content = re.sub(r'icon="(/images/[^"]*)"', r'icon={img("\1")}', content)
    content = re.sub(r'url: "(/images/[^"]*)"', r'url: img("\1")', content)
    content = re.sub(r'icon: "(/images/[^"]*)"', r'icon: img("\1")', content)
    content = re.sub(r'avatarUrl: "(/images/[^"]*)"', r'avatarUrl: img("\1")', content)
    
    # Fix template literals
    content = re.sub(r'src=`(/images/[^`]*)`', r'src={img(`\1`)}', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

# Fix all JSX files
for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.jsx'):
            filepath = os.path.join(root, file)
            if fix_file(filepath):
                print(f"Fixed: {filepath}")

print("Done!")
