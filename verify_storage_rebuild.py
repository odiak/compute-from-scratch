from pathlib import Path
from time import monotonic
import hashlib,json,shutil,struct,sys,tempfile
sys.path.insert(0,str(Path.cwd()))
sys.path.insert(0,str(Path.cwd()/'.local'))
from guest_tool import Guest
from verify_shell import read_prompt
from verify_source_import import receive
from verify_development import enter
from observer_qmp import read_memory
from verify_storage_format import filesystem,executable,sha256,archive,decode

def rebuild(manifest, manifest_dir):
 root=Path(tempfile.mkdtemp(prefix='042-clean-rebuild-',dir='.local')).resolve();work=root/'clean-0';work.mkdir()
 shutil.copyfile(manifest_dir/manifest['boot']['path'],work/'guest.hex')
 inputs={name:(manifest_dir/item['path']).read_bytes() for name,item in manifest['inputs'].items()};names=list(inputs)
 for name,data in inputs.items():
  assert len(data)==manifest['inputs'][name]['bytes'] and sha256(data)==manifest['inputs'][name]['sha256']
 assert sha256(bytes.fromhex((work/'guest.hex').read_text()))==manifest['boot']['sha256']
 result={'work':str(root),'accepted':False,'purpose':'independent empty-disk reproduction from frozen candidate21 source/data inputs','inputs':{n:{'size':len(d),'sha256':sha256(d)} for n,d in inputs.items()},'kernel_sha256':sha256(bytes.fromhex((work/'guest.hex').read_text()))};(root/'inputs.json').write_text(json.dumps(result,indent=2)+'\n');g=Guest(work);output=bytearray()
 try:
  (work/'disk.img').write_bytes(bytes(1024*1024));(root/'empty-disk.img').write_bytes(bytes(1024*1024))
  q=Path(tempfile.mkdtemp(dir='/tmp'))/'q.sock'
  g.boot(disk=True,observer_socket=q);read_prompt(g)
  for name,data in inputs.items():receive(g,name.encode(),data)
  from verify_environment_rebuild import files as legacy_files
  loaded=(work/'disk.img').read_bytes();assert legacy_files(loaded)==inputs
  (root/'initial-disk.img').write_bytes(loaded);result['initial_disk_sha256']=sha256(loaded)
  result['input_placement']='Trusted guest formats a fresh zero disk; exact21declaredsource/data files imported through raw UART recv, no host filesystem conversion.'
  check_name=names[4];g.serial_send(('cat '+check_name+'\n').encode().hex());assert read_prompt(g)==inputs[check_name]+b'\nshell> '
  print('uploaded and checked exact inputs',len(inputs),flush=True)
  g.serial_send(b'batch bootplan\n'.hex());deadline=monotonic()+300
  while monotonic()<deadline:
   part=bytes.fromhex(g.serial_read(100)['hex']);output.extend(part)
   if part:
    print(part[-1000:].decode(errors='replace'),end='',flush=True)
   if any(x in output for x in (b'build error',b'assembly error',b'plan stopped',b'batch stopped',b'invalid file')):
    raise ValueError('Rebuild failure observed; no dependent observer command will be issued')
   if b'source-only-rebuild-complete\n' in output and output.endswith(b'dev42> '):
    result['rebuild_completed']=True;break
  else:raise TimeoutError('Rebuild completion marker not observed')
  files,limits=filesystem((work/'disk.img').read_bytes());cc=executable(files['cc'],131064,5915992)
  assert read_memory(q,0x41100000,len(cc),root/'installed-compiler.bin')==cc
  result['installed_compiler_equal']=True
  result['outputs']={n:{'size':len(files[n]),'sha256':sha256(files[n]),'code_sha256':sha256(executable(files[n],131064,5915992))} for n in ('cc','dev','start','echo','cat','basename','sha','mend','red','blue')}
  result['files']={n:{'size':len(d),'sha256':sha256(d)} for n,d in files.items()}
  result['quit_output']=enter(g,b'quit',prompt=b'shell> ').decode()
  enter(g,b'ls',prompt=b'shell> ')
  enter(g,b'enter start - dev',prompt=b'dev42> ')
  assert enter(g,b'@red',prompt=b'dev42> ')==b'red revised 2000\ndev42> '
  assert enter(g,b'@blue',prompt=b'dev42> ')==b'blue project\nstatus 7\ndev42> '
  g.stop();g.boot(disk=True,observer_socket=q);read_prompt(g);enter(g,b'enter start - dev',prompt=b'dev42> ')
  assert enter(g,b'@red',prompt=b'dev42> ')==b'red revised 2000\ndev42> '
  assert read_memory(q,0x41100000,len(cc),root/'reboot-compiler.bin')==cc
  result['cold_boot_and_return']=True
  result['accepted']=True
 except Exception as error:
  result['error']=str(error);raise
 finally:
  g.stop();result['serial_tail']=output[-2000:].decode(errors='replace');(root/'result.json').write_text(json.dumps(result,indent=2)+'\n');(root/'rebuild-console.bin').write_bytes(output);print('\nindependent raw records',root,flush=True)
 return result

def main():
 path=Path(sys.argv[1]);manifest=json.loads(path.read_text())
 for name,entry in manifest['archives'].items():
  data=(path.parent/manifest['inputs'][name]['path']).read_bytes()
  members=archive(decode(data) if entry['compressed'] else data)
  assert set(members)==set(entry['members'])
  for n,d in members.items():assert sha256(d)==entry['members'][n]['sha256'] and d==(path.parent/entry['members'][n]['path']).read_bytes()
 runs=[rebuild(manifest,path.parent) for _ in range(2)]
 assert all(r['accepted'] for r in runs)
 assert runs[0]['outputs']==runs[1]['outputs']==manifest['outputs']
 assert runs[0]['files']==runs[1]['files']==manifest['generated_files']
 print(json.dumps({'accepted':True,'runs':[r['work'] for r in runs]},indent=2))

if __name__=='__main__':main()
