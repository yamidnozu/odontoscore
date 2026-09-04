import { build } from 'esbuild';
import { createRequire } from 'node:module';
import { readFile } from 'node:fs/promises';
import assert from 'node:assert/strict';
import { performance } from 'node:perf_hooks';

await build({entryPoints:['source/App.template.tsx'],bundle:true,platform:'node',format:'cjs',outfile:'/tmp/lf-decoder.cjs',define:{'process.env.NODE_ENV':'"production"'}});
const require=createRequire(import.meta.url);
const {bilinearSample,decodePixels}=require('/tmp/lf-decoder.cjs');
const rgba=await readFile('/tmp/lf-encoded.rgba');
const encoded={width:2400,height:2800,data:new Uint8ClampedArray(rgba)};
const output={width:400,height:400,data:new Uint8ClampedArray(400*400*4)};
const sample=new Uint8ClampedArray(4);
bilinearSample({width:2,height:2,data:new Uint8ClampedArray([0,0,0,255,100,20,40,255,40,120,20,255,200,220,240,255])},.25,.75,sample,0);
// Weights: 3/16, 1/16, 9/16, 3/16. Expected RGB: 66.25,110,58.75.
assert.deepEqual([...sample],[66,110,59,255]);
for(let b=0;b<7;b++)for(let a=0;a<6;a++){
  decodePixels(encoded,a,b,output);
  for(let t=0;t<400;t++)for(let s=0;s<400;s++){
    const from=((t*7+b)*2400+s*6+a)*4,to=(t*400+s)*4;
    for(let c=0;c<4;c++)assert.equal(output.data[to+c],encoded.data[from+c]);
  }
}
decodePixels(encoded,5.9,6.9,output);
for(let s=0;s<400;s++)assert.equal(output.data[s*4],encoded.data[(6*2400+s*6+5)*4]);
const times=[];for(let i=0;i<24;i++){const start=performance.now();decodePixels(encoded,(i*.271)%5,(i*.381)%6,output);times.push(performance.now()-start);}times.sort((a,b)=>a-b);
console.log(JSON.stringify({four_neighbor_bilinear:'PASS',all_42_integer_views:'PASS',boundary_clamping:'PASS',decode_ms_median:times[12],decode_ms_p95:times[22],source_png_bytes:rgba.length},null,2));
