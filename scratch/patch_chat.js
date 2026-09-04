const fs = require('fs');
const files = [
  'C:/Users/PREDATOR/AppData/Local/npm-cache/_npx/0d29dd9f4e472da9/node_modules/notebooklm-mcp/dist/notebooklm/chat.js',
  'C:/Users/PREDATOR/AppData/Local/npm-cache/_npx/16baa19dd5d31de6/node_modules/notebooklm-mcp/dist/notebooklm/chat.js'
];
for (const file of files) {
  if (fs.existsSync(file)) {
    let content = fs.readFileSync(file, 'utf8');
    // Replace the entire isPlaceholder function cleanly
    const isPlaceholderRegex = /function isPlaceholder\(text\) \{[\s\S]*?return false;\s*\}/;
    const replacement = `function isPlaceholder(text) {
    const lower = text.toLowerCase();
    if (PLACEHOLDER_SNIPPETS.some((s) => lower.includes(s)))
        return true;
    if (lower.includes("abriendo") || lower.includes("procesando") || lower.includes("descubriendo") || lower.includes("examinando") || lower.includes("buscando") || lower.includes("leyendo") || lower.includes("comprobando") || lower.includes("notas") || lower.includes("material") || lower.includes("respondiendo") || lower.includes("pensando"))
        return true;
    const trimmed = text.trim();
    if (text.length < 200 && (trimmed.endsWith("...") || trimmed.endsWith("\\u2026") || trimmed.includes("\\u2026") || trimmed.endsWith("…") || trimmed.includes("…")))
        return true;
    return false;
}`;
    content = content.replace(isPlaceholderRegex, replacement);
    fs.writeFileSync(file, content, 'utf8');
    console.log('Fixed:', file);
  }
}
