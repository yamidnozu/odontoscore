with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's see the order of sections in content
# We know where the component returns children:
# children: [v("style", ...), X("div", {className: "sticky top-0 ...}), section1, section2, section3, section4, section5, footer]

import re
pos_div = content.find('children:[v("style"')
print("pos of children:[v style:", pos_div)
snippet = content[pos_div:pos_div+1000]
print("Snippet:", snippet[:300])
