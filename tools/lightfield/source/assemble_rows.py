"""Build a clean 6x7 atlas from seven six-view reference sheets.

The generator determines appearance. This script only isolates, uniformly scales,
and places the existing raster specimens; it does not invent angles or anatomy.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[1]

def specimens(path):
    image=Image.open(path).convert('RGB')
    array=np.asarray(image)
    color=array.astype(float)
    mask=(color.mean(axis=2)<231)|((color.max(axis=2)-color.min(axis=2)>14)&(color.min(axis=2)<240))
    mask=ndimage.binary_closing(mask,iterations=2)
    labels,count=ndimage.label(mask)
    sizes=np.bincount(labels.ravel());sizes[0]=0
    selected=np.argsort(sizes)[-6:]
    if len(selected)!=6 or sizes[selected].min()<image.width*image.height*.008:
        raise ValueError(f'Cannot isolate six full specimens: {path}')
    objects=[]
    for label in selected:
        yy,xx=np.where(labels==label)
        objects.append(dict(label=int(label),cx=float(xx.mean()),cy=float(yy.mean()),bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]))
    vertical=sorted(objects,key=lambda o:o['cy'])
    ordered=sorted(vertical[:3],key=lambda o:o['cx'])+sorted(vertical[3:],key=lambda o:o['cx'])
    extracted=[]
    for item in ordered:
        x0,y0,x1,y1=item['bbox']
        pad=12
        x0=max(0,x0-pad);y0=max(0,y0-pad);x1=min(image.width,x1+pad);y1=min(image.height,y1+pad)
        # Retain the complete antialiased specimen, remove disconnected neighbors.
        keep=ndimage.binary_dilation(labels==item['label'],iterations=pad)
        crop=array[y0:y1,x0:x1].copy()
        crop[~keep[y0:y1,x0:x1]]=255
        extracted.append((Image.fromarray(crop),min(image.width/3,image.height/2),[x0,y0,x1,y1]))
    return extracted

def main():
    parser=argparse.ArgumentParser();parser.add_argument('mapping',type=Path)
    args=parser.parse_args();mapping=json.loads(args.mapping.read_text())
    elevations=[60,40,20,0,-20,-40,-60]
    rows=[specimens(args.mapping.resolve().parent / mapping[str(e)]) for e in elevations]
    maximum=max(max(tile.width,tile.height)/unit for row in rows for tile,unit,_ in row)
    factor=320/maximum
    atlas=Image.new('RGB',(2400,2800),'white');metadata=[]
    for b,row in enumerate(rows):
        for a,(tile,unit,bounds) in enumerate(row):
            size=(round(tile.width/unit*factor),round(tile.height/unit*factor))
            resized=tile.resize(size,Image.Resampling.LANCZOS)
            x=a*400+(400-size[0])//2;y=b*400+(400-size[1])//2
            atlas.paste(resized,(x,y))
            metadata.append(dict(row=b,column=a,elevation_target=elevations[b],yaw_target=a*60,source=mapping[str(elevations[b])],source_crop=bounds,placed_at=[x,y],placed_size=list(size)))
    target=ROOT/'source'/'atlas.png'
    atlas.save(target,format='PNG',compress_level=6)
    (ROOT/'source'/'atlas-calibration.json').write_text(json.dumps(metadata,indent=2))
    data=np.asarray(atlas)
    for b in range(7):
        for a in range(6):
            tile=data[b*400:(b+1)*400,a*400:(a+1)*400]
            assert tile[:35].min()==255 and tile[-35:].min()==255
            assert tile[:,:35].min()==255 and tile[:,-35:].min()==255
    print('PASS: 42 isolated specimens, 400px cells, common scale, clean borders >=35px.')

if __name__=='__main__':main()
