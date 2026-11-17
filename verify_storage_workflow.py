from pathlib import Path
import json,sys,tempfile,shutil,re,struct
sys.path[:0]=[str(Path.cwd()),str(Path.cwd()/'.local')]
from guest_tool import Guest
from verify_shell import read_prompt
from verify_development import enter
from observer_qmp import read_memory
from verify_storage_format import filesystem,executable,sha256
base=Path(sys.argv[1]); root=Path(tempfile.mkdtemp(prefix='042-final-workflow-',dir='.local')).resolve()
for n in ('guest.hex','disk.img'):shutil.copyfile(base/n,root/n)
g=Guest(root);q=Path(tempfile.mkdtemp(dir='/tmp'))/'q.sock';result={'accepted':False,'work':str(root),'commands':[]}
def cmd(s,p=b'dev42> ',ok=True):
 out=enter(g,s.encode(),prompt=p);result['commands'].append([s,out.decode(errors='replace')]);print(s,repr(out[-180:]),flush=True)
 if ok:assert b'status ' not in out and b'error' not in out and b'failed' not in out,(s,out)
 return out

def edit(name,data):
 cmd('edit '+name,b'edit42> ')
 for i,line in enumerate(data.decode().splitlines(),1):
  out=enter(g,f'i {i} {line}'.encode(),prompt=b'edit42> ')
  assert not any(x in out for x in (b'error',b'failed',b'capacity')),(i,out)
 cmd('w',b'edit42> ');cmd('q')
 actual,_=filesystem((root/'disk.img').read_bytes());assert actual[name]==data

def boot():
 g.boot(disk=True,observer_socket=q);read_prompt(g);cmd('enter start - dev')
def mem(addr,n,name):return read_memory(q,addr,n,root/name)
try:
 boot();initial,_=filesystem((root/'disk.img').read_bytes());cc=mem(0x41100000,131064,'cc-initial.bin')
 A='Maple-73.c';B='Cobalt-29.c';appA='maple-native';appB='cobalt-native'
 large=Path('fixtures/c-native/large-project.c').read_bytes();flt=Path('fixtures/c-native/binary-project.c').read_bytes()
 edit(A,large);edit(B,flt)
 out=cmd('build '+A);n=int(out.splitlines()[0]);assert n>65536;result['large_code_size']=n
 cmd('save '+appA)
 for step,seed,expected in [(1,0,3591),(3,17,4808),(9,29995,8397),(7,30000,7202)]:assert cmd(f'exec Maple {step} {seed}')==f'{expected}\ndev42> '.encode()
 a=mem(0x411c0000,131064,'user-large.bin')
 cmd(B+' generate 81937 12345 > maple-data')
 cmd('@cat maple-data | '+B+' | @cat > cobalt-data')
 actual,_=filesystem((root/'disk.img').read_bytes());expected=bytearray();state=12345
 for _ in range(81937):
  state^=(state<<13)&0xffffffff;state^=state>>17;state^=(state<<5)&0xffffffff;expected.append(state&255)
 expected=bytes(expected);upper=bytes(c-32 if 97<=c<=122 else c for c in expected)
 assert actual['maple-data']==expected;assert actual['cobalt-data']==upper
 assert mem(0x411c0000,131064,'user-after-pipes.bin')==a
 assert mem(0x41100000,131064,'cc-after-pipes.bin')==cc
 cmd('build '+B);cmd('save '+appB);b=filesystem((root/'disk.img').read_bytes())[0][appB]
 cmd('@'+appB+' exit 2> cobalt-errors',ok=False)
 cmd('@echo -n tail >> cobalt-data');cmd('@echo -n > empty-data')
 files,_=filesystem((root/'disk.img').read_bytes());assert files['cobalt-data']==upper+b'tail';assert files['cobalt-errors']==b'nested exit\n';assert files['empty-data']==b''
 g.stop();boot();cmd('load '+appA);assert cmd('exec Maple 7 30000')==b'7202\ndev42> '
 # Edit only project A, including discard, a failed build, and correction.
 cmd('edit '+A,b'edit42> ');cmd('r 1 BROKEN_DISCARDED',b'edit42> ');cmd('q');assert filesystem((root/'disk.img').read_bytes())[0][A]==large
 cmd('edit '+A,b'edit42> ');cmd('r 1 invalid_symbol;',b'edit42> ');cmd('w',b'edit42> ');cmd('q')
 user=mem(0x411c0000,131064,'before-bad-build.bin');out=cmd('build '+A,ok=False);assert b'status 1' in out
 assert mem(0x411c0000,131064,'after-bad-build.bin')==user;assert mem(0x41100000,131064,'cc-after-bad-build.bin')==cc
 # No dependent save or execution after failure. Correct the source first.
 cmd('edit '+A,b'edit42> ');cmd('r 1 '+large.decode().splitlines()[0],b'edit42> ')
 lines=large.decode().splitlines();ix=next(i for i,l in enumerate(lines,1) if 'decimal(value);' in l)
 cmd(f'r {ix}     decimal(value+1);',b'edit42> ');cmd('w',b'edit42> ');cmd('q');cmd('build '+A);cmd('save '+appA);assert cmd('exec Maple 7 30000')==b'7203\ndev42> '
 files,_=filesystem((root/'disk.img').read_bytes());assert files[B]==flt and files[appB]==b and files['maple-data']==expected
 for name in ('cc','dev','start','echo','cat','basename','sha','mend'):assert files[name]==initial[name]
 g.stop();boot();cmd('load '+appA);assert cmd('exec AfterReboot 7 30000')==b'7203\ndev42> '
 cmd('load '+appB);cmd('exec Cobalt < maple-data > cobalt-again');assert filesystem((root/'disk.img').read_bytes())[0]['cobalt-again']==upper
 assert mem(0x41100000,131064,'cc-final.bin')==cc
 result['large_source_bytes']=len(large);result['binary_bytes']=len(expected);result['binary_sha256']=sha256(expected);result['two_projects_and_editor']=True
 # Target's ordinary source fixtures; each independently invoked, each must pass.
 for fixture in ('test.c','bounds.c','ppbound.c','physical.c'):
  user=mem(0x411c0000,131064,'user-before-'+fixture+'.bin');cmd(fixture)
  assert mem(0x411c0000,131064,'user-after-'+fixture+'.bin')==user
  assert mem(0x41100000,131064,'cc-after-'+fixture+'.bin')==cc
 result['capacity_and_preservation_fixtures']=True
 cmd('check');result['accepted']=True
except Exception as e:result['error']=repr(e);raise
finally:
 g.stop();(root/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('records',root,flush=True)
