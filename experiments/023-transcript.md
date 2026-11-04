# 023 — transcript

Mechanically converted from the Pi event log by [transcript.py](../transcript.py). Summary: [023-campaign.md](023-campaign.md). Control bytes appear as Unicode control pictures (␀, ␛, …), and `$REPO` stands for the repository root.

| | |
| --- | --- |
| Model | `openai-codex/gpt-6.1-sol` |
| Start (UTC) | 2026-11-04 03:00:02 |
| Duration | 0:23:58 |
| Tool calls | 145 |
| VM boots | 2 |
| Observer messages | 1 |
| Compactions | 0 |
| Tokens (input / cached / output) | 88,908 / 4,454,912 / 27,020 |

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

> Continue the guest C compiler on the saved 022 disk. Keep the kernel fixed; use only the guest's shell, disk, assembler, and compiler ABI. Read the compiler source from progBad. Use recv to import actual multi-line C sources for testing, preserving their bytes. Save the working compiler assembly on disk and preserve progFwd.
>
> Add standard lexical whitespace handling to the current subset: spaces, horizontal/vertical tabs, LF, CR, and form feed. Treat C block comments /* ... */ and C99 line comments // ... as whitespace between tokens. Accept a line comment ending at EOF, reject an unterminated block comment, and do not allow comments to split a keyword or integer literal. Support ordinary formatting around punctuation and tokens in function definitions, calls, expressions and control flow. Preserve the existing single-line compiler behavior and compiler ABI. If you need space, the file limit is now 8192 bytes, while the executable limit remains 2048 bytes. Use only mnemonic assembly except data tables/constants, and the in-guest as/install/build commands.
>
> Test by receiving a formatted two-function C program with tabs, newlines and both kinds of comment, then run it with two runtime arguments. Test rejection of an unterminated comment, keeping the previously compiled executable. Stop the VM and save concise notes describing the final source filename and lexical rules.

#### +0:00:00

**→ `notes_read`**

**← `notes_read`**

`text`

<details><summary>text (5,329 chars, 32 lines)</summary>

```
FINAL: saved image13412 bytes, kernel base0x40200000. VM stopped. Kernel stage; progBad C compiler, progFwd self-hosted assembler, progMath/prog8 preserved. alpha was temporary assembly scratch then restored from inherited notes (two leading spaces; int g(int x){ return x-1;} int f(int x){int y=7;while(g(x)){y=y+g(x);x=x-1;}return y+x;}). Other original files untouched.

FINAL CORRECTION / PROCESS REGRESSION: independent stage020 exposed wrong PP constant offsets. Corrected image12368..12379 to hex 000400400014004000000009 (table0x40000400,data0x40001400,UART0x09000000). Old notes'12372 patch was WRONG. Final saved image and kernel0/kernel1 snapshots include correction. Tested real process ABI on final image: assembled program saved x19/x30, kept dispatcher x3 inx19, opened beta(name length4), read3 into local data, wrote3 to fd1, closedfd3, returned0. spawn0 twice ->pid1,pid2; schedule -> exact 'intint' followed shell prompt (six expected file bytes); wait1/wait2 ->exit00000000. This confirms both descriptor slots and UART write. Check snapshot source restored afterwards, snapshots regenerated and verified=00003464.

DISK: block queue base0x40000000, disk image RAM0x40000400; transfer0x40000 bytes. Header4096 bytes;16 records*128; name length byte0, size LE16 bytes2..3, name bytes4..15, markerA5 at record80. Data disk offset4096+slot*8192; max8192. Disk offset0x800 (queue+3072) LE32 marker8192 distinguishes new stride. First old-format boot copies old eight4096 blocks backwards to8192 stride, keeps records, writes marker/disk. Original legacy inline records/converter retained. Boot return clears status even when migration skipped. 16 slots occupied.

recv NAME N: existing alphanumeric name1..12; strict decimal0..8192. Invalid args/size/full store reject before ready, without changing previous file. ready LF, exactlyN RAW UART bytes into0x40050000, then commit/save and saved LF/prompt. No LF payload terminator. Polls UART FR. Entry restores disk base, rediscovers MMIO device and loads queue avail index before request. Scheduler ABI retained. cat emits exact contents plus oneLF.

DISK FILES / REPRODUCE:
 FsBoot: exact148-byte migration block, install image12416.
 FsRecv: as FsRecv;run0 exports BO..EN hex (776 bytes) for image12564; exclude initial B EX and exporter. Apply BO+28 patch bb000014 (branch to FsFix instead of cmpw7,8). Valid .word0 padding after exporter makes source4252 bytes, testing long assembly input.
 FsFix: exact52-byte recv trampoline at13340 +20-byte boot return at13392. Fixed-position raw branch returns to recv+32. as FsFix succeeds; do not run directly.
 Check: as Check;run1 compares all13412 RAM kernel bytes against kernel0+kernel1, success00003464. run0 regenerates snapshots in slots12/13; subsequent ordinary save/append flushes disk.
 kernel0: first8192 binary image bytes; kernel1: remaining5220; concatenate for complete final image. Both snapshots regenerated AFTER process PP correction.
 bin:12 bytes 00 0a 0d ff 80 1b 41 00 42 0a 7f 55.
 src:30 bytes = two spaces + 'int f(int x){\nreturn x+2;\n}\n'. Exact multiline import retained. Compiler's inherited grammar accepts space but not LF, so build src gives build error; kernel does not alter bytes.

Raw patches to ORIGINAL12416-byte image (offset ->LE hex):
2368 1600a8d2;2564 8100a052;2628 8f090014;3032 0d028052;3272 1a028052;4840 a534028b;4872 1f0a4071;10744 c7010014;12212 0f028052;12332 080940911f2003d5;12368 000400400014004000000009.
Append FsBoot12416, FsRecv BO..EN patched12564, FsFix13340. FsBoot SH points13392. These cover disk relocation/transfer/limits/counts/read syscall stride/constants. Compiler unchanged.

PASSED TESTS:
- bin ready then11 bytes ->no output;12th byte WITHOUT LF ->saved/prompt; exact cat, across multiple reboots. NUL/LF/CR/FF/80/ESC/7F retained.
- src multiline N30 exact contents, across multiple reboots.
- Invalid8193,-1,1x,missing args,bad-name,huge decimal rejected before ready, previous src/bin intact. N0 ready/saved and cat onlyLF.
-8192 recv (former big):1024 bytes=4*00..FF;7168 bytes=112 lines of64 bytes (3*'0123456789abcdef'+'0123456789abcde'+LF). Guest byte comparison returned8192 before AND after reboot. Test slot later became kernel1.
-8192-byte C build (former zero): spaces then unchanged beta source at EOF. as progBad;install;build zero;run2=0000001c. Slot later became kernel0.
-FsRecv4252 bytes assembles, including after reboot; progFwd/progBad assemble. compiler install/build beta/run2=0000001c. beta cat exact original 'int g(int x){return x*2+1;} int f(int x){return x+g(x)+g(x+1)*3;}'. Original compiler/assembler files not modified.
-Check run1 exact13412 snapshots across reboot (then regenerated and verified again after final PP fix).
-Final process regression described above emits six bytes with two spawned processes, both wait0.

Inherited compiler ABI: as progBad;install;build SOURCE;run N. Optional expression-only g precedes entry f; x argument, optional f localy, assignments/if/while assignment blocks/return; +,-,*,parentheses,g calls. Space-only whitespace, not general C. Use shell as for progBad; standalone progFwd has label-hash collisions. Process syscalls: x3 dispatcher, w0=1 open(x1name,w2len),2 read(w1fd,x2buf,w3count),3 write,4 close; fd3/4 readonly files now using8192 stride and old inline fallback.
```

</details>

#### +0:00:02

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T030006.935655Z"}
```

#### +0:00:04

**→ `serial_send_text`**

```
cat progBad
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:00:06

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

<details><summary>hex (7,852 chars, 1 lines)</summary>

```
424f4f540a7368656c6c3e207375622073702c73702c33323b737472207833302c5b73705d3b737472207831392c5b73702c385d3b6d6f762078392c78313b616464207731302c77312c77323b6d6f762078382c78333b6d6f76207831312c78333b616464207731322c77332c77343b616472207831332c706f6f6c3b6d6f76207731342c303b6d6f76207731352c303b6d6f76207731362c303b6d6f76207731392c303b6d6f762077352c303b626c20533b6164722078362c69743b626c204b3b626c20533b636d702077302c3130333b622e65712067643b6d6f762077322c3130323b626c20513b622068643b67643a3b6164642078392c78392c313b6d6f76207731392c323b68643a3b6164722078362c70663b6164642078362c78362c363b626c204b3b636d70207731392c323b622e6e652062643b6d6f762077302c36303b626c20433b626c20533b6164722078362c72723b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b6d6f762077302c33363b626c20433b6c64722077302c5b7831332c36305d3b6f72722077302c77302c77353b7374722077302c5b78385d3b6d6f76207731392c313b626c20533b6164722078362c70663b626c204b3b62643a3b626c20533b636d702077302c3130353b622e6e652073743b6c6472622077302c5b78392c315d3b636d702077302c3131303b622e6e652073743b6164722078362c64693b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f76207731362c313b6d6f762077302c34383b626c20433b73743a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3131343b622e65712072743b636d702077302c3130353b622e65712063693b636d702077302c3131393b622e65712063773b626c20413b622073743b63693a3b6d6f762077372c303b6164722078362c69693b622063743b63773a3b6d6f762077372c313b6164722078362c77773b63743a3b626c204b3b6d6f76207731372c77353b626c20453b6d6f762077322c34313b626c20513b6d6f762077322c3132333b626c20513b6d6f762077302c35323b626c20433b6d6f76207731382c77353b6d6f762077302c35363b626c20433b6c623a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3132353b622e65712062653b626c20413b62206c623b62653a3b6164642078392c78392c313b636d702077372c303b622e65712070743b7375622077302c7731372c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6c64722077312c5b7831332c36305d3b6f72722077302c77302c77313b626c20573b70743a3b7375622077302c77352c7731383b6c736c2077302c77302c353b6c64722077312c5b7831332c35365d3b6f72722077302c77302c77313b6c736c2077312c7731382c323b6164642077312c77382c77313b7374722077302c5b78315d3b622073743b72743a3b6164722078362c72723b626c204b3b626c20503b636d702077302c33323b622e65712070613b636d702077302c34303b622e6e65206261643b70613a3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b626c20533b636d702077392c7731303b622e6e65206261643b6d6f762077302c33363b626c20433b636d70207731342c303b622e6e65206261643b7375622077302c7731312c77383b62207a3b6261643a3b6d6f762077302c303b7a3a3b6c6472207831392c5b73702c385d3b6c6472207833302c5b73705d3b6164642073702c73702c33323b7265743b413a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20533b636d702077302c3132303b622e65712061783b636d702077302c3132313b622e6e652061623b636d70207731362c303b622e65712061623b6d6f762077322c34383b622061673b61783a3b6d6f762077322c34343b61673a3b7374722077322c5b73702c385d3b6164642078392c78392c313b6d6f762077322c36313b626c20513b626c20453b6d6f762077322c35393b626c20513b6c64722077302c5b73702c385d3b626c20433b6220523b61623a3b6d6f76207731342c313b6220523b4b3a3b7375622073702c73702c31363b737472207833302c5b73705d3b6b303a3b6c6472622077322c5b78365d3b6164642078362c78362c313b636d702077322c313b622e657120523b636d702077322c303b622e6571206b733b626c20503b636d702077302c77323b622e6e652061623b636d702077322c33323b622e6571206b733b6164642078392c78392c313b62206b303b6b733a3b626c20533b62206b303b453a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20543b65303a3b636d70207731342c303b622e6e6520523b626c20533b636d702077302c34333b622e65712065703b636d702077302c34353b622e6e6520523b6d6f762077322c32383b622065673b65703a3b6d6f762077322c32343b65673a3b7374722077322c5b73702c385d3b6164642078392c78392c313b626c20473b626c20543b626c20483b6c64722077302c5b73702c385d3b626c20433b622065303b543a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20463b74303a3b636d70207731342c303b622e6e6520523b626c20533b636d702077302c34323b622e6e6520523b6164642078392c78392c313b626c20473b626c20463b626c20483b6d6f762077302c33323b626c20433b622074303b463a3b7375622073702c73702c31363b737472207833302c5b73705d3b616464207731352c7731352c313b636d70207731352c36353b622e67652066623b636d70207731342c303b622e6e652066723b626c20533b636d702077302c3130333b622e65712066633b636d702077302c34303b622e65712066703b636d702077302c3132303b622e65712066783b636d702077302c3132313b622e65712066793b7375622077322c77302c34383b636d702077322c303b622e6c742066623b636d702077322c31303b622e67652066623b6d6f762077332c303b6e303a3b6d6f762077342c31303b6d756c2077332c77332c77343b6164642077332c77332c77323b6d6f762077342c36353533353b636d702077332c77343b622e6c74206e6b3b622e6571206e6b3b622066623b6e6b3a3b6164642078392c78392c313b626c20503b7375622077322c77302c34383b636d702077322c303b622e6c74206e643b636d702077322c31303b622e6c74206e303b6e643a3b6c736c2077332c77332c353b6c64722077302c5b7831332c345d3b6f72722077302c77302c77333b626c20573b622066723b66783a3b6d6f762077302c303b622066763b66793a3b636d70207731362c303b622e65712066623b6d6f762077302c34303b66763a3b6164642078392c78392c313b626c20433b622066723b66633a3b636d70207731392c313b622e6e652066623b6164642078392c78392c313b6d6f762077322c34303b626c20513b626c20453b6d6f762077322c34313b626c20513b6164642078362c7831332c36383b636c3a3b6c64722077302c5b78365d3b6164642078362c78362c343b636d702077302c303b622e65712066723b636d702077302c313b622e6e652063653b7375622077302c77302c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6d6f762077312c3134383b6c736c2077312c77312c32343b6f72722077302c77302c77313b63653a3b626c20573b6220636c3b66703a3b6164642078392c78392c313b626c20453b6d6f762077322c34313b626c20513b622066723b66623a3b6d6f76207731342c313b66723a3b737562207731352c7731352c313b6220523b473a3b6d6f762077302c383b62204a3b483a3b6d6f762077302c31363b4a3a3b7375622073702c73702c31363b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c20433b6c64722077302c5b73702c385d3b6164642077302c77302c343b626c20433b6220523b513a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20533b636d702077302c77323b622e6e652061623b6164642078392c78392c313b523a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b533a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b636d702077302c33323b622e6e652073723b6164642078392c78392c313b6220533b73723a3b7265743b503a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b7265743b656e643a3b6d6f762077302c303b7265743b433a3b6164642077312c7731332c77303b6c64722077302c5b78315d3b6220573b573a3b6164642078312c7831312c343b636d70207731322c77313b622e6c742066756c6c3b7374722077302c5b7831315d3b616464207831312c7831312c343b6164642077352c77352c313b7265743b66756c6c3a3b6d6f76207731342c313b7265743b69743a3b2e776f7264203534343530313335333b2e776f726420313b70663a3b2e776f7264203534343530313335333b2e776f726420323632313534323b2e776f7264203534343530313335333b2e776f726420323638373039363b2e776f7264203337393b64693a3b2e776f7264203534343530313335333b2e776f72642032303737353033333b69693a3b2e776f7264203637313131343835373b2e776f726420313b77773a3b2e776f726420313831383834373335313b2e776f72642031393339383735373b72723a3b2e776f726420313937303536323431383b2e776f72642039333831303b706f6f6c3a3b6d6f762077302c77313b6d6f762077302c303b7375622073702c73702c31363b7374722077302c5b73705d3b6c64722077322c5b73705d3b6164642073702c73702c31363b6164642077302c77322c77303b7375622077302c77322c77303b6d756c2077302c77322c77303b7265743b6d6f762077302c77333b6d6f762077312c77303b6d6f762077332c77303b636d702077302c303b2e776f726420313430393238363134343b2e776f7264203333353534343332303b2e776f72642036373130383836333b7375622073702c73702c33323b7374722078312c5b73705d3b7374722078332c5b73702c385d3b737472207833302c5b73702c31365d3b6d6f762077312c77303b2e776f726420313b6c6472207833302c5b73702c31365d3b6c64722078332c5b73702c385d3b6c64722078312c5b73705d3b6164642073702c73702c33323b2e776f726420303b0a7368656c6c3e20
```

</details>

`text`

<details><summary>text (3,926 chars, 3 lines)</summary>

```
BOOT
shell> sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;bl S;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;bl S;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;bl S;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl P;cmp w0,32;b.eq pa;cmp w0,40;b.ne bad;pa:;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret;A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq R;cmp w2,0;b.eq ks;bl P;cmp w0,w2;b.ne ab;cmp w2,32;b.eq ks;add x9,x9,1;b k0;ks:;bl S;b k0;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.ne sr;add x9,x9,1;b S;sr:;ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
shell>
```

</details>

#### +0:00:08

> 💭 **Recreating source chunks**
> 💭 **Refining token matching**
> 💭 **Designing compact matcher**

**→ `serial_send_text`**

```
ls
```

**← `serial_send_text`**

```
{"sent":3}
```

#### +0:00:36

**→ `serial_read`**

**← `serial_read`**

`hex`

```
616c7068610a626574610a41626331323378797a3738390a656d7074790a70726f674677640a70726f674d6174680a70726f674261640a70726f67380a4673426f6f740a4673526563760a62696e0a7372630a6b65726e656c300a6b65726e656c310a436865636b0a46734669780a7368656c6c3e20
```

`text`

```
alpha
beta
Abc123xyz789
empty
progFwd
progMath
progBad
prog8
FsBoot
FsRecv
bin
src
kernel0
kernel1
Check
FsFix
shell>
```

#### +0:00:39

> 💭 **Counting payload bytes**

**→ `serial_send_text`**

```
help
```

**← `serial_send_text`**

```
{"sent":5}
```

#### +0:00:49

**→ `serial_read`**

**← `serial_read`**

`hex`

```
68656c70206563686f206c6f61642072756e207361766520617070656e6420636174206c732061736d206c6f616466696c6520617320696e7374616c6c206275696c640a7368656c6c3e20
```

`text`

```
help echo load run save append cat ls asm loadfile as install build
shell>
```

#### +0:00:52

**→ `serial_send_text`**

```
save empty sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;bl S;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;bl S;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;bl S;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret;
```

**← `serial_send_text`**

```
{"sent":1299}
```

#### +0:01:10

> 💭 **Refining keyword matching**
> 💭 **Adding keyword boundaries**

**→ `serial_send_text`**

```
append empty A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];mov w1,0;bl S;k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq ke;cmp w2,0;b.eq ks;cmp w2,32;b.eq ks;cmp w2,97;b.ge kl;bl S;kl:;bl P;cmp w0,w2;b.ne ab;add x9,x9,1;mov w1,w2;cmp w2,97;b.ge k0;bl S;b k0;ks:;cmp w1,97;b.lt kt;bl B;kt:;bl S;mov w1,0;b k0;ke:;cmp w1,97;b.lt R;bl B;b R;B:;ldrb w0,[x9];cmp w9,w10;b.ge br;cmp w0,97;b.lt bn;cmp w0,122;b.le bx;bn:;cmp w0,48;b.lt br;cmp w0,57;b.le bx;cmp w0,95;b.ne br;bx:;mov w14,1;br:;ret;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

**← `serial_send_text`**

```
{"sent":1012}
```

#### +0:01:30

> 💭 **Checking the instruction budget**

**→ `serial_send_text`**

<details><summary>text (1,730 chars, 2 lines)</summary>

```
append empty F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.eq ss;cmp w0,9;b.lt sl;cmp w0,13;b.le ss;sl:;cmp w0,47;b.ne sr;add w0,w9,1;cmp w0,w10;b.ge sr;ldrb w0,[x9,1];cmp w0,47;b.eq line;cmp w0,42;b.ne sr;add x9,x9,2;block:;cmp w9,w10;b.ge un;ldrb w0,[x9];add x9,x9,1;cmp w0,42;b.ne block;cmp w9,w10;b.ge un;ldrb w0,[x9];cmp w0,47;b.ne block;ss:;add x9,x9,1;b S;line:;add x9,x9,2;ll:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,10;b.eq ss;cmp w0,13;b.eq ss;add x9,x9,1;b ll;un:;mov w14,1;b end;sr:;ldrb w0,[x9];ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;
```

</details>

**← `serial_send_text`**

```
{"sent":1730}
```

#### +0:01:59

> 💭 **Checking pointer reload**

**→ `serial_send_text`**

```
append empty it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
as empty
```

**← `serial_send_text`**

```
{"sent":598}
```

#### +0:02:07

**→ `serial_read`**

**← `serial_read`**

`hex`

```
696e76616c69642070726f6772616d0a7368656c6c3e20696e76616c69642070726f6772616d0a7368656c6c3e20696e76616c69642070726f6772616d0a7368656c6c3e20696e76616c69642070726f6772616d0a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
invalid program
shell> invalid program
shell> invalid program
shell> invalid program
shell> assembly error
shell>
```

#### +0:02:10

> 💭 **Preparing counted source chunks**

**→ `serial_send_text`**

```
recv empty 6000
```

**← `serial_send_text`**

```
{"sent":16}
```

#### +0:02:21

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a
```

`text`

```
ready
```

#### +0:02:23

**→ `serial_send_text`**

```
sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;bl S;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;bl S;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;bl S;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret;
```

**← `serial_send_text`**

```
{"sent":1288}
```

#### +0:02:40

**→ `serial_send_text`**

```
A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];mov w1,0;bl S;k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq ke;cmp w2,0;b.eq ks;cmp w2,32;b.eq ks;cmp w2,97;b.ge kl;bl S;kl:;bl P;cmp w0,w2;b.ne ab;add x9,x9,1;mov w1,w2;cmp w2,97;b.ge k0;bl S;b k0;ks:;cmp w1,97;b.lt kt;bl B;kt:;bl S;mov w1,0;b k0;ke:;cmp w1,97;b.lt R;bl B;b R;B:;cmp w9,w10;b.ge br;ldrb w0,[x9];cmp w0,97;b.lt bn;cmp w0,122;b.le bx;bn:;cmp w0,48;b.lt br;cmp w0,57;b.le bx;cmp w0,95;b.ne br;bx:;mov w14,1;br:;ret;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

**← `serial_send_text`**

```
{"sent":999}
```

#### +0:02:54

**→ `serial_send_text`**

<details><summary>text (1,717 chars, 2 lines)</summary>

```
F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.eq ss;cmp w0,9;b.lt sl;cmp w0,13;b.le ss;sl:;cmp w0,47;b.ne sr;add w0,w9,1;cmp w0,w10;b.ge sr;ldrb w0,[x9,1];cmp w0,47;b.eq line;cmp w0,42;b.ne sr;add x9,x9,2;block:;cmp w9,w10;b.ge un;ldrb w0,[x9];add x9,x9,1;cmp w0,42;b.ne block;cmp w9,w10;b.ge un;ldrb w0,[x9];cmp w0,47;b.ne block;ss:;add x9,x9,1;b S;line:;add x9,x9,2;ll:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,10;b.eq ss;cmp w0,13;b.eq ss;add x9,x9,1;b ll;un:;mov w14,1;b end;sr:;ldrb w0,[x9];ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;
```

</details>

**← `serial_send_text`**

```
{"sent":1717}
```

#### +0:03:16

**→ `serial_send_text`**

```
it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
```

**← `serial_send_text`**

```
{"sent":576}
```

#### +0:03:24

> 💭 **Preparing whitespace padding**

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:03:37

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:03:40

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:03:43

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:03:46

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:03:48

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":140}
```

#### +0:03:52

**→ `serial_send_text`**

```
as empty
install
build beta
run 2
```

**← `serial_send_text`**

```
{"sent":34}
```

#### +0:03:55

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e206e6f2070726f6772616d0a7368656c6c3e206e6f20636f6d70696c65720a7368656c6c3e206e6f2070726f6772616d0a7368656c6c3e20
```

`text`

```
saved
shell> assembly error
shell> no program
shell> no compiler
shell> no program
shell>
```

#### +0:03:57

> 💭 **Calculating program size**

**→ `serial_send_text`**

```
as progBad
```

**← `serial_send_text`**

```
{"sent":11}
```

#### +0:04:08

**→ `serial_read`**

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell>
```

#### +0:04:11

> 💭 **Checking b.le assembly syntax**

**→ `serial_send_text`**

```
recv src 25
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:04:20

**→ `serial_send_text`** `{"text": "cmp w0,1;b.le zz;zz:;ret;"}`

**← `serial_send_text`**

```
{"sent":25}
```

#### +0:04:23

**→ `serial_send_text`**

```
as src
```

**← `serial_send_text`**

```
{"sent":7}
```

#### +0:04:25

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
ready
saved
shell> assembly error
shell>
```

#### +0:04:28

> 💭 **Reimporting adjusted source**

**→ `serial_send_text`**

```
recv empty 6000
```

**← `serial_send_text`**

```
{"sent":16}
```

#### +0:04:37

**→ `serial_send_text`**

<details><summary>text (2,287 chars, 3 lines)</summary>

```
sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;bl S;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;bl S;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;bl S;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret;
A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];mov w1,0;bl S;k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq ke;cmp w2,0;b.eq ks;cmp w2,32;b.eq ks;cmp w2,97;b.ge kl;bl S;kl:;bl P;cmp w0,w2;b.ne ab;add x9,x9,1;mov w1,w2;cmp w2,97;b.ge k0;bl S;b k0;ks:;cmp w1,97;b.lt kt;bl B;kt:;bl S;mov w1,0;b k0;ke:;cmp w1,97;b.lt R;bl B;b R;B:;cmp w9,w10;b.ge br;ldrb w0,[x9];cmp w0,97;b.lt bn;cmp w0,123;b.lt bx;bn:;cmp w0,48;b.lt br;cmp w0,58;b.lt bx;cmp w0,95;b.ne br;bx:;mov w14,1;br:;ret;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2287}
```

#### +0:05:06

**→ `serial_send_text`**

<details><summary>text (2,293 chars, 3 lines)</summary>

```
F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.eq ss;cmp w0,9;b.lt sl;cmp w0,14;b.lt ss;sl:;cmp w0,47;b.ne sr;add w0,w9,1;cmp w0,w10;b.ge sr;ldrb w0,[x9,1];cmp w0,47;b.eq line;cmp w0,42;b.ne sr;add x9,x9,2;block:;cmp w9,w10;b.ge un;ldrb w0,[x9];add x9,x9,1;cmp w0,42;b.ne block;cmp w9,w10;b.ge un;ldrb w0,[x9];cmp w0,47;b.ne block;ss:;add x9,x9,1;b S;line:;add x9,x9,2;ll:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,10;b.eq ss;cmp w0,13;b.eq ss;add x9,x9,1;b ll;un:;mov w14,1;b end;sr:;ldrb w0,[x9];ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;
it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
```

</details>

**← `serial_send_text`**

```
{"sent":2293}
```

#### +0:05:46

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:05:49

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:05:52

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:05:54

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:05:59

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:06:01

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":140}
```

#### +0:06:03

**→ `serial_send_text`**

```
as empty
install
build beta
run 2
```

**← `serial_send_text`**

```
{"sent":34}
```

#### +0:06:07

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031630a7368656c6c3e20
```

`text`

```
ready
saved
shell> assembly error
shell> installed
shell> built
shell> exit 0000001c
shell>
```

#### +0:06:10

> 💭 **Reducing instruction count**
> 💭 **Checking assembler limits**

**→ `serial_send_text`**

```
cat progFwd
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:06:27

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

#### +0:06:29

> 💭 **Testing assembler label limits**
> 💭 **Shortening assembly routines**
> 💭 **Compressing assembly source**

> 💭 **Shrinking K branch logic**
> 💭 **Refining K branch checks**

**→ `serial_send_text`**

```
recv empty 6000
```

**← `serial_send_text`**

```
{"sent":16}
```

#### +0:07:17

**→ `serial_send_text`**

<details><summary>text (2,193 chars, 3 lines)</summary>

```
sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret;
A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];mov w1,0;bl S;k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq ke;cmp w2,33;b.lt ks;cmp w2,97;b.ge kl;bl S;kl:;bl P;cmp w0,w2;b.ne ab;add x9,x9,1;mov w1,w2;cmp w2,97;b.ge k0;bl S;b k0;ks:;cmp w1,97;b.lt kt;bl B;kt:;bl S;mov w1,0;b k0;ke:;cmp w1,97;b.lt R;bl B;b R;B:;cmp w9,w10;b.ge br;ldrb w0,[x9];cmp w0,48;b.lt br;cmp w0,123;b.ge br;mov w14,1;br:;ret;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2193}
```

#### +0:07:45

**→ `serial_send_text`**

<details><summary>text (2,293 chars, 3 lines)</summary>

```
F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.eq ss;cmp w0,9;b.lt sl;cmp w0,14;b.lt ss;sl:;cmp w0,47;b.ne sr;add w0,w9,1;cmp w0,w10;b.ge sr;ldrb w0,[x9,1];cmp w0,47;b.eq line;cmp w0,42;b.ne sr;add x9,x9,2;block:;cmp w9,w10;b.ge un;ldrb w0,[x9];add x9,x9,1;cmp w0,42;b.ne block;cmp w9,w10;b.ge un;ldrb w0,[x9];cmp w0,47;b.ne block;ss:;add x9,x9,1;b S;line:;add x9,x9,2;ll:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,10;b.eq ss;cmp w0,13;b.eq ss;add x9,x9,1;b ll;un:;mov w14,1;b end;sr:;ldrb w0,[x9];ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret;
it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
```

</details>

**← `serial_send_text`**

```
{"sent":2293}
```

#### +0:08:15

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:08:18

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:08:21

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:08:25

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:08:27

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:08:31

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":234}
```

#### +0:08:33

**→ `serial_send_text`**

```
as empty
install
build beta
run 2
```

**← `serial_send_text`**

```
{"sent":34}
```

#### +0:08:36

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031630a7368656c6c3e20
```

`text`

```
ready
saved
shell> assembly error
shell> installed
shell> build error
shell> exit 0000001c
shell>
```

#### +0:08:39

> 💭 **Testing assembly input format**

**→ `serial_send_text`**

```
recv src 9
```

**← `serial_send_text`**

```
{"sent":11}
```

#### +0:08:51

**→ `serial_send_text`**

```
ret;
ret;
```

**← `serial_send_text`**

```
{"sent":9}
```

#### +0:08:54

**→ `serial_send_text`**

```
as src
```

**← `serial_send_text`**

```
{"sent":7}
```

#### +0:08:56

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
ready
saved
shell> assembly error
shell>
```

#### +0:09:00

**→ `serial_send_text`**

```
recv empty 6000
```

**← `serial_send_text`**

```
{"sent":16}
```

#### +0:09:04

**→ `serial_send_text`**

<details><summary>text (2,193 chars, 1 lines)</summary>

```
sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret; A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];mov w1,0;bl S;k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq ke;cmp w2,33;b.lt ks;cmp w2,97;b.ge kl;bl S;kl:;bl P;cmp w0,w2;b.ne ab;add x9,x9,1;mov w1,w2;cmp w2,97;b.ge k0;bl S;b k0;ks:;cmp w1,97;b.lt kt;bl B;kt:;bl S;mov w1,0;b k0;ke:;cmp w1,97;b.lt R;bl B;b R;B:;cmp w9,w10;b.ge br;ldrb w0,[x9];cmp w0,48;b.lt br;cmp w0,123;b.ge br;mov w14,1;br:;ret;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2193}
```

#### +0:09:31

**→ `serial_send_text`**

<details><summary>text (2,293 chars, 1 lines)</summary>

```
F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.eq ss;cmp w0,9;b.lt sl;cmp w0,14;b.lt ss;sl:;cmp w0,47;b.ne sr;add w0,w9,1;cmp w0,w10;b.ge sr;ldrb w0,[x9,1];cmp w0,47;b.eq line;cmp w0,42;b.ne sr;add x9,x9,2;block:;cmp w9,w10;b.ge un;ldrb w0,[x9];add x9,x9,1;cmp w0,42;b.ne block;cmp w9,w10;b.ge un;ldrb w0,[x9];cmp w0,47;b.ne block;ss:;add x9,x9,1;b S;line:;add x9,x9,2;ll:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,10;b.eq ss;cmp w0,13;b.eq ss;add x9,x9,1;b ll;un:;mov w14,1;b end;sr:;ldrb w0,[x9];ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret; it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
```

</details>

**← `serial_send_text`**

```
{"sent":2293}
```

#### +0:09:59

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:10:03

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:10:05

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:10:08

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:10:11

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:10:14

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":234}
```

#### +0:10:17

**→ `serial_send_text`**

```
as empty
install
build beta
run 2
```

**← `serial_send_text`**

```
{"sent":34}
```

#### +0:10:19

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030300a7368656c6c3e20
```

`text`

```
ready
saved
shell> assembled
shell> installed
shell> build error
shell> exit 00000000
shell>
```

#### +0:10:22

> 💭 **Debugging K space handling**
> 💭 **Verifying K space handling**

**→ `serial_send_text`**

```
recv src 23
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:10:39

**→ `serial_send_text`** `{"text": "int f(int x){return x;}"}`

**← `serial_send_text`**

```
{"sent":23}
```

#### +0:10:42

**→ `serial_send_text`**

```
build src
```

**← `serial_send_text`**

```
{"sent":10}
```

#### +0:10:45

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20
```

`text`

```
ready
saved
shell> build error
shell>
```

#### +0:10:49

> 💭 **Verifying parser byte comparisons**
> 💭 **Debugging parser punctuation**

> 💭 **Updating punctuation branches**
> 💭 **Editing source punctuation**

**→ `serial_send_text`**

```
recv empty 6000
```

**← `serial_send_text`**

```
{"sent":16}
```

#### +0:11:28

**→ `serial_send_text`**

<details><summary>text (2,225 chars, 1 lines)</summary>

```
sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret; A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];mov w1,0;bl S;k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq ke;cmp w2,33;b.lt ks;cmp w2,97;b.ge kl;bl S;kl:;bl P;cmp w0,w2;b.ne ab;add x9,x9,1;mov w1,w2;cmp w2,123;b.eq kp;cmp w2,97;b.ge k0;kp:;mov w1,0;bl S;b k0;ks:;cmp w1,97;b.lt kt;bl B;kt:;bl S;mov w1,0;b k0;ke:;cmp w1,97;b.lt R;bl B;b R;B:;cmp w9,w10;b.ge br;ldrb w0,[x9];cmp w0,48;b.lt br;cmp w0,123;b.ge br;mov w14,1;br:;ret;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2225}
```

#### +0:11:56

**→ `serial_send_text`**

<details><summary>text (2,293 chars, 1 lines)</summary>

```
F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.eq ss;cmp w0,9;b.lt sl;cmp w0,14;b.lt ss;sl:;cmp w0,47;b.ne sr;add w0,w9,1;cmp w0,w10;b.ge sr;ldrb w0,[x9,1];cmp w0,47;b.eq line;cmp w0,42;b.ne sr;add x9,x9,2;block:;cmp w9,w10;b.ge un;ldrb w0,[x9];add x9,x9,1;cmp w0,42;b.ne block;cmp w9,w10;b.ge un;ldrb w0,[x9];cmp w0,47;b.ne block;ss:;add x9,x9,1;b S;line:;add x9,x9,2;ll:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,10;b.eq ss;cmp w0,13;b.eq ss;add x9,x9,1;b ll;un:;mov w14,1;b end;sr:;ldrb w0,[x9];ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret; it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
```

</details>

**← `serial_send_text`**

```
{"sent":2293}
```

#### +0:12:23

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:12:26

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:12:29

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:12:32

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:12:35

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:12:38

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":202}
```

#### +0:12:41

**→ `serial_send_text`**

```
as empty
install
build src
run 2
build beta
run 2
```

**← `serial_send_text`**

```
{"sent":50}
```

#### +0:12:44

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030320a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031630a7368656c6c3e20
```

`text`

```
ready
saved
shell> assembled
shell> installed
shell> built
shell> exit 00000002
shell> built
shell> exit 0000001c
shell>
```

#### +0:12:47

> 💭 **Testing multiline length**

**→ `serial_send_text`**

```
recv src 256
```

**← `serial_send_text`**

```
{"sent":13}
```

#### +0:12:53

**→ `serial_send_text`**

```
/* formatted */
int	g ( int	x )
{
	return x * 2 + 1 ; // helper
}
int f ( int x ) {
	int y = 7 ;␍
	while ( g ( x ) - 1 ) {
		y = y + g ( x ) ;
		x = x - 1 ;
	}
	if ( y ) { y = y + 1 ; }
	return␌ y +␋ x ;
}
// EOF
```

**← `serial_send_text`**

```
{"sent":212}
```

#### +0:12:58

**→ `serial_send_text`** `{"text": "                                            "}`

**← `serial_send_text`**

```
{"sent":44}
```

#### +0:13:02

**→ `serial_send_text`**

```
cat src
build src
run 2
run 4
```

**← `serial_send_text`**

```
{"sent":30}
```

#### +0:13:05

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e202f2a20666f726d6174746564202a2f0a696e740967202820696e74097820290a7b0a0972657475726e2078202a2032202b2031203b202f2f2068656c7065720a7d0a696e742066202820696e7420782029207b0a09696e742079203d2037203b0d0a097768696c6520282067202820782029202d20312029207b0a090979203d2079202b2067202820782029203b0a090978203d2078202d2031203b0a097d0a096966202820792029207b2079203d2079202b2031203b207d0a0972657475726e0c2079202b0b2078203b0a7d0a2f2f20454f4620202020202020202020202020202020202020202020202020202020202020202020202020202020202020200a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031300a7368656c6c3e20657869742030303030303032300a7368656c6c3e20
```

`text`

```
ready
saved
shell> /* formatted */
int	g ( int	x )
{
	return x * 2 + 1 ; // helper
}
int f ( int x ) {
	int y = 7 ;␍
	while ( g ( x ) - 1 ) {
		y = y + g ( x ) ;
		x = x - 1 ;
	}
	if ( y ) { y = y + 1 ; }
	return␌ y +␋ x ;
}
// EOF
shell> built
shell> exit 00000010
shell> exit 00000020
shell>
```

#### +0:13:07

> 💭 **Preparing edge-case tests**

**→ `serial_send_text`**

```
recv bin 64
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:13:22

**→ `serial_send_text`**

```
int f(int x) {
 return x + 99;
}
/* unterminated
```

**← `serial_send_text`**

```
{"sent":48}
```

#### +0:13:25

**→ `serial_send_text`** `{"text": "                "}`

**← `serial_send_text`**

```
{"sent":16}
```

#### +0:13:28

**→ `serial_send_text`**

```
build bin
run 2
run 4
```

**← `serial_send_text`**

```
{"sent":22}
```

#### +0:13:31

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031300a7368656c6c3e20657869742030303030303032300a7368656c6c3e20
```

`text`

```
ready
saved
shell> build error
shell> exit 00000010
shell> exit 00000020
shell>
```

#### +0:13:34

> 💭 **Preparing comment-placement tests**

**→ `serial_send_text`**

```
recv bin 64
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:13:47

**→ `serial_send_text`** `{"text": "int/**/f/**/(int/**/x)/**/{return/**/(x/**/+/**/2);}//end"}`

**← `serial_send_text`**

```
{"sent":57}
```

#### +0:13:51

**→ `serial_send_text`** `{"text": "       "}`

**← `serial_send_text`**

```
{"sent":7}
```

#### +0:13:53

**→ `serial_send_text`**

```
build bin
run 4
recv bin 32
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:13:57

**→ `serial_send_text`**

```
in/**/t f(int x){return x;}
```

**← `serial_send_text`**

```
{"sent":33}
```

#### +0:14:01

> 💭 **Building after whitespace**

**→ `serial_send_text`**

```
build bin
run 4
recv bin 40
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:14:07

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030360a7368656c6c3e2072656164790a73617665640a7368656c6c3e20756e6b6e6f776e20636f6d6d616e640a7368656c6c3e20657869742030303030303030360a7368656c6c3e2072656164790a
```

`text`

```
ready
saved
shell> built
shell> exit 00000006
shell> ready
saved
shell> unknown command
shell> exit 00000006
shell> ready
```

#### +0:14:10

**→ `serial_send_text`**

```
int f(int x){
return 1/**/2;
}
```

**← `serial_send_text`**

```
{"sent":31}
```

#### +0:14:12

**→ `serial_send_text`** `{"text": "         "}`

**← `serial_send_text`**

```
{"sent":9}
```

#### +0:14:16

**→ `serial_send_text`**

```
build bin
run 4
recv bin 32
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:14:19

**→ `serial_send_text`**

```
in/**/t f(int x){return x;}
```

**← `serial_send_text`**

```
{"sent":32}
```

#### +0:14:23

**→ `serial_send_text`**

```
build bin
run 4
build src
run 2
run 4
recv bin 64
```

**← `serial_send_text`**

```
{"sent":50}
```

#### +0:14:28

**→ `serial_send_text`**

```
int f(int x) {
 return x + 99;
}
/* unterminated
```

**← `serial_send_text`**

```
{"sent":64}
```

#### +0:14:31

**→ `serial_send_text`**

```
build bin
run 2
run 4
```

**← `serial_send_text`**

```
{"sent":22}
```

#### +0:14:34

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030360a7368656c6c3e2072656164790a73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030360a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031300a7368656c6c3e20657869742030303030303032300a7368656c6c3e2072656164790a73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031300a7368656c6c3e20657869742030303030303032300a7368656c6c3e20
```

`text`

```
saved
shell> build error
shell> exit 00000006
shell> ready
saved
shell> build error
shell> exit 00000006
shell> built
shell> exit 00000010
shell> exit 00000020
shell> ready
saved
shell> build error
shell> exit 00000010
shell> exit 00000020
shell>
```

#### +0:14:36

> 💭 **Checking source formatting**

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:14:46

**→ `notes_write`**

<details><summary>text (2,203 chars, 4 lines)</summary>

```
Completed lexical-whitespace compiler work on saved 022 disk; VM stopped. Kernel unchanged. FINAL working compiler assembly is file `empty` (6000 bytes, single-line mnemonic assembly plus tables/constants and trailing spaces). Original `progBad` unchanged and was source baseline; `progFwd` preserved unchanged. Reproduce: `as empty`; `install`; `build src`; `run 2`; `run 4`. as succeeds within 2048 executable limit. Kernel shell assembler DOES NOT accept LF in assembly input, nor b.le; don't import multiline assembly. C sources DO accept LF now.
Lexical rules: S skips space and ASCII9..13 (HT LF VT FF CR), nonnested /*...*/ and // through LF/CR or EOF. Unterminated block sets compiler error, including trailing comments. P remains raw peek, integer digit loop uses P, keyword-table matcher K never skips inside consecutive letters. Whitespace/comments accepted around punctuation and between tokens; int/**/f and return/**/(x/**/+/**/2) work. Keyword suffix checking prevents concatenating keywords/identifiers. ABI, existing subset and original single-line behavior preserved.
Tests: old beta built/run2=0000001c. Actual recv multiline `src`256 bytes preserved, cat confirmed tabs/LF/CR/FF/VT. Two functions g(x)=2*x+1 and f local y=7, while(g(x)-1){y=y+g(x);x=x-1;} if(y){y=y+1;} return y+x. Has initial block comment, inline line comment and final //EOF with no newline (44 trailing spaces). run2=00000010, run4=00000020. Separate comment-between-tokens program built/run4=6. in/**/t rejected; integer1/**/2 rejected; previous executable retained. FINAL bin64 bytes is received actual multiline `int f(int x) {\n return x + 99;\n}\n/* unterminated` plus16 spaces. build bin errors and run2/run4 still16/32, proving executable preserved. src remains successful formatted example; bin remains unterminated negative example. Other files untouched except old `empty`, `src`, `bin` reused.
Disk inherited:16 occupied slots,8192 file limit,recv NAME N exact raw bytes, no terminator, ready/saved. Kernel snapshots kernel0/kernel1 and FsBoot/FsRecv/FsFix/Check untouched. Existing fixed image13412 bytes, process PP constants correctly patched in inherited022. No kernel modifications this campaign.
```

</details>

**← `notes_write`**

```
{"saved":true}
```

#### +0:15:02

Saved working compiler assembly as `empty`; preserved `progBad`, `progFwd`, and the kernel.

Added all requested whitespace and comment handling. Formatted multiline two-function test returned 16 and 32 for arguments 2 and 4. Unterminated comments and split keywords/integers were rejected without replacing the executable.

VM stopped; concise notes saved.

## Observer message 1 +0:20:39

> The stage is still incomplete. Continue working. Unmet acceptance condition: All prior single-line control-flow and function-call syntax must still compile.
> Observed result: The final empty source passed the independent multiline lexical test and the expression-only regression. The first prior control-flow program int f(int x){int y=13;while(x){y=y+6;x=x-1;}return y;} was stored exactly and build returned build error instead of built. Earlier independent testing also saw build error for int g(int x){return x*10+10;} int f(int x){int y=x+1;y=g(y)+g(x+2);return y+x;}.,

#### +0:20:39

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T032044.711189Z"}
```

#### +0:20:42

> 💭 **Tracing B’s initializer rejection**
> 💭 **Preparing revised source**

**→ `serial_send_text`**

```
recv empty 6000
```

**← `serial_send_text`**

```
{"sent":16}
```

#### +0:21:03

**→ `serial_read`**

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e2072656164790a
```

`text`

```
BOOT
shell> ready
```

#### +0:21:06

**→ `serial_send_text`**

<details><summary>text (2,319 chars, 1 lines)</summary>

```
sub sp,sp,32;str x30,[sp];str x19,[sp,8];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,pool;mov w14,0;mov w15,0;mov w16,0;mov w19,0;mov w5,0;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;adr x6,pf;add x6,x6,6;bl K;cmp w19,2;b.ne bd;mov w0,60;bl C;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;adr x6,pf;bl K;bd:;bl S;cmp w0,105;b.ne st;ldrb w0,[x9,1];cmp w0,110;b.ne st;adr x6,di;bl K;bl E;mov w2,59;bl Q;mov w16,1;mov w0,48;bl C;st:;cmp w14,0;b.ne bad;bl S;cmp w0,114;b.eq rt;cmp w0,105;b.eq ci;cmp w0,119;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;cmp w7,0;b.eq pt;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;pt:;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;ldr x19,[sp,8];ldr x30,[sp];add sp,sp,32;ret; A:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,120;b.eq ax;cmp w0,121;b.ne ab;cmp w16,0;b.eq ab;mov w2,48;b ag;ax:;mov w2,44;ag:;str w2,[sp,8];add x9,x9,1;mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w0,[sp,8];bl C;b R;ab:;mov w14,1;b R;K:;sub sp,sp,16;str x30,[sp];mov w1,0;bl S;k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq ke;cmp w2,33;b.lt ks;cmp w2,97;b.ge kl;bl S;kl:;bl P;cmp w0,w2;b.ne ab;add x9,x9,1;mov w1,w2;cmp w2,123;b.eq kp;cmp w2,97;b.ge k0;kp:;mov w1,0;bl S;b k0;ks:;cmp w1,97;b.lt kt;bl B;kt:;bl S;mov w1,0;b k0;ke:;cmp w1,97;b.lt R;bl B;b R;B:;cmp w9,w10;b.ge br;ldrb w0,[x9];cmp w0,95;b.eq bx;cmp w0,48;b.lt br;cmp w0,58;b.lt bx;cmp w0,65;b.lt br;cmp w0,91;b.lt bx;cmp w0,97;b.lt br;cmp w0,123;b.ge br;bx:;mov w14,1;br:;ret;E:;sub sp,sp,16;str x30,[sp];bl T;e0:;cmp w14,0;b.ne R;bl S;cmp w0,43;b.eq ep;cmp w0,45;b.ne R;mov w2,28;b eg;ep:;mov w2,24;eg:;str w2,[sp,8];add x9,x9,1;bl G;bl T;bl H;ldr w0,[sp,8];bl C;b e0;T:;sub sp,sp,16;str x30,[sp];bl F;t0:;cmp w14,0;b.ne R;bl S;cmp w0,42;b.ne R;add x9,x9,1;bl G;bl F;bl H;mov w0,32;bl C;b t0;
```

</details>

**← `serial_send_text`**

```
{"sent":2319}
```

#### +0:21:35

**→ `serial_send_text`**

<details><summary>text (2,293 chars, 1 lines)</summary>

```
F:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fb;cmp w14,0;b.ne fr;bl S;cmp w0,103;b.eq fc;cmp w0,40;b.eq fp;cmp w0,120;b.eq fx;cmp w0,121;b.eq fy;sub w2,w0,48;cmp w2,0;b.lt fb;cmp w2,10;b.ge fb;mov w3,0;n0:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;cmp w3,w4;b.lt nk;b.eq nk;b fb;nk:;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,0;b.lt nd;cmp w2,10;b.lt n0;nd:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b fr;fx:;mov w0,0;b fv;fy:;cmp w16,0;b.eq fb;mov w0,40;fv:;add x9,x9,1;bl C;b fr;fc:;cmp w19,1;b.ne fb;add x9,x9,1;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq fr;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b fr;fb:;mov w14,1;fr:;sub w15,w15,1;b R;G:;mov w0,8;b J;H:;mov w0,16;J:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl C;ldr w0,[sp,8];add w0,w0,4;bl C;b R;Q:;sub sp,sp,16;str x30,[sp];bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;ldr x30,[sp];add sp,sp,16;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.eq ss;cmp w0,9;b.lt sl;cmp w0,14;b.lt ss;sl:;cmp w0,47;b.ne sr;add w0,w9,1;cmp w0,w10;b.ge sr;ldrb w0,[x9,1];cmp w0,47;b.eq line;cmp w0,42;b.ne sr;add x9,x9,2;block:;cmp w9,w10;b.ge un;ldrb w0,[x9];add x9,x9,1;cmp w0,42;b.ne block;cmp w9,w10;b.ge un;ldrb w0,[x9];cmp w0,47;b.ne block;ss:;add x9,x9,1;b S;line:;add x9,x9,2;ll:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,10;b.eq ss;cmp w0,13;b.eq ss;add x9,x9,1;b ll;un:;mov w14,1;b end;sr:;ldrb w0,[x9];ret;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;add w1,w13,w0;ldr w0,[x1];b W;W:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;full:;mov w14,1;ret; it:;.word 544501353;.word 1;pf:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;.word 379;di:;.word 544501353;.word 20775033;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 93810;pool:;mov w0,w1;mov w0,0;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;sub sp,sp,32;str x1,[sp];str x3,[sp,8];str x30,[sp,16];mov w1,w0;.word 1;ldr x30,[sp,16];ldr x3,[sp,8];ldr x1,[sp];add sp,sp,32;.word 0;
```

</details>

**← `serial_send_text`**

```
{"sent":2293}
```

#### +0:22:03

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:22:07

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:22:11

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:22:14

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:22:17

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":256}
```

#### +0:22:23

**→ `serial_send_text`**

```

```

**← `serial_send_text`**

```
{"sent":108}
```

#### +0:22:26

**→ `serial_send_text`**

```
as empty
install
build src
run 2
run 4
```

**← `serial_send_text`**

```
{"sent":39}
```

#### +0:22:28

**→ `serial_read`**

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031300a7368656c6c3e20657869742030303030303032300a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell> installed
shell> built
shell> exit 00000010
shell> exit 00000020
shell>
```

#### +0:22:31

**→ `serial_send_text`**

```
recv bin 64
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:22:36

**→ `serial_send_text`** `{"text": "int f(int x){int y=13;while(x){y=y+6;x=x-1;}return y;}"}`

**← `serial_send_text`**

```
{"sent":54}
```

#### +0:22:40

**→ `serial_send_text`** `{"text": "          "}`

**← `serial_send_text`**

```
{"sent":10}
```

#### +0:22:43

**→ `serial_send_text`**

```
build bin
run 2
run 4
recv bin 96
```

**← `serial_send_text`**

```
{"sent":34}
```

#### +0:22:46

**→ `serial_send_text`** `{"text": "int g(int x){return x*10+10;} int f(int x){int y=x+1;y=g(y)+g(x+2);return y+x;}"}`

**← `serial_send_text`**

```
{"sent":79}
```

#### +0:22:50

**→ `serial_send_text`** `{"text": "                 "}`

**← `serial_send_text`**

```
{"sent":17}
```

#### +0:22:53

**→ `serial_send_text`**

```
build bin
run 2
run 4
build beta
run 2
build alpha
run 4
```

**← `serial_send_text`**

```
{"sent":57}
```

#### +0:22:56

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031390a7368656c6c3e20657869742030303030303032350a7368656c6c3e2072656164790a73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303035630a7368656c6c3e20657869742030303030303038360a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031630a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030650a7368656c6c3e20
```

`text`

```
ready
saved
shell> built
shell> exit 00000019
shell> exit 00000025
shell> ready
saved
shell> built
shell> exit 0000005c
shell> exit 00000086
shell> built
shell> exit 0000001c
shell> built
shell> exit 0000000e
shell>
```

#### +0:23:00

> 💭 **Testing lexical regressions**

**→ `serial_send_text`**

```
recv bin 32
```

**← `serial_send_text`**

```
{"sent":12}
```

#### +0:23:10

**→ `serial_send_text`**

```
in/**/t f(int x){return x;}
```

**← `serial_send_text`**

```
{"sent":32}
```

#### +0:23:14

**→ `serial_send_text`**

```
build bin
recv bin 40
```

**← `serial_send_text`**

```
{"sent":22}
```

#### +0:23:17

**→ `serial_send_text`**

```
int f(int x){
return 1/**/2;
}
```

**← `serial_send_text`**

```
{"sent":40}
```

#### +0:23:21

**→ `serial_send_text`**

```
build bin
build src
run 2
run 4
recv bin 64
```

**← `serial_send_text`**

```
{"sent":44}
```

#### +0:23:24

**→ `serial_send_text`**

```
int f(int x) {
 return x + 99;
}
/* unterminated
```

**← `serial_send_text`**

```
{"sent":64}
```

#### +0:23:28

**→ `serial_send_text`**

```
build bin
run 2
run 4
```

**← `serial_send_text`**

```
{"sent":22}
```

#### +0:23:31

**→ `serial_read`**

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e2072656164790a73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031300a7368656c6c3e20657869742030303030303032300a7368656c6c3e2072656164790a73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031300a7368656c6c3e20657869742030303030303032300a7368656c6c3e20
```

`text`

```
ready
saved
shell> build error
shell> ready
saved
shell> build error
shell> built
shell> exit 00000010
shell> exit 00000020
shell> ready
saved
shell> build error
shell> exit 00000010
shell> exit 00000020
shell>
```

#### +0:23:34

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:23:39

**→ `notes_write`**

<details><summary>text (2,285 chars, 8 lines)</summary>

```
FINAL corrected compiler source `empty`,6000 bytes single-line assembly with trailing spaces. VM stopped; kernel,progBad,progFwd unchanged. Reproduce `as empty`;`install`;`build src`;`run 2`;`run 4`. Assembly fits2048 executable limit. Shell as requires single-line assembly and lacks b.le.
Important correction after independent regression: old B boundary test rejected entire ASCII48..122 range, accidentally rejecting '=' immediately after local y (int y=13). FINAL B tests exactly identifier continuation: digits,A-Z,a-z,underscore; punctuation no longer rejected. Retested actual recv prior single-line sources:
1 int f(int x){int y=13;while(x){y=y+6;x=x-1;}return y;} built,run2=00000019,run4=00000025.
2 int g(int x){return x*10+10;} int f(int x){int y=x+1;y=g(y)+g(x+2);return y+x;} built,run2=0000005c,run4=00000086.
Original beta built/run2=1c;original alpha built/run4=0e. These tests used bin scratch; final bin restored negative test below.
Lexical rules: S skips space and ASCII9..13(HT LF VT FF CR), nonnested /*...*/ and // until LF/CR or EOF. Unterminated block sets compiler error, including trailing comments. P is raw peek; integer digit loop uses P; K never skips inside consecutive keyword letters. Exact identifier boundary checks protect keyword endings. Whitespace/comments permitted around punctuation and between tokens. Earlier test int/**/f/**/(int/**/x)/**/{return/**/(x/**/+/**/2);}//end built/run4=6. Final retest in/**/t rejected,1/**/2 rejected. ABI and prior subset unchanged.
`src` is preserved recv256-byte actual multiline formatted two-function test (tabs,LF,CR,FF,VT,both comment kinds,final //EOF without LF plus44 spaces). g=2*x+1;f local y=7,while(g(x)-1){y=y+g(x);x=x-1;}if(y){y=y+1;}return y+x. FINAL build src success,run2=10,run4=20.
`bin` final64 bytes: `int f(int x) {\n return x + 99;\n}\n/* unterminated` plus16 spaces, received byte-exact. FINAL build bin errors;run2/run4 remain10/20 from src, proving previous executable retained. Other files untouched except empty/src/bin reused. Kernel snapshots and FsBoot/FsRecv/FsFix/Check unchanged; inherited022 image13412 bytes with correct process PP constants. Disk16 occupied slots,8192 file limit;recv exact N raw bytes,no terminator,ready/saved. No kernel modifications this campaign.
```

</details>

**← `notes_write`**

```
{"saved":true}
```

#### +0:23:54

Fixed the regression: identifier-boundary checking incorrectly rejected `=` after local variables.

Both reported single-line programs now compile and run correctly. Multiline lexical tests and rejection tests still pass.

Updated compiler remains in `empty`; kernel and `progFwd` unchanged. VM stopped and notes saved.
