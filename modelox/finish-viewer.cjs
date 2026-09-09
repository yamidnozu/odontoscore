const fs=require('fs');let s=fs.readFileSync('index.html','utf8');
const a=s.indexOf('let w0=(c)=>'),b=s.indexOf(',X1=',a);
if(a<0||b<0)throw Error('No se encontró control de cámara');
s=s.slice(0,a)+`let w0=(c)=>{const control=$.current;if(!control||!J.current)return;const camera=control.object;const box=new T6().setFromObject(J.current);const size=box.getSize(new h);const distance=Math.max(size.x,size.y,size.z)/Math.min(1,camera.aspect)/(2*Math.tan(camera.fov*Math.PI/360))*1.3;B(c==='reset'?'perspectiva':c);control.target.set(0,0,0);if(c==='lateral')camera.position.set(distance,0,0);else if(c==='oclusal')camera.position.set(0,distance,.001);else camera.position.set(0,0,distance);if(c==='reset')s(false);control.update()}`+s.slice(b);
fs.writeFileSync('index.html',s);
