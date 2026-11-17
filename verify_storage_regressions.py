from pathlib import Path
import json,sys,tempfile,shutil,subprocess
sys.path[:0]=[str(Path.cwd()),str(Path.cwd()/'.local')]
from guest_tool import Guest
from verify_shell import read_prompt
from verify_development import enter
from verify_storage_format import filesystem,sha256
base=Path(sys.argv[1]);root=Path(tempfile.mkdtemp(prefix='042-regressions-',dir='.local')).resolve()
for n in ('guest.hex','disk.img'):shutil.copyfile(base/n,root/n)
g=Guest(root);r={'accepted':False,'work':str(root),'commands':[]}
def cmd(s):
 out=enter(g,s.encode(),prompt=b'dev42> ');r['commands'].append([s,out.decode(errors='replace')]);print(s,repr(out[-180:]),flush=True);return out
try:
 g.boot(disk=True);read_prompt(g);cmd('enter start - dev');initial,_=filesystem((root/'disk.img').read_bytes())
 for name in ('semantics','preprocessor'):
  data=Path('fixtures/c-native/'+name+'.c').read_bytes();enter(g,('edit '+name+'.c').encode(),prompt=b'edit42> ')
  for i,line in enumerate(data.decode().splitlines(),1):assert enter(g,f'i {i} {line}'.encode(),prompt=b'edit42> ')==b'edit42> '
  assert b'saved' in enter(g,b'w',prompt=b'edit42> ');enter(g,b'q',prompt=b'dev42> ')
  out=cmd('build '+name+'.c');assert b'status ' not in out
  assert cmd('exec independent argument')==b'dev42> '
 refs=Path(sys.argv[2]);refdir=root/'reference';refdir.mkdir();(refdir/'input.bin').write_bytes(initial['input.bin'])
 for prog,cases in {'echo':[[],['one','two'],['-n','tail'],['-z']], 'basename':[['/dir/thing.c','.c'],['/'],['foo','foo'],[],['-z'],['a','b','c']], 'cat':[['input.bin'],['-u','input.bin'],['absent','input.bin'],['-z']]}.items():
  for args in cases:
   host=subprocess.run([prog,*args],executable=str((refs/(prog+'-reference')).resolve()),cwd=refdir,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   out=cmd('@'+' '.join([prog,*args]));want=host.stdout+(f'status {host.returncode}\n'.encode() if host.returncode else b'')+b'dev42> ';assert out==want,(prog,args,out[:200],want[:200])
 assert cmd('@cat < input.bin | @cat')==initial['input.bin']+b'dev42> '
 # Reach actual128 filename boundary, retain every new ordinary file through cold boot.
 before,_=filesystem((root/'disk.img').read_bytes());count=128-len(before)
 for i in range(count):assert cmd(f'put retained-{i:02d} value-{i}')==b'dev42> '
 assert cmd('put overflow denied')==b'status 1\ndev42> '
 assert cmd('check')==b'dev42> '
 g.stop();g.boot(disk=True);read_prompt(g);cmd('enter start - dev');after,_=filesystem((root/'disk.img').read_bytes());assert len(after)==128
 for n,data in before.items():assert after[n]==data,n
 for i in range(count):assert after[f'retained-{i:02d}']==f'value-{i}'.encode()
 r['retained_files']=128;r['new_ordinary_files']=count;r['accepted']=True
except Exception as e:r['error']=repr(e);raise
finally:g.stop();(root/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('records',root,flush=True)
