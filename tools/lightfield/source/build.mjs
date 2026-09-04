import { build } from 'esbuild';
import { readFile, writeFile } from 'node:fs/promises';

const png=await readFile('dist/lightfield_encoded.png');
const template=await readFile('source/App.template.tsx','utf8');
const app=template.replace('__ENCODED_PNG_DATA_URI__','data:image/png;base64,'+png.toString('base64'));
await writeFile('source/App.tsx',app);
await build({stdin:{contents:"import React from 'react';import{createRoot}from'react-dom/client';import App from './source/App.tsx';createRoot(document.getElementById('root')).render(<App/>);",resolveDir:process.cwd(),loader:'tsx'},bundle:true,minify:true,format:'iife',target:['es2020'],define:{'process.env.NODE_ENV':'"production"'},outfile:'dist/lightfield-app.js'});
const js=await readFile('dist/lightfield-app.js','utf8');
await writeFile('dist/index.html','<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Una sola imagen = 3D</title></head><body><div id="root"></div><script>'+js.replaceAll('</script','<\\/script')+'</script></body></html>');
console.log('Built standalone React page and complete App.tsx; PNG embedded as base64.');
