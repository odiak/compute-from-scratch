# 032 — transcript

Mechanically converted from the Pi event log by [transcript.py](../transcript.py). Summary: [032-campaign.md](032-campaign.md). Control bytes appear as Unicode control pictures (␀, ␛, …), and `$REPO` stands for the repository root.

| | |
| --- | --- |
| Model | `openai-codex/gpt-6.1-sol` |
| Start (UTC) | 2026-11-04 09:32:36 |
| Duration | 0:43:29 |
| Tool calls | 207 |
| VM boots | 8 |
| Observer messages | 1 |
| Compactions | 0 |
| Tokens (input / cached / output) | 90,379 / 12,521,472 / 51,322 |

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

> Bootstrap a compiler written in C inside the guest. Start with the stage-031 kernel and disk. Keep the kernel fixed. Existing compiler src (stage 030), progMath, prog8, progFwd, empty and the other 16 inherited files are read-only for this stage. You may repurpose only the eight storage-test slots new1, longasm, raw, extra1, extra2, extra3, extra4 and extra5. The observer has backed them up. Files hold 32768 bytes; assembled, installed and generated code can be up to 8192 bytes. Use the guest assembler to build any new assembly seed. Use only the guest for builds and executions.
>
> The deliverable is a reproducible toolchain: assemble and install your seed in the guest, have it compile a small compiler written in C, install that result, and use that C-built compiler to compile and run further C source. It does not need to compile itself in this stage. The C-built compiler must parse real source, use the build ABI (x1 input, w2 length, x3 output, w4 capacity, w0 length or zero), and handle at least an int-returning function of a runtime integer parameter with integer literals, addition and subtraction. It must generate executable code whose result varies with both the actual source and runtime input. Reject malformed source safely without replacing a previous runnable program. Demonstrate two different inputs to the C-built compiler and multiple runtime arguments.
>
> Choose the smallest useful C dialect that lets you write the C-built compiler naturally. The seed should handle multiple named functions and multiple arguments, named local variables, char pointer reads and int pointer writes/indexing, conditionals and loops, and emit relocatable code suitable for install. Reuse the stage-030 toolchain if useful, but a new assembly seed alongside it is fine. Document the exact seed dialect and entry conventions so the observer can write an independent C program for it. Avoid introducing a special syntax or runtime helper that only implements the particular test compiler. A port of an outside compiler is not available in this isolated experiment.
>
> Save the complete exact assembly seed and C compiler source on disk. Record the file names, reproduction commands, and ABI, then stop the VM. Preserve existing inherited files. If anything is incomplete, record the observed behavior and remaining issue in the handoff.

#### +0:00:00

**→ `notes_read`**

**← `notes_read`**

`text`

<details><summary>text (7,583 chars, 44 lines)</summary>

```
Stage031 expanded filesystem implemented. Saved campaign guest image is 16008 bytes (stage029 15820-byte base plus188-byte guest-assembled migration). Persistent stage030 disk migrated IN GUEST. Final VM must be stopped (see final tool calls). Disk source files: src=UNCHANGED stage030 C compiler; bin=UNCHANGED four-local/helper demo. Earlier compilers/assembler and kernel0/kernel1 retained. All16 inherited names: alpha,beta,Abc123xyz789,empty,progFwd,progMath,progBad,prog8,FsBoot,FsRecv,bin,src,kernel0,kernel1,Check,FsFix. The observer restored empty after migration to its original 6000-byte stage-023 compiler. No other inherited file used for testing.

FINAL FORMAT (all offsets bytes, integers little-endian): virtual disk1MiB; driver reads/writes first0xe0000=917504 bytes. Directory at disk0, 24 fixed128-byte entries. byte0 name length (zero=unused), u16 at+2 logical byte length, name at+4 (1..12 ASCII alnum). +80=0xa5 means external payload at disk4096+slot*32768. Otherwise inherited inline data at entry+16 remains supported. Max24 files,32768 bytes/file, metadata u16 supports exact32768. New format marker u32=32768 at disk3072. Old disk had16 entries, external stride8192, same payload base4096; marker8192 at disk2048. Directory expansion consumes old marker. Unused directory bytes remain padding. No on-disk kernel boot sectors: kernel is campaign guest image, not either historical snapshot.

MIGRATION: appended code tests new marker; if absent, copies all16 old external8192-byte extents from slot15 DOWN to0 into32768-byte spaced extents; reverse slot order avoids overlap. Original128-byte entries and inline contents remain unchanged. Clears only new slots16..23 (1024 bytes), including old marker, sets new marker, writes disk. Then enters inherited shell. Rerun boots see marker and skip. No host disk conversion. This supports the inherited8192-stride stage030 disk, NOT arbitrary older4096-stride disks. Not power-fail-transactional; observer has original backup.

MEMORY: kernel40200000. Disk virtio workspace/cache base x22=40400000 (moved away from recv staging and existing runtime/network buffers); disk0 DMA maps40400400, directory40400400, external payload base40401400, new marker40401000. DMA ends404e0400. recv staging remains40050000..40058000, UART09000000. Existing code limits8192 retained. Process open metadata/payload base constants relocated40400400/40401400, its iteration count24 and external stride32768 patched. Main as/build/cat/save share external payload resolver patched to new stride. recv has separate resolver patched likewise, count24 and bound32768. Existing inline fallback unchanged. Shell line bound128 unchanged.

REPRODUCTION manifest also ON DISK extra2. extra1 is EXACT guest assembler migration source (188 bytes after as extra1); append assembled bytes at kernel offset0x3dcc. Base stage029 size0x3dcc=15820. Patch kernel offsets HEX with these literal replacement bytes (LE):
0940:1608a8d2 (x22 cache)
0a04:c101a052 (DMA length0xe0000)
0bd8:0d038052 (main file scan24)
0cc8:1a038052 (ls24)
12e8:a53c028b (shared data resolver shift15)
1308:1f224071 (save/append bound32768)
2fb4:0f038052 (process file scan24)
302c:08214091 (process file data stride32768)
3050:0004404000144040 (two process FS base pointers)
3080:53030014 (branch to migration3dcc)
31cc:02009052 (recv bound32768)
3218:0a038052 (recv scan24)
32f0:42401153 (recv stride shift15)
Appended hex EXACT:
c902209129012091220140b9010090523f00026ba0040054ea018052c5021091a5002091a500209142491353a500020bc6021091c6002091c600209142411153c600020b04008452a10040b9c10000b9a5100091c6100091841000519f00007141ffff544a0500515f0100718afdff54c50230910480805201008052a10000b9a5100091841000519f00007181ffff5401009052210100b921008052d0000010100240b900023fd690000010100240b900021fd6500a204050342040

EXTRA FILES (all8 beyond inherited16 occupied): new1=guest assembly generator of longasm; longasm=32768-byte assembler source (32754 ASCII spaces followed EXACTLY mov w0,77;ret;); raw=8 binary bytes 00 0a ff 0d 1b 80 41 7f; extra1=migration source; extra2=format/patch manifest text; extra3=longasm complete length+byte verifier; extra4=guest assembly generator of32754 spaces in extra5; extra5=32768-byte assembler source,32754 spaces then mov w0,88;ret;. new1/extra3 hardcode longasm slot17, extra4 hardcodes extra5 slot23. All new utility sources remain reproducible through as NAME/run. Do not execute extra1 as ordinary utility: it is kernel boot code. All inherited logical contents verified against the pre-stage disk after restoring empty.

EXTRACTION: raw disk entry i at128*i. Read name via byte0 and+4. Read u16 length+2. If byte+80=a5 extract exactly length bytes at4096+32768*i, else at128*i+16. Do not strip whitespace or zero bytes. In guest cat NAME writes logical bytes then ONE extra newline/prompt; account for framing, especially for binary/32768-byte sources. cat src and cat extra1/extra2 expose compiler and implementation. recv NAME N consumes exactly N raw bytes without CR/LF interpretation, N0..32768. Rejects too-large N before ready and before modifying old file. No executable format capacity change.

TESTS:
- First migrated boot ls retained16 names; cat bin exact original demo; as src/install/build bin/run2 =>0x31(49). New save new1 hello/cat worked beyond inherited16.
- longasm generated in guest, flushed, rebooted: as longasm =>assembled; run=>0x4d(77). Instructions exist ONLY in final14 bytes beyond8192 (indeed beyond32754).
- extra3 verifies directory word size32768/name length7, ALL32754 spaces AND exact14-byte instruction suffix; run=>0x8000 after multiple reboots including browser boot.
- recv raw8 received NUL, LF, ff, CR, ESC,80,A,7f. cat raw serial HEX exactly000aff0d1b80417f plus framing. recv raw32769=>error; subsequent cat SAME bytes. Repeat after reboot/browser reboot confirms persistence.
- Filled slots16..23; ls lists24 names. Attempt save extra6 six=>store full; all24 remain.
- append longasm x at32768=>invalid file; as longasm/run still77.
- extra4 generated32754 spaces in extra5. Reboot; append extra5 mov w0,88;ret;=>saved. as extra5/run=>0x58(88). append extra5 x=>invalid file; as/run STILL88. Thus shell append accepts >8192-byte source and exact32768 boundary, rejects overflow transactionally.
- Final compiler as src/install/build bin: run0=19,run2=49,run5=91. exec bin2 after build=>49. (exec immediately after assembling compiler but before build ran currently loaded compiler and returned0, so build before exec.)
- vm_boot_browser20261104T092632.657565Z: normal HTTP/ARP boot prints GREEN FIELD HTML; screen-001.png renders GREEN FIELD/OPEN WINDOW correctly. Same boot verified longasm, raw and C toolchain results. Final disk boot20261104T092905.780489Z verified expanded append and C demo. No exhaustive independent pre/post content hash comparison of all inherited files was performed; migration preserves their headers and copies entire old extents.

Prior compiler ABI: src current inherited C implementation supports31-char case-sensitive identifiers, parameter and four locals, helper, control flow, arrays/pointers; bin four-local demo result run0=19/run2=49/run5=91. Reassemble/install/build after boot as needed; installed executable/compiler RAM not persisted.

OBSERVER FINAL UPDATE: empty was a 6000-byte compiler, not blank. The observer restored its original bytes from the pre-stage disk via the new guest recv command. All 16 original files now match their original logical contents byte for byte; there are 24 files total. No kernel bytes were edited by the observer.
```

</details>

#### +0:00:03

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T093241.292273Z"}
```

#### +0:00:05

**→ `serial_send_text`**

```
cat src
```

**← `serial_send_text`**

```
{"sent":8}
```

#### +0:00:08

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

<details><summary>hex (8,192 chars, 1 lines)</summary>

```
424f4f540a7368656c6c3e202e776f726420323834373839383631313b6d6f762078392c78313b616464207731302c77312c77323b6d6f762078382c78333b6d6f76207831312c78333b616464207731322c77332c77343b616472207831332c706f3b6d6f76207731342c303b6d6f76207731362c303b6d6f76207731392c303b6d6f762077352c303b616472207831352c74623b6164722078362c69743b626c204b3b626c20533b636d702077302c3130333b622e65712067643b6d6f762077322c3130323b626c20513b622068643b67643a3b6164642078392c78392c313b6d6f76207731392c323b68643a3b626c204a3b636d70207731392c323b622e6e652062643b6d6f762077302c36303b626c20433b6d6f76207731362c343b67683a3b626c20533b6164722078362c72723b626c20543b636d702077302c313b622e65712067723b626c20413b622067683b67723a3b6164722078362c72723b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b6d6f762077302c33363b626c20433b6c64722077302c5b7831332c36305d3b6f72722077302c77302c77353b7374722077302c5b78385d3b6d6f76207731392c313b6164722078362c69743b626c204b3b6d6f762077322c3130323b626c20513b626c204a3b62643a3b626c20533b6164722078362c61643b626c20543b636d702077302c313b622e65712064613b622067656e3b626c20533b636d702077302c3130353b622e6e652067656e3b6c6472622077302c5b78392c315d3b636d702077302c3131303b622e6e652067656e3b7374722077392c5b7831352c34345d3b6164722078362c69743b626c204b3b626c20533b636d702077302c34323b6c64722077392c5b7831352c34345d3b622e6e652067656e3b62206261643b64613a3b6164722078362c61643b626c204b3b626c20503b7375622077322c77302c34383b636d702077322c313b622e6c74206261643b636d702077322c31303b622e6765206261643b626c20463b636d702077332c3531333b622e6765206261643b6d6f762077322c39333b626c20513b6d6f762077322c35393b626c20513b6d6f76207731362c333b6d6f762077302c39363b626c20433b616c3a3b6d6f762077302c3130343b626c20433b622073743b67656e3a3b6d6f76207731362c343b6c64722077302c5b7831332c3132345d3b626c20573b6d6f762077302c3130343b626c20433b64653a3b626c20533b6164722078362c69743b626c20543b636d702077302c313b622e6e652073743b6164722078362c69743b626c204b3b626c20533b636d702077302c34323b622e65712064703b626c204e3b626c204c3b636d702077332c303b622e6765206261643b6c64722077332c5b7831352c34305d3b636d702077332c353b622e6765206261643b7374722077312c5b7831352c34345d3b7374722077322c5b7831352c34385d3b6d6f762077322c36313b626c20513b626c20453b6d6f762077322c35393b626c20513b6c64722077332c5b7831352c34305d3b7375622077302c77332c313b6c736c2077302c77302c31303b6c64722077312c5b7831332c3133325d3b6f72722077302c77302c77313b626c20573b6c64722077312c5b7831352c34345d3b6c64722077322c5b7831352c34385d3b6c736c2077332c77332c333b6164642077332c7731352c77333b7374722077312c5b78335d3b7374722077322c5b78332c345d3b6c64722077332c5b7831352c34305d3b6164642077332c77332c313b7374722077332c5b7831352c34305d3b622064653b73743a3b636d70207731342c303b622e6e65206261643b626c20533b6164722078362c72723b626c20543b636d702077302c313b622e65712072743b6164722078362c69693b626c20543b636d702077302c313b622e65712063693b6164722078362c77773b626c20543b636d702077302c313b622e65712063773b626c20413b622073743b63693a3b6d6f762077372c303b6164722078362c69693b622063743b63773a3b6d6f762077372c313b6164722078362c77773b63743a3b626c204b3b6d6f76207731372c77353b626c20453b6d6f762077322c34313b626c20513b6d6f762077322c3132333b626c20513b6d6f762077302c35323b626c20433b6d6f76207731382c77353b6d6f762077302c35363b626c20433b6c623a3b636d70207731342c303b622e6e65206261643b626c20533b636d702077302c3132353b622e65712062653b626c20413b62206c623b62653a3b6164642078392c78392c313b2e776f7264203837323431353436333b7375622077302c7731372c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6c64722077312c5b7831332c36305d3b6f72722077302c77302c77313b626c20573b7375622077302c77352c7731383b6c736c2077302c77302c353b6c64722077312c5b7831332c35365d3b6f72722077302c77302c77313b6c736c2077312c7731382c323b6164642077312c77382c77313b7374722077302c5b78315d3b622073743b72743a3b6164722078362c72723b626c204b3b626c20453b6d6f762077322c35393b626c20513b6d6f762077322c3132353b626c20513b626c20533b636d702077392c7731303b622e6e65206261643b636d70207731362c343b622e6e65206f723b6c64722077302c5b7831332c3132385d3b626c20573b622072653b6f723a3b636d70207731362c323b622e6c742072653b6d6f762077302c3131363b626c20433b72653a3b6d6f762077302c33363b626c20433b636d70207731342c303b622e6e65206261643b7375622077302c7731312c77383b62207a3b6261643a3b6d6f762077302c303b7a3a3b2e776f726420323833313235323436373b7265743b413a3b2e776f726420343136323738353237383b626c20533b636d70207731362c343b622e657120616e3b636d702077302c39373b622e65712061613b636d702077302c34323b622e65712061703b636d702077302c3132313b622e65712079703b636d702077302c3132303b622e6e652061623b6d6f762077322c34343b6164642078392c78392c313b622061683b616e3a3b626c204e3b626c204c3b636d702077332c303b622e6c742061623b6d6f762077322c34343b636d702077332c303b622e65712061683b7375622077332c77332c313b6c736c2077332c77332c31303b6c64722077322c5b7831332c3133325d3b6f72722077322c77322c77333b622061683b61613a3b626c20493b626c20473b6d6f762077322c36313b626c20513b626c20453b626c20483b6d6f762077322c3132303b622061653b61703a3b636d70207731362c323b622e6e652061623b6164642078392c78392c313b6d6f762077322c3131323b626c20513b626c20423b6d6f762077322c3131323b61683a3b7374722077322c5b73702c385d3b6d6f762077322c36313b626c20513b626c20453b6c64722077322c5b73702c385d3b61653a3b7374722077322c5b73702c385d3b6d6f762077322c35393b626c20513b6c64722077302c5b73702c385d3b636d70207731362c343b622e6e652061633b636d702077302c34343b622e65712061633b626c20573b6220523b61633a3b626c20433b6220523b61623a3b6d6f76207731342c313b6220523b493a3b2e776f726420343136323738353237383b636d70207731362c333b622e6e652061623b6164642078392c78392c313b6d6f762077322c39313b626c20513b626c20453b6d6f762077322c39333b626c20513b6d6f762077302c31323b626c20433b6220523b4b3a3b2e776f726420343136323738353237383b626c20533b6b303a3b6c6472622077322c5b78365d3b6164642078362c78362c313b636d702077322c313b622e657120523b636d702077322c33333b622e6c74206b733b636d702077322c39373b622e6765206b6c3b626c20533b6b6c3a3b626c20503b636d702077302c77323b622e6e652061623b6164642078392c78392c313b6d6f762077312c77323b636d702077322c39373b622e6c74206b703b636d702077322c3132333b622e6e65206b303b6b703a3b626c20533b62206b303b6b733a3b636d702077312c39373b622e6c74206b743b626c20423b6b743a3b626c20533b62206b303b423a3b636d702077392c7731303b622e67652062723b6c6472622077302c5b78395d3b636d702077302c39353b622e65712062783b636d702077302c34383b622e6c742062723b636d702077302c35383b622e6c742062783b6d6f762077342c33323b6f72722077302c77302c77343b636d702077302c39373b622e6c742062723b636d702077302c3132333b622e67652062723b62783a3b6d6f76207731342c313b62723a3b7265743b453a3b6d6f762077322c313b563a3b2e776f726420323834373836393935303b626c20463b65303a3b626c20533b6d6f762077322c32343b6d6f762077332c313b636d702077302c34333b622e65712065673b6d6f762077322c32383b636d702077302c34353b622e65712065673b6d6f762077322c33323b6d6f762077332c323b636d702077302c34323b622e6e6520523b65673a3b6c64722077342c5b73702c385d3b636d702077332c77343b622e6c7420523b7374722077322c5b73702c31325d3b6164642078392c78392c313b626c20473b6164642077322c77332c313b626c20563b626c20483b6c64722077302c5b73702c31325d3b626c20433b622065303b463a3b2e776f726420343136323738353237383b626c20533b636d70207731362c343b622e657120666e3b636d70207731392c323b622e657120666e3b636d702077302c39373b622e65712066613b636d702077302c34323b622e65712066643b636d702077302c3130333b622e65712066633b636d702077302c3132303b622e65712066783b666e3a3b636d702077302c34303b622e65712066703b7375622077322c77302c34383b636d702077322c303b622e6c74206e613b636d702077322c31303b622e6765206e613b6d6f762077332c303b6e303a3b6d6f762077342c31303b2e776f7264203435333234393132333b2e776f726420313339333538393334343b636d702077302c303b622e6e652061623b6164642078392c78392c313b626c20503b7375622077322c77302c34383b636d702077322c31303b2e776f726420313432363036333037353b6c736c2077332c77332c353b6c64722077302c5b7831332c345d3b6f72722077302c77302c77333b626c20573b6220523b6e613a3b626c204e3b636d702077322c313b622e6e65206c6f3b6c6472622077302c5b78315d3b636d702077302c3130333b622e6e65206c6f3b626c20533b636d702077302c34303b622e65712063673b6c6f3a3b626c204c3b636d702077332c303b622e6c742061623b636d702077332c303b622e65712066303b7375622077332c77332c313b6c736c2077332c77332c31303b6c64722077302c5b7831332c3133365d3b6f72722077302c77302c77333b626c20573b6220523b66303a3b6d6f762077302c303b626c20433b6220523b66613a3b626c20493b6d6f762077302c32303b626c20433b62
```

</details>

`text`

<details><summary>text (4,096 chars, 2 lines)</summary>

```
BOOT
shell> .word 2847898611;mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;adr x13,po;mov w14,0;mov w16,0;mov w19,0;mov w5,0;adr x15,tb;adr x6,it;bl K;bl S;cmp w0,103;b.eq gd;mov w2,102;bl Q;b hd;gd:;add x9,x9,1;mov w19,2;hd:;bl J;cmp w19,2;b.ne bd;mov w0,60;bl C;mov w16,4;gh:;bl S;adr x6,rr;bl T;cmp w0,1;b.eq gr;bl A;b gh;gr:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;mov w0,36;bl C;ldr w0,[x13,60];orr w0,w0,w5;str w0,[x8];mov w19,1;adr x6,it;bl K;mov w2,102;bl Q;bl J;bd:;bl S;adr x6,ad;bl T;cmp w0,1;b.eq da;b gen;bl S;cmp w0,105;b.ne gen;ldrb w0,[x9,1];cmp w0,110;b.ne gen;str w9,[x15,44];adr x6,it;bl K;bl S;cmp w0,42;ldr w9,[x15,44];b.ne gen;b bad;da:;adr x6,ad;bl K;bl P;sub w2,w0,48;cmp w2,1;b.lt bad;cmp w2,10;b.ge bad;bl F;cmp w3,513;b.ge bad;mov w2,93;bl Q;mov w2,59;bl Q;mov w16,3;mov w0,96;bl C;al:;mov w0,104;bl C;b st;gen:;mov w16,4;ldr w0,[x13,124];bl W;mov w0,104;bl C;de:;bl S;adr x6,it;bl T;cmp w0,1;b.ne st;adr x6,it;bl K;bl S;cmp w0,42;b.eq dp;bl N;bl L;cmp w3,0;b.ge bad;ldr w3,[x15,40];cmp w3,5;b.ge bad;str w1,[x15,44];str w2,[x15,48];mov w2,61;bl Q;bl E;mov w2,59;bl Q;ldr w3,[x15,40];sub w0,w3,1;lsl w0,w0,10;ldr w1,[x13,132];orr w0,w0,w1;bl W;ldr w1,[x15,44];ldr w2,[x15,48];lsl w3,w3,3;add w3,w15,w3;str w1,[x3];str w2,[x3,4];ldr w3,[x15,40];add w3,w3,1;str w3,[x15,40];b de;st:;cmp w14,0;b.ne bad;bl S;adr x6,rr;bl T;cmp w0,1;b.eq rt;adr x6,ii;bl T;cmp w0,1;b.eq ci;adr x6,ww;bl T;cmp w0,1;b.eq cw;bl A;b st;ci:;mov w7,0;adr x6,ii;b ct;cw:;mov w7,1;adr x6,ww;ct:;bl K;mov w17,w5;bl E;mov w2,41;bl Q;mov w2,123;bl Q;mov w0,52;bl C;mov w18,w5;mov w0,56;bl C;lb:;cmp w14,0;b.ne bad;bl S;cmp w0,125;b.eq be;bl A;b lb;be:;add x9,x9,1;.word 872415463;sub w0,w17,w5;ldr w1,[x13,64];and w0,w0,w1;ldr w1,[x13,60];orr w0,w0,w1;bl W;sub w0,w5,w18;lsl w0,w0,5;ldr w1,[x13,56];orr w0,w0,w1;lsl w1,w18,2;add w1,w8,w1;str w0,[x1];b st;rt:;adr x6,rr;bl K;bl E;mov w2,59;bl Q;mov w2,125;bl Q;bl S;cmp w9,w10;b.ne bad;cmp w16,4;b.ne or;ldr w0,[x13,128];bl W;b re;or:;cmp w16,2;b.lt re;mov w0,116;bl C;re:;mov w0,36;bl C;cmp w14,0;b.ne bad;sub w0,w11,w8;b z;bad:;mov w0,0;z:;.word 2831252467;ret;A:;.word 4162785278;bl S;cmp w16,4;b.eq an;cmp w0,97;b.eq aa;cmp w0,42;b.eq ap;cmp w0,121;b.eq yp;cmp w0,120;b.ne ab;mov w2,44;add x9,x9,1;b ah;an:;bl N;bl L;cmp w3,0;b.lt ab;mov w2,44;cmp w3,0;b.eq ah;sub w3,w3,1;lsl w3,w3,10;ldr w2,[x13,132];orr w2,w2,w3;b ah;aa:;bl I;bl G;mov w2,61;bl Q;bl E;bl H;mov w2,120;b ae;ap:;cmp w16,2;b.ne ab;add x9,x9,1;mov w2,112;bl Q;bl B;mov w2,112;ah:;str w2,[sp,8];mov w2,61;bl Q;bl E;ldr w2,[sp,8];ae:;str w2,[sp,8];mov w2,59;bl Q;ldr w0,[sp,8];cmp w16,4;b.ne ac;cmp w0,44;b.eq ac;bl W;b R;ac:;bl C;b R;ab:;mov w14,1;b R;I:;.word 4162785278;cmp w16,3;b.ne ab;add x9,x9,1;mov w2,91;bl Q;bl E;mov w2,93;bl Q;mov w0,12;bl C;b R;K:;.word 4162785278;bl S;k0:;ldrb w2,[x6];add x6,x6,1;cmp w2,1;b.eq R;cmp w2,33;b.lt ks;cmp w2,97;b.ge kl;bl S;kl:;bl P;cmp w0,w2;b.ne ab;add x9,x9,1;mov w1,w2;cmp w2,97;b.lt kp;cmp w2,123;b.ne k0;kp:;bl S;b k0;ks:;cmp w1,97;b.lt kt;bl B;kt:;bl S;b k0;B:;cmp w9,w10;b.ge br;ldrb w0,[x9];cmp w0,95;b.eq bx;cmp w0,48;b.lt br;cmp w0,58;b.lt bx;mov w4,32;orr w0,w0,w4;cmp w0,97;b.lt br;cmp w0,123;b.ge br;bx:;mov w14,1;br:;ret;E:;mov w2,1;V:;.word 2847869950;bl F;e0:;bl S;mov w2,24;mov w3,1;cmp w0,43;b.eq eg;mov w2,28;cmp w0,45;b.eq eg;mov w2,32;mov w3,2;cmp w0,42;b.ne R;eg:;ldr w4,[sp,8];cmp w3,w4;b.lt R;str w2,[sp,12];add x9,x9,1;bl G;add w2,w3,1;bl V;bl H;ldr w0,[sp,12];bl C;b e0;F:;.word 4162785278;bl S;cmp w16,4;b.eq fn;cmp w19,2;b.eq fn;cmp w0,97;b.eq fa;cmp w0,42;b.eq fd;cmp w0,103;b.eq fc;cmp w0,120;b.eq fx;fn:;cmp w0,40;b.eq fp;sub w2,w0,48;cmp w2,0;b.lt na;cmp w2,10;b.ge na;mov w3,0;n0:;mov w4,10;.word 453249123;.word 1393589344;cmp w0,0;b.ne ab;add x9,x9,1;bl P;sub w2,w0,48;cmp w2,10;.word 1426063075;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl W;b R;na:;bl N;cmp w2,1;b.ne lo;ldrb w0,[x1];cmp w0,103;b.ne lo;bl S;cmp w0,40;b.eq cg;lo:;bl L;cmp w3,0;b.lt ab;cmp w3,0;b.eq f0;sub w3,w3,1;lsl w3,w3,10;ldr w0,[x13,136];orr w0,w0,w3;bl W;b R;f0:;mov w0,0;bl C;b R;fa:;bl I;mov w0,20;bl C;b
```

</details>

#### +0:00:10

> 💭 **Inspecting docs and commands**

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

<details><summary>hex (6,760 chars, 1 lines)</summary>

```
20523b66643a3b636d70207731362c323b622e6e652061623b6164642078392c78392c313b6d6f762077322c3131323b626c20513b626c20423b6d6f762077302c3130383b626c20433b6220523b66783a3b6164642078392c78392c313b6d6f762077302c303b626c20433b6220523b66633a3b6164642078392c78392c313b63673a3b636d70207731392c313b622e6e652061623b6d6f762077322c34303b626c20513b626c20453b6d6f762077322c34313b626c20513b6164642078362c7831332c36383b636c3a3b6c64722077302c5b78365d3b6164642078362c78362c343b636d702077302c303b622e657120523b636d702077302c313b622e6e652063653b7375622077302c77302c77353b6c64722077312c5b7831332c36345d3b616e642077302c77302c77313b6d6f762077312c3134383b6c736c2077312c77312c32343b6f72722077302c77302c77313b63653a3b626c20573b6220636c3b66703a3b6164642078392c78392c313b626c20453b6d6f762077322c34313b626c20513b6220523b473a3b6d6f762077302c383b6220433b483a3b6d6f762077302c31363b6220433b513a3b2e776f726420343136323738353237383b626c20533b636d702077302c77323b622e6e652061623b6164642078392c78392c313b523a3b2e776f726420343136353031313435343b7265743b533a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b636d702077302c33323b622e65712073733b636d702077302c393b622e6c7420736c3b636d702077302c31343b622e6c742073733b736c3a3b636d702077302c34373b622e6e6520503b6164642077302c77392c313b636d702077302c7731303b622e676520503b6c6472622077302c5b78392c315d3b636d702077302c34373b622e6571206c693b636d702077302c34323b622e6e6520503b6164642078392c78392c323b626b3a3b636d702077392c7731303b622e676520756e3b6c6472622077302c5b78395d3b6164642078392c78392c313b636d702077302c34323b622e6e6520626b3b636d702077392c7731303b622e676520756e3b6c6472622077302c5b78395d3b636d702077302c34373b622e6e6520626b3b73733a3b6164642078392c78392c313b6220533b6c693a3b6164642078392c78392c323b6c6c3a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b636d702077302c31303b622e65712073733b636d702077302c31333b622e65712073733b6164642078392c78392c313b62206c6c3b756e3a3b6d6f76207731342c313b6220656e643b503a3b636d702077392c7731303b622e676520656e643b6c6472622077302c5b78395d3b7265743b656e643a3b6d6f762077302c303b7265743b433a3b2e776f726420333039333331383034383b573a3b6164642078312c7831312c343b636d70207731322c77313b622e6c742066753b7374722077302c5b7831315d3b616464207831312c7831312c343b6164642077352c77352c313b7265743b66753a3b6d6f76207731342c313b7265743b4a3a3b2e776f726420343136323738353237383b6164722078362c6f703b626c204b3b626c204e3b7374722077312c5b7831355d3b7374722077322c5b7831352c345d3b6d6f762077302c313b7374722077302c5b7831352c34305d3b6164722078362c63703b626c204b3b6220523b4e3a3b2e776f726420343136323738353237383b626c20533b6164722078362c69743b626c20543b636d702077302c313b622e65712061623b6164722078362c61643b626c20543b636d702077302c313b622e65712061623b6164722078362c72723b626c20543b636d702077302c313b622e65712061623b6164722078362c69693b626c20543b636d702077302c313b622e65712061623b6164722078362c77773b626c20543b636d702077302c313b622e65712061623b626c20503b6d6f762078312c78393b6d6f762077322c303b636d702077302c39353b622e6571206e633b6d6f762077342c33323b6f72722077302c77302c77343b636d702077302c39373b622e6c742061623b636d702077302c3132333b622e67652061623b6e633a3b6164642078392c78392c313b6164642077322c77322c313b636d702077322c33323b622e67652061623b626c20503b636d702077302c39353b622e6571206e633b636d702077302c34383b622e6c7420523b636d702077302c35383b622e6c74206e633b6d6f762077342c33323b6f72722077302c77302c77343b636d702077302c39373b622e6c7420523b636d702077302c3132333b622e6c74206e633b6220523b4c3a3b7374722077322c5b7831352c35325d3b6d6f762077332c303b6c793a3b6c64722077302c5b7831352c34305d3b636d702077332c77303b622e6765206c6e3b6c736c2077342c77332c333b6164642077342c7731352c77343b6c64722077302c5b78342c345d3b636d702077302c77323b622e6e65206c743b6c64722077342c5b78345d3b6d6f762077362c303b6c633a3b6164642077302c77312c77363b6c6472622077302c5b78305d3b6c6472622077322c5b78345d3b636d702077302c77323b622e6e65206c643b6164642078342c78342c313b6164642077362c77362c313b6c64722077322c5b7831352c35325d3b636d702077362c77323b622e6c74206c633b7265743b6c643a3b6c64722077322c5b7831352c35325d3b6c743a3b6164642077332c77332c313b62206c793b6c6e3a3b6d6f762077332c303b7375622077332c77332c313b7265743b69743a3b2e776f7264203534343530313335333b2e776f726420313b6f703a3b2e776f726420313935333339323933363b2e776f7264203238383b63703a3b2e776f72642039373036353b2e776f726420313b69693a3b2e776f7264203637313131343835373b2e776f726420313b77773a3b2e776f726420313831383834373335313b2e776f72642031393339383735373b72723a3b2e776f726420313937303536323431383b2e776f72642031383930323634323b70643a3b2e776f7264203534343530313335333b2e776f726420313032353533363034323b2e776f7264203939373739353336303b2e776f726420313b61643a3b2e776f726420313931383938363333393b2e776f72642032323736353835363b706f3a3b6d6f762077302c77313b6d6f762077302c303b2e776f726420333038393034333432343b6164642077302c77342c77303b2e776f726420333039313236393630323b6c6472622077302c5b78305d3b6164642077302c77322c77303b7375622077302c77322c77303b6d756c2077302c77322c77303b7265743b6d6f762077302c77333b6d6f762077312c77303b6d6f762077332c77303b636d702077302c303b2e776f726420313430393238363134343b2e776f7264203333353534343332303b2e776f72642036373130383836333b2e776f726420343136323731393734323b2e776f726420323833353338363333373b6d6f762077312c77303b2e776f726420313b2e776f726420323833393538303634313b2e776f726420343136353037363939303b2e776f726420303b7375622073702c73702c31363b7374722077332c5b73705d3b6164642078342c73702c303b6c64722077302c5b78345d3b7374722077302c5b78345d3b6164642073702c73702c31363b737472622077302c5b78325d3b7375622073702c73702c31363b6164642073702c73702c31363b7374722077302c5b78345d3b6c64722077302c5b78345d3b74623a3b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b543a3b6d6f762078312c78393b746c3a3b6c6472622077322c5b78365d3b636d702077322c39373b622e6c742074653b6c6472622077302c5b78315d3b636d702077302c77323b622e6e6520746e3b6164642078312c78312c313b6164642078362c78362c313b6220746c3b74653a3b6c6472622077302c5b78315d3b636d702077302c39353b622e657120746e3b636d702077302c34383b622e6c742074793b636d702077302c35383b622e6c7420746e3b6d6f762077342c33323b6f72722077302c77302c77343b636d702077302c39373b622e6c742074793b636d702077302c3132333b622e6c7420746e3b74793a3b6d6f762077302c313b7265743b746e3a3b6d6f762077302c303b7265743b64703a3b6c64722077302c5b7831352c31325d3b636d702077302c313b622e6e65206261643b6c64722077302c5b7831352c385d3b6c6472622077302c5b78305d3b636d702077302c3132313b622e6e65206261643b6c64722077302c5b7831352c34305d3b636d702077302c323b622e6e65206261643b6164722078362c70643b6164642078362c78362c343b626c204b3b6d6f76207731362c323b622073743b79703a3b636d70207731362c323b622e6e652061623b6164642078392c78392c313b6d6f762077322c3131323b622061683b0a7368656c6c3e20
```

</details>

`text`

<details><summary>text (3,380 chars, 2 lines)</summary>

```
 R;fd:;cmp w16,2;b.ne ab;add x9,x9,1;mov w2,112;bl Q;bl B;mov w0,108;bl C;b R;fx:;add x9,x9,1;mov w0,0;bl C;b R;fc:;add x9,x9,1;cg:;cmp w19,1;b.ne ab;mov w2,40;bl Q;bl E;mov w2,41;bl Q;add x6,x13,68;cl:;ldr w0,[x6];add x6,x6,4;cmp w0,0;b.eq R;cmp w0,1;b.ne ce;sub w0,w0,w5;ldr w1,[x13,64];and w0,w0,w1;mov w1,148;lsl w1,w1,24;orr w0,w0,w1;ce:;bl W;b cl;fp:;add x9,x9,1;bl E;mov w2,41;bl Q;b R;G:;mov w0,8;b C;H:;mov w0,16;b C;Q:;.word 4162785278;bl S;cmp w0,w2;b.ne ab;add x9,x9,1;R:;.word 4165011454;ret;S:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,32;b.eq ss;cmp w0,9;b.lt sl;cmp w0,14;b.lt ss;sl:;cmp w0,47;b.ne P;add w0,w9,1;cmp w0,w10;b.ge P;ldrb w0,[x9,1];cmp w0,47;b.eq li;cmp w0,42;b.ne P;add x9,x9,2;bk:;cmp w9,w10;b.ge un;ldrb w0,[x9];add x9,x9,1;cmp w0,42;b.ne bk;cmp w9,w10;b.ge un;ldrb w0,[x9];cmp w0,47;b.ne bk;ss:;add x9,x9,1;b S;li:;add x9,x9,2;ll:;cmp w9,w10;b.ge end;ldrb w0,[x9];cmp w0,10;b.eq ss;cmp w0,13;b.eq ss;add x9,x9,1;b ll;un:;mov w14,1;b end;P:;cmp w9,w10;b.ge end;ldrb w0,[x9];ret;end:;mov w0,0;ret;C:;.word 3093318048;W:;add x1,x11,4;cmp w12,w1;b.lt fu;str w0,[x11];add x11,x11,4;add w5,w5,1;ret;fu:;mov w14,1;ret;J:;.word 4162785278;adr x6,op;bl K;bl N;str w1,[x15];str w2,[x15,4];mov w0,1;str w0,[x15,40];adr x6,cp;bl K;b R;N:;.word 4162785278;bl S;adr x6,it;bl T;cmp w0,1;b.eq ab;adr x6,ad;bl T;cmp w0,1;b.eq ab;adr x6,rr;bl T;cmp w0,1;b.eq ab;adr x6,ii;bl T;cmp w0,1;b.eq ab;adr x6,ww;bl T;cmp w0,1;b.eq ab;bl P;mov x1,x9;mov w2,0;cmp w0,95;b.eq nc;mov w4,32;orr w0,w0,w4;cmp w0,97;b.lt ab;cmp w0,123;b.ge ab;nc:;add x9,x9,1;add w2,w2,1;cmp w2,32;b.ge ab;bl P;cmp w0,95;b.eq nc;cmp w0,48;b.lt R;cmp w0,58;b.lt nc;mov w4,32;orr w0,w0,w4;cmp w0,97;b.lt R;cmp w0,123;b.lt nc;b R;L:;str w2,[x15,52];mov w3,0;ly:;ldr w0,[x15,40];cmp w3,w0;b.ge ln;lsl w4,w3,3;add w4,w15,w4;ldr w0,[x4,4];cmp w0,w2;b.ne lt;ldr w4,[x4];mov w6,0;lc:;add w0,w1,w6;ldrb w0,[x0];ldrb w2,[x4];cmp w0,w2;b.ne ld;add x4,x4,1;add w6,w6,1;ldr w2,[x15,52];cmp w6,w2;b.lt lc;ret;ld:;ldr w2,[x15,52];lt:;add w3,w3,1;b ly;ln:;mov w3,0;sub w3,w3,1;ret;it:;.word 544501353;.word 1;op:;.word 1953392936;.word 288;cp:;.word 97065;.word 1;ii:;.word 671114857;.word 1;ww:;.word 1818847351;.word 19398757;rr:;.word 1970562418;.word 18902642;pd:;.word 544501353;.word 1025536042;.word 997795360;.word 1;ad:;.word 1918986339;.word 22765856;po:;mov w0,w1;mov w0,0;.word 3089043424;add w0,w4,w0;.word 3091269602;ldrb w0,[x0];add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ret;mov w0,w3;mov w1,w0;mov w3,w0;cmp w0,0;.word 1409286144;.word 335544320;.word 67108863;.word 4162719742;.word 2835386337;mov w1,w0;.word 1;.word 2839580641;.word 4165076990;.word 0;sub sp,sp,16;str w3,[sp];add x4,sp,0;ldr w0,[x4];str w0,[x4];add sp,sp,16;strb w0,[x2];sub sp,sp,16;add sp,sp,16;str w0,[x4];ldr w0,[x4];tb:;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;T:;mov x1,x9;tl:;ldrb w2,[x6];cmp w2,97;b.lt te;ldrb w0,[x1];cmp w0,w2;b.ne tn;add x1,x1,1;add x6,x6,1;b tl;te:;ldrb w0,[x1];cmp w0,95;b.eq tn;cmp w0,48;b.lt ty;cmp w0,58;b.lt tn;mov w4,32;orr w0,w0,w4;cmp w0,97;b.lt ty;cmp w0,123;b.lt tn;ty:;mov w0,1;ret;tn:;mov w0,0;ret;dp:;ldr w0,[x15,12];cmp w0,1;b.ne bad;ldr w0,[x15,8];ldrb w0,[x0];cmp w0,121;b.ne bad;ldr w0,[x15,40];cmp w0,2;b.ne bad;adr x6,pd;add x6,x6,4;bl K;mov w16,2;b st;yp:;cmp w16,2;b.ne ab;add x9,x9,1;mov w2,112;b ah;
shell>
```

</details>

#### +0:00:19

> 💭 **Designing assembly compiler**
> 💭 **Defining compiler state**

**→ `serial_send_text`**

```
help
cat bin
```

**← `serial_send_text`**

```
{"sent":13}
```

#### +0:00:52

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
68656c70206563686f206c6f61642072756e207361766520617070656e6420636174206c732061736d206c6f616466696c6520617320696e7374616c6c206275696c640a7368656c6c3e20696e74206728696e742068656c7065725f617267297b68656c7065725f6172673d68656c7065725f6172672b313b72657475726e2068656c7065725f6172672a333b7d696e74206628696e7420696e7075745f76616c7565297b696e7420636f6d6d6f6e5072656669783d696e7075745f76616c75652b313b696e7420636f6d6d6f6e507265666978323d636f6d6d6f6e5072656669782a323b696e742074686972645f333d6728636f6d6d6f6e50726566697832293b696e7420466f757274683d74686972645f332b636f6d6d6f6e5072656669783b696628696e7075745f76616c7565297b466f757274683d466f757274682b323b7d7768696c6528696e7075745f76616c7565297b696e7075745f76616c75653d696e7075745f76616c75652d313b74686972645f333d74686972645f332b313b7d72657475726e20466f757274682b74686972645f333b7d0a7368656c6c3e20
```

`text`

```
help echo load run save append cat ls asm loadfile as install build
shell> int g(int helper_arg){helper_arg=helper_arg+1;return helper_arg*3;}int f(int input_value){int commonPrefix=input_value+1;int commonPrefix2=commonPrefix*2;int third_3=g(commonPrefix2);int Fourth=third_3+commonPrefix;if(input_value){Fourth=Fourth+2;}while(input_value){input_value=input_value-1;third_3=third_3+1;}return Fourth+third_3;}
shell>
```

#### +0:01:00

> 💭 **Designing instruction templates**
> 💭 **Updating local frame access**

**→ `serial_send_text`**

<details><summary>text (2,684 chars, 33 lines)</summary>

```
save new1 sub sp,sp,96;str x19,[sp];str x20,[sp,8];str x21,[sp,16];str x22,[sp,24];str x23,[sp,32];
append new1 str x24,[sp,40];str x25,[sp,48];str x26,[sp,56];str x27,[sp,64];str x28,[sp,72];str x30,[sp,80];
append new1 mov x19,x1;add x20,x1,x2;mov x21,x3;mov x22,x3;add x23,x3,x4;mov w24,0;mov w25,0;
append new1 mov w0,0;bl emit;bl next;top:;bl tok;cmp w0,0;b.eq done;cmp w24,0;b.ne done;bl function;b top;
append new1 done:;cmp w25,0;b.eq fail;cmp w24,0;b.ne fail;sub w0,w27,w22;lsr w0,w0,2;
append new1 mov w1,5120;lsl w1,w1,16;orr w0,w0,w1;str w0,[x22];sub w0,w21,w22;b finish;
append new1 fail:;mov w0,0;finish:;ldr x19,[sp];ldr x20,[sp,8];ldr x21,[sp,16];ldr x22,[sp,24];
append new1 ldr x23,[sp,32];ldr x24,[sp,40];ldr x25,[sp,48];ldr x26,[sp,56];ldr x27,[sp,64];
append new1 ldr x28,[sp,72];ldr x30,[sp,80];add sp,sp,96;ret;
append new1 emit:;add x9,x21,4;cmp x9,x23;b.hi overflow;str w0,[x21];mov x21,x9;ret;
append new1 overflow:;mov w24,1;ret;tpl:;adr x9,templates;add x9,x9,x0;ldr w0,[x9];b emit;
append new1 tok:;adr x9,token;ldr w0,[x9];ret;value:;adr x9,token;ldr w0,[x9,4];ret;
append new1 expect:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl tok;ldr w1,[sp,8];cmp w0,w1;
append new1 b.eq exok;mov w24,1;exok:;bl next;ldr x30,[sp];add sp,sp,16;ret;
append new1 next:;mov w0,0;mov w1,0;mov x2,x19;mov w3,0;skip:;cmp x19,x20;b.hs ntstore;
append new1 ldrb w0,[x19];cmp w0,32;b.hi lex;add x19,x19,1;b skip;
append new1 lex:;mov x2,x19;cmp w0,48;b.lo ident;cmp w0,57;b.hi ident;mov w1,0;
append new1 digits:;sub w0,w0,48;mov w9,10;mul w1,w1,w9;add w1,w1,w0;add x19,x19,1;
append new1 cmp x19,x20;b.hs numend;ldrb w0,[x19];cmp w0,48;b.lo numend;cmp w0,57;b.ls digits;
append new1 numend:;mov w0,256;b ntstore;
append new1 ident:;cmp w0,95;b.eq idstart;orr w9,w0,32;cmp w9,97;b.lo punct;cmp w9,122;b.hi punct;
append new1 idstart:;mov w3,0;idloop:;add x19,x19,1;add w3,w3,1;cmp w3,31;b.hi lexerr;
append new1 cmp x19,x20;b.hs idend;ldrb w9,[x19];cmp w9,95;b.eq idloop;
append new1 cmp w9,48;b.lo idalpha;cmp w9,57;b.ls idloop;idalpha:;orr w9,w9,32;
append new1 cmp w9,97;b.lo idend;cmp w9,122;b.ls idloop;
append new1 idend:;mov w0,257;adr x10,keywords;mov w11,258;
append new1 kwloop:;ldrb w12,[x10];cmp w12,0;b.eq ntstore;cmp w12,w3;b.ne kwnext;
append new1 mov w13,0;kwcmp:;add x14,x10,x13;ldrb w15,[x14,1];add x14,x2,x13;ldrb w14,[x14];
append new1 cmp w14,w15;b.ne kwnext;add w13,w13,1;cmp w13,w3;b.lo kwcmp;mov w0,w11;b ntstore;
append new1 kwnext:;add x10,x10,x12;add x10,x10,1;add w11,w11,1;b kwloop;
append new1 punct:;add x19,x19,1;b ntstore;lexerr:;mov w24,1;mov w0,0;
append new1 ntstore:;adr x9,token;str w0,[x9];str w1,[x9,4];str x2,[x9,8];str w3,[x9,16];ret;
```

</details>

**← `serial_send_text`**

```
{"sent":2684}
```

#### +0:01:53

> 💭 **Testing assembler branch support**

**→ `serial_send_text`**

```
as new1
```

**← `serial_send_text`**

```
{"sent":8}
```

#### +0:01:59

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
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
shell> assembly error
shell>
```

#### +0:02:03

> 💭 **Checking shell line lengths**

**→ `serial_send_text`**

<details><summary>text (3,032 chars, 40 lines)</summary>

```
append new1 find:;adr x9,locals;cmp w0,0;b.eq flocal;adr x9,funcs;mov w8,w25;b fbegin;
append new1 flocal:;mov w8,w26;fbegin:;adr x10,token;ldr x11,[x10,8];ldr w12,[x10,16];mov w0,0;
append new1 floop:;cmp w0,w8;b.ge fmiss;ldr w13,[x9,8];cmp w13,w12;b.ne fstep;
append new1 ldr x13,[x9];mov w14,0;fcmp:;add x15,x11,x14;ldrb w15,[x15];
append new1 add x16,x13,x14;ldrb w16,[x16];cmp w15,w16;b.ne fstep;add w14,w14,1;
append new1 cmp w14,w12;b.lt fcmp;ret;fstep:;add x9,x9,32;add w0,w0,1;b floop;
append new1 fmiss:;mov w0,0;sub w0,w0,1;ret;
append new1 addlocal:;sub sp,sp,32;str x30,[sp];str w0,[sp,8];bl tok;cmp w0,257;b.ne albad;
append new1 mov w0,0;bl find;cmp w0,0;b.ge albad;cmp w26,32;b.ge albad;
append new1 adr x9,locals;lsl w10,w26,5;add x9,x9,x10;adr x10,token;ldr x11,[x10,8];
append new1 str x11,[x9];ldr w11,[x10,16];str w11,[x9,8];ldr w11,[sp,8];str w11,[x9,12];
append new1 str w26,[sp,12];add w26,w26,1;bl next;ldr w0,[sp,12];b alend;
append new1 albad:;mov w24,1;mov w0,0;alend:;ldr x30,[sp];add sp,sp,32;ret;
append new1 type:;sub sp,sp,16;str x30,[sp];bl tok;cmp w0,258;b.eq tyint;cmp w0,259;b.ne tybad;
append new1 mov w0,1;str w0,[sp,8];bl next;mov w0,42;bl expect;b tyout;
append new1 tyint:;mov w0,0;str w0,[sp,8];bl next;bl tok;cmp w0,42;b.ne tyout;
append new1 bl next;mov w0,2;str w0,[sp,8];b tyout;tybad:;mov w24,1;
append new1 tyout:;ldr w0,[sp,8];ldr x30,[sp];add sp,sp,16;ret;
append new1 function:;sub sp,sp,32;str x30,[sp];mov w26,0;mov w0,258;bl expect;bl tok;
append new1 cmp w0,257;b.ne fnerror;mov w0,1;bl find;cmp w0,0;b.ge fnerror;
append new1 cmp w25,16;b.ge fnerror;adr x9,funcs;lsl w10,w25,5;add x9,x9,x10;
append new1 adr x10,token;ldr x11,[x10,8];str x11,[x9];ldr w11,[x10,16];str w11,[x9,8];
append new1 str x21,[x9,16];mov x27,x21;str x9,[sp,8];add w25,w25,1;bl next;mov w0,40;bl expect;
append new1 mov w0,0;bl tpl;mov w0,4;bl tpl;mov w0,8;bl tpl;mov w0,12;bl tpl;
append new1 params:;bl tok;cmp w0,41;b.eq paramend;cmp w24,0;b.ne fnexit;cmp w26,4;b.ge fnerror;
append new1 bl type;bl addlocal;lsl w1,w0,10;add w1,w1,w26;mov w0,92;bl gettpl;
append new1 orr w0,w0,w1;bl emit;bl tok;cmp w0,44;b.ne paramend;bl next;b params;
append new1 paramend:;ldr x9,[sp,8];str w26,[x9,20];mov w0,41;bl expect;bl block;
append new1 mov w0,96;bl tpl;bl epilogue;b fnexit;fnerror:;mov w24,1;
append new1 fnexit:;ldr x30,[sp];add sp,sp,32;ret;
append new1 gettpl:;adr x9,templates;add x9,x9,x0;ldr w0,[x9];ret;
append new1 epilogue:;sub sp,sp,16;str x30,[sp];mov w0,16;bl tpl;mov w0,20;bl tpl;
append new1 mov w0,24;bl tpl;mov w0,28;bl tpl;ldr x30,[sp];add sp,sp,16;ret;
append new1 loadlocal:;lsl w1,w0,10;mov w0,88;bl gettpl;orr w0,w0,w1;b emit;
append new1 storelocal:;lsl w1,w0,10;mov w0,92;bl gettpl;orr w0,w0,w1;b emit;
append new1 block:;sub sp,sp,16;str x30,[sp];mov w0,123;bl expect;
append new1 bloop:;bl tok;cmp w0,125;b.eq bend;cmp w0,0;b.eq berror;cmp w24,0;b.ne bexit;
append new1 bl stmt;b bloop;berror:;mov w24,1;b bexit;bend:;bl next;
append new1 bexit:;ldr x30,[sp];add sp,sp,16;ret;
```

</details>

**← `serial_send_text`**

```
{"sent":3032}
```

#### +0:02:51

> 💭 **Rewriting local slot helpers**
> 💭 **Implementing expression precedence**

**→ `serial_send_text`**

<details><summary>text (3,265 chars, 43 lines)</summary>

```
append new1 loadslot:;lsl w1,w0,10;adr x9,templates;ldr w0,[x9,88];orr w0,w0,w1;b emit;
append new1 storeslot:;lsl w1,w0,10;adr x9,templates;ldr w0,[x9,92];orr w0,w0,w1;b emit;
append new1 push:;sub sp,sp,16;str x30,[sp];mov w0,32;bl tpl;mov w0,36;bl tpl;
append new1 ldr x30,[sp];add sp,sp,16;ret;
append new1 pop:;sub sp,sp,16;str x30,[sp];mov w0,40;bl tpl;mov w0,44;bl tpl;
append new1 ldr x30,[sp];add sp,sp,16;ret;
append new1 expression:;mov w0,1;expr:;sub sp,sp,32;str x30,[sp];str w0,[sp,8];bl primary;
append new1 str w1,[sp,20];eloop:;bl tok;mov w2,1;mov w3,0;cmp w0,60;b.eq eoperator;
append new1 mov w3,4;cmp w0,62;b.eq eoperator;mov w2,2;mov w3,48;cmp w0,43;b.eq eoperator;
append new1 mov w3,52;cmp w0,45;b.eq eoperator;mov w2,3;mov w3,56;cmp w0,42;b.ne eend;
append new1 eoperator:;ldr w4,[sp,8];cmp w2,w4;b.lt eend;str w3,[sp,12];str w2,[sp,16];
append new1 bl next;bl push;ldr w0,[sp,16];add w0,w0,1;bl expr;bl pop;ldr w0,[sp,12];
append new1 cmp w0,8;b.ge enormal;str w0,[sp,24];mov w0,104;bl tpl;ldr w0,[sp,24];
append new1 add w0,w0,108;bl tpl;mov w1,0;str w1,[sp,20];b eloop;
append new1 enormal:;bl tpl;b eloop;eend:;ldr w1,[sp,20];ldr x30,[sp];add sp,sp,32;ret;
append new1 primary:;sub sp,sp,48;str x30,[sp];bl tok;cmp w0,256;b.eq number;
append new1 cmp w0,40;b.eq paren;cmp w0,42;b.eq deref;cmp w0,257;b.ne prbad;
append new1 mov w0,0;bl find;cmp w0,0;b.lt call;str w0,[sp,8];ldr w1,[x9,12];
append new1 str w1,[sp,12];bl next;ldr w0,[sp,8];bl loadslot;b postfix;
append new1 number:;bl value;cmp w0,65535;b.hi prbad;lsl w1,w0,5;mov w0,96;bl gettpl;
append new1 orr w0,w0,w1;bl emit;mov w1,0;str w1,[sp,12];bl next;b postfix;
append new1 paren:;bl next;bl expression;str w1,[sp,12];mov w0,41;bl expect;b postfix;
append new1 deref:;bl next;bl primary;cmp w1,0;b.eq prbad;cmp w1,1;b.eq dchar;
append new1 mov w0,64;b dread;dchar:;mov w0,60;dread:;bl tpl;mov w1,0;str w1,[sp,12];b postfix;
append new1 call:;mov w0,1;bl find;cmp w0,0;b.lt prbad;str x9,[sp,16];bl next;
append new1 mov w0,40;bl expect;mov w0,0;str w0,[sp,20];bl tok;cmp w0,41;b.eq callend;
append new1 callargs:;bl expression;bl push;ldr w0,[sp,20];add w0,w0,1;str w0,[sp,20];
append new1 cmp w0,4;b.gt prbad;bl tok;cmp w0,44;b.ne callend;bl next;b callargs;
append new1 callend:;ldr x9,[sp,16];ldr w0,[x9,20];ldr w1,[sp,20];cmp w0,w1;b.ne prbad;
append new1 mov w0,41;bl expect;callpop:;ldr w1,[sp,20];cmp w1,0;b.eq calldo;
append new1 mov w0,40;bl gettpl;sub w0,w0,2;orr w0,w0,w1;bl emit;mov w0,44;bl tpl;
append new1 ldr w0,[sp,20];sub w0,w0,1;str w0,[sp,20];b callpop;
append new1 calldo:;ldr x9,[sp,16];ldr x0,[x9,16];sub w0,w0,w21;asr w0,w0,2;
append new1 mov w1,1023;lsl w1,w1,16;add w1,w1,65535;and w0,w0,w1;
append new1 mov w1,37888;lsl w1,w1,16;orr w0,w0,w1;bl emit;mov w1,0;str w1,[sp,12];
append new1 postfix:;bl tok;cmp w0,91;b.ne prend;ldr w1,[sp,12];cmp w1,0;b.eq prbad;
append new1 bl next;bl push;bl expression;mov w0,93;bl expect;bl pop;ldr w1,[sp,12];
append new1 cmp w1,1;b.eq ixchar;mov w0,68;bl tpl;mov w0,64;bl tpl;b ixend;
append new1 ixchar:;mov w0,48;bl tpl;mov w0,60;bl tpl;
append new1 ixend:;mov w1,0;str w1,[sp,12];b postfix;
append new1 prbad:;mov w24,1;mov w1,0;str w1,[sp,12];
append new1 prend:;ldr w1,[sp,12];ldr x30,[sp];add sp,sp,48;ret;
```

</details>

**← `serial_send_text`**

```
{"sent":3265}
```

#### +0:03:41

> 💭 **Reviewing ARM assembly fixes**
> 💭 **Preparing source-rewrite utility**
> 💭 **Testing assembler immediates**

**→ `serial_send_text`**

```
save raw orr w9,w0,32;add w1,w1,65535;cmp w0,65535;ret;
as raw
```

**← `serial_send_text`**

```
{"sent":63}
```

#### +0:04:17

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

<details><summary>hex (2,176 chars, 1 lines)</summary>

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
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
shell> assembly error
shell>
```

#### +0:04:21

**→ `serial_send_text`**

<details><summary>text (3,333 chars, 47 lines)</summary>

```
append new1 stmt:;sub sp,sp,48;str x30,[sp];bl tok;cmp w0,123;b.eq sblock;
append new1 cmp w0,258;b.eq decl;cmp w0,259;b.eq decl;cmp w0,260;b.eq sreturn;
append new1 cmp w0,261;b.eq sif;cmp w0,263;b.eq swhile;cmp w0,257;b.eq assign;
append new1 cmp w0,42;b.eq sindirect;mov w24,1;b sexit;
append new1 sblock:;bl block;b sexit;sreturn:;bl next;bl expression;mov w0,59;bl expect;
append new1 bl epilogue;b sexit;
append new1 decl:;bl type;bl addlocal;str w0,[sp,8];bl tok;cmp w0,61;b.ne dnoinit;
append new1 bl next;bl expression;ldr w0,[sp,8];bl storeslot;b dsemi;
append new1 dnoinit:;mov w0,96;bl tpl;ldr w0,[sp,8];bl storeslot;
append new1 dsemi:;mov w0,59;bl expect;b sexit;
append new1 assign:;mov w0,0;bl find;cmp w0,0;b.lt serror;str w0,[sp,8];ldr w1,[x9,12];
append new1 str w1,[sp,12];bl next;bl tok;cmp w0,91;b.eq sindex;mov w0,61;bl expect;
append new1 bl expression;ldr w0,[sp,8];bl storeslot;b ssemi;
append new1 sindex:;ldr w0,[sp,8];bl loadslot;bl push;bl next;bl expression;
append new1 mov w0,93;bl expect;bl pop;ldr w1,[sp,12];cmp w1,0;b.eq serror;
append new1 cmp w1,1;b.eq sachar;mov w0,68;bl tpl;b addressready;
append new1 sachar:;mov w0,48;bl tpl;b addressready;
append new1 sindirect:;bl next;bl primary;str w1,[sp,12];cmp w1,0;b.eq serror;
append new1 addressready:;bl push;mov w0,61;bl expect;bl expression;bl pop;
append new1 ldr w1,[sp,12];cmp w1,1;b.eq sschar;mov w0,72;bl tpl;b ssemi;
append new1 sschar:;mov w0,76;bl tpl;ssemi:;mov w0,59;bl expect;b sexit;
append new1 sif:;bl next;mov w0,40;bl expect;bl expression;mov w0,41;bl expect;
append new1 str x21,[sp,16];mov w0,80;bl tpl;bl stmt;bl tok;cmp w0,262;b.eq selse;
append new1 ldr x0,[sp,16];bl patchzero;b sexit;
append new1 selse:;str x21,[sp,24];mov w0,84;bl tpl;ldr x0,[sp,16];bl patchzero;
append new1 bl next;bl stmt;ldr x0,[sp,24];bl patchbranch;b sexit;
append new1 swhile:;str x21,[sp,24];bl next;mov w0,40;bl expect;bl expression;
append new1 mov w0,41;bl expect;str x21,[sp,16];mov w0,80;bl tpl;bl stmt;
append new1 ldr x0,[sp,24];sub w0,w0,w21;asr w0,w0,2;lsl w0,w0,6;lsr w0,w0,6;
append new1 mov w1,5120;lsl w1,w1,16;orr w0,w0,w1;bl emit;ldr x0,[sp,16];bl patchzero;b sexit;
append new1 serror:;mov w24,1;sexit:;ldr x30,[sp];add sp,sp,48;ret;
append new1 patchzero:;sub w1,w21,w0;lsl w1,w1,3;mov w2,13312;lsl w2,w2,16;
append new1 orr w1,w1,w2;str w1,[x0];ret;
append new1 patchbranch:;sub w1,w21,w0;lsr w1,w1,2;mov w2,5120;lsl w2,w2,16;
append new1 orr w1,w1,w2;str w1,[x0];ret;
append new1 templates:;.word 3506701311;.word 4177551358;.word 4177550333;.word 2432697341;
append new1 .word 4181745662;.word 4181744637;.word 2432959487;.word 3596551104;
append new1 .word 3506455551;.word 3103785952;.word 3107976162;.word 2432713727;
append new1 .word 184549440;.word 1258291264;.word 452066368;.word 960495616;
append new1 .word 3107971072;.word 184551488;.word 3103785024;.word 956301376;
append new1 .word 872415232;.word 335544320;.word 3107972000;.word 3103777696;
append new1 .word 1384120320;.word 2483027968;.word 1795162207;.word 446670816;.word 446682080;
append new1 keywords:;.word 1953392899;.word 1634231044;.word 1912996466;.word 1920300133;
append new1 .word 1718153842;.word 1936483588;.word 1752622437;.word 1701603703;.word 0;
append new1 token:;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 locals:;
```

</details>

**← `serial_send_text`**

```
{"sent":3333}
```

#### +0:04:57

> 💭 **Preparing a source patcher**
> 💭 **Building a source patcher**

**→ `serial_send_text`**

```
save raw mov w9,16448;lsl w9,w9,16;add w9,w9,3072;ldrb w5,[x9,2];ldrb w6,[x9,3];
append raw lsl w6,w6,8;orr w5,w5,w6;mov w10,16456;lsl w10,w10,16;mov w6,5120;add w10,w10,w6;
append raw mov w11,16458;lsl w11,w11,16;mov w6,37888;add w11,w11,w6;mov x12,x11;
append raw mov w13,16459;lsl w13,w13,16;mov w6,5120;add w13,w13,w6;
append raw mov w14,16459;lsl w14,w14,16;mov w6,37888;add w14,w14,w6;
append raw ldrb w7,[x9,770];ldrb w6,[x9,771];lsl w6,w6,8;orr w7,w7,w6;
append raw ldrb w8,[x9,898];ldrb w6,[x9,899];lsl w6,w6,8;orr w8,w8,w6;
append raw mov w0,0;mov w1,0;editloop:;cmp w1,w5;b.ge editdone;mov w2,0;cmp w7,0;b.eq copyone;
append raw match:;add w3,w1,w2;cmp w3,w5;b.ge copyone;add x4,x10,x3;ldrb w4,[x4];
append raw add x6,x13,x2;ldrb w6,[x6];cmp w4,w6;b.ne copyone;add w2,w2,1;cmp w2,w7;b.lt match;
append raw mov w2,0;reploop:;cmp w2,w8;b.ge replend;add x3,x14,x2;ldrb w3,[x3];
append raw strb w3,[x12];add x12,x12,1;add w2,w2,1;b reploop;
append raw replend:;add w1,w1,w7;add w0,w0,1;b editloop;
append raw copyone:;add x3,x10,x1;ldrb w3,[x3];strb w3,[x12];add x12,x12,1;add w1,w1,1;b editloop;
append raw editdone:;sub w5,w12,w11;strb w5,[x9,2];lsr w6,w5,8;strb w6,[x9,3];
append raw mov w1,0;back:;cmp w1,w5;b.ge endedit;add x2,x11,x1;ldrb w2,[x2];
append raw add x3,x10,x1;strb w2,[x3];add w1,w1,1;b back;endedit:;ret;
as raw
```

**← `serial_send_text`**

```
{"sent":1338}
```

#### +0:05:36

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

<details><summary>hex (1,682 chars, 1 lines)</summary>

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
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
shell> assembly error
shell>
```

#### +0:05:41

> 💭 **Isolating assembly error**

**→ `serial_send_text`**

```
save extra4 mov w9,16448;lsl w9,w9,16;add w9,w9,3072;ldrb w5,[x9,2];ret;
as extra4
save extra4 add x2,x11,x1;ldrb w2,[x2];strb w2,[x3];ret;
as extra4
save extra4 mov w6,37888;cmp w1,w5;b.ge endedit;endedit:;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":222}
```

#### +0:05:50

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell> saved
shell> assembly error
shell> saved
shell> assembled
shell>
```

#### +0:05:53

> 💭 **Checking x register support**

**→ `serial_send_text`**

```
save extra4 add x2,x11,x1;ret;
as extra4
save extra4 ldrb w2,[x2];strb w2,[x3];ret;
as extra4
save extra4 add w2,w11,w1;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":135}
```

#### +0:06:00

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
saved
shell> assembly error
shell> saved
shell> assembled
shell> saved
shell> assembled
shell>
```

#### +0:06:03

> 💭 **Rewriting x-register arithmetic**

**→ `serial_send_text`**

```
save raw mov w9,16448;lsl w9,w9,16;add w9,w9,3072;ldrb w5,[x9,2];ldrb w6,[x9,3];
append raw lsl w6,w6,8;orr w5,w5,w6;mov w10,16456;lsl w10,w10,16;mov w6,5120;add w10,w10,w6;
append raw mov w11,16458;lsl w11,w11,16;mov w6,37888;add w11,w11,w6;mov x12,x11;
append raw mov w13,16459;lsl w13,w13,16;mov w6,5120;add w13,w13,w6;
append raw mov w14,16459;lsl w14,w14,16;mov w6,37888;add w14,w14,w6;
append raw ldrb w7,[x9,770];ldrb w6,[x9,771];lsl w6,w6,8;orr w7,w7,w6;
append raw ldrb w8,[x9,898];ldrb w6,[x9,899];lsl w6,w6,8;orr w8,w8,w6;
append raw mov w0,0;mov w1,0;editloop:;cmp w1,w5;b.ge editdone;mov w2,0;cmp w7,0;b.eq copyone;
append raw match:;add w3,w1,w2;cmp w3,w5;b.ge copyone;add w4,w10,w3;ldrb w4,[x4];
append raw add w6,w13,w2;ldrb w6,[x6];cmp w4,w6;b.ne copyone;add w2,w2,1;cmp w2,w7;b.lt match;
append raw mov w2,0;reploop:;cmp w2,w8;b.ge replend;add w3,w14,w2;ldrb w3,[x3];
append raw strb w3,[x12];add x12,x12,1;add w2,w2,1;b reploop;
append raw replend:;add w1,w1,w7;add w0,w0,1;b editloop;
append raw copyone:;add w3,w10,w1;ldrb w3,[x3];strb w3,[x12];add x12,x12,1;add w1,w1,1;b editloop;
append raw editdone:;sub w5,w12,w11;strb w5,[x9,2];lsr w6,w5,8;strb w6,[x9,3];
append raw mov w1,0;back:;cmp w1,w5;b.ge endedit;add w2,w11,w1;ldrb w2,[x2];
append raw add w3,w10,w1;strb w2,[x3];add w1,w1,1;b back;endedit:;ret;
as raw
```

**← `serial_send_text`**

```
{"sent":1338}
```

#### +0:06:20

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
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
shell> assembly error
shell>
```

#### +0:06:23

> 💭 **Testing ldrb immediate syntax**

**→ `serial_send_text`**

```
save extra4 ldrb w7,[x9,770];strb w5,[x9,2];ret;
as extra4
save extra4 add x12,x12,1;mov x12,x11;ret;
as extra4
save extra4 mov w0,0;mov w1,0;editloop:;cmp w1,w5;b.ge editdone;mov w2,0;editdone:;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":210}
```

#### +0:06:28

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell> saved
shell> assembled
shell> saved
shell> assembled
shell>
```

#### +0:06:30

> 💭 **Checking assembler limits**

**→ `serial_send_text`**

```
cat raw
```

**← `serial_send_text`**

```
{"sent":8}
```

#### +0:06:41

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

<details><summary>hex (2,274 chars, 1 lines)</summary>

```
6d6f762077392c31363434383b6c736c2077392c77392c31363b6164642077392c77392c333037323b6c6472622077352c5b78392c325d3b6c6472622077362c5b78392c335d3b6c736c2077362c77362c383b6f72722077352c77352c77363b6d6f76207731302c31363435363b6c736c207731302c7731302c31363b6d6f762077362c353132303b616464207731302c7731302c77363b6d6f76207731312c31363435383b6c736c207731312c7731312c31363b6d6f762077362c33373838383b616464207731312c7731312c77363b6d6f76207831322c7831313b6d6f76207731332c31363435393b6c736c207731332c7731332c31363b6d6f762077362c353132303b616464207731332c7731332c77363b6d6f76207731342c31363435393b6c736c207731342c7731342c31363b6d6f762077362c33373838383b616464207731342c7731342c77363b6c6472622077372c5b78392c3737305d3b6c6472622077362c5b78392c3737315d3b6c736c2077362c77362c383b6f72722077372c77372c77363b6c6472622077382c5b78392c3839385d3b6c6472622077362c5b78392c3839395d3b6c736c2077362c77362c383b6f72722077382c77382c77363b6d6f762077302c303b6d6f762077312c303b656469746c6f6f703a3b636d702077312c77353b622e67652065646974646f6e653b6d6f762077322c303b636d702077372c303b622e657120636f70796f6e653b6d617463683a3b6164642077332c77312c77323b636d702077332c77353b622e676520636f70796f6e653b6164642077342c7731302c77333b6c6472622077342c5b78345d3b6164642077362c7731332c77323b6c6472622077362c5b78365d3b636d702077342c77363b622e6e6520636f70796f6e653b6164642077322c77322c313b636d702077322c77373b622e6c74206d617463683b6d6f762077322c303b7265706c6f6f703a3b636d702077322c77383b622e6765207265706c656e643b6164642077332c7731342c77323b6c6472622077332c5b78335d3b737472622077332c5b7831325d3b616464207831322c7831322c313b6164642077322c77322c313b62207265706c6f6f703b7265706c656e643a3b6164642077312c77312c77373b6164642077302c77302c313b6220656469746c6f6f703b636f70796f6e653a3b6164642077332c7731302c77313b6c6472622077332c5b78335d3b737472622077332c5b7831325d3b616464207831322c7831322c313b6164642077312c77312c313b6220656469746c6f6f703b65646974646f6e653a3b7375622077352c7731322c7731313b737472622077352c5b78392c325d3b6c73722077362c77352c383b737472622077362c5b78392c335d3b6d6f762077312c303b6261636b3a3b636d702077312c77353b622e676520656e64656469743b6164642077322c7731312c77313b6c6472622077322c5b78325d3b6164642077332c7731302c77313b737472622077322c5b78335d3b6164642077312c77312c313b62206261636b3b656e64656469743a3b7265743b0a7368656c6c3e20
```

</details>

`text`

```
mov w9,16448;lsl w9,w9,16;add w9,w9,3072;ldrb w5,[x9,2];ldrb w6,[x9,3];lsl w6,w6,8;orr w5,w5,w6;mov w10,16456;lsl w10,w10,16;mov w6,5120;add w10,w10,w6;mov w11,16458;lsl w11,w11,16;mov w6,37888;add w11,w11,w6;mov x12,x11;mov w13,16459;lsl w13,w13,16;mov w6,5120;add w13,w13,w6;mov w14,16459;lsl w14,w14,16;mov w6,37888;add w14,w14,w6;ldrb w7,[x9,770];ldrb w6,[x9,771];lsl w6,w6,8;orr w7,w7,w6;ldrb w8,[x9,898];ldrb w6,[x9,899];lsl w6,w6,8;orr w8,w8,w6;mov w0,0;mov w1,0;editloop:;cmp w1,w5;b.ge editdone;mov w2,0;cmp w7,0;b.eq copyone;match:;add w3,w1,w2;cmp w3,w5;b.ge copyone;add w4,w10,w3;ldrb w4,[x4];add w6,w13,w2;ldrb w6,[x6];cmp w4,w6;b.ne copyone;add w2,w2,1;cmp w2,w7;b.lt match;mov w2,0;reploop:;cmp w2,w8;b.ge replend;add w3,w14,w2;ldrb w3,[x3];strb w3,[x12];add x12,x12,1;add w2,w2,1;b reploop;replend:;add w1,w1,w7;add w0,w0,1;b editloop;copyone:;add w3,w10,w1;ldrb w3,[x3];strb w3,[x12];add x12,x12,1;add w1,w1,1;b editloop;editdone:;sub w5,w12,w11;strb w5,[x9,2];lsr w6,w5,8;strb w6,[x9,3];mov w1,0;back:;cmp w1,w5;b.ge endedit;add w2,w11,w1;ldrb w2,[x2];add w3,w10,w1;strb w2,[x3];add w1,w1,1;b back;endedit:;ret;
shell>
```

#### +0:06:44

**→ `serial_send_text`**

```
save extra4 mov w0,0;editloop:;b editloop;editdone:;ret;
as extra4
save extra4 lsr w6,w5,8;orr w7,w7,w6;sub w5,w12,w11;ret;
as extra4
save extra4 strb w3,[x12];add x12,x12,1;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":189}
```

#### +0:06:50

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell> saved
shell> assembly error
shell> saved
shell> assembled
shell>
```

#### +0:06:55

> 💭 **Checking lsr support**

**→ `serial_send_text`**

```
save extra4 lsr w6,w5,8;ret;
as extra4
save extra4 orr w7,w7,w6;ret;
as extra4
save extra4 sub w5,w12,w11;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":121}
```

#### +0:07:03

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
saved
shell> assembly error
shell> saved
shell> assembled
shell> saved
shell> assembled
shell>
```

#### +0:07:05

> 💭 **Testing ASR support**

**→ `serial_send_text`**

```
save extra4 asr w0,w0,2;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":39}
```

#### +0:07:15

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
saved
shell> assembly error
shell>
```

#### +0:07:19

**→ `serial_send_text`**

```
save raw mov w9,16448;lsl w9,w9,16;add w9,w9,3072;ldrb w5,[x9,2];ldrb w6,[x9,3];
append raw lsl w6,w6,8;orr w5,w5,w6;mov w10,16456;lsl w10,w10,16;mov w6,5120;add w10,w10,w6;
append raw mov w11,16458;lsl w11,w11,16;mov w6,37888;add w11,w11,w6;mov x12,x11;
append raw mov w13,16459;lsl w13,w13,16;mov w6,5120;add w13,w13,w6;
append raw mov w14,16459;lsl w14,w14,16;mov w6,37888;add w14,w14,w6;
append raw ldrb w7,[x9,770];ldrb w6,[x9,771];lsl w6,w6,8;orr w7,w7,w6;
append raw ldrb w8,[x9,898];ldrb w6,[x9,899];lsl w6,w6,8;orr w8,w8,w6;
append raw mov w0,0;mov w1,0;editloop:;cmp w1,w5;b.ge editdone;mov w2,0;cmp w7,0;b.eq copyone;
append raw match:;add w3,w1,w2;cmp w3,w5;b.ge copyone;add w4,w10,w3;ldrb w4,[x4];
append raw add w6,w13,w2;ldrb w6,[x6];cmp w4,w6;b.ne copyone;add w2,w2,1;cmp w2,w7;b.lt match;
append raw mov w2,0;reploop:;cmp w2,w8;b.ge replend;add w3,w14,w2;ldrb w3,[x3];
append raw strb w3,[x12];add x12,x12,1;add w2,w2,1;b reploop;
append raw replend:;add w1,w1,w7;add w0,w0,1;b editloop;
append raw copyone:;add w3,w10,w1;ldrb w3,[x3];strb w3,[x12];add x12,x12,1;add w1,w1,1;b editloop;
append raw editdone:;sub w5,w12,w11;strb w5,[x9,2];.word 1393065126;strb w6,[x9,3];
append raw mov w1,0;back:;cmp w1,w5;b.ge endedit;add w2,w11,w1;ldrb w2,[x2];
append raw add w3,w10,w1;strb w2,[x3];add w1,w1,1;b back;endedit:;ret;
as raw
save extra4 orr w9,w0,32;
save extra5 mov w9,32;orr w9,w0,w9;
run
```

**← `serial_send_text`**

```
{"sent":1409}
```

#### +0:07:37

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e20
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
shell> assembled
shell> saved
shell> saved
shell> exit 00000001
shell>
```

#### +0:07:40

> 💭 **Updating register-width additions**
> 💭 **Building register-width fixer**
> 💭 **Patching branch conditions**

**→ `serial_send_text`**

```
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
```

**← `serial_send_text`**

```
{"sent":154}
```

#### +0:08:12

> 💭 **Preparing table storage**

**→ `serial_send_text`**

<details><summary>text (3,222 chars, 48 lines)</summary>

```
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
append new1 funcs:;
save extra1 mov w9,16456;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;
append extra1 mov w10,16448;lsl w10,w10,16;add w10,w10,3072;ldrb w11,[x10,2];ldrb w12,[x10,3];
append extra1 lsl w12,w12,8;orr w11,w11,w12;add w11,w9,w11;mov w0,0;
append extra1 scan:;cmp w9,w11;b.ge out;ldrb w1,[x9];cmp w1,97;b.eq ckadd;cmp w1,99;b.eq ckcmp;b step;
append extra1 ckadd:;ldrb w1,[x9,1];cmp w1,100;b.ne step;ldrb w1,[x9,2];cmp w1,100;b.ne step;b ckx;
append extra1 ckcmp:;ldrb w1,[x9,1];cmp w1,109;b.ne step;ldrb w1,[x9,2];cmp w1,112;b.ne step;
append extra1 ckx:;ldrb w1,[x9,4];cmp w1,120;b.ne step;add x9,x9,4;
append extra1 rewrite:;ldrb w1,[x9];cmp w1,59;b.eq step;cmp w1,120;b.ne rnext;
append extra1 mov w1,119;strb w1,[x9];add w0,w0,1;rnext:;add x9,x9,1;b rewrite;
append extra1 step:;add x9,x9,1;b scan;out:;ret;
as extra1
run
as raw
save extra4 orr w9,w9,32;
save extra5 mov w16,32;orr w9,w9,w16;
run
```

</details>

**← `serial_send_text`**

```
{"sent":3222}
```

#### +0:08:49

> 💭 **Patching keyword constants**
> 💭 **Patching keyword encodings**

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303033370a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e20
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
shell> assembled
shell> exit 00000037
shell> assembled
shell> saved
shell> saved
shell> exit 00000001
shell>
```

#### +0:09:16

**→ `serial_send_text`**

<details><summary>text (2,194 chars, 110 lines)</summary>

```
save extra4 b.hs
save extra5 b.ge
run
save extra4 b.hi
save extra5 b.gt
run
save extra4 b.lo
save extra5 b.lt
run
save extra4 b.ls
save extra5 b.le
run
save extra4 lsr w0,w0,2;
save extra5 .word 1392671744;
run
save extra4 lsr w1,w1,2;
save extra5 .word 1392671777;
run
save extra4 asr w0,w0,2;
save extra5 .word 318783488;
run
save extra4 lsr w0,w0,6;
save extra5 .word 1392933888;
run
save extra4 add w1,w1,65535;
save extra5 mov w2,65535;orr w1,w1,w2;
run
save extra4 cmp w0,65535;
save extra5 mov w1,65535;cmp w0,w1;
run
save extra4 .word 3506701311;
save extra5 sub sp,sp,256;
run
save extra4 .word 4177551358;
save extra5 str x30,[sp,248];
run
save extra4 .word 4177550333;
save extra5 str x29,[sp,240];
run
save extra4 .word 2432697341;
save extra5 add x29,sp,0;
run
save extra4 .word 4181745662;
save extra5 ldr x30,[sp,248];
run
save extra4 .word 4181744637;
save extra5 ldr x29,[sp,240];
run
save extra4 .word 2432959487;
save extra5 add sp,sp,256;
run
save extra4 .word 3596551104;
save extra5 ret;
run
save extra4 .word 3506455551;
save extra5 sub sp,sp,16;
run
save extra4 .word 3103785952;
save extra5 str w0,[sp];
run
save extra4 .word 3107976162;
save extra5 ldr w2,[sp];
run
save extra4 .word 2432713727;
save extra5 add sp,sp,16;
run
save extra4 .word 184549440;
save extra5 add w0,w2,w0;
run
save extra4 .word 1258291264;
save extra5 sub w0,w2,w0;
run
save extra4 .word 452066368;
save extra5 mul w0,w2,w0;
run
save extra4 .word 960495616;
save extra5 ldrb w0,[x0];
run
save extra4 .word 3107971072;
save extra5 ldr w0,[x0];
run
save extra4 .word 3103785024;
save extra5 str w0,[x2];
run
save extra4 .word 956301376;
save extra5 strb w0,[x2];
run
save extra4 .word 3107972000;
save extra5 ldr w0,[x29];
run
save extra4 .word 3103777696;
save extra5 str w0,[x29];
run
save extra4 .word 1384120320;
save extra5 mov w0,0;
run
save extra4 .word 1795162207;
save extra5 cmp w2,w0;
run
save extra4 .word 1912996466;.word 1920300133;
save extra5 .word 1701971570;.word 1852994932;
run
save extra4 .word 1718153842;.word 1936483588;
save extra5 .word 73820418;.word 1702063205;
run
save extra4 .word 1752622437;.word 1701603703;
save extra5 .word 1768453893;.word 25964;
run
as new1
```

</details>

**← `serial_send_text`**

```
{"sent":2194}
```

#### +0:09:39

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

<details><summary>hex (3,428 chars, 1 lines)</summary>

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030330a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030360a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030360a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030330a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030320a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

</details>

`text`

<details><summary>text (1,714 chars, 110 lines)</summary>

```
saved
shell> saved
shell> exit 00000003
shell> saved
shell> saved
shell> exit 00000006
shell> saved
shell> saved
shell> exit 00000006
shell> saved
shell> saved
shell> exit 00000003
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000002
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> assembly error
shell>
```

</details>

#### +0:09:42

> 💭 **Checking assembly error**

**→ `serial_send_text`**

```
save extra4 sub sp,sp,96;str x19,[sp];ldr x19,[sp];add sp,sp,96;ret;
as extra4
save extra4 mov w0,0;add x29,sp,0;and w0,w0,w1;ret;
as extra4
save extra4 cmp w0,0;b.gt x;x:;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":187}
```

#### +0:09:55

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell> saved
shell> assembled
shell> saved
shell> assembly error
shell>
```

#### +0:09:58

> 💭 **Testing b.gt support**

**→ `serial_send_text`**

```
save extra4 cmp w0,0;b.le aa;aa:;ret;
as extra4
save extra4 cmp w0,0;b.ge aa;aa:;ret;
as extra4
save extra4 cmp w0,0;b.gt aa;aa:;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":144}
```

#### +0:10:04

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
saved
shell> assembly error
shell> saved
shell> assembled
shell> saved
shell> assembly error
shell>
```

#### +0:10:09

> 💭 **Rewrite comparison branches**

**→ `serial_send_text`**

```
as raw
save extra4 b.gt
save extra5 b.ge
run
save extra4 cmp w0,57;b.le
save extra5 cmp w0,58;b.lt
run
save extra4 cmp w9,57;b.le
save extra5 cmp w9,58;b.lt
run
save extra4 cmp w9,122;b.le
save extra5 cmp w9,123;b.lt
run
as new1
```

**← `serial_send_text`**

```
{"sent":229}
```

#### +0:10:27

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030370a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> saved
shell> saved
shell> exit 00000007
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> assembly error
shell>
```

#### +0:10:30

> 💭 **Testing label limits**
> 💭 **Preparing diagnostic source**
> 💭 **Checking assembler syntax**

> 💭 **Checking b.le and asr**

**→ `serial_send_text`**

```
as raw
save extra4 b.le
save extra5 b.lt
run
save extra4 lsr
save extra5 lsl
run
save extra4 asr
save extra5 lsl
run
as new1
```

**← `serial_send_text`**

```
{"sent":125}
```

#### +0:11:14

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030300a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030300a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030300a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> saved
shell> saved
shell> exit 00000000
shell> saved
shell> saved
shell> exit 00000000
shell> saved
shell> saved
shell> exit 00000000
shell> assembly error
shell>
```

#### +0:11:19

> 💭 **Implementing diagnostic filter**
> 💭 **Splitting semicolon statements**

**→ `serial_send_text`**

```
save extra1 mov w8,w1;mov w9,16456;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;
append extra1 mov w10,16448;lsl w10,w10,16;add w10,w10,3072;ldrb w11,[x10,2];ldrb w12,[x10,3];
append extra1 lsl w12,w12,8;orr w11,w11,w12;add w11,w9,w11;mov w12,16459;lsl w12,w12,16;
append extra1 mov w13,5120;add w12,w12,w13;mov w13,w12;mov w0,0;
append extra1 dl:;cmp w9,w11;b.ge dout;cmp w8,0;b.eq dgo;cmp w0,w8;b.ge dout;
append extra1 dgo:;mov w14,w9;mov w15,0;ldrb w1,[x9];cmp w1,98;b.eq dskip;
append extra1 cmp w1,97;b.ne dscan;ldrb w1,[x9,1];cmp w1,100;b.eq dskip;b dscan;
append extra1 dskip:;mov w15,1;dscan:;ldrb w1,[x9];add x9,x9,1;cmp w1,58;b.ne dnocol;
append extra1 mov w15,1;dnocol:;cmp w1,59;b.ne dscan;add w0,w0,1;cmp w15,0;b.ne dl;
append extra1 dc:;cmp w14,w9;b.ge dl;ldrb w1,[x14];strb w1,[x12];add x14,x14,1;add x12,x12,1;b dc;
append extra1 dout:;sub w1,w12,w13;strb w1,[x10,770];.word 1393064993;strb w1,[x10,771];ret;
as extra1
run
as extra4
```

**← `serial_send_text`**

```
{"sent":945}
```

#### +0:11:40

> 💭 **Verifying shift result**

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303461630a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
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
shell> assembled
shell> exit 000004ac
shell> assembly error
shell>
```

#### +0:11:47

> 💭 **Bisecting the statement prefix**

**→ `serial_send_text`**

```
as extra1
run 600
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:11:53

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303235380a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 00000258
shell> assembled
shell>
```

#### +0:11:56

**→ `serial_send_text`**

```
as extra1
run 900
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:12:02

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303338340a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 00000384
shell> assembled
shell>
```

#### +0:12:05

**→ `serial_send_text`**

```
as extra1
run 1050
as extra4
```

**← `serial_send_text`**

```
{"sent":29}
```

#### +0:12:10

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303431610a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 0000041a
shell> assembly error
shell>
```

#### +0:12:13

> 💭 **Locating trailing templates**

**→ `serial_send_text`**

```
as extra1
run 975
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:12:22

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303363660a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003cf
shell> assembly error
shell>
```

#### +0:12:27

**→ `serial_send_text`**

```
as extra1
run 938
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:12:31

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361610a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003aa
shell> assembled
shell>
```

#### +0:12:34

**→ `serial_send_text`**

```
as extra1
run 956
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:12:37

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303362630a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003bc
shell> assembled
shell>
```

#### +0:12:40

**→ `serial_send_text`**

```
as extra1
run 966
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:12:44

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303363360a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003c6
shell> assembly error
shell>
```

#### +0:12:49

**→ `serial_send_text`**

```
as extra1
run 961
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:12:54

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303363310a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003c1
shell> assembled
shell>
```

#### +0:12:58

**→ `serial_send_text`**

```
as extra1
run 963
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:13:03

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303363330a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003c3
shell> assembled
shell>
```

#### +0:13:06

**→ `serial_send_text`**

```
as extra1
run 964
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:13:12

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303363340a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003c4
shell> assembled
shell>
```

#### +0:13:15

> 💭 **Rewriting the statement extractor**

**→ `serial_send_text`**

```
save extra1 mov w8,w1;mov w9,16456;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;mov w0,0;
append extra1 el:;mov w14,w9;es:;ldrb w1,[x9];add x9,x9,1;cmp w1,59;b.ne es;add w0,w0,1;
append extra1 cmp w0,w8;b.lt el;mov w12,16459;lsl w12,w12,16;mov w13,5120;add w12,w12,w13;
append extra1 mov w13,w12;ec:;cmp w14,w9;b.ge ed;ldrb w1,[x14];strb w1,[x12];
append extra1 add x14,x14,1;add x12,x12,1;b ec;ed:;sub w1,w12,w13;
append extra1 mov w10,16448;lsl w10,w10,16;add w10,w10,3840;strb w1,[x10,2];mov w1,0;
append extra1 strb w1,[x10,3];ret;
as extra1
run 965
cat extra4
```

**← `serial_send_text`**

```
{"sent":560}
```

#### +0:13:29

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303363350a7368656c6c3e202e776f726420303b0a7368656c6c3e20
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
shell> assembled
shell> exit 000003c5
shell> .word 0;
shell>
```

#### +0:13:32

> 💭 **Checking assembler output limits**
> 💭 **Checking assembler output limits**

**→ `serial_send_text`**

```
as extra4
run 1
```

**← `serial_send_text`**

```
{"sent":16}
```

#### +0:13:55

**→ `serial_read`** `{"wait_ms": 100}`

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

#### +0:13:58

> 💭 **Checking .word0 VM crash**

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:14:07

> 💭 **Checking save persistence**
> 💭 **Building guest assembler**
> 💭 **Relocating locals and functions**

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T094716.376098Z"}
```

#### +0:14:40

**→ `serial_send_text`**

```
as raw
save extra4 .word 0;
save extra5
run
save extra4 adr x9,funcs;
save extra5 adr x9,locals;add x9,x9,1024;
run
save extra2 pending
as new1
```

**← `serial_send_text`**

```
{"sent":144}
```

#### +0:14:45

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20696e76616c69642066696c650a7368656c6c3e20657869742030303030303130370a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030320a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
BOOT
shell> assembled
shell> saved
shell> invalid file
shell> exit 00000107
shell> saved
shell> saved
shell> exit 00000002
shell> saved
shell> assembly error
shell>
```

#### +0:14:47

> 💭 **Removing stray lsl text**
> 💭 **Restoring corrupted source**

**→ `serial_send_text`**

```
save extra4 lsllsl
save extra5 .word 0;.word 0;
run
save extra4 lsltoken:
save extra5 .word 0;token:
run
save extra4 .word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;
save extra5 ;
run
save extra2 pending
as new1
```

**← `serial_send_text`**

```
{"sent":228}
```

#### +0:15:12

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303038330a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303032300a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> exit 00000083
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000020
shell> saved
shell> assembly error
shell>
```

#### +0:15:14

> 💭 **Regenerating diagnostic prefix**

**→ `serial_send_text`**

```
save extra1 mov w8,w1;mov w9,16456;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;
append extra1 mov w10,16448;lsl w10,w10,16;add w10,w10,3072;ldrb w11,[x10,2];ldrb w12,[x10,3];
append extra1 lsl w12,w12,8;orr w11,w11,w12;add w11,w9,w11;mov w12,16459;lsl w12,w12,16;
append extra1 mov w13,5120;add w12,w12,w13;mov w13,w12;mov w0,0;
append extra1 dl:;cmp w9,w11;b.ge dout;cmp w8,0;b.eq dgo;cmp w0,w8;b.ge dout;
append extra1 dgo:;mov w14,w9;mov w15,0;ldrb w1,[x9];cmp w1,98;b.eq dskip;
append extra1 cmp w1,97;b.ne dscan;ldrb w1,[x9,1];cmp w1,100;b.eq dskip;b dscan;
append extra1 dskip:;mov w15,1;dscan:;ldrb w1,[x9];add x9,x9,1;cmp w1,58;b.ne dnocol;
append extra1 mov w15,1;dnocol:;cmp w1,59;b.ne dscan;add w0,w0,1;cmp w15,0;b.ne dl;
append extra1 dc:;cmp w14,w9;b.ge dl;ldrb w1,[x14];strb w1,[x12];add x14,x14,1;add x12,x12,1;b dc;
append extra1 dout:;sub w1,w12,w13;strb w1,[x10,770];.word 1393064993;strb w1,[x10,771];ret;
as extra1
run
as extra4
```

**← `serial_send_text`**

```
{"sent":945}
```

#### +0:15:28

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303363650a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
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
shell> assembled
shell> exit 000003ce
shell> assembly error
shell>
```

#### +0:15:33

> 💭 **Checking filtered output length**

**→ `serial_send_text`**

```
save extra5 mov w9,16448;lsl w9,w9,16;add w9,w9,3840;ldrb w0,[x9,2];ldrb w1,[x9,3];lsl w1,w1,8;orr w0,w0,w1;ret;
as extra5
run
```

**← `serial_send_text`**

```
{"sent":127}
```

#### +0:15:44

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030313639660a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell> exit 0000169f
shell>
```

#### +0:15:47

> 💭 **Checking instruction count**

**→ `serial_send_text`**

```
save extra5 mov w9,16459;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;mov w0,0;mov w1,5791;
append extra5 cl:;cmp w1,0;b.eq ce;ldrb w2,[x9];cmp w2,59;b.ne cn;add w0,w0,1;
append extra5 cn:;add x9,x9,1;sub w1,w1,1;b cl;ce:;ret;
as extra5
run
```

**← `serial_send_text`**

```
{"sent":236}
```

#### +0:15:57

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303230360a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> saved
shell> assembled
shell> exit 00000206
shell>
```

#### +0:15:59

> 💭 **Counting assembler instructions**
> 💭 **Planning seed linker**
> 💭 **Preparing seed linker**

> 💭 **Checking code length**
> 💭 **Implementing two-pass assembler**

**→ `serial_send_text`**

```
save extra4 adr x0,here;here:;ret;
as extra4
run
```

**← `serial_send_text`**

```
{"sent":49}
```

#### +0:16:43

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742034303134303030340a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell> exit 40140004
shell>
```

#### +0:16:46

> 💭 **Inspecting tiny routine entry**
> 💭 **Creating copy utility**
> 💭 **Building two-pass parser**

> 💭 **Designing decimal output helper**
> 💭 **Encoding ARM instruction words**

> 💭 **Preparing segmented assembly**
> 💭 **Removing empty semicolons**

**→ `serial_send_text`**

```
as raw
save extra4 ;;
save extra5 ;
run
run
run
run
run
save extra2 pending
as new1
```

**← `serial_send_text`**

```
{"sent":84}
```

#### +0:17:59

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303031300a7368656c6c3e20657869742030303030303030380a7368656c6c3e20657869742030303030303030340a7368656c6c3e20657869742030303030303030320a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> saved
shell> saved
shell> exit 00000010
shell> exit 00000008
shell> exit 00000004
shell> exit 00000002
shell> exit 00000001
shell> saved
shell> assembly error
shell>
```

#### +0:18:02

> 💭 **Filtering new1 with extra1**

**→ `serial_send_text`**

```
as extra1
run
as extra4
```

**← `serial_send_text`**

```
{"sent":24}
```

#### +0:18:10

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361660a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003af
shell> assembly error
shell>
```

#### +0:18:14

> 💭 **Retesting prefix lengths**

**→ `serial_send_text`**

```
as extra1
run 925
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:18:24

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303339640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 0000039d
shell> assembled
shell>
```

#### +0:18:27

> 💭 **Inspecting the filtered tail**

**→ `serial_send_text`**

```
as extra1
run 935
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:18:36

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361370a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003a7
shell> assembled
shell>
```

#### +0:18:40

**→ `serial_send_text`**

```
as extra1
run 940
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:18:45

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361630a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ac
shell> assembled
shell>
```

#### +0:18:48

> 💭 **Checking the final labels**

**→ `serial_send_text`**

```
as extra1
run 941
as extra4
as extra1
run 942
as extra4
```

**← `serial_send_text`**

```
{"sent":56}
```

#### +0:18:58

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361640a7368656c6c3e20617373656d626c65640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ad
shell> assembled
shell> assembled
shell> exit 000003ae
shell> assembly error
shell>
```

#### +0:19:01

> 💭 **Extracting last statements**

**→ `serial_send_text`**

```
save extra5 mov w8,w1;mov w9,16456;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;mov w0,0;
append extra5 el:;mov w14,w9;es:;ldrb w1,[x9];add x9,x9,1;cmp w1,59;b.ne es;add w0,w0,1;
append extra5 cmp w0,w8;b.lt el;mov w12,16459;lsl w12,w12,16;mov w13,5120;add w12,w12,w13;
append extra5 mov w13,w12;ec:;cmp w14,w9;b.ge ed;ldrb w1,[x14];strb w1,[x12];
append extra5 add x14,x14,1;add x12,x12,1;b ec;ed:;sub w1,w12,w13;
append extra5 mov w10,16448;lsl w10,w10,16;add w10,w10,3840;strb w1,[x10,2];mov w1,0;
append extra5 strb w1,[x10,3];ret;
as extra5
run 942
cat extra4
```

**← `serial_send_text`**

```
{"sent":560}
```

#### +0:19:14

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e203b0a7368656c6c3e20
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
shell> assembled
shell> exit 000003ae
shell> ;
shell>
```

#### +0:19:17

> 💭 **Checking semicolon collapse**
> 💭 **Fixing standalone semicolon**

**→ `serial_send_text`**

```
as raw
save extra4 ;;
save extra5 ;
run
run
save extra2 pending
as new1
```

**← `serial_send_text`**

```
{"sent":72}
```

#### +0:19:34

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e20657869742030303030303030300a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> saved
shell> saved
shell> exit 00000001
shell> exit 00000000
shell> saved
shell> assembly error
shell>
```

#### +0:19:37

> 💭 **Filtering full new1**

**→ `serial_send_text`**

```
as extra1
run
as extra4
```

**← `serial_send_text`**

```
{"sent":24}
```

#### +0:19:45

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembled
shell>
```

#### +0:19:49

**→ `serial_send_text`**

```
save extra5 mov w9,16456;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;mov w0,0;
append extra5 mov w10,16448;lsl w10,w10,16;add w10,w10,3072;ldrb w11,[x10,2];ldrb w12,[x10,3];
append extra5 lsl w12,w12,8;orr w11,w11,w12;add w11,w9,w11;
append extra5 cl:;cmp w9,w11;b.ge ce;ldrb w2,[x9];cmp w2,58;b.ne cn;add w0,w0,1;
append extra5 cn:;add x9,x9,1;b cl;ce:;ret;
as extra5
run
```

**← `serial_send_text`**

```
{"sent":369}
```

#### +0:19:56

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303036610a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> assembled
shell> exit 0000006a
shell>
```

#### +0:20:01

> 💭 **Testing assembler label limits**

**→ `serial_send_text`**

```
save extra4 bl expression;expression:;ret;
as extra4
save extra4 adr x9,abcdefghijkl;abcdefghijkl:;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":114}
```

#### +0:20:12

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell> saved
shell> assembled
shell>
```

#### +0:20:15

> 💭 **Checking branch label capacity**
> 💭 **Removing unused routines**
> 💭 **Testing label capacity**

**→ `serial_send_text`**

```
save extra5 mov w8,w1;mov w9,16459;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;mov w10,w9;
append extra5 mov w2,97;mov w3,97;mov w0,0;gen:;cmp w0,w8;b.ge gend;
append extra5 mov w4,76;strb w4,[x9];strb w2,[x9,1];strb w3,[x9,2];mov w4,58;strb w4,[x9,3];
append extra5 mov w4,59;strb w4,[x9,4];add x9,x9,5;add w0,w0,1;add w3,w3,1;
append extra5 cmp w3,123;b.lt gen;mov w3,97;add w2,w2,1;b gen;
append extra5 gend:;mov w4,114;strb w4,[x9];mov w4,101;strb w4,[x9,1];mov w4,116;strb w4,[x9,2];
append extra5 mov w4,59;strb w4,[x9,3];add x9,x9,4;sub w1,w9,w10;
append extra5 mov w10,16448;lsl w10,w10,16;add w10,w10,3840;strb w1,[x10,2];
append extra5 .word 1393064993;strb w1,[x10,3];ret;
as extra5
run 106
as extra4
```

**← `serial_send_text`**

```
{"sent":708}
```

#### +0:20:48

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303036610a7368656c6c3e20617373656d626c65640a7368656c6c3e20
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
shell> assembled
shell> exit 0000006a
shell> assembled
shell>
```

#### +0:20:51

> 💭 **Checking missing branch references**
> 💭 **Building branch-reference diagnostic**

**→ `serial_send_text`**

```
save extra1 mov w8,w1;mov w9,16456;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;
append extra1 mov w10,16448;lsl w10,w10,16;add w10,w10,3072;ldrb w11,[x10,2];ldrb w12,[x10,3];
append extra1 lsl w12,w12,8;orr w11,w11,w12;add w11,w9,w11;mov w12,16459;lsl w12,w12,16;
append extra1 mov w13,5120;add w12,w12,w13;mov w13,w12;mov w0,0;
append extra1 dl:;cmp w9,w11;b.ge dout;mov w14,w9;mov w15,0;ldrb w1,[x9];cmp w1,98;b.eq dskip;
append extra1 cmp w1,97;b.ne dscan;ldrb w1,[x9,1];cmp w1,100;b.eq dskip;b dscan;
append extra1 dskip:;mov w15,1;dscan:;ldrb w1,[x9];add x9,x9,1;cmp w1,58;b.ne dnocol;
append extra1 mov w15,0;dnocol:;cmp w1,59;b.ne dscan;add w0,w0,1;cmp w15,0;b.eq dc;
append extra1 cmp w8,w0;b.ge dc;mov w1,114;strb w1,[x12];mov w1,101;strb w1,[x12,1];
append extra1 mov w1,116;strb w1,[x12,2];mov w1,59;strb w1,[x12,3];add x12,x12,4;b dl;
append extra1 dc:;cmp w14,w9;b.ge dl;ldrb w1,[x14];strb w1,[x12];add x14,x14,1;add x12,x12,1;b dc;
append extra1 dout:;sub w1,w12,w13;strb w1,[x10,770];.word 1393064993;strb w1,[x10,771];ret;
as extra1
run 0
as extra4
```

**← `serial_send_text`**

```
{"sent":1061}
```

#### +0:21:09

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c65640a7368656c6c3e20
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
shell> assembled
shell> exit 000003ae
shell> assembled
shell>
```

#### +0:21:13

> 💭 **Bisecting unknown reference**

**→ `serial_send_text`**

```
as extra1
run 475
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:21:19

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembly error
shell>
```

#### +0:21:22

**→ `serial_send_text`**

```
as extra1
run 235
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:21:26

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembly error
shell>
```

#### +0:21:29

**→ `serial_send_text`**

```
as extra1
run 117
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:21:32

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembled
shell>
```

#### +0:21:36

**→ `serial_send_text`**

```
as extra1
run 176
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:21:40

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembled
shell>
```

#### +0:21:45

**→ `serial_send_text`**

```
as extra1
run 205
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:21:49

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembled
shell>
```

#### +0:21:52

**→ `serial_send_text`**

```
as extra1
run 220
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:21:55

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembly error
shell>
```

#### +0:21:58

**→ `serial_send_text`**

```
as extra1
run 212
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:22:02

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembly error
shell>
```

#### +0:22:06

**→ `serial_send_text`**

```
as extra1
run 208
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:22:11

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembly error
shell>
```

#### +0:22:14

**→ `serial_send_text`**

```
as extra1
run 206
as extra4
```

**← `serial_send_text`**

```
{"sent":28}
```

#### +0:22:17

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20657869742030303030303361650a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> exit 000003ae
shell> assembled
shell>
```

#### +0:22:20

> 💭 **Extracting statement 208**

**→ `serial_send_text`**

```
save extra5 mov w8,w1;mov w9,16456;lsl w9,w9,16;mov w10,5120;add w9,w9,w10;mov w0,0;
append extra5 el:;mov w14,w9;es:;ldrb w1,[x9];add x9,x9,1;cmp w1,59;b.ne es;add w0,w0,1;
append extra5 cmp w0,w8;b.lt el;mov w12,16459;lsl w12,w12,16;mov w13,5120;add w12,w12,w13;
append extra5 mov w13,w12;ec:;cmp w14,w9;b.ge ed;ldrb w1,[x14];strb w1,[x12];
append extra5 add x14,x14,1;add x12,x12,1;b ec;ed:;sub w1,w12,w13;
append extra5 mov w10,16448;lsl w10,w10,16;add w10,w10,3840;strb w1,[x10,2];mov w1,0;
append extra5 strb w1,[x10,3];ret;
as extra5
run 207
cat extra4
run 208
cat extra4
```

**← `serial_send_text`**

```
{"sent":579}
```

#### +0:22:31

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20657869742030303030303063660a7368656c6c3e206164722078392c6c6f63616c733b0a7368656c6c3e20657869742030303030303064300a7368656c6c3e20636d702077302c303b0a7368656c6c3e20
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
shell> assembled
shell> exit 000000cf
shell> adr x9,locals;
shell> exit 000000d0
shell> cmp w0,0;
shell>
```

#### +0:22:35

**→ `serial_send_text`**

```
append new1 ret;
as new1
```

**← `serial_send_text`**

```
{"sent":25}
```

#### +0:22:45

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell>
```

#### +0:22:48

> 💭 **Appending data for assembly**

**→ `serial_send_text`**

```
install
save extra4 int f(int x){return x+7;}
build extra4
run 2
```

**← `serial_send_text`**

```
{"sent":65}
```

#### +0:23:02

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030300a7368656c6c3e20
```

`text`

```
installed
shell> saved
shell> build error
shell> exit 00000000
shell>
```

#### +0:23:06

> 💭 **Exposing parser error location**
> 💭 **Patching parser offset output**

**→ `serial_send_text`**

```
as raw
save extra4 mov x19,x1;
save extra5 mov x28,x1;mov x19,x1;
run
save extra4 fail:;mov w0,0;
save extra5 fail:;sub w0,w19,w28;lsl w0,w0,5;mov w1,21120;lsl w1,w1,16;orr w0,w0,w1;
run
save extra4 finish:;
save extra5 str w0,[x22];adr x9,templates;ldr w0,[x9,28];str w0,[x22,4];mov w0,8;finish:;
run
save extra4 int f(int x){return x+7;}
as new1
install
build extra4
run 2
```

**← `serial_send_text`**

```
{"sent":375}
```

#### +0:23:33

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030300a7368656c6c3e20
```

`text`

```
assembled
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> assembly error
shell> installed
shell> build error
shell> exit 00000000
shell>
```

#### +0:23:38

> 💭 **Tracing assembly error**
> 💭 **Reading new1 error**

**→ `serial_send_text`**

```
cat new1
```

**← `serial_send_text`**

```
{"sent":9}
```

#### +0:23:57

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

<details><summary>result (12,308 chars, 1 lines)</summary>

```
{"hex":"7375622073702c73702c39363b737472207831392c5b73705d3b737472207832302c5b73702c385d3b737472207832312c5b73702c31365d3b737472207832322c5b73702c32345d3b737472207832332c5b73702c33325d3b737472207832342c5b73702c34305d3b737472207832352c5b73702c34385d3b737472207832362c5b73702c35365d3b737472207832372c5b73702c36345d3b737472207832382c5b73702c37325d3b737472207833302c5b73702c38305d3b6d6f76207832382c78313b6d6f76207831392c78313b616464207732302c77312c77323b6d6f76207832312c78333b6d6f76207832322c78333b616464207732332c77332c77343b6d6f76207732342c303b6d6f76207732352c303b6d6f762077302c303b626c20656d69743b626c206e6578743b746f703a3b626c20746f6b3b636d702077302c303b622e657120646f6e653b636d70207732342c303b622e6e6520646f6e653b626c2066756e6374696f6e3b6220746f703b646f6e653a3b636d70207732352c303b622e6571206661696c3b636d70207732342c303b622e6e65206661696c3b7375622077302c7732372c7732323b2e776f726420313339323637313734343b6d6f762077312c353132303b6c736c2077312c77312c31363b6f72722077302c77302c77313b7374722077302c5b7832325d3b7375622077302c7732312c7732323b622066696e6973683b6661696c3a3b7375622077302c7731392c7732383b6c736c2077302c77302c353b6d6f762077312c32313132303b6c736c2077312c77312c31363b6f72722077302c77302c77313b7374722077302c5b7832325d3b6164722078392c74656d706c617465733b6c64722077302c5b78392c32385d3b7374722077302c5b7832322c345d3b6d6f762077302c383b66696e6973683a3b6c6472207831392c5b73705d3b6c6472207832302c5b73702c385d3b6c6472207832312c5b73702c31365d3b6c6472207832322c5b73702c32345d3b6c6472207832332c5b73702c33325d3b6c6472207832342c5b73702c34305d3b6c6472207832352c5b73702c34385d3b6c6472207832362c5b73702c35365d3b6c6472207832372c5b73702c36345d3b6c6472207832382c5b73702c37325d3b6c6472207833302c5b73702c38305d3b6164642073702c73702c39363b7265743b656d69743a3b6164642077392c7732312c343b636d702077392c7732333b622e6765206f766572666c6f773b7374722077302c5b7832315d3b6d6f76207832312c78393b7265743b6f766572666c6f773a3b6d6f76207732342c313b7265743b74706c3a3b6164722078392c74656d706c617465733b6164642077392c77392c77303b6c64722077302c5b78395d3b6220656d69743b746f6b3a3b6164722078392c746f6b656e3b6c64722077302c5b78395d3b7265743b76616c75653a3b6164722078392c746f6b656e3b6c64722077302c5b78392c345d3b7265743b6578706563743a3b7375622073702c73702c31363b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c20746f6b3b6c64722077312c5b73702c385d3b636d702077302c77313b622e65712065786f6b3b6d6f76207732342c313b65786f6b3a3b626c206e6578743b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b6e6578743a3b6d6f762077302c303b6d6f762077312c303b6d6f762078322c7831393b6d6f762077332c303b736b69703a3b636d70207731392c7732303b622e6765206e7473746f72653b6c6472622077302c5b7831395d3b636d702077302c33323b622e6765206c65783b616464207731392c7731392c313b6220736b69703b6c65783a3b6d6f762078322c7831393b636d702077302c34383b622e6c74206964656e743b636d702077302c35373b622e6765206964656e743b6d6f762077312c303b6469676974733a3b7375622077302c77302c34383b6d6f762077392c31303b6d756c2077312c77312c77393b6164642077312c77312c77303b616464207731392c7731392c313b636d70207731392c7732303b622e6765206e756d656e643b6c6472622077302c5b7831395d3b636d702077302c34383b622e6c74206e756d656e643b636d702077302c35383b622e6c74206469676974733b6e756d656e643a3b6d6f762077302c3235363b62206e7473746f72653b6964656e743a3b636d702077302c39353b622e657120696473746172743b6d6f762077392c33323b6f72722077392c77302c77393b636d702077392c39373b622e6c742070756e63743b636d702077392c3132323b622e67652070756e63743b696473746172743a3b6d6f762077332c303b69646c6f6f703a3b616464207731392c7731392c313b6164642077332c77332c313b636d702077332c33313b622e6765206c65786572723b636d70207731392c7732303b622e6765206964656e643b6c6472622077392c5b7831395d3b636d702077392c39353b622e65712069646c6f6f703b636d702077392c34383b622e6c74206964616c7068613b636d702077392c35383b622e6c742069646c6f6f703b6964616c7068613a3b6d6f76207731362c33323b6f72722077392c77392c7731363b636d702077392c39373b622e6c74206964656e643b636d702077392c3132333b622e6c742069646c6f6f703b6964656e643a3b6d6f762077302c3235373b616472207831302c6b6579776f7264733b6d6f76207731312c3235383b6b776c6f6f703a3b6c647262207731322c5b7831305d3b636d70207731322c303b622e6571206e7473746f72653b636d70207731322c77333b622e6e65206b776e6578743b6d6f76207731332c303b6b77636d703a3b616464207731342c7731302c7731333b6c647262207731352c5b7831342c315d3b616464207731342c77322c7731333b6c647262207731342c5b7831345d3b636d70207731342c7731353b622e6e65206b776e6578743b616464207731332c7731332c313b636d70207731332c77333b622e6c74206b77636d703b6d6f762077302c7731313b62206e7473746f72653b6b776e6578743a3b616464207731302c7731302c7731323b616464207731302c7731302c313b616464207731312c7731312c313b62206b776c6f6f703b70756e63743a3b616464207731392c7731392c313b62206e7473746f72653b6c65786572723a3b6d6f76207732342c313b6d6f762077302c303b6e7473746f72653a3b6164722078392c746f6b656e3b7374722077302c5b78395d3b7374722077312c5b78392c345d3b7374722078322c5b78392c385d3b7374722077332c5b78392c31365d3b7265743b66696e643a3b6164722078392c6c6f63616c733b636d702077302c303b622e657120666c6f63616c3b6164722078392c6c6f63616c733b6164642078392c78392c313032343b6d6f762077382c7732353b622066626567696e3b666c6f63616c3a3b6d6f762077382c7732363b66626567696e3a3b616472207831302c746f6b656e3b6c6472207831312c5b7831302c385d3b6c6472207731322c5b7831302c31365d3b6d6f762077302c303b666c6f6f703a3b636d702077302c77383b622e676520666d6973733b6c6472207731332c5b78392c385d3b636d70207731332c7731323b622e6e652066737465703b6c6472207831332c5b78395d3b6d6f76207731342c303b66636d703a3b616464207731352c7731312c7731343b6c647262207731352c5b7831355d3b616464207731362c7731332c7731343b6c647262207731362c5b7831365d3b636d70207731352c7731363b622e6e652066737465703b616464207731342c7731342c313b636d70207731342c7731323b622e6c742066636d703b7265743b66737465703a3b6164642077392c77392c33323b6164642077302c77302c313b6220666c6f6f703b666d6973733a3b6d6f762077302c303b7375622077302c77302c313b7265743b6164646c6f63616c3a3b7375622073702c73702c33323b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c20746f6b3b636d702077302c3235373b622e6e6520616c6261643b6d6f762077302c303b626c2066696e643b636d702077302c303b622e676520616c6261643b636d70207732362c33323b622e676520616c6261643b6164722078392c6c6f63616c733b6c736c207731302c7732362c353b6164642077392c77392c7731303b616472207831302c746f6b656e3b6c6472207831312c5b7831302c385d3b737472207831312c5b78395d3b6c6472207731312c5b7831302c31365d3b737472207731312c5b78392c385d3b6c6472207731312c5b73702c385d3b737472207731312c5b78392c31325d3b737472207732362c5b73702c31325d3b616464207732362c7732362c313b626c206e6578743b6c64722077302c5b73702c31325d3b6220616c656e643b616c6261643a3b6d6f76207732342c313b6d6f762077302c303b616c656e643a3b6c6472207833302c5b73705d3b6164642073702c73702c33323b7265743b747970653a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20746f6b3b636d702077302c3235383b622e6571207479696e743b636d702077302c3235393b622e6e652074796261643b6d6f762077302c313b7374722077302c5b73702c385d3b626c206e6578743b6d6f762077302c34323b626c206578706563743b622074796f75743b7479696e743a3b6d6f762077302c303b7374722077302c5b73702c385d3b626c206e6578743b626c20746f6b3b636d702077302c34323b622e6e652074796f75743b626c206e6578743b6d6f762077302c323b7374722077302c5b73702c385d3b622074796f75743b74796261643a3b6d6f76207732342c313b74796f75743a3b6c64722077302c5b73702c385d3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b66756e6374696f6e3a3b7375622073702c73702c33323b737472207833302c5b73705d3b6d6f76207732362c303b6d6f762077302c3235383b626c206578706563743b626c20746f6b3b636d702077302c3235373b622e6e6520666e6572726f723b6d6f762077302c313b626c2066696e643b636d702077302c303b622e676520666e6572726f723b636d70207732352c31363b622e676520666e6572726f723b6164722078392c6c6f63616c733b6164642078392c78392c313032343b6c736c207731302c7732352c353b6164642077392c77392c7731303b616472207831302c746f6b656e3b6c6472207831312c5b7831302c385d3b737472207831312c5b78395d3b6c6472207731312c5b7831302c31365d3b737472207731312c5b78392c385d3b737472207832312c5b78392c31365d3b6d6f76207832372c7832313b7374722078392c5b73702c385d3b616464207732352c7732352c313b626c206e6578743b6d6f762077302c34303b626c206578706563743b6d6f762077302c303b626c2074706c3b6d6f762077302c343b626c2074706c3b6d6f762077302c383b626c2074706c3b6d6f762077302c31323b626c2074706c3b706172616d733a3b626c20746f6b3b636d702077302c34313b622e657120","text":"sub sp,sp,96;str x19,[sp];str x20,[sp,8];str x21,[sp,16];str x22,[sp,24];str x23,[sp,32];str x24,[sp,40];str x25,[sp,48];str x26,[sp,56];str x27,[sp,64];str x28,[sp,72];str x30,[sp,80];mov x28,x1;mov x19,x1;add w20,w1,w2;mov x21,x3;mov x22,x3;add w23,w3,w4;mov w24,0;mov w25,0;mov w0,0;bl emit;bl next;top:;bl tok;cmp w0,0;b.eq done;cmp w24,0;b.ne done;bl function;b top;done:;cmp w25,0;b.eq fail;cmp w24,0;b.ne fail;sub w0,w27,w22;.word 1392671744;mov w1,5120;lsl w1,w1,16;orr w0,w0,w1;str w0,[x22];sub w0,w21,w22;b finish;fail:;sub w0,w19,w28;lsl w0,w0,5;mov w1,21120;lsl w1,w1,16;orr w0,w0,w1;str w0,[x22];adr x9,templates;ldr w0,[x9,28];str w0,[x22,4];mov w0,8;finish:;ldr x19,[sp];ldr x20,[sp,8];ldr x21,[sp,16];ldr x22,[sp,24];ldr x23,[sp,32];ldr x24,[sp,40];ldr x25,[sp,48];ldr x26,[sp,56];ldr x27,[sp,64];ldr x28,[sp,72];ldr x30,[sp,80];add sp,sp,96;ret;emit:;add w9,w21,4;cmp w9,w23;b.ge overflow;str w0,[x21];mov x21,x9;ret;overflow:;mov w24,1;ret;tpl:;adr x9,templates;add w9,w9,w0;ldr w0,[x9];b emit;tok:;adr x9,token;ldr w0,[x9];ret;value:;adr x9,token;ldr w0,[x9,4];ret;expect:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl tok;ldr w1,[sp,8];cmp w0,w1;b.eq exok;mov w24,1;exok:;bl next;ldr x30,[sp];add sp,sp,16;ret;next:;mov w0,0;mov w1,0;mov x2,x19;mov w3,0;skip:;cmp w19,w20;b.ge ntstore;ldrb w0,[x19];cmp w0,32;b.ge lex;add w19,w19,1;b skip;lex:;mov x2,x19;cmp w0,48;b.lt ident;cmp w0,57;b.ge ident;mov w1,0;digits:;sub w0,w0,48;mov w9,10;mul w1,w1,w9;add w1,w1,w0;add w19,w19,1;cmp w19,w20;b.ge numend;ldrb w0,[x19];cmp w0,48;b.lt numend;cmp w0,58;b.lt digits;numend:;mov w0,256;b ntstore;ident:;cmp w0,95;b.eq idstart;mov w9,32;orr w9,w0,w9;cmp w9,97;b.lt punct;cmp w9,122;b.ge punct;idstart:;mov w3,0;idloop:;add w19,w19,1;add w3,w3,1;cmp w3,31;b.ge lexerr;cmp w19,w20;b.ge idend;ldrb w9,[x19];cmp w9,95;b.eq idloop;cmp w9,48;b.lt idalpha;cmp w9,58;b.lt idloop;idalpha:;mov w16,32;orr w9,w9,w16;cmp w9,97;b.lt idend;cmp w9,123;b.lt idloop;idend:;mov w0,257;adr x10,keywords;mov w11,258;kwloop:;ldrb w12,[x10];cmp w12,0;b.eq ntstore;cmp w12,w3;b.ne kwnext;mov w13,0;kwcmp:;add w14,w10,w13;ldrb w15,[x14,1];add w14,w2,w13;ldrb w14,[x14];cmp w14,w15;b.ne kwnext;add w13,w13,1;cmp w13,w3;b.lt kwcmp;mov w0,w11;b ntstore;kwnext:;add w10,w10,w12;add w10,w10,1;add w11,w11,1;b kwloop;punct:;add w19,w19,1;b ntstore;lexerr:;mov w24,1;mov w0,0;ntstore:;adr x9,token;str w0,[x9];str w1,[x9,4];str x2,[x9,8];str w3,[x9,16];ret;find:;adr x9,locals;cmp w0,0;b.eq flocal;adr x9,locals;add x9,x9,1024;mov w8,w25;b fbegin;flocal:;mov w8,w26;fbegin:;adr x10,token;ldr x11,[x10,8];ldr w12,[x10,16];mov w0,0;floop:;cmp w0,w8;b.ge fmiss;ldr w13,[x9,8];cmp w13,w12;b.ne fstep;ldr x13,[x9];mov w14,0;fcmp:;add w15,w11,w14;ldrb w15,[x15];add w16,w13,w14;ldrb w16,[x16];cmp w15,w16;b.ne fstep;add w14,w14,1;cmp w14,w12;b.lt fcmp;ret;fstep:;add w9,w9,32;add w0,w0,1;b floop;fmiss:;mov w0,0;sub w0,w0,1;ret;addlocal:;sub sp,sp,32;str x30,[sp];str w0,[sp,8];bl tok;cmp w0,257;b.ne albad;mov w0,0;bl find;cmp w0,0;b.ge albad;cmp w26,32;b.ge albad;adr x9,locals;lsl w10,w26,5;add w9,w9,w10;adr x10,token;ldr x11,[x10,8];str x11,[x9];ldr w11,[x10,16];str w11,[x9,8];ldr w11,[sp,8];str w11,[x9,12];str w26,[sp,12];add w26,w26,1;bl next;ldr w0,[sp,12];b alend;albad:;mov w24,1;mov w0,0;alend:;ldr x30,[sp];add sp,sp,32;ret;type:;sub sp,sp,16;str x30,[sp];bl tok;cmp w0,258;b.eq tyint;cmp w0,259;b.ne tybad;mov w0,1;str w0,[sp,8];bl next;mov w0,42;bl expect;b tyout;tyint:;mov w0,0;str w0,[sp,8];bl next;bl tok;cmp w0,42;b.ne tyout;bl next;mov w0,2;str w0,[sp,8];b tyout;tybad:;mov w24,1;tyout:;ldr w0,[sp,8];ldr x30,[sp];add sp,sp,16;ret;function:;sub sp,sp,32;str x30,[sp];mov w26,0;mov w0,258;bl expect;bl tok;cmp w0,257;b.ne fnerror;mov w0,1;bl find;cmp w0,0;b.ge fnerror;cmp w25,16;b.ge fnerror;adr x9,locals;add x9,x9,1024;lsl w10,w25,5;add w9,w9,w10;adr x10,token;ldr x11,[x10,8];str x11,[x9];ldr w11,[x10,16];str w11,[x9,8];str x21,[x9,16];mov x27,x21;str x9,[sp,8];add w25,w25,1;bl next;mov w0,40;bl expect;mov w0,0;bl tpl;mov w0,4;bl tpl;mov w0,8;bl tpl;mov w0,12;bl tpl;params:;bl tok;cmp w0,41;b.eq "}
```

</details>

#### +0:24:01

## Observer message 1 +0:25:36

> The stage is still incomplete. Continue working. Unmet acceptance condition: The guest-built seed must compile the C-written compiler, which must then build and run independent C inputs.
> Observed result: The session ended with Error: terminated. Before it ended, as new1 succeeded once and install succeeded, but build extra4 rejected int f(int x){return x+7;}. The subsequent edited candidate reported assembly error. The existing campaign disk and logs are preserved.

#### +0:25:36

**→ `serial_read`** `{"wait_ms": 0}`

**← `serial_read`** ⚠️ error

```
Boot a VM first
```

#### +0:25:40

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T095822.375217Z"}
```

#### +0:25:46

> 💭 **Diagnosing the assembly error**

**→ `serial_send_text`**

```
as new1
cat new1
```

**← `serial_send_text`**

```
{"sent":17}
```

#### +0:26:04

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

<details><summary>hex (8,192 chars, 1 lines)</summary>

```
424f4f540a7368656c6c3e20617373656d626c65640a7368656c6c3e207375622073702c73702c39363b737472207831392c5b73705d3b737472207832302c5b73702c385d3b737472207832312c5b73702c31365d3b737472207832322c5b73702c32345d3b737472207832332c5b73702c33325d3b737472207832342c5b73702c34305d3b737472207832352c5b73702c34385d3b737472207832362c5b73702c35365d3b737472207832372c5b73702c36345d3b737472207832382c5b73702c37325d3b737472207833302c5b73702c38305d3b6d6f76207832382c78313b6d6f76207831392c78313b616464207732302c77312c77323b6d6f76207832312c78333b6d6f76207832322c78333b616464207732332c77332c77343b6d6f76207732342c303b6d6f76207732352c303b6d6f762077302c303b626c20656d69743b626c206e6578743b746f703a3b626c20746f6b3b636d702077302c303b622e657120646f6e653b636d70207732342c303b622e6e6520646f6e653b626c2066756e6374696f6e3b6220746f703b646f6e653a3b636d70207732352c303b622e6571206661696c3b636d70207732342c303b622e6e65206661696c3b7375622077302c7732372c7732323b2e776f726420313339323637313734343b6d6f762077312c353132303b6c736c2077312c77312c31363b6f72722077302c77302c77313b7374722077302c5b7832325d3b7375622077302c7732312c7732323b622066696e6973683b6661696c3a3b7375622077302c7731392c7732383b6c736c2077302c77302c353b6d6f762077312c32313132303b6c736c2077312c77312c31363b6f72722077302c77302c77313b7374722077302c5b7832325d3b6164722078392c74656d706c617465733b6c64722077302c5b78392c32385d3b7374722077302c5b7832322c345d3b6d6f762077302c383b66696e6973683a3b6c6472207831392c5b73705d3b6c6472207832302c5b73702c385d3b6c6472207832312c5b73702c31365d3b6c6472207832322c5b73702c32345d3b6c6472207832332c5b73702c33325d3b6c6472207832342c5b73702c34305d3b6c6472207832352c5b73702c34385d3b6c6472207832362c5b73702c35365d3b6c6472207832372c5b73702c36345d3b6c6472207832382c5b73702c37325d3b6c6472207833302c5b73702c38305d3b6164642073702c73702c39363b7265743b656d69743a3b6164642077392c7732312c343b636d702077392c7732333b622e6765206f766572666c6f773b7374722077302c5b7832315d3b6d6f76207832312c78393b7265743b6f766572666c6f773a3b6d6f76207732342c313b7265743b74706c3a3b6164722078392c74656d706c617465733b6164642077392c77392c77303b6c64722077302c5b78395d3b6220656d69743b746f6b3a3b6164722078392c746f6b656e3b6c64722077302c5b78395d3b7265743b76616c75653a3b6164722078392c746f6b656e3b6c64722077302c5b78392c345d3b7265743b6578706563743a3b7375622073702c73702c31363b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c20746f6b3b6c64722077312c5b73702c385d3b636d702077302c77313b622e65712065786f6b3b6d6f76207732342c313b65786f6b3a3b626c206e6578743b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b6e6578743a3b6d6f762077302c303b6d6f762077312c303b6d6f762078322c7831393b6d6f762077332c303b736b69703a3b636d70207731392c7732303b622e6765206e7473746f72653b6c6472622077302c5b7831395d3b636d702077302c33323b622e6765206c65783b616464207731392c7731392c313b6220736b69703b6c65783a3b6d6f762078322c7831393b636d702077302c34383b622e6c74206964656e743b636d702077302c35373b622e6765206964656e743b6d6f762077312c303b6469676974733a3b7375622077302c77302c34383b6d6f762077392c31303b6d756c2077312c77312c77393b6164642077312c77312c77303b616464207731392c7731392c313b636d70207731392c7732303b622e6765206e756d656e643b6c6472622077302c5b7831395d3b636d702077302c34383b622e6c74206e756d656e643b636d702077302c35383b622e6c74206469676974733b6e756d656e643a3b6d6f762077302c3235363b62206e7473746f72653b6964656e743a3b636d702077302c39353b622e657120696473746172743b6d6f762077392c33323b6f72722077392c77302c77393b636d702077392c39373b622e6c742070756e63743b636d702077392c3132323b622e67652070756e63743b696473746172743a3b6d6f762077332c303b69646c6f6f703a3b616464207731392c7731392c313b6164642077332c77332c313b636d702077332c33313b622e6765206c65786572723b636d70207731392c7732303b622e6765206964656e643b6c6472622077392c5b7831395d3b636d702077392c39353b622e65712069646c6f6f703b636d702077392c34383b622e6c74206964616c7068613b636d702077392c35383b622e6c742069646c6f6f703b6964616c7068613a3b6d6f76207731362c33323b6f72722077392c77392c7731363b636d702077392c39373b622e6c74206964656e643b636d702077392c3132333b622e6c742069646c6f6f703b6964656e643a3b6d6f762077302c3235373b616472207831302c6b6579776f7264733b6d6f76207731312c3235383b6b776c6f6f703a3b6c647262207731322c5b7831305d3b636d70207731322c303b622e6571206e7473746f72653b636d70207731322c77333b622e6e65206b776e6578743b6d6f76207731332c303b6b77636d703a3b616464207731342c7731302c7731333b6c647262207731352c5b7831342c315d3b616464207731342c77322c7731333b6c647262207731342c5b7831345d3b636d70207731342c7731353b622e6e65206b776e6578743b616464207731332c7731332c313b636d70207731332c77333b622e6c74206b77636d703b6d6f762077302c7731313b62206e7473746f72653b6b776e6578743a3b616464207731302c7731302c7731323b616464207731302c7731302c313b616464207731312c7731312c313b62206b776c6f6f703b70756e63743a3b616464207731392c7731392c313b62206e7473746f72653b6c65786572723a3b6d6f76207732342c313b6d6f762077302c303b6e7473746f72653a3b6164722078392c746f6b656e3b7374722077302c5b78395d3b7374722077312c5b78392c345d3b7374722078322c5b78392c385d3b7374722077332c5b78392c31365d3b7265743b66696e643a3b6164722078392c6c6f63616c733b636d702077302c303b622e657120666c6f63616c3b6164722078392c6c6f63616c733b6164642078392c78392c313032343b6d6f762077382c7732353b622066626567696e3b666c6f63616c3a3b6d6f762077382c7732363b66626567696e3a3b616472207831302c746f6b656e3b6c6472207831312c5b7831302c385d3b6c6472207731322c5b7831302c31365d3b6d6f762077302c303b666c6f6f703a3b636d702077302c77383b622e676520666d6973733b6c6472207731332c5b78392c385d3b636d70207731332c7731323b622e6e652066737465703b6c6472207831332c5b78395d3b6d6f76207731342c303b66636d703a3b616464207731352c7731312c7731343b6c647262207731352c5b7831355d3b616464207731362c7731332c7731343b6c647262207731362c5b7831365d3b636d70207731352c7731363b622e6e652066737465703b616464207731342c7731342c313b636d70207731342c7731323b622e6c742066636d703b7265743b66737465703a3b6164642077392c77392c33323b6164642077302c77302c313b6220666c6f6f703b666d6973733a3b6d6f762077302c303b7375622077302c77302c313b7265743b6164646c6f63616c3a3b7375622073702c73702c33323b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c20746f6b3b636d702077302c3235373b622e6e6520616c6261643b6d6f762077302c303b626c2066696e643b636d702077302c303b622e676520616c6261643b636d70207732362c33323b622e676520616c6261643b6164722078392c6c6f63616c733b6c736c207731302c7732362c353b6164642077392c77392c7731303b616472207831302c746f6b656e3b6c6472207831312c5b7831302c385d3b737472207831312c5b78395d3b6c6472207731312c5b7831302c31365d3b737472207731312c5b78392c385d3b6c6472207731312c5b73702c385d3b737472207731312c5b78392c31325d3b737472207732362c5b73702c31325d3b616464207732362c7732362c313b626c206e6578743b6c64722077302c5b73702c31325d3b6220616c656e643b616c6261643a3b6d6f76207732342c313b6d6f762077302c303b616c656e643a3b6c6472207833302c5b73705d3b6164642073702c73702c33323b7265743b747970653a3b7375622073702c73702c31363b737472207833302c5b73705d3b626c20746f6b3b636d702077302c3235383b622e6571207479696e743b636d702077302c3235393b622e6e652074796261643b6d6f762077302c313b7374722077302c5b73702c385d3b626c206e6578743b6d6f762077302c34323b626c206578706563743b622074796f75743b7479696e743a3b6d6f762077302c303b7374722077302c5b73702c385d3b626c206e6578743b626c20746f6b3b636d702077302c34323b622e6e652074796f75743b626c206e6578743b6d6f762077302c323b7374722077302c5b73702c385d3b622074796f75743b74796261643a3b6d6f76207732342c313b74796f75743a3b6c64722077302c5b73702c385d3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b66756e6374696f6e3a3b7375622073702c73702c33323b737472207833302c5b73705d3b6d6f76207732362c303b6d6f762077302c3235383b626c206578706563743b626c20746f6b3b636d702077302c3235373b622e6e6520666e6572726f723b6d6f762077302c313b626c2066696e643b636d702077302c303b622e676520666e6572726f723b636d70207732352c31363b622e676520666e6572726f723b6164722078392c6c6f63616c733b6164642078392c78392c313032343b6c736c207731302c7732352c353b6164642077392c77392c7731303b616472207831302c746f6b656e3b6c6472207831312c5b7831302c385d3b737472207831312c5b78395d3b6c6472207731312c5b7831302c31365d3b737472207731312c5b78392c385d3b737472207832312c5b78392c31365d3b6d6f76207832372c7832313b7374722078392c5b73702c385d3b616464207732352c7732352c313b626c206e6578743b6d6f762077302c34303b626c206578706563743b6d6f762077302c303b626c2074706c3b6d6f762077302c343b626c2074706c3b6d6f762077302c383b626c2074706c3b6d6f762077302c31323b626c2074706c3b70
```

</details>

`text`

<details><summary>text (4,096 chars, 3 lines)</summary>

```
BOOT
shell> assembled
shell> sub sp,sp,96;str x19,[sp];str x20,[sp,8];str x21,[sp,16];str x22,[sp,24];str x23,[sp,32];str x24,[sp,40];str x25,[sp,48];str x26,[sp,56];str x27,[sp,64];str x28,[sp,72];str x30,[sp,80];mov x28,x1;mov x19,x1;add w20,w1,w2;mov x21,x3;mov x22,x3;add w23,w3,w4;mov w24,0;mov w25,0;mov w0,0;bl emit;bl next;top:;bl tok;cmp w0,0;b.eq done;cmp w24,0;b.ne done;bl function;b top;done:;cmp w25,0;b.eq fail;cmp w24,0;b.ne fail;sub w0,w27,w22;.word 1392671744;mov w1,5120;lsl w1,w1,16;orr w0,w0,w1;str w0,[x22];sub w0,w21,w22;b finish;fail:;sub w0,w19,w28;lsl w0,w0,5;mov w1,21120;lsl w1,w1,16;orr w0,w0,w1;str w0,[x22];adr x9,templates;ldr w0,[x9,28];str w0,[x22,4];mov w0,8;finish:;ldr x19,[sp];ldr x20,[sp,8];ldr x21,[sp,16];ldr x22,[sp,24];ldr x23,[sp,32];ldr x24,[sp,40];ldr x25,[sp,48];ldr x26,[sp,56];ldr x27,[sp,64];ldr x28,[sp,72];ldr x30,[sp,80];add sp,sp,96;ret;emit:;add w9,w21,4;cmp w9,w23;b.ge overflow;str w0,[x21];mov x21,x9;ret;overflow:;mov w24,1;ret;tpl:;adr x9,templates;add w9,w9,w0;ldr w0,[x9];b emit;tok:;adr x9,token;ldr w0,[x9];ret;value:;adr x9,token;ldr w0,[x9,4];ret;expect:;sub sp,sp,16;str x30,[sp];str w0,[sp,8];bl tok;ldr w1,[sp,8];cmp w0,w1;b.eq exok;mov w24,1;exok:;bl next;ldr x30,[sp];add sp,sp,16;ret;next:;mov w0,0;mov w1,0;mov x2,x19;mov w3,0;skip:;cmp w19,w20;b.ge ntstore;ldrb w0,[x19];cmp w0,32;b.ge lex;add w19,w19,1;b skip;lex:;mov x2,x19;cmp w0,48;b.lt ident;cmp w0,57;b.ge ident;mov w1,0;digits:;sub w0,w0,48;mov w9,10;mul w1,w1,w9;add w1,w1,w0;add w19,w19,1;cmp w19,w20;b.ge numend;ldrb w0,[x19];cmp w0,48;b.lt numend;cmp w0,58;b.lt digits;numend:;mov w0,256;b ntstore;ident:;cmp w0,95;b.eq idstart;mov w9,32;orr w9,w0,w9;cmp w9,97;b.lt punct;cmp w9,122;b.ge punct;idstart:;mov w3,0;idloop:;add w19,w19,1;add w3,w3,1;cmp w3,31;b.ge lexerr;cmp w19,w20;b.ge idend;ldrb w9,[x19];cmp w9,95;b.eq idloop;cmp w9,48;b.lt idalpha;cmp w9,58;b.lt idloop;idalpha:;mov w16,32;orr w9,w9,w16;cmp w9,97;b.lt idend;cmp w9,123;b.lt idloop;idend:;mov w0,257;adr x10,keywords;mov w11,258;kwloop:;ldrb w12,[x10];cmp w12,0;b.eq ntstore;cmp w12,w3;b.ne kwnext;mov w13,0;kwcmp:;add w14,w10,w13;ldrb w15,[x14,1];add w14,w2,w13;ldrb w14,[x14];cmp w14,w15;b.ne kwnext;add w13,w13,1;cmp w13,w3;b.lt kwcmp;mov w0,w11;b ntstore;kwnext:;add w10,w10,w12;add w10,w10,1;add w11,w11,1;b kwloop;punct:;add w19,w19,1;b ntstore;lexerr:;mov w24,1;mov w0,0;ntstore:;adr x9,token;str w0,[x9];str w1,[x9,4];str x2,[x9,8];str w3,[x9,16];ret;find:;adr x9,locals;cmp w0,0;b.eq flocal;adr x9,locals;add x9,x9,1024;mov w8,w25;b fbegin;flocal:;mov w8,w26;fbegin:;adr x10,token;ldr x11,[x10,8];ldr w12,[x10,16];mov w0,0;floop:;cmp w0,w8;b.ge fmiss;ldr w13,[x9,8];cmp w13,w12;b.ne fstep;ldr x13,[x9];mov w14,0;fcmp:;add w15,w11,w14;ldrb w15,[x15];add w16,w13,w14;ldrb w16,[x16];cmp w15,w16;b.ne fstep;add w14,w14,1;cmp w14,w12;b.lt fcmp;ret;fstep:;add w9,w9,32;add w0,w0,1;b floop;fmiss:;mov w0,0;sub w0,w0,1;ret;addlocal:;sub sp,sp,32;str x30,[sp];str w0,[sp,8];bl tok;cmp w0,257;b.ne albad;mov w0,0;bl find;cmp w0,0;b.ge albad;cmp w26,32;b.ge albad;adr x9,locals;lsl w10,w26,5;add w9,w9,w10;adr x10,token;ldr x11,[x10,8];str x11,[x9];ldr w11,[x10,16];str w11,[x9,8];ldr w11,[sp,8];str w11,[x9,12];str w26,[sp,12];add w26,w26,1;bl next;ldr w0,[sp,12];b alend;albad:;mov w24,1;mov w0,0;alend:;ldr x30,[sp];add sp,sp,32;ret;type:;sub sp,sp,16;str x30,[sp];bl tok;cmp w0,258;b.eq tyint;cmp w0,259;b.ne tybad;mov w0,1;str w0,[sp,8];bl next;mov w0,42;bl expect;b tyout;tyint:;mov w0,0;str w0,[sp,8];bl next;bl tok;cmp w0,42;b.ne tyout;bl next;mov w0,2;str w0,[sp,8];b tyout;tybad:;mov w24,1;tyout:;ldr w0,[sp,8];ldr x30,[sp];add sp,sp,16;ret;function:;sub sp,sp,32;str x30,[sp];mov w26,0;mov w0,258;bl expect;bl tok;cmp w0,257;b.ne fnerror;mov w0,1;bl find;cmp w0,0;b.ge fnerror;cmp w25,16;b.ge fnerror;adr x9,locals;add x9,x9,1024;lsl w10,w25,5;add w9,w9,w10;adr x10,token;ldr x11,[x10,8];str x11,[x9];ldr w11,[x10,16];str w11,[x9,8];str x21,[x9,16];mov x27,x21;str x9,[sp,8];add w25,w25,1;bl next;mov w0,40;bl expect;mov w0,0;bl tpl;mov w0,4;bl tpl;mov w0,8;bl tpl;mov w0,12;bl tpl;p
```

</details>

#### +0:26:07

> 💭 **Testing the diagnostic**

**→ `serial_send_text`**

```
install
save extra4 int f(int x){return x+7;}
build extra4
run 2
```

**← `serial_send_text`**

```
{"sent":65}
```

#### +0:26:19

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

<details><summary>result (12,308 chars, 1 lines)</summary>

```
{"hex":"6172616d733a3b626c20746f6b3b636d702077302c34313b622e657120706172616d656e643b636d70207732342c303b622e6e6520666e657869743b636d70207732362c343b622e676520666e6572726f723b626c20747970653b626c206164646c6f63616c3b6c736c2077312c77302c31303b6164642077312c77312c7732363b6d6f762077302c39323b626c2067657474706c3b6f72722077302c77302c77313b626c20656d69743b626c20746f6b3b636d702077302c34343b622e6e6520706172616d656e643b626c206e6578743b6220706172616d733b706172616d656e643a3b6c64722078392c5b73702c385d3b737472207732362c5b78392c32305d3b6d6f762077302c34313b626c206578706563743b626c20626c6f636b3b6d6f762077302c39363b626c2074706c3b626c206570696c6f6775653b6220666e657869743b666e6572726f723a3b6d6f76207732342c313b666e657869743a3b6c6472207833302c5b73705d3b6164642073702c73702c33323b7265743b67657474706c3a3b6164722078392c74656d706c617465733b6164642077392c77392c77303b6c64722077302c5b78395d3b7265743b6570696c6f6775653a3b7375622073702c73702c31363b737472207833302c5b73705d3b6d6f762077302c31363b626c2074706c3b6d6f762077302c32303b626c2074706c3b6d6f762077302c32343b626c2074706c3b6d6f762077302c32383b626c2074706c3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b6c6f61646c6f63616c3a3b6c736c2077312c77302c31303b6d6f762077302c38383b626c2067657474706c3b6f72722077302c77302c77313b6220656d69743b73746f72656c6f63616c3a3b6c736c2077312c77302c31303b6d6f762077302c39323b626c2067657474706c3b6f72722077302c77302c77313b6220656d69743b626c6f636b3a3b7375622073702c73702c31363b737472207833302c5b73705d3b6d6f762077302c3132333b626c206578706563743b626c6f6f703a3b626c20746f6b3b636d702077302c3132353b622e65712062656e643b636d702077302c303b622e657120626572726f723b636d70207732342c303b622e6e652062657869743b626c2073746d743b6220626c6f6f703b626572726f723a3b6d6f76207732342c313b622062657869743b62656e643a3b626c206e6578743b62657869743a3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b6c6f6164736c6f743a3b6c736c2077312c77302c31303b6164722078392c74656d706c617465733b6c64722077302c5b78392c38385d3b6f72722077302c77302c77313b6220656d69743b73746f7265736c6f743a3b6c736c2077312c77302c31303b6164722078392c74656d706c617465733b6c64722077302c5b78392c39325d3b6f72722077302c77302c77313b6220656d69743b707573683a3b7375622073702c73702c31363b737472207833302c5b73705d3b6d6f762077302c33323b626c2074706c3b6d6f762077302c33363b626c2074706c3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b706f703a3b7375622073702c73702c31363b737472207833302c5b73705d3b6d6f762077302c34303b626c2074706c3b6d6f762077302c34343b626c2074706c3b6c6472207833302c5b73705d3b6164642073702c73702c31363b7265743b65787072657373696f6e3a3b6d6f762077302c313b657870723a3b7375622073702c73702c33323b737472207833302c5b73705d3b7374722077302c5b73702c385d3b626c207072696d6172793b7374722077312c5b73702c32305d3b656c6f6f703a3b626c20746f6b3b6d6f762077322c313b6d6f762077332c303b636d702077302c36303b622e657120656f70657261746f723b6d6f762077332c343b636d702077302c36323b622e657120656f70657261746f723b6d6f762077322c323b6d6f762077332c34383b636d702077302c34333b622e657120656f70657261746f723b6d6f762077332c35323b636d702077302c34353b622e657120656f70657261746f723b6d6f762077322c333b6d6f762077332c35363b636d702077302c34323b622e6e652065656e643b656f70657261746f723a3b6c64722077342c5b73702c385d3b636d702077322c77343b622e6c742065656e643b7374722077332c5b73702c31325d3b7374722077322c5b73702c31365d3b626c206e6578743b626c20707573683b6c64722077302c5b73702c31365d3b6164642077302c77302c313b626c20657870723b626c20706f703b6c64722077302c5b73702c31325d3b636d702077302c383b622e676520656e6f726d616c3b7374722077302c5b73702c32345d3b6d6f762077302c3130343b626c2074706c3b6c64722077302c5b73702c32345d3b6164642077302c77302c3130383b626c2074706c3b6d6f762077312c303b7374722077312c5b73702c32305d3b6220656c6f6f703b656e6f726d616c3a3b626c2074706c3b6220656c6f6f703b65656e643a3b6c64722077312c5b73702c32305d3b6c6472207833302c5b73705d3b6164642073702c73702c33323b7265743b7072696d6172793a3b7375622073702c73702c34383b737472207833302c5b73705d3b626c20746f6b3b636d702077302c3235363b622e6571206e756d6265723b636d702077302c34303b622e657120706172656e3b636d702077302c34323b622e65712064657265663b636d702077302c3235373b622e6e652070726261643b6d6f762077302c303b626c2066696e643b636d702077302c303b622e6c742063616c6c3b7374722077302c5b73702c385d3b6c64722077312c5b78392c31325d3b7374722077312c5b73702c31325d3b626c206e6578743b6c64722077302c5b73702c385d3b626c206c6f6164736c6f743b6220706f73746669783b6e756d6265723a3b626c2076616c75653b6d6f762077312c36353533353b636d702077302c77313b622e67652070726261643b6c736c2077312c77302c353b6d6f762077302c39363b626c2067657474706c3b6f72722077302c77302c77313b626c20656d69743b6d6f762077312c303b7374722077312c5b73702c31325d3b626c206e6578743b6220706f73746669783b706172656e3a3b626c206e6578743b626c2065787072657373696f6e3b7374722077312c5b73702c31325d3b6d6f762077302c34313b626c206578706563743b6220706f73746669783b64657265663a3b626c206e6578743b626c207072696d6172793b636d702077312c303b622e65712070726261643b636d702077312c313b622e65712064636861723b6d6f762077302c36343b622064726561643b64636861723a3b6d6f762077302c36303b64726561643a3b626c2074706c3b6d6f762077312c303b7374722077312c5b73702c31325d3b6220706f73746669783b63616c6c3a3b6d6f762077302c313b626c2066696e643b636d702077302c303b622e6c742070726261643b7374722078392c5b73702c31365d3b626c206e6578743b6d6f762077302c34303b626c206578706563743b6d6f762077302c303b7374722077302c5b73702c32305d3b626c20746f6b3b636d702077302c34313b622e65712063616c6c656e643b63616c6c617267733a3b626c2065787072657373696f6e3b626c20707573683b6c64722077302c5b73702c32305d3b6164642077302c77302c313b7374722077302c5b73702c32305d3b636d702077302c343b622e67652070726261643b626c20746f6b3b636d702077302c34343b622e6e652063616c6c656e643b626c206e6578743b622063616c6c617267733b63616c6c656e643a3b6c64722078392c5b73702c31365d3b6c64722077302c5b78392c32305d3b6c64722077312c5b73702c32305d3b636d702077302c77313b622e6e652070726261643b6d6f762077302c34313b626c206578706563743b63616c6c706f703a3b6c64722077312c5b73702c32305d3b636d702077312c303b622e65712063616c6c646f3b6d6f762077302c34303b626c2067657474706c3b7375622077302c77302c323b6f72722077302c77302c77313b626c20656d69743b6d6f762077302c34343b626c2074706c3b6c64722077302c5b73702c32305d3b7375622077302c77302c313b7374722077302c5b73702c32305d3b622063616c6c706f703b63616c6c646f3a3b6c64722078392c5b73702c31365d3b6c64722078302c5b78392c31365d3b7375622077302c77302c7732313b2e776f7264203331383738333438383b6d6f762077312c313032333b6c736c2077312c77312c31363b6d6f762077322c36353533353b6f72722077312c77312c77323b616e642077302c77302c77313b6d6f762077312c33373838383b6c736c2077312c77312c31363b6f72722077302c77302c77313b626c20656d69743b6d6f762077312c303b7374722077312c5b73702c31325d3b706f73746669783a3b626c20746f6b3b636d702077302c39313b622e6e65207072656e643b6c64722077312c5b73702c31325d3b636d702077312c303b622e65712070726261643b626c206e6578743b626c20707573683b626c2065787072657373696f6e3b6d6f762077302c39333b626c206578706563743b626c20706f703b6c64722077312c5b73702c31325d3b636d702077312c313b622e6571206978636861723b6d6f762077302c36383b626c2074706c3b6d6f762077302c36343b626c2074706c3b62206978656e643b6978636861723a3b6d6f762077302c34383b626c2074706c3b6d6f762077302c36303b626c2074706c3b6978656e643a3b6d6f762077312c303b7374722077312c5b73702c31325d3b6220706f73746669783b70726261643a3b6d6f76207732342c313b6d6f762077312c303b7374722077312c5b73702c31325d3b7072656e643a3b6c64722077312c5b73702c31325d3b6c6472207833302c5b73705d3b6164642073702c73702c34383b7265743b73746d743a3b7375622073702c73702c34383b737472207833302c5b73705d3b626c20746f6b3b636d702077302c3132333b622e65712073626c6f636b3b636d702077302c3235383b622e6571206465636c3b636d702077302c3235393b622e6571206465636c3b636d702077302c3236303b622e6571207372657475726e3b636d702077302c3236313b622e6571207369663b636d702077302c3236333b622e657120737768696c653b636d702077302c3235373b622e65712061737369676e3b636d702077302c34323b622e65712073696e6469726563743b6d6f76207732342c313b622073657869743b73626c6f636b3a3b626c20626c6f636b3b622073657869743b7372657475726e3a3b626c206e6578743b626c2065787072657373696f6e3b6d6f762077302c35393b626c206578706563743b626c206570696c6f6775653b622073657869743b6465636c3a3b626c20747970653b626c206164646c6f63616c3b7374722077302c5b73702c385d3b626c20746f6b3b636d702077302c36313b622e6e6520646e6f696e69743b626c206e6578743b626c2065787072657373696f6e3b6c647220","text":"arams:;bl tok;cmp w0,41;b.eq paramend;cmp w24,0;b.ne fnexit;cmp w26,4;b.ge fnerror;bl type;bl addlocal;lsl w1,w0,10;add w1,w1,w26;mov w0,92;bl gettpl;orr w0,w0,w1;bl emit;bl tok;cmp w0,44;b.ne paramend;bl next;b params;paramend:;ldr x9,[sp,8];str w26,[x9,20];mov w0,41;bl expect;bl block;mov w0,96;bl tpl;bl epilogue;b fnexit;fnerror:;mov w24,1;fnexit:;ldr x30,[sp];add sp,sp,32;ret;gettpl:;adr x9,templates;add w9,w9,w0;ldr w0,[x9];ret;epilogue:;sub sp,sp,16;str x30,[sp];mov w0,16;bl tpl;mov w0,20;bl tpl;mov w0,24;bl tpl;mov w0,28;bl tpl;ldr x30,[sp];add sp,sp,16;ret;loadlocal:;lsl w1,w0,10;mov w0,88;bl gettpl;orr w0,w0,w1;b emit;storelocal:;lsl w1,w0,10;mov w0,92;bl gettpl;orr w0,w0,w1;b emit;block:;sub sp,sp,16;str x30,[sp];mov w0,123;bl expect;bloop:;bl tok;cmp w0,125;b.eq bend;cmp w0,0;b.eq berror;cmp w24,0;b.ne bexit;bl stmt;b bloop;berror:;mov w24,1;b bexit;bend:;bl next;bexit:;ldr x30,[sp];add sp,sp,16;ret;loadslot:;lsl w1,w0,10;adr x9,templates;ldr w0,[x9,88];orr w0,w0,w1;b emit;storeslot:;lsl w1,w0,10;adr x9,templates;ldr w0,[x9,92];orr w0,w0,w1;b emit;push:;sub sp,sp,16;str x30,[sp];mov w0,32;bl tpl;mov w0,36;bl tpl;ldr x30,[sp];add sp,sp,16;ret;pop:;sub sp,sp,16;str x30,[sp];mov w0,40;bl tpl;mov w0,44;bl tpl;ldr x30,[sp];add sp,sp,16;ret;expression:;mov w0,1;expr:;sub sp,sp,32;str x30,[sp];str w0,[sp,8];bl primary;str w1,[sp,20];eloop:;bl tok;mov w2,1;mov w3,0;cmp w0,60;b.eq eoperator;mov w3,4;cmp w0,62;b.eq eoperator;mov w2,2;mov w3,48;cmp w0,43;b.eq eoperator;mov w3,52;cmp w0,45;b.eq eoperator;mov w2,3;mov w3,56;cmp w0,42;b.ne eend;eoperator:;ldr w4,[sp,8];cmp w2,w4;b.lt eend;str w3,[sp,12];str w2,[sp,16];bl next;bl push;ldr w0,[sp,16];add w0,w0,1;bl expr;bl pop;ldr w0,[sp,12];cmp w0,8;b.ge enormal;str w0,[sp,24];mov w0,104;bl tpl;ldr w0,[sp,24];add w0,w0,108;bl tpl;mov w1,0;str w1,[sp,20];b eloop;enormal:;bl tpl;b eloop;eend:;ldr w1,[sp,20];ldr x30,[sp];add sp,sp,32;ret;primary:;sub sp,sp,48;str x30,[sp];bl tok;cmp w0,256;b.eq number;cmp w0,40;b.eq paren;cmp w0,42;b.eq deref;cmp w0,257;b.ne prbad;mov w0,0;bl find;cmp w0,0;b.lt call;str w0,[sp,8];ldr w1,[x9,12];str w1,[sp,12];bl next;ldr w0,[sp,8];bl loadslot;b postfix;number:;bl value;mov w1,65535;cmp w0,w1;b.ge prbad;lsl w1,w0,5;mov w0,96;bl gettpl;orr w0,w0,w1;bl emit;mov w1,0;str w1,[sp,12];bl next;b postfix;paren:;bl next;bl expression;str w1,[sp,12];mov w0,41;bl expect;b postfix;deref:;bl next;bl primary;cmp w1,0;b.eq prbad;cmp w1,1;b.eq dchar;mov w0,64;b dread;dchar:;mov w0,60;dread:;bl tpl;mov w1,0;str w1,[sp,12];b postfix;call:;mov w0,1;bl find;cmp w0,0;b.lt prbad;str x9,[sp,16];bl next;mov w0,40;bl expect;mov w0,0;str w0,[sp,20];bl tok;cmp w0,41;b.eq callend;callargs:;bl expression;bl push;ldr w0,[sp,20];add w0,w0,1;str w0,[sp,20];cmp w0,4;b.ge prbad;bl tok;cmp w0,44;b.ne callend;bl next;b callargs;callend:;ldr x9,[sp,16];ldr w0,[x9,20];ldr w1,[sp,20];cmp w0,w1;b.ne prbad;mov w0,41;bl expect;callpop:;ldr w1,[sp,20];cmp w1,0;b.eq calldo;mov w0,40;bl gettpl;sub w0,w0,2;orr w0,w0,w1;bl emit;mov w0,44;bl tpl;ldr w0,[sp,20];sub w0,w0,1;str w0,[sp,20];b callpop;calldo:;ldr x9,[sp,16];ldr x0,[x9,16];sub w0,w0,w21;.word 318783488;mov w1,1023;lsl w1,w1,16;mov w2,65535;orr w1,w1,w2;and w0,w0,w1;mov w1,37888;lsl w1,w1,16;orr w0,w0,w1;bl emit;mov w1,0;str w1,[sp,12];postfix:;bl tok;cmp w0,91;b.ne prend;ldr w1,[sp,12];cmp w1,0;b.eq prbad;bl next;bl push;bl expression;mov w0,93;bl expect;bl pop;ldr w1,[sp,12];cmp w1,1;b.eq ixchar;mov w0,68;bl tpl;mov w0,64;bl tpl;b ixend;ixchar:;mov w0,48;bl tpl;mov w0,60;bl tpl;ixend:;mov w1,0;str w1,[sp,12];b postfix;prbad:;mov w24,1;mov w1,0;str w1,[sp,12];prend:;ldr w1,[sp,12];ldr x30,[sp];add sp,sp,48;ret;stmt:;sub sp,sp,48;str x30,[sp];bl tok;cmp w0,123;b.eq sblock;cmp w0,258;b.eq decl;cmp w0,259;b.eq decl;cmp w0,260;b.eq sreturn;cmp w0,261;b.eq sif;cmp w0,263;b.eq swhile;cmp w0,257;b.eq assign;cmp w0,42;b.eq sindirect;mov w24,1;b sexit;sblock:;bl block;b sexit;sreturn:;bl next;bl expression;mov w0,59;bl expect;bl epilogue;b sexit;decl:;bl type;bl addlocal;str w0,[sp,8];bl tok;cmp w0,61;b.ne dnoinit;bl next;bl expression;ldr "}
```

</details>

#### +0:26:23

> 💭 **Preparing a fresh diagnostic compile**

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

<details><summary>hex (4,612 chars, 1 lines)</summary>

```
77302c5b73702c385d3b626c2073746f7265736c6f743b62206473656d693b646e6f696e69743a3b6d6f762077302c39363b626c2074706c3b6c64722077302c5b73702c385d3b626c2073746f7265736c6f743b6473656d693a3b6d6f762077302c35393b626c206578706563743b622073657869743b61737369676e3a3b6d6f762077302c303b626c2066696e643b636d702077302c303b622e6c7420736572726f723b7374722077302c5b73702c385d3b6c64722077312c5b78392c31325d3b7374722077312c5b73702c31325d3b626c206e6578743b626c20746f6b3b636d702077302c39313b622e65712073696e6465783b6d6f762077302c36313b626c206578706563743b626c2065787072657373696f6e3b6c64722077302c5b73702c385d3b626c2073746f7265736c6f743b62207373656d693b73696e6465783a3b6c64722077302c5b73702c385d3b626c206c6f6164736c6f743b626c20707573683b626c206e6578743b626c2065787072657373696f6e3b6d6f762077302c39333b626c206578706563743b626c20706f703b6c64722077312c5b73702c31325d3b636d702077312c303b622e657120736572726f723b636d702077312c313b622e6571207361636861723b6d6f762077302c36383b626c2074706c3b62206164647265737372656164793b7361636861723a3b6d6f762077302c34383b626c2074706c3b62206164647265737372656164793b73696e6469726563743a3b626c206e6578743b626c207072696d6172793b7374722077312c5b73702c31325d3b636d702077312c303b622e657120736572726f723b6164647265737372656164793a3b626c20707573683b6d6f762077302c36313b626c206578706563743b626c2065787072657373696f6e3b626c20706f703b6c64722077312c5b73702c31325d3b636d702077312c313b622e6571207373636861723b6d6f762077302c37323b626c2074706c3b62207373656d693b7373636861723a3b6d6f762077302c37363b626c2074706c3b7373656d693a3b6d6f762077302c35393b626c206578706563743b622073657869743b7369663a3b626c206e6578743b6d6f762077302c34303b626c206578706563743b626c2065787072657373696f6e3b6d6f762077302c34313b626c206578706563743b737472207832312c5b73702c31365d3b6d6f762077302c38303b626c2074706c3b626c2073746d743b626c20746f6b3b636d702077302c3236323b622e65712073656c73653b6c64722078302c5b73702c31365d3b626c2070617463687a65726f3b622073657869743b73656c73653a3b737472207832312c5b73702c32345d3b6d6f762077302c38343b626c2074706c3b6c64722078302c5b73702c31365d3b626c2070617463687a65726f3b626c206e6578743b626c2073746d743b6c64722078302c5b73702c32345d3b626c2070617463686272616e63683b622073657869743b737768696c653a3b737472207832312c5b73702c32345d3b626c206e6578743b6d6f762077302c34303b626c206578706563743b626c2065787072657373696f6e3b6d6f762077302c34313b626c206578706563743b737472207832312c5b73702c31365d3b6d6f762077302c38303b626c2074706c3b626c2073746d743b6c64722078302c5b73702c32345d3b7375622077302c77302c7732313b2e776f7264203331383738333438383b6c736c2077302c77302c363b2e776f726420313339323933333838383b6d6f762077312c353132303b6c736c2077312c77312c31363b6f72722077302c77302c77313b626c20656d69743b6c64722078302c5b73702c31365d3b626c2070617463687a65726f3b622073657869743b736572726f723a3b6d6f76207732342c313b73657869743a3b6c6472207833302c5b73705d3b6164642073702c73702c34383b7265743b70617463687a65726f3a3b7375622077312c7732312c77303b6c736c2077312c77312c333b6d6f762077322c31333331323b6c736c2077322c77322c31363b6f72722077312c77312c77323b7374722077312c5b78305d3b7265743b70617463686272616e63683a3b7375622077312c7732312c77303b2e776f726420313339323637313737373b6d6f762077322c353132303b6c736c2077322c77322c31363b6f72722077312c77312c77323b7374722077312c5b78305d3b7265743b74656d706c617465733a3b7375622073702c73702c3235363b737472207833302c5b73702c3234385d3b737472207832392c5b73702c3234305d3b616464207832392c73702c303b6c6472207833302c5b73702c3234385d3b6c6472207832392c5b73702c3234305d3b6164642073702c73702c3235363b7265743b7375622073702c73702c31363b7374722077302c5b73705d3b6c64722077322c5b73705d3b6164642073702c73702c31363b6164642077302c77322c77303b7375622077302c77322c77303b6d756c2077302c77322c77303b6c6472622077302c5b78305d3b6c64722077302c5b78305d3b2e776f7264203138343535313438383b7374722077302c5b78325d3b737472622077302c5b78325d3b2e776f7264203837323431353233323b2e776f7264203333353534343332303b6c64722077302c5b7832395d3b7374722077302c5b7832395d3b6d6f762077302c303b2e776f726420323438333032373936383b636d702077322c77303b2e776f7264203434363637303831363b2e776f7264203434363638323038303b6b6579776f7264733a3b2e776f726420313935333339323839393b2e776f726420313633343233313034343b2e776f726420313730313937313537303b2e776f726420313835323939343933323b2e776f72642037333832303431383b2e776f726420313730323036333230353b2e776f726420313736383435333839333b2e776f72642032353936343b2e776f726420303b746f6b656e3a3b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b2e776f726420303b6c6f63616c733a3b66756e63733a3b7265743b0a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030340a7368656c6c3e20
```

</details>

`text`

<details><summary>text (2,306 chars, 6 lines)</summary>

```
w0,[sp,8];bl storeslot;b dsemi;dnoinit:;mov w0,96;bl tpl;ldr w0,[sp,8];bl storeslot;dsemi:;mov w0,59;bl expect;b sexit;assign:;mov w0,0;bl find;cmp w0,0;b.lt serror;str w0,[sp,8];ldr w1,[x9,12];str w1,[sp,12];bl next;bl tok;cmp w0,91;b.eq sindex;mov w0,61;bl expect;bl expression;ldr w0,[sp,8];bl storeslot;b ssemi;sindex:;ldr w0,[sp,8];bl loadslot;bl push;bl next;bl expression;mov w0,93;bl expect;bl pop;ldr w1,[sp,12];cmp w1,0;b.eq serror;cmp w1,1;b.eq sachar;mov w0,68;bl tpl;b addressready;sachar:;mov w0,48;bl tpl;b addressready;sindirect:;bl next;bl primary;str w1,[sp,12];cmp w1,0;b.eq serror;addressready:;bl push;mov w0,61;bl expect;bl expression;bl pop;ldr w1,[sp,12];cmp w1,1;b.eq sschar;mov w0,72;bl tpl;b ssemi;sschar:;mov w0,76;bl tpl;ssemi:;mov w0,59;bl expect;b sexit;sif:;bl next;mov w0,40;bl expect;bl expression;mov w0,41;bl expect;str x21,[sp,16];mov w0,80;bl tpl;bl stmt;bl tok;cmp w0,262;b.eq selse;ldr x0,[sp,16];bl patchzero;b sexit;selse:;str x21,[sp,24];mov w0,84;bl tpl;ldr x0,[sp,16];bl patchzero;bl next;bl stmt;ldr x0,[sp,24];bl patchbranch;b sexit;swhile:;str x21,[sp,24];bl next;mov w0,40;bl expect;bl expression;mov w0,41;bl expect;str x21,[sp,16];mov w0,80;bl tpl;bl stmt;ldr x0,[sp,24];sub w0,w0,w21;.word 318783488;lsl w0,w0,6;.word 1392933888;mov w1,5120;lsl w1,w1,16;orr w0,w0,w1;bl emit;ldr x0,[sp,16];bl patchzero;b sexit;serror:;mov w24,1;sexit:;ldr x30,[sp];add sp,sp,48;ret;patchzero:;sub w1,w21,w0;lsl w1,w1,3;mov w2,13312;lsl w2,w2,16;orr w1,w1,w2;str w1,[x0];ret;patchbranch:;sub w1,w21,w0;.word 1392671777;mov w2,5120;lsl w2,w2,16;orr w1,w1,w2;str w1,[x0];ret;templates:;sub sp,sp,256;str x30,[sp,248];str x29,[sp,240];add x29,sp,0;ldr x30,[sp,248];ldr x29,[sp,240];add sp,sp,256;ret;sub sp,sp,16;str w0,[sp];ldr w2,[sp];add sp,sp,16;add w0,w2,w0;sub w0,w2,w0;mul w0,w2,w0;ldrb w0,[x0];ldr w0,[x0];.word 184551488;str w0,[x2];strb w0,[x2];.word 872415232;.word 335544320;ldr w0,[x29];str w0,[x29];mov w0,0;.word 2483027968;cmp w2,w0;.word 446670816;.word 446682080;keywords:;.word 1953392899;.word 1634231044;.word 1701971570;.word 1852994932;.word 73820418;.word 1702063205;.word 1768453893;.word 25964;.word 0;token:;.word 0;.word 0;.word 0;.word 0;.word 0;.word 0;locals:;funcs:;ret;
shell> installed
shell> saved
shell> built
shell> exit 00000004
shell>
```

</details>

#### +0:26:35

> 💭 **Correcting whitespace tokenization**

**→ `serial_send_text`**

```
as raw
save extra4 cmp w0,32;b.ge lex;
save extra5 cmp w0,33;b.ge lex;
run
save extra4 cmp w0,57;b.ge ident;
save extra5 cmp w0,58;b.ge ident;
run
save extra4 cmp w9,122;b.ge punct;
save extra5 cmp w9,123;b.ge punct;
run
save extra4 int f(int x){return x+7;}
as new1
```

**← `serial_send_text`**

```
{"sent":267}
```

#### +0:26:51

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
assembled
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> assembled
shell>
```

#### +0:26:54

**→ `serial_send_text`**

```
install
build extra4
run 2
run 5
```

**← `serial_send_text`**

```
{"sent":33}
```

#### +0:26:57

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030390a7368656c6c3e20657869742030303030303030630a7368656c6c3e20
```

`text`

```
installed
shell> built
shell> exit 00000009
shell> exit 0000000c
shell>
```

#### +0:27:02

> 💭 **Patching failure handling**
> 💭 **Extending compiler constants**

> 💭 **Designing safe input reads**
> 💭 **Building parser helpers**

> 💭 **Preparing capacity-checked output**
> 💭 **Checking generated code size**

> 💭 **Parsing direct s[p] reads**

> 💭 **Implementing return parsing**
> 💭 **Adding parser checks**

> 💭 **Completing longasm source**
> 💭 **Moving seed tables**
> 💭 **Stack-allocating seed tables**

**→ `serial_send_text`**

```
as raw
save extra4 mov x28,x1;mov x19,x1;
save extra5 sub sp,sp,1632;add x28,sp,0;mov x19,x1;
run
save extra4 adr x9,locals;
save extra5 mov x9,x28;
run
save extra4 adr x9,token;
save extra5 add x9,x28,1536;
run
save extra4 adr x10,token;
save extra5 add x10,x28,1536;
run
save extra4 fail:;sub w0,w19,w28;
save extra5 fail:;mov w0,0;b finish;sub w0,w19,w28;
run
save extra4 finish:;
save extra5 finish:;add sp,sp,1632;
run
save extra2 pending
as new1
```

**← `serial_send_text`**

```
{"sent":452}
```

#### +0:29:28

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030340a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030330a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030330a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembled
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000004
shell> saved
shell> saved
shell> exit 00000003
shell> saved
shell> saved
shell> exit 00000003
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> assembly error
shell>
```

#### +0:29:33

> 💭 **Testing add x28, sp**

**→ `serial_send_text`**

```
save extra4 sub sp,sp,1632;add x28,sp,0;add x9,x28,1536;add sp,sp,1632;ret;
as extra4
```

**← `serial_send_text`**

```
{"sent":86}
```

#### +0:29:43

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20
```

`text`

```
saved
shell> assembled
shell>
```

#### +0:29:46

> 💭 **Retrying asnew1**

**→ `serial_send_text`**

```
as new1
```

**← `serial_send_text`**

```
{"sent":8}
```

#### +0:29:57

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c79206572726f720a7368656c6c3e20
```

`text`

```
assembly error
shell>
```

#### +0:30:03

> 💭 **Rebooting to flush cache**

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:30:16

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T100300.407709Z"}
```

#### +0:30:24

**→ `serial_send_text`**

```
as new1
install
save extra4 int f(int x){return x+7;}
build extra4
run 2
```

**← `serial_send_text`**

```
{"sent":73}
```

#### +0:30:28

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030390a7368656c6c3e20
```

`text`

```
BOOT
shell> assembled
shell> installed
shell> saved
shell> built
shell> exit 00000009
shell>
```

#### +0:30:32

> 💭 **Documenting reboot requirement**

**→ `serial_send_text`**

```
save extra4 int add(int a,int b){return a+b;}int f(int x){int z=0;while(x>0){z=add(z,x);x=x-1;}return z;}
build extra4
run 3
run 5
```

**← `serial_send_text`**

```
{"sent":131}
```

#### +0:30:45

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e20
```

`text`

```
saved
shell>
```

#### +0:30:50

> 💭 **Recomputing ASR constant**
> 💭 **Checking call-frame overlap**

> 💭 **Stopping VM for patch**

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:31:33

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T100413.657170Z"}
```

#### +0:31:37

**→ `serial_send_text`**

```
as raw
save extra4 str x9,[sp,16];
save extra5 str w9,[sp,16];
run
save extra4 ldr x9,[sp,16];
save extra5 ldr w9,[sp,16];
run
save extra4 .word 318783488;
save extra5 .word 318929920;
run
save extra4 .word 446682080;
save extra5 .word 446683104;
run
save extra2 pending
```

**← `serial_send_text`**

```
{"sent":271}
```

#### +0:31:43

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e20617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030320a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030320a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20
```

`text`

```
BOOT
shell> assembled
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000002
shell> saved
shell> saved
shell> exit 00000002
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell>
```

#### +0:31:48

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:31:51

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T100433.948117Z"}
```

#### +0:31:57

**→ `serial_send_text`**

```
as new1
install
save extra4 int add(int a,int b){return a+b;}int f(int x){int z=0;while(x>0){z=add(z,x);x=x-1;}return z;}
build extra4
run 3
run 5
```

**← `serial_send_text`**

```
{"sent":147}
```

#### +0:32:02

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030360a7368656c6c3e20657869742030303030303030660a7368656c6c3e20
```

`text`

```
BOOT
shell> assembled
shell> installed
shell> saved
shell> built
shell> exit 00000006
shell> exit 0000000f
shell>
```

#### +0:32:06

> 💭 **Optimizing C source**

**→ `serial_send_text`**

<details><summary>text (2,402 chars, 29 lines)</summary>

```
save longasm int alpha(int c){if(c>64){if(c<91){return 1;}}if(c>96){if(c<123){return 1;}}
append longasm if(c-95){return 0;}return 1;}
append longasm int digit(int c){if(c<48){return 0;}if(c>57){return 0;}return 1;}
append longasm int ws(char *p,int end){while(p<end){if(*p>32){return p;}p=p+1;}return p;}
append longasm int ident(char *p,int end){int c=0;if(p<end){c=*p;}if(alpha(c)<1){return 0;}
append longasm p=p+1;while(p<end){c=*p;if(alpha(c)){p=p+1;}else{if(digit(c)){p=p+1;}else{return p;}}}return p;}
append longasm int key(char *p,int end){if(end-p<4){return 0;}if(*p-105){return 0;}p=p+1;
append longasm if(*p-110){return 0;}p=p+1;if(*p-116){return 0;}p=p+1;if(*p>32){return 0;}return ws(p,end);}
append longasm int compile(char *s,int n,int *out,int cap){int end=s+n;char *p=ws(s,end);char *q=p;
append longasm char *ps=p;char *pe=p;int c=0;int v=0;int hi=0;int used=1;
append longasm if(cap<12){return 0;}p=key(p,end);if(p<1){return 0;}p=ident(p,end);if(p<1){return 0;}
append longasm p=ws(p,end);if(p<end){if(*p-40){return 0;}}else{return 0;}p=ws(p+1,end);
append longasm p=key(p,end);if(p<1){return 0;}ps=p;p=ident(p,end);if(p<1){return 0;}pe=p;p=ws(p,end);
append longasm if(p<end){if(*p-41){return 0;}}else{return 0;}p=ws(p+1,end);
append longasm if(p<end){if(*p-123){return 0;}}else{return 0;}p=ws(p+1,end);
append longasm if(end-p<7){return 0;}if(*p-114){return 0;}p=p+1;if(*p-101){return 0;}p=p+1;
append longasm if(*p-116){return 0;}p=p+1;if(*p-117){return 0;}p=p+1;if(*p-114){return 0;}p=p+1;
append longasm if(*p-110){return 0;}p=p+1;if(*p>32){return 0;}p=ws(p,end);q=p;p=ident(p,end);
append longasm if(p<1){return 0;}if(p-q-pe+ps){return 0;}while(ps<pe){if(*ps-*q){return 0;}ps=ps+1;q=q+1;}
append longasm out[0]=10753*256*256+992;p=ws(p,end);if(p<end){c=*p;}else{return 0;}
append longasm while(c-59){if(c-43){if(c-45){return 0;}hi=20736;}else{hi=4352;}p=ws(p+1,end);
append longasm if(p<end){c=*p;}else{return 0;}if(digit(c)<1){return 0;}v=0;
append longasm while(digit(c)){v=v*10+c-48;if(v>4095){return 0;}p=p+1;if(p<end){c=*p;}else{return 0;}}
append longasm if(cap<used*4+8){return 0;}out[used]=hi*256*256+v*1024;used=used+1;
append longasm p=ws(p,end);if(p<end){c=*p;}else{return 0;}}
append longasm p=ws(p+1,end);if(p<end){if(*p-125){return 0;}}else{return 0;}p=ws(p+1,end);
append longasm if(p-end){return 0;}out[used]=54879*256*256+960;return used*4+4;}
build longasm
```

</details>

**← `serial_send_text`**

```
{"sent":2402}
```

#### +0:32:33

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20
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
shell> built
shell>
```

#### +0:32:36

> 💭 **Installing the built package**

**→ `serial_send_text`**

```
install
save extra4 int f(int x){return x+7;}
build extra4
run 2
run 5
```

**← `serial_send_text`**

```
{"sent":71}
```

#### +0:32:45

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030390a7368656c6c3e20657869742030303030303030630a7368656c6c3e20
```

`text`

```
installed
shell> saved
shell> built
shell> exit 00000009
shell> exit 0000000c
shell>
```

#### +0:32:51

**→ `serial_send_text`**

```
save extra5 int Independent(int value){return value+19-4+2;}
build extra5
run 0
run 3
run 20
save extra3 int bad(int x){return wrong+7;}
build extra3
run 3
save extra3 int bad(int x){return x+;}
build extra3
run 20
```

**← `serial_send_text`**

```
{"sent":215}
```

#### +0:32:55

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031310a7368656c6c3e20657869742030303030303031340a7368656c6c3e20657869742030303030303032350a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303031340a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032350a7368656c6c3e20
```

`text`

```
saved
shell> built
shell> exit 00000011
shell> exit 00000014
shell> exit 00000025
shell> saved
shell> build error
shell> exit 00000014
shell> saved
shell> build error
shell> exit 00000025
shell>
```

#### +0:33:00

> 💭 **Tidying seed-source diagnostics**
> 💭 **Tightening Cbuilt bounds**

> 💭 **Preparing pointer-write tests**

> 💭 **Tightening malformed-input handling**
> 💭 **Fixing EOF whitespace state**

> 💭 **Completing exact-source cleanup**

> 💭 **Testing serial readiness**
> 💭 **Removing diagnostic chains**

**→ `serial_send_text`**

```
as raw
save extra4 fail:;mov w0,0;b finish;sub w0,w19,w28;lsl w0,w0,5;mov w1,21120;lsl w1,w1,16;orr w0,w0,w1;
save extra5 fail:;mov w0,0;
run
save extra4 str w0,[x22];adr x9,templates;ldr w0,[x9,28];str w0,[x22,4];mov w0,8;finish:;
save extra5 finish:;
run
save extra4 cmp w0,4;b.ge prbad;
save extra5 cmp w0,5;b.ge prbad;
run
save extra4 cmp w3,31;b.ge lexerr;
save extra5 cmp w3,32;b.ge lexerr;
run
save extra4 cmp w9,w23;b.ge overflow;
save extra5 cmp w23,w9;b.lt overflow;
run
save extra4 skip:;cmp w19,w20;b.ge ntstore;
save extra5 skip:;cmp w19,w20;b.ge nteof;
run
save extra4 lexerr:;mov w24,1;mov w0,0;
save extra5 lexerr:;mov w24,1;nteof:;mov w0,0;
run
save extra4 lex:;mov x2,x19;
save extra5 lex:;cmp w0,0;b.eq lexerr;mov x2,x19;
run
save extra4 digits:;sub w0,w0,48;
save extra5 digits:;cmp w1,6554;b.lt digitok;mov w24,1;digitok:;sub w0,w0,48;
run
save extra4 loadlocal:;lsl w1,w0,10;mov w0,88;bl gettpl;orr w0,w0,w1;b emit;
recv extra5 0
run
save extra4 storelocal:;lsl w1,w0,10;mov w0,92;bl gettpl;orr w0,w0,w1;b emit;
run
save extra4 locals:;funcs:;ret;
run
save extra2 seed-final
```

**← `serial_send_text`**

```
{"sent":1097}
```

#### +0:34:59

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e2072656164790a73617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20
```

`text`

```
assembled
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> saved
shell> exit 00000001
shell> saved
shell> ready
saved
shell> exit 00000001
shell> saved
shell> exit 00000001
shell> saved
shell> exit 00000001
shell> saved
shell>
```

#### +0:35:04

> 💭 **Replacing invalid immediate compare**
> 💭 **Patching directory offsets**

> 💭 **Preparing validation compiler**
> 💭 **Fixing comparison before reboot**

**→ `serial_send_text`**

```
save extra4 cmp w1,6554;
save extra5 mov w9,6554;cmp w1,w9;
run
save extra2 seed-final
```

**← `serial_send_text`**

```
{"sent":87}
```

#### +0:35:53

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e20657869742030303030303030310a7368656c6c3e2073617665640a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> exit 00000001
shell> saved
shell>
```

#### +0:35:57

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:36:00

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T100841.144082Z"}
```

#### +0:36:05

**→ `serial_send_text`**

```
as new1
install
save extra1 int sum(int a,int b,int c,int d){return a+b+c+d;}
append extra1 int make(char *s,int n,int *out,int cap){int i=0;int v=0;while(i<n){v=v+s[i];i=i+1;}
append extra1 if(cap<8){return 0;}out[0]=21120*256*256+sum(v,n,3,4)*32;
append extra1 out[1]=54879*256*256+960;return 8;}
build extra1
install
save extra4 abc
build extra4
run 0
```

**← `serial_send_text`**

```
{"sent":355}
```

#### +0:36:11

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303133300a7368656c6c3e20
```

`text`

```
BOOT
shell> assembled
shell> installed
shell> saved
shell> saved
shell> saved
shell> saved
shell> built
shell> installed
shell> saved
shell> built
shell> exit 00000130
shell>
```

#### +0:36:14

**→ `serial_send_text`**

```
as new1
install
recv extra4 26
```

**← `serial_send_text`**

```
{"sent":31}
```

#### +0:36:23

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2072656164790a
```

`text`

```
assembled
shell> installed
shell> ready
```

#### +0:36:26

**→ `serial_send_text`**

```
int f(int x){return x+7;}
```

**← `serial_send_text`**

```
{"sent":26}
```

#### +0:36:31

**→ `serial_send_text`**

```
build extra4
run 8
```

**← `serial_send_text`**

```
{"sent":19}
```

#### +0:36:35

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030660a7368656c6c3e20
```

`text`

```
saved
shell> built
shell> exit 0000000f
shell>
```

#### +0:36:39

> 💭 **Rewriting C source**

**→ `serial_send_text`**

<details><summary>text (2,508 chars, 33 lines)</summary>

```
save longasm int alpha(int c){if(c>64){if(c<91){return 1;}}if(c>96){if(c<123){return 1;}}
append longasm if(c-95){return 0;}return 1;}
append longasm int digit(int c){if(c<48){return 0;}if(c>57){return 0;}return 1;}
append longasm int ws(char *p,int end){while(p<end){if(*p>32){return p;}p=p+1;}return p;}
append longasm int ident(char *p,int end){int c=0;if(p<end){c=*p;}if(alpha(c)<1){return 0;}
append longasm p=p+1;while(p<end){c=*p;if(alpha(c)){p=p+1;}else{if(digit(c)){p=p+1;}else{return p;}}}return p;}
append longasm int key(char *p,int end){if(end-p<4){return 0;}if(*p-105){return 0;}p=p+1;
append longasm if(*p-110){return 0;}p=p+1;if(*p-116){return 0;}p=p+1;if(*p>32){return 0;}return ws(p,end);}
append longasm int compile(char *s,int n,int *out,int cap){int end=s+n;char *p=ws(s,end);char *q=p;
append longasm char *ps=p;char *pe=p;int c=0;int v=0;int hi=0;int used=1;
append longasm if(n<1){return 0;}if(n>32768){return 0;}if(cap>8192){cap=8192;}
append longasm if(cap<12){return 0;}p=key(p,end);if(p<1){return 0;}p=ident(p,end);if(p<1){return 0;}
append longasm p=ws(p,end);if(p<end){if(*p-40){return 0;}}else{return 0;}p=ws(p+1,end);
append longasm p=key(p,end);if(p<1){return 0;}ps=p;p=ident(p,end);if(p<1){return 0;}pe=p;p=ws(p,end);
append longasm if(p<end){if(*p-41){return 0;}}else{return 0;}p=ws(p+1,end);
append longasm if(p<end){if(*p-123){return 0;}}else{return 0;}p=ws(p+1,end);
append longasm if(end-p<7){return 0;}if(*p-114){return 0;}p=p+1;if(*p-101){return 0;}p=p+1;
append longasm if(*p-116){return 0;}p=p+1;if(*p-117){return 0;}p=p+1;if(*p-114){return 0;}p=p+1;
append longasm if(*p-110){return 0;}p=p+1;if(*p>32){return 0;}p=ws(p,end);q=p;p=ident(p,end);
append longasm if(p<1){return 0;}if(p-q-pe+ps){return 0;}while(ps<pe){if(*ps-*q){return 0;}ps=ps+1;q=q+1;}
append longasm out[0]=10753*256*256+992;p=ws(p,end);if(p<end){c=*p;}else{return 0;}
append longasm while(c-59){if(c-43){if(c-45){return 0;}hi=20736;}else{hi=4352;}p=ws(p+1,end);
append longasm if(p<end){c=*p;}else{return 0;}if(digit(c)<1){return 0;}v=0;
append longasm while(digit(c)){v=v*10+c-48;if(v>4095){return 0;}p=p+1;if(p<end){c=*p;}else{return 0;}}
append longasm if(cap<used*4+8){return 0;}out[used]=hi*256*256+v*1024;used=used+1;
append longasm p=ws(p,end);if(p<end){c=*p;}else{return 0;}}
append longasm p=ws(p+1,end);if(p<end){if(*p-125){return 0;}}else{return 0;}p=ws(p+1,end);
append longasm if(p-end){return 0;}out[used]=54879*256*256+960;return used*4+4;}
build longasm
install
build extra4
run 8
```

</details>

**← `serial_send_text`**

```
{"sent":2508}
```

#### +0:37:06

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030660a7368656c6c3e20
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
shell> built
shell> installed
shell> built
shell> exit 0000000f
shell>
```

#### +0:37:10

> 💭 **Reordering compiler bounds checks**
> 💭 **Documenting compiler dialect**

> 💭 **Removing obsolete scratch note**
> 💭 **Preparing raw documentation**

> 💭 **Checking runtime arguments**
> 💭 **Rechecking fresh-boot chain**

> 💭 **Preparing ABI documentation**
> 💭 **Documenting generated-code ABI**

**→ `serial_send_text`**

<details><summary>text (4,534 chars, 46 lines)</summary>

```
save raw SEED DIALECT (new1). All source is ordinary ASCII C subset; no preprocessor, comments, globals or libraries.;
append raw Translation unit: 1..16 named int-returning functions; definitions before use (recursion allowed).;
append raw Entry is LAST function, regardless of name. Up to FOUR typed parameters, passed in w1,w2,w3,w4; return w0.;
append raw Types: int, char*, int*. Guest pointers are 32-bit; implicit pointer/int conversions are permitted.;
append raw Each function has at most 32 unique variable names INCLUDING parameters; function-wide scope, no shadowing.;
append raw Locals may be declared anywhere, optionally initialized; omitted initializer means zero.;
append raw Identifiers: case sensitive, [A-Za-z_][A-Za-z_0-9]*, maximum 31 bytes. Do not use keywords as names.;
append raw Decimal literals 0..65534; binary *, +, -, <, > with C precedence and left associativity; parentheses.;
append raw Comparisons are signed and yield 0/1. Arithmetic wraps to 32 bits. No unary minus: use (0-value).;
append raw Unary * reads unsigned char or int according to pointer type; p[i] reads/writes char or int (int stride4).;
append raw Assignment: name=expr; p[i]=expr; *p=expr;. Pointer+integer arithmetic is BYTE based: use indexing for int*.;
append raw Statements: blocks, declarations, assignments, return expr;, if(expr) statement [else statement], while(expr).;
append raw Calls with 0..4 arguments may occur in expressions. No call/expression statements: assign result to a local.;
append raw No arrays, address-of, strings, chars, structs, casts, ++, break, logical ops, equality ops, division or modulo.;
append raw Whitespace: ASCII <=32; NUL rejected by seed. Input is length bounded and need not have a terminator.;
append raw Generated ABI: w1..w4 arguments, w0 result; x29 preserved, stack16-aligned. Last-function entry branch.;
append raw Build ABI: x1 source, w2 bytes, x3 output, w4 byte capacity; w0 emitted bytes or ZERO on failure.;
append raw Output is raw little-endian AArch64, PC-relative internal calls/branches, no runtime helpers or fixed addresses.;
append raw Seed uses stack for parser symbols; installed/generated code survives relocation through shell install.;
append raw extra1 is an INDEPENDENT seed-dialect program using four-argument helper, named locals, loop and pointers.;
save extra2 REPRODUCTION (fresh stage031 boot, kernel unchanged). Command separator | below means a shell newline.;
append extra2 as new1 | install | build longasm | install | build extra4 | run 2 | run 5 | build extra5 | run 0 | run 3 | run 20;
append extra2 Expected decimal results: 9,12 for extra4; 17,20,37 for extra5. Then build extra3 => build error; run 20 =>37.;
append extra2 Files: new1 COMPLETE EXACT assembly seed; longasm COMPLETE C compiler; raw dialect/ABI; extra2 this manifest.;
append extra2 extra4 target A (with final LF); extra5 target B; extra3 malformed target; extra1 independent seed program.;
append extra2 All builds/executions performed inside guest. No inherited file was written; no kernel modification.;
append extra2 The installed C-built compiler parses: int NAME(int PARAM){return PARAM {(+|-) DECIMAL}*;} plus whitespace.;
append extra2 Names are case-sensitive ASCII identifiers; actual return identifier must match PARAM. Literals 0..4095.;
append extra2 Target output starts mov w0,w1, then source-directed immediate additions/subtractions, then ret.;
append extra2 Target entry receives runtime integer in w1. Results depend on both source literals/operators and runtime input.;
append extra2 Invalid syntax, wrong parameter reference, missing digits/braces, trailing junk, huge literals return zero.;
append extra2 C compiler checks capacity before writes, minimum12, clamps to8192, uses no global state or external helpers.;
append extra2 Shell build stages output and commits only on success; errors do not replace the previous runnable program.;
append extra2 RAM installed tools are not persistent: always repeat as/install/build/install after a boot.;
append extra2 Extra seed test: as new1 | install | build extra1 | install | save extra3 abc | build extra3 | run 0 =>304.;
append extra2 That result is ASCII checksum(abc)+length+3+4; restore extra3 from malformed text below before final tests.;
append extra2 Malformed saved extra3: int bad(int x){return x+;} . No self-compilation claimed or required.;
save extra3 int bad(int x){return x+;}
save extra5 int Independent(int value){return value+19-4+2;}
build extra5
run 0
run 3
run 20
build extra3
run 20
```

</details>

**← `serial_send_text`** ⚠️ error

<details><summary>result (4,706 chars, 7 lines)</summary>

```
Validation failed for tool "serial_send_text":
  - text: expected at most 4096 characters

Received arguments:
{
  "text": "save raw SEED DIALECT (new1). All source is ordinary ASCII C subset; no preprocessor, comments, globals or libraries.;\nappend raw Translation unit: 1..16 named int-returning functions; definitions before use (recursion allowed).;\nappend raw Entry is LAST function, regardless of name. Up to FOUR typed parameters, passed in w1,w2,w3,w4; return w0.;\nappend raw Types: int, char*, int*. Guest pointers are 32-bit; implicit pointer/int conversions are permitted.;\nappend raw Each function has at most 32 unique variable names INCLUDING parameters; function-wide scope, no shadowing.;\nappend raw Locals may be declared anywhere, optionally initialized; omitted initializer means zero.;\nappend raw Identifiers: case sensitive, [A-Za-z_][A-Za-z_0-9]*, maximum 31 bytes. Do not use keywords as names.;\nappend raw Decimal literals 0..65534; binary *, +, -, <, > with C precedence and left associativity; parentheses.;\nappend raw Comparisons are signed and yield 0/1. Arithmetic wraps to 32 bits. No unary minus: use (0-value).;\nappend raw Unary * reads unsigned char or int according to pointer type; p[i] reads/writes char or int (int stride4).;\nappend raw Assignment: name=expr; p[i]=expr; *p=expr;. Pointer+integer arithmetic is BYTE based: use indexing for int*.;\nappend raw Statements: blocks, declarations, assignments, return expr;, if(expr) statement [else statement], while(expr).;\nappend raw Calls with 0..4 arguments may occur in expressions. No call/expression statements: assign result to a local.;\nappend raw No arrays, address-of, strings, chars, structs, casts, ++, break, logical ops, equality ops, division or modulo.;\nappend raw Whitespace: ASCII <=32; NUL rejected by seed. Input is length bounded and need not have a terminator.;\nappend raw Generated ABI: w1..w4 arguments, w0 result; x29 preserved, stack16-aligned. Last-function entry branch.;\nappend raw Build ABI: x1 source, w2 bytes, x3 output, w4 byte capacity; w0 emitted bytes or ZERO on failure.;\nappend raw Output is raw little-endian AArch64, PC-relative internal calls/branches, no runtime helpers or fixed addresses.;\nappend raw Seed uses stack for parser symbols; installed/generated code survives relocation through shell install.;\nappend raw extra1 is an INDEPENDENT seed-dialect program using four-argument helper, named locals, loop and pointers.;\nsave extra2 REPRODUCTION (fresh stage031 boot, kernel unchanged). Command separator | below means a shell newline.;\nappend extra2 as new1 | install | build longasm | install | build extra4 | run 2 | run 5 | build extra5 | run 0 | run 3 | run 20;\nappend extra2 Expected decimal results: 9,12 for extra4; 17,20,37 for extra5. Then build extra3 => build error; run 20 =>37.;\nappend extra2 Files: new1 COMPLETE EXACT assembly seed; longasm COMPLETE C compiler; raw dialect/ABI; extra2 this manifest.;\nappend extra2 extra4 target A (with final LF); extra5 target B; extra3 malformed target; extra1 independent seed program.;\nappend extra2 All builds/executions performed inside guest. No inherited file was written; no kernel modification.;\nappend extra2 The installed C-built compiler parses: int NAME(int PARAM){return PARAM {(+|-) DECIMAL}*;} plus whitespace.;\nappend extra2 Names are case-sensitive ASCII identifiers; actual return identifier must match PARAM. Literals 0..4095.;\nappend extra2 Target output starts mov w0,w1, then source-directed immediate additions/subtractions, then ret.;\nappend extra2 Target entry receives runtime integer in w1. Results depend on both source literals/operators and runtime input.;\nappend extra2 Invalid syntax, wrong parameter reference, missing digits/braces, trailing junk, huge literals return zero.;\nappend extra2 C compiler checks capacity before writes, minimum12, clamps to8192, uses no global state or external helpers.;\nappend extra2 Shell build stages output and commits only on success; errors do not replace the previous runnable program.;\nappend extra2 RAM installed tools are not persistent: always repeat as/install/build/install after a boot.;\nappend extra2 Extra seed test: as new1 | install | build extra1 | install | save extra3 abc | build extra3 | run 0 =>304.;\nappend extra2 That result is ASCII checksum(abc)+length+3+4; restore extra3 from malformed text below before final tests.;\nappend extra2 Malformed saved extra3: int bad(int x){return x+;} . No self-compilation claimed or required.;\nsave extra3 int bad(int x){return x+;}\nsave extra5 int Independent(int value){return value+19-4+2;}\nbuild extra5\nrun 0\nrun 3\nrun 20\nbuild extra3\nrun 20\n"
}
```

</details>

#### +0:39:18

> 💭 **Splitting document lines**

**→ `serial_send_text`**

<details><summary>text (2,292 chars, 21 lines)</summary>

```
save raw SEED DIALECT (new1). Ordinary ASCII C subset; no preprocessor, comments, globals or libraries.;
append raw Translation unit: 1..16 named int-returning functions; definitions before use (recursion allowed).;
append raw Entry is LAST function, regardless of name. Up to FOUR typed parameters in w1,w2,w3,w4; return w0.;
append raw Types: int, char*, int*. Guest pointers are 32-bit; implicit pointer/int conversions are permitted.;
append raw Each function has at most 32 unique variable names INCLUDING parameters; function-wide scope, no shadowing.;
append raw Locals may be declared anywhere, optionally initialized; omitted initializer means zero.;
append raw Identifiers: case sensitive, [A-Za-z_][A-Za-z_0-9]*, maximum 31 bytes. Do not use keywords as names.;
append raw Decimal literals 0..65534; binary *, +, -, <, > with C precedence and left associativity; parentheses.;
append raw Comparisons are signed and yield 0/1. Arithmetic wraps to 32 bits. No unary minus: use (0-value).;
append raw Unary * reads unsigned char or int according to pointer type; p[i] reads/writes char or int (int stride4).;
append raw Assignment: name=expr; p[i]=expr; *p=expr;. Pointer+integer arithmetic is BYTE based: use indexing for int*.;
append raw Statements: blocks, declarations, assignments, return expr;, if(expr) statement [else statement], while(expr).;
append raw Calls with 0..4 arguments may occur in expressions. No call/expression statements: assign result to a local.;
append raw No arrays, address-of, strings, chars, structs, casts, ++, break, logical ops, equality ops, division or modulo.;
append raw Whitespace: ASCII <=32; NUL rejected by seed. Input is length bounded and need not have a terminator.;
append raw Generated ABI: w1..w4 arguments, w0 result; x29 preserved, stack16-aligned. Last-function entry branch.;
append raw Build ABI: x1 source, w2 bytes, x3 output, w4 byte capacity; w0 emitted bytes or ZERO on failure.;
append raw Output: raw little-endian AArch64, PC-relative internal calls/branches, no runtime helpers or fixed addresses.;
append raw Seed uses stack for parser symbols; installed/generated code survives relocation through shell install.;
append raw extra1: independent seed program using four-argument helper, named locals, loop and pointers.;
```

</details>

**← `serial_send_text`**

```
{"sent":2292}
```

#### +0:39:35

**→ `serial_send_text`**

<details><summary>text (2,094 chars, 26 lines)</summary>

```
save extra2 REPRODUCTION (fresh stage031 boot, kernel unchanged). Command separator | below means a shell newline.;
append extra2 as new1 | install | build longasm | install | build extra4 | run 2 | run 5;
append extra2 Then build extra5 | run 0 | run 3 | run 20. Decimal results: 9,12 for extra4; 17,20,37 for extra5.;
append extra2 Then build extra3 => build error; run 20 =>37. Prior runnable program survives rejected builds.;
append extra2 new1: COMPLETE EXACT assembly seed; longasm: COMPLETE C compiler; raw: dialect/ABI; extra2: manifest.;
append extra2 extra4: target A (with final LF); extra5: target B; extra3: malformed target; extra1: independent seed C.;
append extra2 All builds/executions performed inside guest. No inherited file was written; no kernel modification.;
append extra2 C-built compiler parses: int NAME(int PARAM){return PARAM {(+|-) DECIMAL}*;} plus whitespace.;
append extra2 Case-sensitive ASCII identifiers; return identifier must match PARAM. Decimal literals 0..4095.;
append extra2 Output: mov w0,w1; source-directed immediate additions/subtractions; ret. No code is hardwired to a name.;
append extra2 Target runtime parameter is w1. Results depend on both actual source literals/operators and runtime input.;
append extra2 Invalid syntax, wrong parameter reference, missing digits/braces, trailing junk, huge literals return zero.;
append extra2 C compiler checks capacity before writes, minimum12, clamps to8192; no global state or external helpers.;
append extra2 Shell build stages output, commits only on success. RAM installed tools are not persistent across boot.;
append extra2 Independent seed test: as new1 | install | build extra1 | install | save extra3 abc | build extra3 | run 0;
append extra2 Result304 = ASCII checksum(abc)+length+3+4; restore extra3 before final reproduction.;
append extra2 Saved malformed extra3: int bad(int x){return x+;} . No self-compilation claimed or required.;
save extra3 int bad(int x){return x+;}
save extra5 int Independent(int value){return value+19-4+2;}
build extra5
run 0
run 3
run 20
build extra3
run 20
```

</details>

**← `serial_send_text`**

```
{"sent":2094}
```

#### +0:39:50

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031310a7368656c6c3e20657869742030303030303031340a7368656c6c3e20657869742030303030303032350a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032350a7368656c6c3e20
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
shell> built
shell> exit 00000011
shell> exit 00000014
shell> exit 00000025
shell> build error
shell> exit 00000025
shell>
```

#### +0:39:54

> 💭 **Updating NUL-handling documentation**

> 💭 **Recording two test inputs**
> 💭 **Preparing malformed-source tests**

**→ `serial_send_text`**

```
recv extra3 0
build extra3
run 20
save extra3 int
build extra3
run 20
save extra3 int bad(int x){return x+4096;}
build extra3
run 20
save extra3 int bad(int x){return x+1;}junk
build extra3
run 20
save extra3 int bad(int x){return wrong+7;}
build extra3
run 20
save extra3 int bad(int x){return x+;}
```

**← `serial_send_text`**

```
{"sent":300}
```

#### +0:40:45

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
72656164790a73617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032350a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032350a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032350a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032350a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032350a7368656c6c3e2073617665640a7368656c6c3e20
```

`text`

```
ready
saved
shell> build error
shell> exit 00000025
shell> saved
shell> build error
shell> exit 00000025
shell> saved
shell> build error
shell> exit 00000025
shell> saved
shell> build error
shell> exit 00000025
shell> saved
shell> build error
shell> exit 00000025
shell> saved
shell>
```

#### +0:40:50

> 💭 **Testing compiler capacity**
> 💭 **Documenting test results**

**→ `serial_send_text`**

<details><summary>text (2,507 chars, 23 lines)</summary>

```
save raw SEED DIALECT (new1). Ordinary ASCII C subset; no preprocessor, comments, globals or libraries.;
append raw Translation unit: 1..16 named int-returning functions; definitions before use (recursion allowed).;
append raw Entry is LAST function, regardless of name. Up to FOUR typed parameters in w1,w2,w3,w4; return w0.;
append raw Types: int, char*, int*. Guest pointers are 32-bit; implicit pointer/int conversions are permitted.;
append raw Each function has at most 32 unique variable names INCLUDING parameters; function-wide scope, no shadowing.;
append raw Locals may be declared anywhere, optionally initialized; omitted initializer means zero.;
append raw Identifiers: case sensitive, [A-Za-z_][A-Za-z_0-9]*, maximum 31 bytes. Do not use keywords as names.;
append raw Decimal literals 0..65534; binary *, +, -, <, > with C precedence and left associativity; parentheses.;
append raw Comparisons are signed and yield 0/1. Arithmetic wraps to 32 bits. No unary minus: use (0-value).;
append raw Unary * reads unsigned char or int according to pointer type; p[i] reads/writes char or int (int stride4).;
append raw Assignment: name=expr; p[i]=expr; *p=expr;. Pointer+integer arithmetic is BYTE based: use indexing for int*.;
append raw Statements: blocks, declarations, assignments, return expr;, if(expr) statement [else statement], while(expr).;
append raw Calls with 0..4 arguments may occur in expressions. No call/expression statements: assign result to a local.;
append raw No arrays, address-of, strings, chars, structs, casts, ++, break, logical ops, equality ops, division or modulo.;
append raw Whitespace bytes <=32, including NUL (extension). Source is length bounded; no terminator required.;
append raw Generated ABI: w1..w4 arguments, w0 result; x29 preserved, stack16-aligned. Last-function entry branch.;
append raw Build ABI: x1 source, w2 bytes, x3 output, w4 byte capacity; w0 emitted bytes or ZERO on failure.;
append raw Output: raw little-endian AArch64, PC-relative internal calls/branches, no runtime helpers or fixed addresses.;
append raw Seed uses stack for parser symbols; installed/generated code survives relocation through shell install.;
append raw extra1: independent seed program using four-argument helper, named locals, loop and pointers.;
append extra2 Also rejected empty source, truncated int, literal4096, trailing junk and wrong return variable.;
append extra2 Each rejection was followed by run20=37, confirming prior runnable program was unchanged.;
```

</details>

**← `serial_send_text`**

```
{"sent":2507}
```

#### +0:41:22

> 💭 **Restarting for fresh repro**

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:41:40

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261104T101421.953494Z"}
```

#### +0:41:45

**→ `serial_send_text`**

```
as new1
install
build longasm
install
build extra4
run 2
run 5
build extra5
run 0
run 3
run 20
build extra3
run 20
ls
```

**← `serial_send_text`**

```
{"sent":118}
```

#### +0:41:56

**→ `serial_read`** `{"wait_ms": 100}`

**← `serial_read`**

`hex`

```
424f4f540a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030390a7368656c6c3e20657869742030303030303030630a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303031310a7368656c6c3e20657869742030303030303031340a7368656c6c3e20657869742030303030303032350a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303032350a7368656c6c3e20616c7068610a626574610a41626331323378797a3738390a656d7074790a70726f674677640a70726f674d6174680a70726f674261640a70726f67380a4673426f6f740a4673526563760a62696e0a7372630a6b65726e656c300a6b65726e656c310a436865636b0a46734669780a6e6577310a6c6f6e6761736d0a7261770a6578747261310a6578747261320a6578747261330a6578747261340a6578747261350a7368656c6c3e20
```

`text`

```
BOOT
shell> assembled
shell> installed
shell> built
shell> installed
shell> built
shell> exit 00000009
shell> exit 0000000c
shell> built
shell> exit 00000011
shell> exit 00000014
shell> exit 00000025
shell> build error
shell> exit 00000025
shell> alpha
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
new1
longasm
raw
extra1
extra2
extra3
extra4
extra5
shell>
```

#### +0:42:04

> 💭 **Confirming fresh-boot proof**
> 💭 **Confirming compiler build**

**→ `notes_write`**

<details><summary>text (7,820 chars, 50 lines)</summary>

```
STAGE032 SUCCESS: new guest-assembled C seed bootstrapped a C-written compiler, which compiled and ran further independent source. Kernel remains EXACT stage031 saved image, never patched. Only eight allowed slots were written. All 16 inherited files (alpha,beta,Abc123xyz789,empty,progFwd,progMath,progBad,prog8,FsBoot,FsRecv,bin,src,kernel0,kernel1,Check,FsFix) were left untouched. No builds/executions outside guest. Stage030 src was not needed.

FINAL EIGHT FILES:
new1 = COMPLETE EXACT ASSEMBLY SEED, assembled by guest as command. It is a general small C compiler, not a special test-compiler helper.
longasm = COMPLETE EXACT C-WRITTEN COMPILER SOURCE (alpha,digit,ws,ident,key,compile functions). Seed compiles this; install installs that C-built output.
raw = exact seed dialect / calling conventions / ABI documentation (plain text, NOT executable).
extra1 = independent C seed-dialect test program: four-argument sum helper plus make(char*s,int n,int*out,int cap). It sums source bytes in a loop, calls sum(v,n,3,4), writes executable return-constant instructions via int-pointer indexing. Separate proof of general seed functionality.
extra2 = on-disk reproduction manifest and results.
extra3 = malformed C input: int bad(int x){return x+;}
extra4 = valid input A EXACTLY int f(int x){return x+7;} followed by LF (26 bytes, received using recv).
extra5 = valid input B: int Independent(int value){return value+19-4+2;}

REPRODUCTION FROM FRESH BOOT:
as new1
install
build longasm
install
build extra4
run 2        -> 00000009 (9)
run 5        -> 0000000c (12)
build extra5
run 0        -> 00000011 (17)
run 3        -> 00000014 (20)
run 20       -> 00000025 (37)
build extra3 -> build error
run 20       -> STILL 00000025 (37)
This COMPLETE chain was repeated successfully on final fresh boot 20261104T101421.953494Z. Serial log explicitly shows assembled,installed,built,installed,built, results9/12,built,results17/20/37,build error,37. ls still lists24 files. Installed compiler/program RAM is not persistent; repeat chain after every boot. Do NOT run new1 directly as a runtime integer function: it implements build ABI and expects pointers.

ADDITIONAL OBSERVED TESTS:
- Independent seed test: as new1/install/build extra1/install; save extra4 abc/build extra4/run0 =>0x130=304, matching97+98+99+3+3+4. Demonstrates four call arguments, four entry arguments, multiple functions, locals, looping, char pointer reads, int pointer indexing writes, generated executable instructions. extra4 later restored to final input A.
- A prior add helper / triangular loop program compiled under seed: run3=6,run5=15; signed > comparisons, two-arg calls and while work.
- Seed built final-LF input A and run8=15.
- C-built compiler rejected empty extra3 (recv extra3 0), truncated int, literal4096, trailing junk after closing brace, wrong return variable, and missing literal. After EACH rejected build, run20 remained37. extra3 restored to final missing-literal test.
- Final C compiler has capacity checks before writes, minimum12, cap clamp8192; literals bounded4095 before multiplication can overflow; bounded source reads. Shell build stages output and only replaces current runnable program on successful nonzero length.

EXACT SEED DIALECT (also raw on disk):
Translation unit1..16 named int-returning function definitions, definitions before calls (recursion allowed). LAST function is entry, arbitrary name. Up to FOUR typed parameters. Types int,char*,int*. Guest pointers32-bit; implicit pointer/integer conversions allowed (needed for natural low-level compiler programming); pointer arithmetic byte-based, use p[i] for int pointer scaling4. No globals, arrays, preprocessor, comments, strings, char literals, casts, structs, address-of, division/modulo, ++, break, logical/equality operators, unary minus. Use (0-value) instead. Decimal literals0..65534. Identifiers [A-Za-z_][A-Za-z_0-9]*, case-sensitive, up to31 bytes, no keyword names (int,char,return,if,else,while). Maximum32 unique variables INCLUDING parameters per function, function-wide scope/no shadowing. Declarations anywhere, optional initializer, otherwise zero. Expressions: literals, variables, function calls0..4 args, parentheses, unary pointer *, pointer indexing, binary * > precedence +,- > precedence <,> (left associative); signed comparisons yield0/1, 32-bit wrapping arithmetic. Statements: blocks, declarations, name=expr;, p[i]=expr;, *p=expr;, return expr;, if(expr) statement [else statement], while(expr) statement. No free expression/call statements; assign helper result to local instead. Char reads unsigned. Whitespace bytes<=32 including NUL extension; length-bounded source, no terminator required. Implementation is a small permissive low-level C dialect, not an ISO C validator/type checker.

ABI / EMISSION:
Seed build entry x1 source,w2 byte length,x3 output,w4 byte capacity; returns w0 emitted bytes or0. C-written compiler uses SAME build ABI. All generated C functions: w1,w2,w3,w4 arguments, w0 result; x29 preserved, stack16-aligned. Output starts PC-relative B to last function. Named functions have256-byte stack frames, save x29/x30; locals frame based, expression temporaries16-byte aligned; relative BLs, no absolute runtime helpers. Seed preserves x19..28/x30 and puts all parser symbol/token storage in1632-byte stack workspace. No fixed data addresses in final seed. All executable templates are assembler-generated instructions plus a few .word encodings for missing assembler mnemonics. Generated/installed output stayed within shell8192-byte bounds.

C-BUILT TARGET DIALECT:
int NAME(int PARAM){return PARAM {(+|-) DECIMAL}*;} with whitespace and ASCII identifiers. PARAM reference must match actual declared name. Decimal0..4095. No multiplication, parentheses, other variables or multiple functions in this narrower target dialect. Generated code is mov w0,w1 followed by SOURCE-DIRECTED add/sub immediate instructions and ret. Thus result varies with both source and actual runtime argument. No hardwired source names or compiler-specific runtime service. Source itself is C compiled by the general seed. Self-compilation is not claimed/needed.

DEVELOPMENT CAVEATS, RESOLVED:
Earlier incomplete attempts rejected whitespace due an accidental >=32 lexer comparison and had an overlapping64-bit call-metadata stack slot plus incorrect ASR/cset constants. All fixed. Removed obsolete diagnostics and broken unused helper routines. Symbols now stack-based, not beyond installed image. Some warm as attempts immediately after in-place disk source patching reported assembly error, but fresh boots assembled exact persisted source correctly. Final source needs NO patch utility, edits or migration; final fresh-boot chain above passes. raw used to be a dangerous in-place source patch utility, but was OVERWRITTEN with plain-text dialect docs. extra1 used to be diagnostics, now independent C test. No unfinished acceptance item remains.

STAGE031 DISK FORMAT preserved: virtual1MiB, driver first0xe0000. Directory24 fixed128-byte slots at disk0. byte0 name length, u16 LE length+2, name+4. +80=a5 => external data at disk4096+slot*32768, else inherited inline entry+16. Filesmax32768, code8192. New files are slots16..23 in listed order. Exact extraction: preserve logical lengths, do not trim spaces/NULs/newlines. Guest cat adds framing newline/prompt. recv NAME N accepts raw bytes up to32768. Seed is new1 slot16, C compiler longasm slot17, docs raw18,extra1 slot19,extra2 slot20,extra3 slot21,extra4 slot22,extra5 slot23. Kernel stage031 migration format details in earlier campaign logs; no migration changes made this stage.

Final VM is to be STOPPED immediately after these notes. User-facing final should simply report files/reproduction and successful results, not claim selfhosting.
```

</details>

**← `notes_write`**

```
{"saved":true}
```

#### +0:43:20

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:43:23

Completed and verified from a fresh boot.

- Assembly seed: `new1`
- C compiler source: `longasm`
- Dialect/ABI: `raw`
- Reproduction commands: `extra2`

Bootstrap:
```text
as new1
install
build longasm
install
```

The C-built compiler compiled two independent sources, producing runtime results **9/12** and **17/20/37**. Malformed builds were rejected without replacing the previous runnable program.

Kernel and inherited files preserved. VM stopped.
