# 021 — transcript

Mechanically converted from the Pi event log by [transcript.py](../transcript.py). Summary: [021-campaign.md](021-campaign.md). Control bytes appear as Unicode control pictures (␀, ␛, …), and `$REPO` stands for the repository root.

| | |
| --- | --- |
| Model | `openai-codex/gpt-6.1-sol` |
| Start (UTC) | 2026-11-04 02:13:07 |
| Duration | 0:09:55 |
| Tool calls | 51 |
| VM boots | 2 |
| Observer messages | 0 |
| Compactions | 0 |
| Tokens (input / cached / output) | 42,062 / 1,231,104 / 18,026 |

**Tools:** `notes_write`, `notes_read`, `vm_boot_disk`, `serial_read`, `serial_send`, `serial_send_text`, `vm_stop`

**System prompt:**

```
You are the experimental agent. Use only the provided tools.

<cwd>
$REPO/.local/experiments/pi-2O5Npq/work
</cwd>
```

_Tools added: `notes_write`, `notes_read`, `vm_boot_disk`, `serial_read`, `serial_send`, `serial_send_text`, `vm_stop`_

## Stage prompt +0:00:00

> Extend the existing C-subset compiler stored as progBad on the persistent disk. Keep the kernel fixed. Use the guest shell and as/install/build to implement and test it. Read the prior notes and actual compiler source with cat. Keep the original compiler source in its existing file until you have a working replacement, using an old test slot if necessary; preserve progFwd (the standalone assembler). No external tools, no host assembler, and no raw application hex loading.
> 
> Add this first valid-C multi-function form: int g(int x){return EXPR;} int f(int x){... return EXPR;}. The g definition precedes f; f remains the entry point. g may be limited to an expression body, but f must retain the prior language and accept g(EXPR) as an expression factor, including in assignments, branches, loops and larger expressions. Emit real callable AArch64 code, pass the evaluated argument and return a result; preserve caller variables and expression temporaries across the call. Recursion and further functions can wait. Keep existing single-function source working and reject malformed calls without replacing the previous executable. Source files are printable ASCII and the compiler assembly must fit the 4096-byte file limit.
> 
> Use runtime arguments that vary, with at least one source invoking g more than once. Demonstrate a loop or assignment using g, and recheck the prior expression or control-flow compiler behavior. Save the final compiler assembly on disk, document its exact filename and grammar in concise notes, and stop the VM.

#### +0:00:00

**→ `notes_read`**

**← `notes_read`**

`text`

<details><summary>text (2,974 chars, 4 lines)</summary>

```
Syscall kernel complete; saved guest image length12416, VM stopped. Standalone assembler progFwd and C compiler progBad preserved untouched. Original scheduler source progMath preserved. New assembly source prog8 reproduces entire new kernel tail: as progFwd; install; build prog8; run emits raw TR..ZZ bytes (500 bytes) before normal exit text. Those bytes belong at image byte11916 (pad original11915-byte image with00). Other kernel patches: byte10952=84028052 (spawn clear loop now20 qwords, clears both FD records); byte11440=77000014 (branch to TR, which supplies x3 dispatcher then br x16). prog8 source's .word encodings are br x16, strb w9,[x2], and unsigned b.lo +8 (assembler lacks those mnemonics). Extension was generated using our standalone assembler, not external references.
ABI: original x0 console /w1 argument/x2 yield preserved; x3=0x40202e94 dispatcher at every scheduled entry. w0 op1=open(x1 name,w2 exact length),2=read(w1 fd,x2 buf,w3 count),3=write(...),4=close(w1 fd). Only caller-save registers used; stack untouched. Two FD records per slot at128,144: pointer64, offset32,length32. Lowest FD3/4; per-process independent; spawn resets both. Files readonly, EOF/zero count supported, fd1 console write. Supports extended disk files and legacy inline records; filename length at directory byte0, extended marker byte80=a5. Directory0x40120400 stride128, extended data0x40121400 stride4096.
Verified final saved kernel: build empty; spawn0; spawn1; schedule; wait1; wait2 -> ABuvCDEFwxyz, both exits0. empty is persistent two-process test source: opens alpha(ABCDEF)/beta(uvwxyz) by spawn argument, reads2, writes, yields, reads4, writes, closes. Saved Abc123xyz789 is more exhaustive assertion app: two opens FD3/4, third fails, close3/reopen beta returns3, reads FD4 around yield preserving offset/data, EOF, zero reads/writes with null buffers, invalid close and unknown op. Spawned both processes, both exits0; repeated twice with deliberately leaked descriptors to verify slot reuse clearing (all four exits0). Shell run regression separately verified with mov w0,42;ret -> exit0000002a. Original beta source had unsupported blr mnemonic in standalone assembler, so initial build regression attempt failed; used .word BLR in final tests. Earlier null-output attempts were debug iterations before correcting disk directory layout. Final tests all pass.
Assembler: progFwd standalone two-pass build ABI x1/w2 source,x3/w4 output/cap,w0 length or0. as progFwd installs volatile seed via install; then build NAME uses it. Lowercase mnemonics, semicolon terminators, NAME:; labels, decimal immediates, no spaces around commas/brackets; source<=4096, shell lines<=127. Supports mov/add/sub/cmp, ldr/str w/x, ldrb, mul/and/orr, lsl w, b/bl/conditional eq/ne/lt/ge, adr,ret,.word; BLR/BR/STRB encoded .word. Files alpha/beta are current test data. empty and Abc123xyz789 tests retained. prog8 dump source retained; progMath old kernel source retained.
```

</details>

#### +0:00:01

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T021311.915878Z"}
```

#### +0:00:04

**→ `serial_read`**

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e20
```

`text`

```
BOOT
shell>
```

#### +0:00:07

**→ `serial_send_text`**

```
help
ls
cat progBad
```

**← `serial_send_text`**

```
{"sent":20}
```

#### +0:00:09

**→ `serial_read`**

**← `serial_read`**

`hex`

<details><summary>hex (7,278 chars, 1 lines)</summary>

```
68656c70206563686f206c6f61642072756e207361766520617070656e6420636174206c732061736d206c6f616466696c6520617320696e7374616c6c206275696c640a7368656c6c3e20616c7068610a626574610a41626331323378797a3738390a656d7074790a70726f674677640a70726f674d6174680a70726f674261640a70726f67380a7368656c6c3e207375622073702c73702c31363b737472207833302c5b73705d3b6d6f762078392c78313b616464207731302c77312c77323b6d6f762078382c78333b6d6f76207831312c78333b616464207731322c77332c77343b616472207831332c706f6f6c3b6d6f76207731342c303b6d6f76207731352c303b6d6f76207731362c303b6d6f762077352c303b626c20533b6164722078362c70663b626c204b3b626c20533b636d702077302c3130353b622e6e652073743b6c6472622077302c5b78392c315d3b636d702077302c3131303b622e6e652073743b6164722078362c64693b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f76207731362c313b6d6f762077302c34383b626c20433b73743a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3131343b622e65712072743b636d702077302c3130353b622e65712063693b636d702077302c3131393b622e65712063773b626c20413b622073743b63693a3b6d6f762077372c303b6164722078362c69693b622063743b63773a3b6d6f762077372c313b6164722078362c77773b63743a3b626c204b3b6d6f76207731372c77353b626c20453b6d6f762077322c34313b626c20513b6d6f762077322c3132333b626c20513b6d6f762077302c35323b626c20433b6d6f76207731382c77353b6d6f762077302c35363b626c20433b6c623a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3132353b622e65712062653b626c20413b62206c623b62653a3b6164642078392c78392c313b636d702077372c303b622e65712070743b7375622077302c7731372c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6c64722077312c5b7831332c36305d3b6f72722077302c77302c77313b626c20573b70743a3b7375622077302c77352c7731383b6c736c2077302c77302c353b6c64722077312c5b7831332c35365d3b6f72722077302c77302c77313b6c736c2077312c7731382c323b6164642077312c77382c77313b7374722077302c5b78315d3b622073743b72743a3b6164722078362c72723b626c204b3b626c20503b636d702077302c33323b622e65712070613b636d702077302c34303b622e6e65206261643b70613a3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b626c20533b636d702077392c7731303b622e6e65206261643b636d70207731342c303b622e6e65206261643b6d6f762077302c33363b626c20433b636d70207731342c303b622e6e65206261643b7375622077302c7731312c77383b62207a3b6261643a3b6d6f762077302c303b7a3a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b413a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20533b636d702077302c3132303b622e65712061783b636d702077302c3132313b622e6e652061623b636d70207731362c303b622e65712061623b6d6f762077322c34383b622061673b61783a3b6d6f762077322c34343b61673a3b7374722077322c5b73702c385d3b6164642078392c78392c313b6d6f762077322c36313b626c20513b626c20453b6d6f762077322c35393b626c20513b6c64722077302c5b73702c385d3b626c20433b622061723b61623a3b6d6f76207731342c313b61723a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b4b3a3b7375622073702c73702c31363b737472207833302c5b73705d3b6b303a3b6c6472622077322c5b78365d3b6164642078362c78362c313b636d702077322c313b622e6571206b723b636d702077322c303b622e6571206b733b626c20503b636d702077302c77323b622e6e65206b623b636d702077322c33323b622e6571206b733b6164642078392c78392c313b62206b303b6b733a3b626c20533b62206b303b6b623a3b6d6f76207731342c313b6b723a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b453a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20543b65303a3b636d70207731342c303b622e6e652065723b626c20533b636d702077302c34333b622e65712065703b636d702077302c34353b622e6e652065723b6d6f762077322c32383b622065673b65703a3b6d6f762077322c32343b65673a3b7374722077322c5b73702c385d3b6164642078392c78392c313b626c20473b626c20543b626c20483b6c64722077302c5b73702c385d3b626c20433b622065303b65723a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b543a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20463b74303a3b636d70207731342c303b622e6e652074723b626c20533b636d702077302c34323b622e6e652074723b6164642078392c78392c313b626c20473b626c20463b626c20483b6d6f762077302c33323b626c20433b622074303b74723a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b463a3b7375622073702c73702c31363b737472207833302c5b73705d3b616464207731352c7731352c313b636d70207731352c36353b622e67652066623b636d70207731342c303b622e6e652066723b626c20533b636d702077302c34303b622e65712066703b636d702077302c3132303b622e65712066783b636d702077302c3132313b622e65712066793b7375622077322c77302c34383b636d702077322c303b622e6c742066623b636d702077322c31303b622e67652066623b6d6f762077332c303b6e303a3b6d6f762077342c31303b6d756c2077332c77332c77343b6164642077332c77332c77323b6d6f762077342c36353533353b636d702077332c77343b622e6c74206e6b3b622e6571206e6b3b622066623b6e6b3a3b6164642078392c78392c313b626c20503b7375622077322c77302c34383b636d702077322c303b622e6c74206e643b636d702077322c31303b622e6c74206e303b6e643a3b6c736c2077332c77332c353b6c64722077302c5b7831332c345d3b6f72722077302c77302c77333b626c20573b622066723b66783a3b6d6f762077302c303b622066763b66793a3b636d70207731362c303b622e65712066623b6d6f762077302c34303b66763a3b6164642078392c78392c313b626c20433b622066723b66703a3b6164642078392c78392c313b626c20453b6d6f762077322c34313b626c20513b622066723b66623a3b6d6f76207731342c313b66723a3b737562207731352c7731352c313b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b473a3b6d6f762077302c383b62204a3b483a3b6d6f762077302c31363b4a3a3b7375622073702c73702c31363b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c20433b6c64722077302c5b73702c385d3b6164642077302c77302c343b626c20433b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b513a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20533b636d702077302c77323b622e6e652071623b6164642078392c78392c313b622071723b71623a3b6d6f76207731342c313b71723a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b533a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b636d702077302c33323b622e6e652073723b6164642078392c78392c313b6220533b73723a3b7265743b503a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b7265743b656e643a3b6d6f762077302c303b7265743b433a3b6164642077312c7731332c77303b6c64722077302c5b78315d3b6220573b573a3b6164642078312c7831312c343b636d70207731322c77313b622e6c742066756c6c3b7374722077302c5b7831315d3b616464207831312c7831312c343b6164642077352c77352c313b7265743b66756c6c3a3b6d6f76207731342c313b7265743b70663a3b2e776f7264203534343530313335333b2e776f726420323632313534323b2e776f7264203534343530313335333b2e776f726420323638373039363b2e776f7264203337393b64693a3b2e776f7264203534343530313335333b2e776f72642032303737353033333b69693a3b2e776f7264203637313131343835373b2e776f726420313b77773a3b2e776f726420313831383834373335313b2e776f72642031393339383735373b72723a3b2e776f726420313937303536323431383b2e776f72642039333831303b706f6f6c3a3b2e776f7264203730343730393630303b2e776f726420313338343132303332303b2e776f726420333530363435353535313b2e776f726420333130333738353935323b2e776f726420333130373938303235383b2e776f726420323433323731333732373b2e776f7264203138343534393434303b2e776f726420313235383239313236343b2e776f7264203435333031363634303b2e776f726420333539363535313130343b2e776f7264203730343834303637323b2e776f7264203730343634343036353b2e776f7264203730343634343036373b2e776f726420313839353832353433393b2e776f726420313430393238363134343b2e776f7264203333353534343332303b2e776f72642036373130383836333b0a7368656c6c3e20
```

</details>

`text`

<details><summary>text (3,639 chars, 11 lines)</summary>

```
help echo load run save append cat ls asm loadfile as install build
shell> alpha
beta
Abc123xyz789
empty
progFwd
progMath
progBad
prog8
shell> sub sp,sp,16;str x30,[sp];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w5,0;bl S;adr x6,pf;bl K;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl P;cmp w0,32;b.eq pa;cmp w0,40;b.ne bad;pa:;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;cmp w14,0;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x30,[sp];add sp,sp,16;ret;A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b ar;ab:;mov w14,1;ar:;ldr x30,[sp];add sp,sp,16;ret;K:;sub sp,sp,16;str x30,[sp];k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq kr;cmp w2,0;b.eq ks;bl P;cmp w0,w2;b.ne kb;cmp w2,32;b.eq ks;add x9,x9,1;b k0;ks:;bl S;b k0;kb:;mov w14,1;kr:;ldr x30,[sp];add sp,sp,16;ret;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne er;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne er;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;er:;ldr x30,[sp];add sp,sp,16;ret;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne tr;bl S;cmp w0,42;b.ne tr;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;tr:;ldr x30,[sp];add sp,sp,16;ret;F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;ldr x30,[sp];add sp,sp,16;ret;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;ldr x30,[sp];add sp,sp,16;ret;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne qb;add x9,x9,1;b qr;qb:;mov w14,1;qr:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.ne sr;add x9,x9,1;b S;sr:;ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;.word 704709600;.word 1384120320;.word 3506455551;.word 3103785952;.word 3107980258;.word 2432713727;.word 184549440;.word 1258291264;.word 453016640;.word 3596551104;.word 704840672;.word 704644065;.word 704644067;.word 1895825439;.word 1409286144;.word 335544320;.word 67108863;
shell>
```

</details>

#### +0:00:11

> 💭 **Shortening compiler source**
> 💭 **Measuring compiler source**

**→ `serial_send_text`**

```
save
append
run 7
```

**← `serial_send_text`**

```
{"sent":18}
```

#### +0:00:25

**→ `serial_read`**

**← `serial_read`**

`hex`

```
756e6b6e6f776e20636f6d6d616e640a7368656c6c3e20756e6b6e6f776e20636f6d6d616e640a7368656c6c3e206e6f2070726f6772616d0a7368656c6c3e20
```

`text`

```
unknown command
shell> unknown command
shell> no program
shell>
```

#### +0:00:28

> 💭 **Preparing save commands**

**→ `serial_send_text`**

```
save alpha int f(int x){return x+1;}
cat alpha
as progBad
install
build alpha
run 7
```

**← `serial_send_text`**

```
{"sent":84}
```

#### +0:00:35

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20696e74206628696e742078297b72657475726e20782b313b7d0a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030380a7368656c6c3e20
```

`text`

```
saved
shell> int f(int x){return x+1;}
shell> assembled
shell> installed
shell> built
shell> exit 00000008
shell>
```

#### +0:00:38

> 💭 **Planning x19 preservation**
> 💭 **Planning entry-branch patch**

> 💭 **Emitting register-save instructions**
> 💭 **Implementing sequence loop**

> 💭 **Checking the assembler parser**

**→ `serial_send_text`**

```
cat progFwd
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:01:25

**→ `serial_read`**

**← `serial_read`**

`hex`

<details><summary>hex (8,116 chars, 1 lines)</summary>

```
7375622073702c73702c313032343b737472207831392c5b73705d3b737472207832302c5b73702c385d3b737472207832312c5b73702c31365d3b737472207832322c5b73702c32345d3b737472207832332c5b73702c33325d3b737472207832342c5b73702c34305d3b737472207833302c5b73702c37325d3b6d6f762078392c78313b616464207731302c77312c77323b6d6f76207831322c78333b616464207731342c77332c77343b616464207831352c73702c3132383b6d6f76207731362c303b6d6f76207731372c303b413a3b6d6f76207831312c78393b6d6f76207831332c7831323b423a3b626c20533b636d702077302c303b622e657120593b636d702077302c35393b622e657120433b6d6f762077362c77303b626c20483b6d6f762077352c77303b626c20533b636d702077302c35383b622e6e6520443b616464207831312c7831312c313b636d70207731372c303b622e6e6520423b6c736c2077312c7731362c333b6164642077312c7731352c77313b7374722077352c5b78315d3b7375622077322c7731332c7731323b7374722077322c5b78312c345d3b616464207731362c7731362c313b6220423b433a3b616464207831312c7831312c313b6220423b443a3b636d70207731372c303b622e6e6520453b616464207831332c7831332c343b473a3b626c20533b636d702077302c303b622e657120593b636d702077302c35393b622e657120433b616464207831312c7831312c313b6220473b453a3b636d702077362c3131343b622e657120563b616472207831392c543b493a3b6c64722077302c5b7831395d3b636d702077302c303b622e657120463b636d702077302c77353b622e6571204a3b616464207831392c7831392c31323b6220493b4a3a3b6c6472207732332c5b7831392c345d3b6c6472207732302c5b7831392c385d3b636d70207732332c373b622e6571204f3b636d70207732332c383b622e6571204f3b636d70207732332c31303b622e657120553b626c20523b6d6f76207732312c77303b6d6f76207732342c77313b636d70207732332c393b622e6571204b3b636d70207732342c303b622e6571204b3b6d6f762077312c313b636d70207732332c343b622e6e6520613b6c736c2077312c77312c33303b6220633b613a3b6c736c2077312c77312c33313b633a3b616464207732302c7732302c77313b4b3a3b616464207831312c7831312c313b636d70207732332c393b622e657120503b636d70207732332c343b622e6571204c3b636d70207732332c313b622e657120573b636d70207732332c333b622e6e65204d3b6d6f76207732322c7732313b6d6f76207732312c33313b62204e3b4d3a3b626c20523b6d6f76207732322c77303b616464207831312c7831312c313b4e3a3b636d70207732332c363b622e657120583b626c20533b636d702077302c3131393b622e6571205a3b636d702077302c3132303b622e6571205a3b626c204e303b636d70207732332c323b622e65712041303b636d70207732332c333b622e6e6520463b41303a3b6c736c2077302c77302c31303b6d6f762077312c313533363b6c736c2077312c77312c31363b616464207732302c7732302c77313b622042303b5a3a3b626c20523b6c736c2077302c77302c31363b42303a3b6c736c2077312c7732322c353b6f7272207732302c7732302c77313b6f7272207732302c7732302c7732313b6f7272207732302c7732302c77303b622055303b573a3b626c20533b636d702077302c3131393b622e65712043303b636d702077302c3132303b622e65712043303b626c204e303b6c736c2077302c77302c353b622044303b43303a3b626c20523b6c736c2077302c77302c31363b6164722078312c4d303b6c6472207732302c5b78315d3b6c736c2077312c7732342c33313b616464207732302c7732302c77313b44303a3b6f7272207732302c7732302c7732313b6f7272207732302c7732302c77303b622055303b4c3a3b616464207831312c7831312c313b626c20523b6d6f76207732322c77303b626c20533b636d702077302c34343b622e6e652046303b616464207831312c7831312c313b626c204e303b622047303b46303a3b6d6f762077302c303b47303a3b616464207831312c7831312c313b636d702077352c3432303b622e65712048303b6d6f762077312c323b626c20653b636d70207732342c303b622e65712048303b6d6f762077312c313b626c20653b48303a3b6c736c2077302c77302c31303b622042303b583a3b626c204e303b6d6f762077312c33323b7375622077312c77312c77303b6c736c2077312c77312c31363b6d6f762077322c33313b7375622077302c77322c77303b6c736c2077302c77302c31303b6f72722077302c77302c77313b622042303b4f3a3b626c204a303b7375622077312c7731332c7731323b7375622077302c77302c77313b6d6f762077312c323b626c20653b636d70207732332c383b622e6571204b303b6c736c2077302c77302c363b6d6f762077312c363b626c20653b6f7272207732302c7732302c77303b622055303b4b303a3b6c736c2077302c77302c31333b6d6f762077312c383b626c20653b6f7272207732302c7732302c77303b622055303b503a3b626c204a303b7375622077312c7731332c7731323b7375622077302c77302c77313b6d6f762077312c323b626c20653b6c736c2077302c77302c31333b6d6f762077312c383b626c20653b6f7272207732302c7732302c77303b6f7272207732302c7732302c7732313b622055303b553a3b626c204e303b6d6f76207732302c77303b622055303b563a3b6164722078312c4d303b6c6472207732302c5b78312c345d3b55303a3b6164642078312c7831332c343b636d70207731342c77313b622e6c7420463b737472207732302c5b7831335d3b616464207831332c7831332c343b616464207831312c7831312c313b6220423b593a3b636d70207731372c303b622e6e652052303b6d6f76207731372c313b6220413b52303a3b7375622077302c7731332c7731323b622053303b463a3b6d6f762077302c303b53303a3b6c6472207831392c5b73705d3b6c6472207832302c5b73702c385d3b6c6472207832312c5b73702c31365d3b6c6472207832322c5b73702c32345d3b6c6472207832332c5b73702c33325d3b6c6472207832342c5b73702c34305d3b6c6472207833302c5b73702c37325d3b6164642073702c73702c313032343b7265743b533a3b636d70207731312c7731303b622e67652054303b6c6472622077302c5b7831315d3b636d702077302c33333b622e67652055313b616464207831312c7831312c313b6220533b54303a3b6d6f762077302c303b55313a3b7265743b483a3b6d6f762077302c303b6d6f762077342c303b6c6472622077312c5b7831315d3b636d702077312c36353b622e6c742056303b636d702077312c39313b622e67652056303b6c736c2077342c77312c383b56303a3b636d70207731312c7731303b622e67652057303b6c6472622077312c5b7831315d3b636d702077312c33333b622e6c742057303b636d702077312c35383b622e65712057303b636d702077312c35393b622e65712057303b6164642077302c77302c77313b616464207831312c7831312c313b622056303b57303a3b6164642077302c77302c77343b7265743b4e303a3b6d6f762077302c303b6d6f762077332c31303b58303a3b6c6472622077312c5b7831315d3b636d702077312c33323b622e6e652059303b616464207831312c7831312c313b622058303b59303a3b7375622077322c77312c34383b5a303a3b6d756c2077302c77302c77333b6164642077302c77302c77323b616464207831312c7831312c313b6c6472622077312c5b7831315d3b7375622077322c77312c34383b636d702077322c303b622e6c7420643b636d702077322c31303b622e6c74205a303b643a3b7265743b523a3b6d6f762078372c7833303b626c20533b6d6f762077362c303b636d702077302c3131393b622e65712041313b6d6f762077362c313b636d702077302c3132303b622e65712041313b616464207831312c7831312c323b6d6f762077302c33313b622042313b41313a3b616464207831312c7831312c313b626c204e303b42313a3b6d6f762077312c77363b6d6f76207833302c78373b7265743b4a303a3b6d6f762078382c7833303b626c20533b626c20483b6d6f762077322c303b6d6f762078332c7831353b43313a3b636d702077322c7731363b622e676520463b6c64722077312c5b78335d3b636d702077302c77313b622e65712044313b6164642078332c78332c383b6164642077322c77322c313b622043313b44313a3b6c64722077302c5b78332c345d3b6d6f76207833302c78383b7265743b653a3b6d6f762077322c33323b7375622077312c77322c77313b6d6f762077322c303b663a3b6164642077322c77322c77323b636d702077302c303b622e676520673b6164642077322c77322c313b673a3b6164642077302c77302c77303b7375622077312c77312c313b636d702077312c303b622e6e6520663b6d6f762077302c77323b7265743b4d303a3b2e776f7264203730343634343036343b2e776f726420333539363535313130343b543a3b2e776f7264203333383b2e776f726420313b2e776f726420313338343132303332303b2e776f7264203239373b2e776f726420323b2e776f7264203138343534393337363b2e776f7264203333303b2e776f726420323b2e776f726420313235383239313230303b2e776f7264203332303b2e776f726420333b2e776f726420313739353136323134333b2e776f7264203332323b2e776f726420343b2e776f726420333130373937393236343b2e776f7264203334353b2e776f726420343b2e776f726420333130333738343936303b2e776f7264203432303b2e776f726420343b2e776f7264203936303439353631363b2e776f7264203333343b2e776f726420353b2e776f7264203435333031363537363b2e776f7264203330373b2e776f726420353b2e776f7264203136373737323136303b2e776f7264203333393b2e776f726420353b2e776f7264203730343634333037323b2e776f7264203333313b2e776f726420363b2e776f726420313339323530383932383b2e776f72642039383b2e776f726420373b2e776f7264203333353534343332303b2e776f7264203230363b2e776f726420373b2e776f726420323438333032373936383b2e776f7264203335383b2e776f726420383b2e776f726420313430393238363134343b2e776f7264203335353b2e776f726420383b2e776f726420313430393238363134353b2e776f7264203336383b2e776f726420383b2e776f726420313430393238363135353b2e776f7264203334383b2e776f726420383b2e776f726420313430393238363135343b2e776f7264203331313b2e776f726420393b2e776f7264203236383433353435363b2e776f7264203439303b2e776f72642031303b2e776f726420303b2e776f726420303b0a7368656c6c3e20
```

</details>

`text`

<details><summary>text (4,058 chars, 2 lines)</summary>

```
sub sp,sp,1024;str x19,[sp];str x20,[sp,8];str x21,[sp,16];str x22,[sp,24];str x23,[sp,32];str x24,[sp,40];str x30,[sp,72];mov x9,x1;add w10,w1,w2;mov x12,x3;add w14,w3,w4;add x15,sp,128;mov w16,0;mov w17,0;A:;mov x11,x9;mov x13,x12;B:;bl S;cmp w0,0;b.eq Y;cmp w0,59;b.eq C;mov w6,w0;bl H;mov w5,w0;bl S;cmp w0,58;b.ne D;add x11,x11,1;cmp w17,0;b.ne B;lsl w1,w16,3;add w1,w15,w1;str w5,[x1];sub w2,w13,w12;str w2,[x1,4];add w16,w16,1;b B;C:;add x11,x11,1;b B;D:;cmp w17,0;b.ne E;add x13,x13,4;G:;bl S;cmp w0,0;b.eq Y;cmp w0,59;b.eq C;add x11,x11,1;b G;E:;cmp w6,114;b.eq V;adr x19,T;I:;ldr w0,[x19];cmp w0,0;b.eq F;cmp w0,w5;b.eq J;add x19,x19,12;b I;J:;ldr w23,[x19,4];ldr w20,[x19,8];cmp w23,7;b.eq O;cmp w23,8;b.eq O;cmp w23,10;b.eq U;bl R;mov w21,w0;mov w24,w1;cmp w23,9;b.eq K;cmp w24,0;b.eq K;mov w1,1;cmp w23,4;b.ne a;lsl w1,w1,30;b c;a:;lsl w1,w1,31;c:;add w20,w20,w1;K:;add x11,x11,1;cmp w23,9;b.eq P;cmp w23,4;b.eq L;cmp w23,1;b.eq W;cmp w23,3;b.ne M;mov w22,w21;mov w21,31;b N;M:;bl R;mov w22,w0;add x11,x11,1;N:;cmp w23,6;b.eq X;bl S;cmp w0,119;b.eq Z;cmp w0,120;b.eq Z;bl N0;cmp w23,2;b.eq A0;cmp w23,3;b.ne F;A0:;lsl w0,w0,10;mov w1,1536;lsl w1,w1,16;add w20,w20,w1;b B0;Z:;bl R;lsl w0,w0,16;B0:;lsl w1,w22,5;orr w20,w20,w1;orr w20,w20,w21;orr w20,w20,w0;b U0;W:;bl S;cmp w0,119;b.eq C0;cmp w0,120;b.eq C0;bl N0;lsl w0,w0,5;b D0;C0:;bl R;lsl w0,w0,16;adr x1,M0;ldr w20,[x1];lsl w1,w24,31;add w20,w20,w1;D0:;orr w20,w20,w21;orr w20,w20,w0;b U0;L:;add x11,x11,1;bl R;mov w22,w0;bl S;cmp w0,44;b.ne F0;add x11,x11,1;bl N0;b G0;F0:;mov w0,0;G0:;add x11,x11,1;cmp w5,420;b.eq H0;mov w1,2;bl e;cmp w24,0;b.eq H0;mov w1,1;bl e;H0:;lsl w0,w0,10;b B0;X:;bl N0;mov w1,32;sub w1,w1,w0;lsl w1,w1,16;mov w2,31;sub w0,w2,w0;lsl w0,w0,10;orr w0,w0,w1;b B0;O:;bl J0;sub w1,w13,w12;sub w0,w0,w1;mov w1,2;bl e;cmp w23,8;b.eq K0;lsl w0,w0,6;mov w1,6;bl e;orr w20,w20,w0;b U0;K0:;lsl w0,w0,13;mov w1,8;bl e;orr w20,w20,w0;b U0;P:;bl J0;sub w1,w13,w12;sub w0,w0,w1;mov w1,2;bl e;lsl w0,w0,13;mov w1,8;bl e;orr w20,w20,w0;orr w20,w20,w21;b U0;U:;bl N0;mov w20,w0;b U0;V:;adr x1,M0;ldr w20,[x1,4];U0:;add x1,x13,4;cmp w14,w1;b.lt F;str w20,[x13];add x13,x13,4;add x11,x11,1;b B;Y:;cmp w17,0;b.ne R0;mov w17,1;b A;R0:;sub w0,w13,w12;b S0;F:;mov w0,0;S0:;ldr x19,[sp];ldr x20,[sp,8];ldr x21,[sp,16];ldr x22,[sp,24];ldr x23,[sp,32];ldr x24,[sp,40];ldr x30,[sp,72];add sp,sp,1024;ret;S:;cmp w11,w10;b.ge T0;ldrb w0,[x11];cmp w0,33;b.ge U1;add x11,x11,1;b S;T0:;mov w0,0;U1:;ret;H:;mov w0,0;mov w4,0;ldrb w1,[x11];cmp w1,65;b.lt V0;cmp w1,91;b.ge V0;lsl w4,w1,8;V0:;cmp w11,w10;b.ge W0;ldrb w1,[x11];cmp w1,33;b.lt W0;cmp w1,58;b.eq W0;cmp w1,59;b.eq W0;add w0,w0,w1;add x11,x11,1;b V0;W0:;add w0,w0,w4;ret;N0:;mov w0,0;mov w3,10;X0:;ldrb w1,[x11];cmp w1,32;b.ne Y0;add x11,x11,1;b X0;Y0:;sub w2,w1,48;Z0:;mul w0,w0,w3;add w0,w0,w2;add x11,x11,1;ldrb w1,[x11];sub w2,w1,48;cmp w2,0;b.lt d;cmp w2,10;b.lt Z0;d:;ret;R:;mov x7,x30;bl S;mov w6,0;cmp w0,119;b.eq A1;mov w6,1;cmp w0,120;b.eq A1;add x11,x11,2;mov w0,31;b B1;A1:;add x11,x11,1;bl N0;B1:;mov w1,w6;mov x30,x7;ret;J0:;mov x8,x30;bl S;bl H;mov w2,0;mov x3,x15;C1:;cmp w2,w16;b.ge F;ldr w1,[x3];cmp w0,w1;b.eq D1;add x3,x3,8;add w2,w2,1;b C1;D1:;ldr w0,[x3,4];mov x30,x8;ret;e:;mov w2,32;sub w1,w2,w1;mov w2,0;f:;add w2,w2,w2;cmp w0,0;b.ge g;add w2,w2,1;g:;add w0,w0,w0;sub w1,w1,1;cmp w1,0;b.ne f;mov w0,w2;ret;M0:;.word 704644064;.word 3596551104;T:;.word 338;.word 1;.word 1384120320;.word 297;.word 2;.word 184549376;.word 330;.word 2;.word 1258291200;.word 320;.word 3;.word 1795162143;.word 322;.word 4;.word 3107979264;.word 345;.word 4;.word 3103784960;.word 420;.word 4;.word 960495616;.word 334;.word 5;.word 453016576;.word 307;.word 5;.word 167772160;.word 339;.word 5;.word 704643072;.word 331;.word 6;.word 1392508928;.word 98;.word 7;.word 335544320;.word 206;.word 7;.word 2483027968;.word 358;.word 8;.word 1409286144;.word 355;.word 8;.word 1409286145;.word 368;.word 8;.word 1409286155;.word 348;.word 8;.word 1409286154;.word 311;.word 9;.word 268435456;.word 490;.word 10;.word 0;.word 0;
shell>
```

</details>

#### +0:01:27

> 💭 **Checking parser source size**
> 💭 **Checking source file size**

**→ `serial_send_text`**

```
save empty sub sp,sp,8192;str x30,[sp];mov x8,x3;mov w0,1;adr x1,n;mov w2,7;.word 3594453248;mov w1,w0;mov w0,2;add x2,sp,16;mov w3,8000;.word 3594453248;ldr x30,[sp];add sp,sp,8192;ret;n:;.word 1735357040;.word 6578498;
as progFwd
install
build empty
run
```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:01:40

> 💭 **Verifying BLR x8 encoding**

**→ `serial_read`**

**← `serial_read`**

`hex`

```
696e76616c69642070726f6772616d0a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20
```

`text`

```
invalid program
shell> assembled
shell> installed
shell> built
shell>
```

#### +0:01:48

> 💭 **Preparing compiler chunks**

**→ `serial_send_text`**

```
save empty sub sp,sp,8192;str x30,[sp];mov x8,x3;mov w0,1;adr x1,n;mov w2,7;.word 3594453248;
append empty mov w1,w0;mov w0,2;add x2,sp,16;mov w3,8000;.word 3594453248;ldr x30,[sp];add sp,sp,8192;ret;
append empty n:;.word 1735357040;.word 6578498;
build empty
run
```

**← `serial_send_text`**

```
{"sent":265}
```

#### +0:01:56

**→ `serial_read`**

**← `serial_read`**

```
{"hex":"","text":""}
```

#### +0:01:58

> 💭 **Waiting on hung VM**

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

```
{"hex":"","text":""}
```

#### +0:02:06

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:02:13

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T021523.371450Z"}
```

#### +0:02:15

**→ `serial_send_text`**

```
save empty sub sp,sp,8192;str x30,[sp];mov x8,x3;mov w0,1;adr x1,n;mov w2,7;.word 3594453248;
append empty mov w1,w0;mov w0,2;add x2,sp,16;mov w3,8000;.word 3594453248;ldr x30,[sp];add sp,sp,8192;ret;
append empty n:;.word 1735357040;.word 6578498;
as progFwd
install
build empty
```

**← `serial_send_text`**

```
{"sent":280}
```

#### +0:02:20

**→ `serial_read`**

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20
```

`text`

```
BOOT
shell> saved
shell> saved
shell> saved
shell> assembled
shell> installed
shell> built
shell>
```

#### +0:02:22

> 💭 **Designing shared epilogue**
> 💭 **Compressing parser strings**

> 💭 **Refining K byte comparison**
> 💭 **Designing shared signature**
> 💭 **Writing the code**

> 💭 **Implementing runtime wrappers**

**→ `serial_send_text`**

```
save empty sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;
append empty mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;
append empty adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;
append empty hd:;adr x6,pf;add x6,x6,6;bl K;cmp w0,0;cmp w19,0;ldrb w0,[x9];
```

**← `serial_send_text`**

```
{"sent":355}
```

#### +0:03:14

> 💭 **Restructuring the initial check**

**→ `serial_send_text`**

<details><summary>text (2,357 chars, 25 lines)</summary>

```
save empty sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;
append empty mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;
append empty adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;
append empty hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;adr x6,rr;bl K;bl E;
append empty mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];
append empty mov w19,1;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;
append empty adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;
append empty cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;
append empty cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;
append empty mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;
append empty be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;
append empty ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;
append empty lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl P;cmp w0,32;b.eq pa;
append empty cmp w0,40;b.ne bad;pa:;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;
append empty mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];
append empty ldr x30,[sp];add sp,sp,32;ret;A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;
append empty cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];
append empty add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;
append empty K:;sub sp,sp,16;str x30,[sp];k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq R;cmp w2,0;b.eq ks;
append empty bl P;cmp w0,w2;b.ne ab;cmp w2,32;b.eq ks;add x9,x9,1;b k0;ks:;bl S;b k0;
append empty E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;
append empty mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;
append empty T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;
append empty add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2357}
```

#### +0:03:42

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell>
```

#### +0:03:44

**→ `serial_send_text`**

<details><summary>text (2,212 chars, 27 lines)</summary>

```
append empty F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;
append empty cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;
append empty cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;
append empty mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;
append empty cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;
append empty fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;
append empty fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;
append empty cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;
append empty ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;
append empty fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;
append empty G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;
append empty ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;
append empty add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];
append empty cmp w0,32;b.ne sr;add x9,x9,1;b S;sr:;ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;
append empty end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;
append empty str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;it:;.word 544501353;.word 1;
append empty pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;
append empty di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;
append empty rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];
append empty ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;
append empty mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;b pool;.word 67108863;
append empty sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;
append empty ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
as progFwd
install
build empty
```

</details>

**← `serial_send_text`**

```
{"sent":2212}
```

#### +0:04:09

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> assembled
shell> installed
shell> built
shell>
```

#### +0:04:12

> 💭 **Creating corrected source**
> 💭 **Rebuilding corrected source**
> 💭 **Rebuilding corrected source**

**→ `serial_send_text`**

```
cat empty
```

**← `serial_send_text`**

```
{"sent":10}
```

#### +0:04:33

**→ `serial_read`**

**← `serial_read`**

`hex`

<details><summary>hex (7,780 chars, 1 lines)</summary>

```
7375622073702c73702c33323b737472207833302c5b73705d3b737472207831392c5b73702c385d3b6d6f762078392c78313b616464207731302c77312c77323b6d6f762078382c78333b6d6f76207831312c78333b616464207731322c77332c77343b616472207831332c706f6f6c3b6d6f76207731342c303b6d6f76207731352c303b6d6f76207731362c303b6d6f76207731392c303b6d6f762077352c303b6164722078362c69743b626c204b3b626c20533b636d702077302c3130333b622e65712067643b6d6f762077322c3130323b626c20513b622068643b67643a3b6164642078392c78392c313b6d6f76207731392c323b68643a3b6164722078362c70663b6164642078362c78362c363b626c204b3b636d70207731392c323b622e6e652062643b6d6f762077302c36303b626c20433b6164722078362c72723b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b6d6f762077302c33363b626c20433b6c64722077302c5b7831332c36305d3b6f72722077302c77302c77353b7374722077302c5b78385d3b6d6f76207731392c313b6164722078362c70663b626c204b3b62643a3b626c20533b636d702077302c3130353b622e6e652073743b6c6472622077302c5b78392c315d3b636d702077302c3131303b622e6e652073743b6164722078362c64693b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f76207731362c313b6d6f762077302c34383b626c20433b73743a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3131343b622e65712072743b636d702077302c3130353b622e65712063693b636d702077302c3131393b622e65712063773b626c20413b622073743b63693a3b6d6f762077372c303b6164722078362c69693b622063743b63773a3b6d6f762077372c313b6164722078362c77773b63743a3b626c204b3b6d6f76207731372c77353b626c20453b6d6f762077322c34313b626c20513b6d6f762077322c3132333b626c20513b6d6f762077302c35323b626c20433b6d6f76207731382c77353b6d6f762077302c35363b626c20433b6c623a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3132353b622e65712062653b626c20413b62206c623b62653a3b6164642078392c78392c313b636d702077372c303b622e65712070743b7375622077302c7731372c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6c64722077312c5b7831332c36305d3b6f72722077302c77302c77313b626c20573b70743a3b7375622077302c77352c7731383b6c736c2077302c77302c353b6c64722077312c5b7831332c35365d3b6f72722077302c77302c77313b6c736c2077312c7731382c323b6164642077312c77382c77313b7374722077302c5b78315d3b622073743b72743a3b6164722078362c72723b626c204b3b626c20503b636d702077302c33323b622e65712070613b636d702077302c34303b622e6e65206261643b70613a3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b626c20533b636d702077392c7731303b622e6e65206261643b6d6f762077302c33363b626c20433b636d70207731342c303b622e6e65206261643b7375622077302c7731312c77383b62207a3b6261643a3b6d6f762077302c303b7a3a3b6c6472207831392c5b73702c385d3b6c6472207833302c5b73705d3b6164642073702c73702c33323b7265743b413a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20533b636d702077302c3132303b622e65712061783b636d702077302c3132313b622e6e652061623b636d70207731362c303b622e65712061623b6d6f762077322c34383b622061673b61783a3b6d6f762077322c34343b61673a3b7374722077322c5b73702c385d3b6164642078392c78392c313b6d6f762077322c36313b626c20513b626c20453b6d6f762077322c35393b626c20513b6c64722077302c5b73702c385d3b626c20433b6220523b61623a3b6d6f76207731342c313b6220523b4b3a3b7375622073702c73702c31363b737472207833302c5b73705d3b6b303a3b6c6472622077322c5b78365d3b6164642078362c78362c313b636d702077322c313b622e657120523b636d702077322c303b622e6571206b733b626c20503b636d702077302c77323b622e6e652061623b636d702077322c33323b622e6571206b733b6164642078392c78392c313b62206b303b6b733a3b626c20533b62206b303b453a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20543b65303a3b636d70207731342c303b622e6e6520523b626c20533b636d702077302c34333b622e65712065703b636d702077302c34353b622e6e6520523b6d6f762077322c32383b622065673b65703a3b6d6f762077322c32343b65673a3b7374722077322c5b73702c385d3b6164642078392c78392c313b626c20473b626c20543b626c20483b6c64722077302c5b73702c385d3b626c20433b622065303b543a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20463b74303a3b636d70207731342c303b622e6e6520523b626c20533b636d702077302c34323b622e6e6520523b6164642078392c78392c313b626c20473b626c20463b626c20483b6d6f762077302c33323b626c20433b622074303b463a3b7375622073702c73702c31363b737472207833302c5b73705d3b616464207731352c7731352c313b636d70207731352c36353b622e67652066623b636d70207731342c303b622e6e652066723b626c20533b636d702077302c3130333b622e65712066633b636d702077302c34303b622e65712066703b636d702077302c3132303b622e65712066783b636d702077302c3132313b622e65712066793b7375622077322c77302c34383b636d702077322c303b622e6c742066623b636d702077322c31303b622e67652066623b6d6f762077332c303b6e303a3b6d6f762077342c31303b6d756c2077332c77332c77343b6164642077332c77332c77323b6d6f762077342c36353533353b636d702077332c77343b622e6c74206e6b3b622e6571206e6b3b622066623b6e6b3a3b6164642078392c78392c313b626c20503b7375622077322c77302c34383b636d702077322c303b622e6c74206e643b636d702077322c31303b622e6c74206e303b6e643a3b6c736c2077332c77332c353b6c64722077302c5b7831332c345d3b6f72722077302c77302c77333b626c20573b622066723b66783a3b6d6f762077302c303b622066763b66793a3b636d70207731362c303b622e65712066623b6d6f762077302c34303b66763a3b6164642078392c78392c313b626c20433b622066723b66633a3b636d70207731392c313b622e6e652066623b6164642078392c78392c313b6d6f762077322c34303b626c20513b626c20453b6d6f762077322c34313b626c20513b6164642078362c7831332c36383b636c3a3b6c64722077302c5b78365d3b6164642078362c78362c343b636d702077302c303b622e65712066723b636d702077302c313b622e6e652063653b7375622077302c77302c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6d6f762077312c3134383b6c736c2077312c77312c32343b6f72722077302c77302c77313b63653a3b626c20573b6220636c3b66703a3b6164642078392c78392c313b626c20453b6d6f762077322c34313b626c20513b622066723b66623a3b6d6f76207731342c313b66723a3b737562207731352c7731352c313b6220523b473a3b6d6f762077302c383b62204a3b483a3b6d6f762077302c31363b4a3a3b7375622073702c73702c31363b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c20433b6c64722077302c5b73702c385d3b6164642077302c77302c343b626c20433b6220523b513a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20533b636d702077302c77323b622e6e652061623b6164642078392c78392c313b523a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b533a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b636d702077302c33323b622e6e652073723b6164642078392c78392c313b6220533b73723a3b7265743b503a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b7265743b656e643a3b6d6f762077302c303b7265743b433a3b6164642077312c7731332c77303b6c64722077302c5b78315d3b6220573b573a3b6164642078312c7831312c343b636d70207731322c77313b622e6c742066756c6c3b7374722077302c5b7831315d3b616464207831312c7831312c343b6164642077352c77352c313b7265743b66756c6c3a3b6d6f76207731342c313b7265743b69743a3b2e776f7264203534343530313335333b2e776f726420313b70663a3b2e776f7264203534343530313335333b2e776f726420323632313534323b2e776f7264203534343530313335333b2e776f726420323638373039363b2e776f7264203337393b64693a3b2e776f7264203534343530313335333b2e776f72642032303737353033333b69693a3b2e776f7264203637313131343835373b2e776f726420313b77773a3b2e776f726420313831383834373335313b2e776f72642031393339383735373b72723a3b2e776f726420313937303536323431383b2e776f72642039333831303b706f6f6c3a3b6d6f762077302c77313b6d6f762077302c303b7375622073702c73702c31363b7374722077302c5b73705d3b6c64722077322c5b73705d3b6164642073702c73702c31363b6164642077302c77322c77303b7375622077302c77322c77303b6d756c2077302c77322c77303b7265743b6d6f762077302c77333b6d6f762077312c77303b6d6f762077332c77303b636d702077302c303b2e776f726420313430393238363134343b6220706f6f6c3b2e776f72642036373130383836333b7375622073702c73702c33323b7374722078312c5b73705d3b7374722078332c5b73702c385d3b737472207833302c5b73702c31365d3b6d6f762077312c77303b2e776f726420313b6c6472207833302c5b73702c31365d3b6c64722078332c5b73702c385d3b6c64722078312c5b73705d3b6164642073702c73702c33323b2e776f726420303b0a7368656c6c3e20
```

</details>

`text`

<details><summary>text (3,890 chars, 2 lines)</summary>

```
sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl P;cmp w0,32;b.eq pa;cmp w0,40;b.ne bad;pa:;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret;A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq R;cmp w2,0;b.eq ks;bl P;cmp w0,w2;b.ne ab;cmp w2,32;b.eq ks;add x9,x9,1;b k0;ks:;bl S;b k0;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.ne sr;add x9,x9,1;b S;sr:;ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;b pool;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
shell>
```

</details>

#### +0:04:35

> 💭 **Preparing a corrected resend**

**→ `serial_send_text`**

<details><summary>text (2,357 chars, 25 lines)</summary>

```
save empty sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;
append empty mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;
append empty adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;
append empty hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;adr x6,rr;bl K;bl E;
append empty mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];
append empty mov w19,1;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;
append empty adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;
append empty cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;
append empty cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;
append empty mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;
append empty be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;
append empty ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;
append empty lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl P;cmp w0,32;b.eq pa;
append empty cmp w0,40;b.ne bad;pa:;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;
append empty mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];
append empty ldr x30,[sp];add sp,sp,32;ret;A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;
append empty cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];
append empty add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;
append empty K:;sub sp,sp,16;str x30,[sp];k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq R;cmp w2,0;b.eq ks;
append empty bl P;cmp w0,w2;b.ne ab;cmp w2,32;b.eq ks;add x9,x9,1;b k0;ks:;bl S;b k0;
append empty E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;
append empty mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;
append empty T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;
append empty add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2357}
```

#### +0:05:04

**→ `serial_send_text`**

<details><summary>text (2,327 chars, 32 lines)</summary>

```
append empty F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;
append empty cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;
append empty cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;
append empty mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;
append empty cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;
append empty fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;
append empty fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;
append empty cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;
append empty ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;
append empty fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;
append empty G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;
append empty ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;
append empty add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];
append empty cmp w0,32;b.ne sr;add x9,x9,1;b S;sr:;ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;
append empty end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;
append empty str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;it:;.word 544501353;.word 1;
append empty pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;
append empty di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;
append empty rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];
append empty ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;
append empty mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;
append empty sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;
append empty ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
build empty
install
build alpha
run 7
save beta int g(int x){return x*2+1;} int f(int x){return x+g(x)+g(x+1)*3;}
build beta
run 2
run 5
```

</details>

**← `serial_send_text`**

```
{"sent":2327}
```

#### +0:05:29

**→ `serial_read`**

**← `serial_read`**

`hex`

<details><summary>hex (1,510 chars, 1 lines)</summary>

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030300a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030300a7368656c6c3e20657869742030303030303030300a7368656c6c3e20
```

</details>

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> built
shell> installed
shell> build error
shell> exit 00000000
shell> saved
shell> build error
shell> exit 00000000
shell> exit 00000000
shell>
```

#### +0:05:31

> 💭 **Checking byte-prefix handling**
> 💭 **Tracing compiler build failure**
> 💭 **Checking alpha source**

**→ `serial_send_text`**

```
cat alpha
save alpha int f(int x){return x;}
build alpha
as empty
install
build alpha
```

**← `serial_send_text`**

```
{"sent":86}
```

#### +0:05:55

**→ `serial_read`**

**← `serial_read`**

`hex`

```
696e74206628696e742078297b72657475726e20782b313b7d0a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20
```

`text`

```
int f(int x){return x+1;}
shell> saved
shell> build error
shell> assembled
shell> installed
shell> built
shell>
```

#### +0:05:57

> 💭 **Running assembler tests**

**→ `serial_send_text`**

```
run 7
build beta
run 2
run 5
```

**← `serial_send_text`**

```
{"sent":29}
```

#### +0:06:05

**→ `serial_read`**

**← `serial_read`**

`hex`

```
657869742030303030303030370a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030320a7368656c6c3e20657869742030303030303030350a7368656c6c3e20
```

`text`

```
exit 00000007
shell> build error
shell> exit 00000002
shell> exit 00000005
shell>
```

#### +0:06:07

> 💭 **Adding a preprocessing step**

**→ `serial_send_text`**

```
save beta int g(int x){return x*2+1;}int f(int x){return x+g(x)+g(x+1)*3;}
build beta
run 2
run 5
```

**← `serial_send_text`**

```
{"sent":98}
```

#### +0:06:16

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031630a7368656c6c3e20657869742030303030303033370a7368656c6c3e20
```

`text`

```
saved
shell> built
shell> exit 0000001c
shell> exit 00000037
shell>
```

#### +0:06:21

> 💭 **Resaving progBad with S**

**→ `serial_send_text`**

<details><summary>text (2,410 chars, 25 lines)</summary>

```
save progBad sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;
append progBad mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;
append progBad adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;
append progBad hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;adr x6,rr;bl K;bl E;
append progBad mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];
append progBad mov w19,1;bl S;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;
append progBad adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;
append progBad cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;
append progBad cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;
append progBad mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;
append progBad be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;
append progBad ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;
append progBad lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl P;cmp w0,32;b.eq pa;
append progBad cmp w0,40;b.ne bad;pa:;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;
append progBad mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];
append progBad ldr x30,[sp];add sp,sp,32;ret;A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;
append progBad cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];
append progBad add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;
append progBad K:;sub sp,sp,16;str x30,[sp];k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq R;cmp w2,0;b.eq ks;
append progBad bl P;cmp w0,w2;b.ne ab;cmp w2,32;b.eq ks;add x9,x9,1;b k0;ks:;bl S;b k0;
append progBad E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;
append progBad mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;
append progBad T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;
append progBad add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2410}
```

#### +0:06:51

**→ `serial_send_text`**

<details><summary>text (2,354 chars, 30 lines)</summary>

```
append progBad F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;
append progBad cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;
append progBad cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;
append progBad mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;
append progBad cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;
append progBad fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;
append progBad fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;
append progBad cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;
append progBad ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;
append progBad fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;
append progBad G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;
append progBad ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;
append progBad add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];
append progBad cmp w0,32;b.ne sr;add x9,x9,1;b S;sr:;ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;
append progBad end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;
append progBad str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;it:;.word 544501353;.word 1;
append progBad pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;
append progBad di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;
append progBad rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];
append progBad ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;
append progBad mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;
append progBad sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;
append progBad ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
as progBad
install
save beta int g(int x){return x*2+1;} int f(int x){return x+g(x)+g(x+1)*3;}
build beta
run 2
run 5
```

</details>

**← `serial_send_text`**

```
{"sent":2354}
```

#### +0:07:17

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031630a7368656c6c3e20657869742030303030303033370a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> assembled
shell> installed
shell> saved
shell> built
shell> exit 0000001c
shell> exit 00000037
shell>
```

#### +0:07:19

> 💭 **Checking loop behavior**

**→ `serial_send_text`**

```
save alpha int g(int x){return x-1;} int f(int x){int y=7;while(g(x)){y=y+g(x);x=x-1;}return y+x;}
build alpha
run 3
run 5
save Abc123xyz789 int g(int x){return x*3;} int f(int x){int y=x+4;if(g(x)){y=g(y)+g(x);}return y+x;}
build Abc123xyz789
run 0
run 2
run 4
save alpha int f(int x){int y=2;while(x){y=y*x;x=x-1;}return y+3*4;}
build alpha
run 3
run 5
save alpha int f(int x){return (x+2)*(x-1)+3;}
build alpha
run 3
run 7
```

**← `serial_send_text`**

```
{"sent":426}
```

#### +0:07:28

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030620a7368656c6c3e20657869742030303030303031320a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030340a7368656c6c3e20657869742030303030303031610a7368656c6c3e20657869742030303030303032380a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031380a7368656c6c3e20657869742030303030303066630a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030640a7368656c6c3e20657869742030303030303033390a7368656c6c3e20
```

`text`

```
saved
shell> built
shell> exit 0000000b
shell> exit 00000012
shell> saved
shell> built
shell> exit 00000004
shell> exit 0000001a
shell> exit 00000028
shell> saved
shell> built
shell> exit 00000018
shell> exit 000000fc
shell> saved
shell> built
shell> exit 0000000d
shell> exit 00000039
shell>
```

#### +0:07:30

> 💭 **Preserving prior executable source**
> 💭 **Refining executable source**

> 💭 **Testing malformed calls**

**→ `serial_send_text`**

```
save alpha int g(int x){return x*2+1;} int f(int x){return g(g(x))+x;}
build alpha
run 3
run 6
save alpha int g(int x){return x+1;} int f(int x){return g();}
build alpha
run 3
save alpha int g(int x){return x+1;} int f(int x){return g(x,2);}
build alpha
run 6
save alpha int g(int x){return x+1;} int f(int x){return g(x;}
build alpha
run 3
save alpha int f(int x){return g(x);}
build alpha
run 6
```

**← `serial_send_text`**

```
{"sent":397}
```

#### +0:07:55

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031320a7368656c6c3e20657869742030303030303032310a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031320a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032310a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031320a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032310a7368656c6c3e20
```

`text`

```
saved
shell> built
shell> exit 00000012
shell> exit 00000021
shell> saved
shell> build error
shell> exit 00000012
shell> saved
shell> build error
shell> exit 00000021
shell> saved
shell> build error
shell> exit 00000012
shell> saved
shell> build error
shell> exit 00000021
shell>
```

#### +0:07:57

**→ `serial_send_text`**

<details><summary>text (2,436 chars, 26 lines)</summary>

```
save progBad sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;
append progBad mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;
append progBad bl S;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;
append progBad gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;
append progBad mov w0,60;bl C;bl S;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;
append progBad ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;bl S;adr x6,pf;bl K;
append progBad bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;
append progBad adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;
append progBad cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;
append progBad cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;
append progBad mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;
append progBad be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;
append progBad ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;
append progBad lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl P;cmp w0,32;b.eq pa;
append progBad cmp w0,40;b.ne bad;pa:;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;
append progBad mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];
append progBad ldr x30,[sp];add sp,sp,32;ret;A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;
append progBad cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];
append progBad add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;
append progBad K:;sub sp,sp,16;str x30,[sp];k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq R;cmp w2,0;b.eq ks;
append progBad bl P;cmp w0,w2;b.ne ab;cmp w2,32;b.eq ks;add x9,x9,1;b k0;ks:;bl S;b k0;
append progBad E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;
append progBad mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;
append progBad T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;
append progBad add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2436}
```

#### +0:08:26

**→ `serial_send_text`**

<details><summary>text (2,404 chars, 33 lines)</summary>

```
append progBad F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;
append progBad cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;
append progBad cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;
append progBad mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;
append progBad cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;
append progBad fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;
append progBad fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;
append progBad cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;
append progBad ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;
append progBad fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;
append progBad G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;
append progBad ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;
append progBad add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];
append progBad cmp w0,32;b.ne sr;add x9,x9,1;b S;sr:;ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;
append progBad end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;
append progBad str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;it:;.word 544501353;.word 1;
append progBad pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;
append progBad di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;
append progBad rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];
append progBad ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;
append progBad mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;
append progBad sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;
append progBad ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
as progBad
install
save alpha   int g(int x){ return x-1;} int f(int x){int y=7;while(g(x)){y=y+g(x);x=x-1;}return y+x;}
build alpha
run 3
run 5
build beta
run 2
run 5
```

</details>

**← `serial_send_text`**

```
{"sent":2404}
```

#### +0:08:54

**→ `serial_read`**

**← `serial_read`**

`hex`

<details><summary>hex (1,562 chars, 1 lines)</summary>

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030620a7368656c6c3e20657869742030303030303031320a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031630a7368656c6c3e20657869742030303030303033370a7368656c6c3e20
```

</details>

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> assembled
shell> installed
shell> saved
shell> built
shell> exit 0000000b
shell> exit 00000012
shell> built
shell> exit 0000001c
shell> exit 00000037
shell>
```

#### +0:08:56

> 💭 **Saving concise campaign notes**
> 💭 **Verifying final compiler output**

**→ `serial_send_text`**

```
save empty int f(int x){int y=2;while(x){y=y*x;x=x-1;}return y+3*4;}
build empty
run 3
run 5
save empty int f(int x){return (x+2)*(x-1)+3;}
build empty
run 3
run 7
build Abc123xyz789
run 0
run 2
save empty int g(int x){return x+1;} int f(int x){return g();}
build empty
run 2
save empty int g(int x){return x+1;} int f(int x){return g(x,2);}
build empty
run 0
save empty int g(int x){return x+1;} int f(int x){return g(x;}
build empty
run 2
save empty int f(int x){return g(x);}
build empty
run 0
save empty int f(int x){return (x+2)*(x-1)+3;}
cat progBad
```

**← `serial_send_text`**

```
{"sent":556}
```

#### +0:09:12

**→ `serial_read`**

**← `serial_read`**

`hex`

<details><summary>hex (8,192 chars, 1 lines)</summary>

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031380a7368656c6c3e20657869742030303030303066630a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030640a7368656c6c3e20657869742030303030303033390a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030340a7368656c6c3e20657869742030303030303031610a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031610a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030340a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031610a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030340a7368656c6c3e2073617665640a7368656c6c3e207375622073702c73702c33323b737472207833302c5b73705d3b737472207831392c5b73702c385d3b6d6f762078392c78313b616464207731302c77312c77323b6d6f762078382c78333b6d6f76207831312c78333b616464207731322c77332c77343b616472207831332c706f6f6c3b6d6f76207731342c303b6d6f76207731352c303b6d6f76207731362c303b6d6f76207731392c303b6d6f762077352c303b626c20533b6164722078362c69743b626c204b3b626c20533b636d702077302c3130333b622e65712067643b6d6f762077322c3130323b626c20513b622068643b67643a3b6164642078392c78392c313b6d6f76207731392c323b68643a3b6164722078362c70663b6164642078362c78362c363b626c204b3b636d70207731392c323b622e6e652062643b6d6f762077302c36303b626c20433b626c20533b6164722078362c72723b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b6d6f762077302c33363b626c20433b6c64722077302c5b7831332c36305d3b6f72722077302c77302c77353b7374722077302c5b78385d3b6d6f76207731392c313b626c20533b6164722078362c70663b626c204b3b62643a3b626c20533b636d702077302c3130353b622e6e652073743b6c6472622077302c5b78392c315d3b636d702077302c3131303b622e6e652073743b6164722078362c64693b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f76207731362c313b6d6f762077302c34383b626c20433b73743a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3131343b622e65712072743b636d702077302c3130353b622e65712063693b636d702077302c3131393b622e65712063773b626c20413b622073743b63693a3b6d6f762077372c303b6164722078362c69693b622063743b63773a3b6d6f762077372c313b6164722078362c77773b63743a3b626c204b3b6d6f76207731372c77353b626c20453b6d6f762077322c34313b626c20513b6d6f762077322c3132333b626c20513b6d6f762077302c35323b626c20433b6d6f76207731382c77353b6d6f762077302c35363b626c20433b6c623a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3132353b622e65712062653b626c20413b62206c623b62653a3b6164642078392c78392c313b636d702077372c303b622e65712070743b7375622077302c7731372c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6c64722077312c5b7831332c36305d3b6f72722077302c77302c77313b626c20573b70743a3b7375622077302c77352c7731383b6c736c2077302c77302c353b6c64722077312c5b7831332c35365d3b6f72722077302c77302c77313b6c736c2077312c7731382c323b6164642077312c77382c77313b7374722077302c5b78315d3b622073743b72743a3b6164722078362c72723b626c204b3b626c20503b636d702077302c33323b622e65712070613b636d702077302c34303b622e6e65206261643b70613a3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b626c20533b636d702077392c7731303b622e6e65206261643b6d6f762077302c33363b626c20433b636d70207731342c303b622e6e65206261643b7375622077302c7731312c77383b62207a3b6261643a3b6d6f762077302c303b7a3a3b6c6472207831392c5b73702c385d3b6c6472207833302c5b73705d3b6164642073702c73702c33323b7265743b413a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20533b636d702077302c3132303b622e65712061783b636d702077302c3132313b622e6e652061623b636d70207731362c303b622e65712061623b6d6f762077322c34383b622061673b61783a3b6d6f762077322c34343b61673a3b7374722077322c5b73702c385d3b6164642078392c78392c313b6d6f762077322c36313b626c20513b626c20453b6d6f762077322c35393b626c20513b6c64722077302c5b73702c385d3b626c20433b6220523b61623a3b6d6f76207731342c313b6220523b4b3a3b7375622073702c73702c31363b737472207833302c5b73705d3b6b303a3b6c6472622077322c5b78365d3b6164642078362c78362c313b636d702077322c313b622e657120523b636d702077322c303b622e6571206b733b626c20503b636d702077302c77323b622e6e652061623b636d702077322c33323b622e6571206b733b6164642078392c78392c313b62206b303b6b733a3b626c20533b62206b303b453a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20543b65303a3b636d70207731342c303b622e6e6520523b626c20533b636d702077302c34333b622e65712065703b636d702077302c34353b622e6e6520523b6d6f762077322c32383b622065673b65703a3b6d6f762077322c32343b65673a3b7374722077322c5b73702c385d3b6164642078392c78392c313b626c20473b626c20543b626c20483b6c64722077302c5b73702c385d3b626c20433b622065303b543a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20463b74303a3b636d70207731342c303b622e6e6520523b626c20533b636d702077302c34323b622e6e6520523b6164642078392c78392c313b626c20473b626c20463b626c20483b6d6f762077302c33323b626c20433b622074303b463a3b7375622073702c73702c31363b737472207833302c5b73705d3b616464207731352c7731352c313b636d70207731352c36353b622e67652066623b636d70207731342c303b622e6e652066723b626c20533b636d702077302c3130333b622e65712066633b636d702077302c34303b622e65712066703b636d702077302c3132303b622e65712066783b636d702077302c3132313b622e65712066793b7375622077322c77302c34383b636d702077322c303b622e6c742066623b636d702077322c31303b622e67652066623b6d6f762077332c303b6e303a3b6d6f762077342c31303b6d756c2077332c77332c77343b6164642077332c77332c77323b6d6f762077342c36353533353b636d702077332c77343b622e6c74206e6b3b622e6571206e6b3b622066623b6e6b3a3b6164642078392c78392c313b626c20503b7375622077322c77302c34383b636d702077322c303b622e6c74206e643b636d702077322c31303b622e6c74206e303b6e643a3b6c736c2077332c77332c353b6c64722077302c5b7831332c345d3b6f72722077302c77302c77333b626c20573b622066723b66783a3b6d6f762077302c303b622066763b66793a3b636d70207731362c303b622e65712066623b6d6f762077302c34303b66763a3b6164642078392c78392c313b626c20433b622066723b66633a3b636d70207731392c313b622e6e652066623b6164642078392c78392c313b6d6f762077322c34303b626c20513b626c20453b6d6f762077322c34313b626c20513b6164642078362c7831332c36383b636c3a3b6c64722077302c5b78365d3b6164642078362c78362c343b636d702077302c303b622e65712066723b636d702077302c313b622e6e652063653b7375622077302c77302c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6d6f762077312c3134383b6c736c2077312c77312c32343b6f72722077302c77302c77313b63653a3b626c20573b6220636c3b66703a3b6164642078392c78392c313b626c20453b6d6f762077322c34313b626c20513b622066723b66623a3b6d6f76207731342c313b66723a3b737562207731352c7731352c313b6220523b473a3b6d6f762077302c383b62204a3b483a3b6d6f762077302c31363b4a3a3b7375622073702c73702c31363b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c20433b6c64722077302c5b73702c385d3b6164642077302c77302c343b626c20433b6220523b513a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20533b636d702077302c77323b622e6e652061623b6164642078392c78392c313b523a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b533a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b636d702077302c33323b622e6e652073723b6164642078392c78392c313b6220533b73723a3b7265743b503a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b7265743b656e643a3b6d6f762077302c303b7265743b433a3b6164642077312c7731332c77303b6c64722077302c5b78315d3b6220573b573a3b6164642078312c7831312c343b636d70207731322c77313b622e6c742066756c6c3b7374722077302c5b7831315d3b616464207831312c7831312c343b6164642077352c77352c313b7265743b66756c6c3a3b6d6f76207731342c313b7265743b69743a3b2e776f7264203534343530313335333b2e776f726420313b70663a3b2e776f7264203534343530313335333b2e776f726420323632313534323b2e776f7264203534343530313335333b2e776f726420323638373039363b2e776f7264203337393b64693a3b2e776f7264203534343530313335333b2e776f72642032303737353033333b69693a3b2e776f7264203637313131343835373b2e776f726420313b77773a3b2e776f726420313831383834373335313b2e776f72642031393339383735373b72723a3b2e776f726420313937303536323431383b2e776f72642039333831303b706f6f6c3a3b6d6f762077302c77313b6d6f762077302c303b7375622073702c73702c31363b7374722077302c5b73705d3b6c64722077322c5b73705d3b6164642073702c73702c31363b6164642077302c77322c77303b7375622077302c77322c77303b6d756c2077302c77322c77303b72
```

</details>

`text`

<details><summary>text (4,096 chars, 25 lines)</summary>

```
saved
shell> built
shell> exit 00000018
shell> exit 000000fc
shell> saved
shell> built
shell> exit 0000000d
shell> exit 00000039
shell> built
shell> exit 00000004
shell> exit 0000001a
shell> saved
shell> build error
shell> exit 0000001a
shell> saved
shell> build error
shell> exit 00000004
shell> saved
shell> build error
shell> exit 0000001a
shell> saved
shell> build error
shell> exit 00000004
shell> saved
shell> sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;bl S;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;bl S;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;bl S;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl P;cmp w0,32;b.eq pa;cmp w0,40;b.ne bad;pa:;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret;A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq R;cmp w2,0;b.eq ks;bl P;cmp w0,w2;b.ne ab;cmp w2,32;b.eq ks;add x9,x9,1;b k0;ks:;bl S;b k0;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.ne sr;add x9,x9,1;b S;sr:;ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;r
```

</details>

#### +0:09:14

**→ `serial_read`**

**← `serial_read`**

`hex`

```
65743b6d6f762077302c77333b6d6f762077312c77303b6d6f762077332c77303b636d702077302c303b2e776f726420313430393238363134343b2e776f7264203333353534343332303b2e776f72642036373130383836333b7375622073702c73702c33323b7374722078312c5b73705d3b7374722078332c5b73702c385d3b737472207833302c5b73702c31365d3b6d6f762077312c77303b2e776f726420313b6c6472207833302c5b73702c31365d3b6c64722078332c5b73702c385d3b6c64722078312c5b73705d3b6164642073702c73702c33323b2e776f726420303b0a7368656c6c3e20
```

`text`

```
et;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
shell>
```

#### +0:09:17

> 💭 **Recording compiler notes**
> 💭 **Stopping VM**

**→ `notes_write`**

<details><summary>text (3,298 chars, 11 lines)</summary>

```
Final compiler assembly is persistent file progBad (printable ASCII, fits 4096-byte disk file; all save/appends accepted, final cat verified tail). Kernel and progFwd unchanged. Read original progBad with cat before editing. Original stayed intact while replacement was built/tested in old empty slot; only then replaced progBad. VM stopped at end.
Rebuild/use: as progBad; install; build SOURCE; run N. Use shell as for compiler assembly, NOT progFwd's build: standalone assembler uses additive label hashes and new compiler has collisions (e.g. hd/eg). progFwd itself preserved untouched. No host tools/raw app loading used.
Grammar (space is supported whitespace): program = optional `int g(int x){return E;}` followed by `int f(int x){` optional `int y=E;` statements `return E;}`. g must precede f and is expression-only; f is entry. Statements: x=E; y=E; if(E){assignments} while(E){assignments}; prior restriction that control blocks contain assignments only retained. E = T ((+|-) T)*; T = factor ('*' factor)*; factor = decimal 0..65535 | x | y (only declared in f) | (E) | g(E) (only in f when g defined). Calls may nest syntactically (g(g(x))) but g cannot call itself; no further functions, unary operators, comparisons, else, nested control statements, or arbitrary identifiers. Depth limit64 retained. Leading/inter-definition spaces and spaces after g's opening brace tested.
Code generation: output begins with B over g to entry f; g at instruction1 ends in RET. g(E) evaluates argument into w0, saves x1 (caller x), x3 (caller y), x30 on aligned32-byte stack frame, mov w1,w0, real backward BL to g, restores saved registers without disturbing result w0. Existing expression stack temporaries remain below call frame. g/f runtime ABI uses w1 argument, w0 result. Compiler preserves added state x19. Shared parser epilogue and mnemonic instruction pool compact source. Failure returns0; shell build leaves previous executable intact.
Retained test sources:
 beta: int g(int x){return x*2+1;} int f(int x){return x+g(x)+g(x+1)*3;} -> run2=28 (1c),run5=55 (37).
 alpha: leading spaces, int g(int x){ return x-1;} int f(int x){int y=7;while(g(x)){y=y+g(x);x=x-1;}return y+x;} -> run3=11,run5=18.
 Abc123xyz789: int g(int x){return x*3;} int f(int x){int y=x+4;if(g(x)){y=g(y)+g(x);}return y+x;} -> run0=4,run2=26,run4=40.
 empty: int f(int x){return (x+2)*(x-1)+3;} -> run3=13,run7=57.
Additional passed: single-function factorial-like while with y=2 then y=y*x,x=x-1 and return y+3*4 -> run3=24,run5=252. Nested g(g(x))+x with g=2*x+1 -> run3=18,run6=33. Malformed calls g(),g(x,2),missing closing paren,undefined g(x) all build error; subsequent runs rechecked prior executable unchanged. Final compiler retested expressions/control/loops/repeated calls and all malformed cases after last edit.
Earlier kernel campaign context: saved kernel image12416; syscall dispatcher supplied x3 at scheduled entry, op w0=1 open(name x1,length w2),2 read(fd w1,buf x2,count w3),3 write,4 close. Two descriptors3/4 per slot, readonly disk files. prog8 retains kernel tail assembly dump; progMath retains original scheduler source. Kernel tail installed by earlier campaign, not modified here. Earlier alpha/beta/empty/Abc syscall test slots repurposed for compiler tests; prog8/progMath retained.
```

</details>

**← `notes_write`**

```
{"saved":true}
```

#### +0:09:48

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:09:50

Implemented and saved compiler assembly as `progBad`.

- Added preceding expression-only `g` and `g(EXPR)` factors throughout `f`.
- Emits real AArch64 calls, preserving variables and expression temporaries.
- Tested repeated calls, loops, assignments, branches, and prior behavior with varying runtime arguments.
- Malformed calls fail without replacing the executable.

Grammar and test results saved in notes. Kernel and `progFwd` unchanged. VM stopped.
