import jsbeautifier

with open('scratch/line24.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Try to beautify or extract JSX/X calls
beautified = jsbeautifier.beautify(code) if hasattr(jsbeautifier, 'beautify') else code
with open('scratch/component_readable.js', 'w', encoding='utf-8') as f:
    f.write(beautified)

print("Readable component saved. Length:", len(beautified))
