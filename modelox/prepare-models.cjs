const fs = require('node:fs');
const zlib = require('node:zlib');
const crypto = require('node:crypto');
const base = 'https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/';
const rows = n => fs.readFileSync('data/'+n,'utf8').trim().split(/\r?\n/).slice(1).map(x=>x.split('\t'));
const names = new Map(rows('isa_parts_list_e.txt').map(([id,rep,name])=>[id,{name,rep}]));
const elements = new Map();
for(const [id,name,file] of rows('isa_element_parts.txt')) {if(!elements.has(id)) elements.set(id,[]); elements.get(id).push(file);}
const boneIds=[52734,52735,52736,52738,52739,52740,52892,52893,53647,53648,53649,53650,52748,53655,53656,52788,52789,9710,54737,54738];
const teeth=[...names].filter(([id,x])=>/secondary.*tooth/.test(x.name)&&!/^third /.test(x.name)&&elements.get(id)?.length===1);
const entries=[...boneIds.map(id=>['FMA'+id,names.get('FMA'+id)]),...teeth].map(([id,x])=>({id:Number(id.slice(3)),name:x.name,representation:x.rep,files:elements.get(id),type:boneIds.includes(Number(id.slice(3)))?(/maxilla/.test(x.name)?'maxilla':/mandible/.test(x.name)?'mandible':'skull'):/incisor/.test(x.name)?'incisivo':/canine/.test(x.name)?'canino':/premolar/.test(x.name)?'premolar':'molar',jaw:/upper/.test(x.name)?'sup':/lower/.test(x.name)?'inf':'skull'}));
(async()=>{
const archiveUrl=base+'isa_BP3D_4.0_obj_99.zip';
const range=async(start,end)=>{const r=await fetch(archiveUrl,{headers:{Range:`bytes=${start}-${end}`}});if(r.status!==206)throw Error('El servidor no aceptó el rango HTTP');return Buffer.from(await r.arrayBuffer());};
const full=fs.existsSync('data/isa_BP3D_4.0_obj_99.zip');
const length=full?fs.statSync('data/isa_BP3D_4.0_obj_99.zip').size:Number((await fetch(archiveUrl,{method:'HEAD'})).headers.get('content-length'));
const zip=full?fs.readFileSync('data/isa_BP3D_4.0_obj_99.zip'):await range(length-65536,length-1);
let end=zip.length-22; while(end>=0&&zip.readUInt32LE(end)!==0x06054b50)end--;
if(end<0)throw Error('ZIP incompleto');
const directoryOffset=zip.readUInt32LE(end+16),directorySize=zip.readUInt32LE(end+12);
const directory=full?zip.subarray(directoryOffset,directoryOffset+directorySize):await range(directoryOffset,directoryOffset+directorySize-1);
let pos=0; const members=new Map();
while(pos+46<=directory.length&&directory.readUInt32LE(pos)===0x02014b50){const method=directory.readUInt16LE(pos+10),size=directory.readUInt32LE(pos+20),nl=directory.readUInt16LE(pos+28),el=directory.readUInt16LE(pos+30),cl=directory.readUInt16LE(pos+32),offset=directory.readUInt32LE(pos+42),name=directory.toString('utf8',pos+46,pos+46+nl);members.set(name.split('/').pop(),{method,size,offset});pos+=46+nl+el+cl;}
const models={},manifest=[];fs.mkdirSync('data/obj',{recursive:true});
for(const entry of entries){if(!entry.files?.length)throw Error('Sin elementos '+entry.id);for(const id of entry.files){if(models[id])continue;const m=members.get(id+'.obj');if(!m)throw Error('No existe '+id);const chunk=full?zip.subarray(m.offset):await range(m.offset,m.offset+30+1024+m.size);const start=30+chunk.readUInt16LE(26)+chunk.readUInt16LE(28);const data=chunk.subarray(start,start+m.size);const raw=m.method===8?zlib.inflateRawSync(data):data;if(!/^v /m.test(raw.toString())||!/^f /m.test(raw.toString()))throw Error('OBJ inválido');models[id]=raw.toString();fs.writeFileSync('data/obj/'+id+'.obj',raw);manifest.push({file:id+'.obj',sha256:crypto.createHash('sha256').update(raw).digest('hex')});}console.log('FMA'+entry.id);}
fs.writeFileSync('data/models.js','window.BP3D='+JSON.stringify({entries,models})+';');
fs.writeFileSync('data/provenance.json',JSON.stringify({source:base,archive:'isa_BP3D_4.0_obj_99.zip',archiveSha256:full?crypto.createHash('sha256').update(zip).digest('hex'):null,method:full?'full ZIP':'HTTP byte ranges from official ZIP',archiveBytes:length,downloaded:new Date().toISOString(),attribution:'BodyParts3D, © The Database Center for Life Science licensed under CC Attribution 4.0 International',entries,files:manifest},null,2));
console.log(entries.length+' estructuras, '+Object.keys(models).length+' OBJ oficiales');
})().catch(e=>{console.error(e);process.exit(1)});
