# 014 — transcript

Mechanically converted from the Pi event log by [transcript.py](../transcript.py). Summary: [014-campaign.md](014-campaign.md). Control bytes appear as Unicode control pictures (␀, ␛, …), and `$REPO` stands for the repository root.

| | |
| --- | --- |
| Model | `openai-codex/gpt-6.1-sol` |
| Start (UTC) | 2026-11-03 23:37:05 |
| Duration | 0:11:56 |
| Tool calls | 28 |
| VM boots | 2 |
| Observer messages | 0 |
| Compactions | 0 |
| Tokens (input / cached / output) | 19,760 / 10,886,272 / 23,068 |

**Tools:** `notes_write`, `notes_read`, `vm_boot_disk`, `serial_read`, `serial_send`, `serial_send_text`, `vm_stop`

**System prompt:**

```
You are the experimental agent. Use only the provided tools.

<cwd>
$REPO/.local/experiments/pi-2O5Npq/work
</cwd>
```

## Stage prompt +0:00:00

> Build the first C-subset compiler entirely inside the existing guest. The kernel is fixed and you have no image write tool. Use vm_boot_disk, write your assembler source to the named file ccsrc via shell save/append and serial input, then use as ccsrc and install. The compiler must be a real guest executable assembled by the existing guest assembler. Do not use load/loadfile to install hand-encoded compiler machine code or use any external references.
> 
> Your compiler receives one source file via the build ABI. Compile the grammar int f(int x){return EXPR;} with optional spaces. EXPR supports x (the runtime argument in w1), unsigned decimal literals 0..65535, parentheses, binary +, -, and * with normal precedence and left associativity. Emit AArch64 into the supplied output buffer and return its byte length, or zero on invalid input. Compiled functions return w0; balance their stack and preserve callee-saved registers. Constant folding is fine when correct, but x must be consumed at runtime. Use no runtime evaluation in the shell.
> 
> Demonstrate two different input values to the same compiled program, different source expressions including parentheses/precedence, and rejection of malformed source. Leave the compiler assembly source in ccsrc, save concise handoff notes, and stop the VM. Existing disk slots may all be used; if needed overwrite an old test file only after checking whether ccsrc already exists. If needed use a reserved test filename as the compiler source and report its exact name in handoff notes.

#### +0:00:00

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261103T233709.413409Z"}
```

#### +0:00:04

**→ `serial_read`** `{"wait_ms": 1000}`

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
ls
cat ccsrc
```

**← `serial_send_text`**

```
{"sent":13}
```

#### +0:00:10

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
616c7068610a626574610a41626331323378797a3738390a656d7074790a70726f674677640a70726f674d6174680a70726f674261640a70726f67380a7368656c6c3e206e6f7420666f756e640a7368656c6c3e20
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
shell> not found
shell>
```

#### +0:00:13

> 💭 **Reading previous notes**

**→ `notes_read`**

**← `notes_read`**

`text`

<details><summary>text (7,407 chars, 37 lines)</summary>

```
Stage-013 FINAL: saved8281-byte(0x2059) raw little-endian AArch64 image, entry0x40200000, QEMUvirtCortex-A53,endexclusive0x40202059. VM STOPPED. Campaign tools/artifacts only. guest_read supports ranges;guest_patch overwrites/appends. vm_boot_disk persistentdisk;vm_boot_http privateARP/HTTP(noDisk);vm_boot neither. serial_send_text accepts LF-separated commands<=4096bytes.

PUBLIC ABI / NEXT COMPILER STAGE:
run [N]: decimaluint32 N=0..4294967295,plainrun=0;argumentleading/trailingspacesallowed,no signs/hex. Badinput -> invalid argument LF withoutcall. Applicationentry0x40140000, x0=consoleputc0x402008a8, w1=N(zeroextended). SP0x40110000aligned16,4KiBdescendingstackbelow. ReturnRET,w0exit;prints exit space+exact8lowercasehexLF/prompt. Preservex19..29 andSP;nonleafsaveLR. Putc ASCIIw0 clobbersx1/x2,leavesw0/preservescallees,so saveargument/sourcepointerbeforeconsolecalls. Otherentryregsunspecified.
install: copiescurrentlyloadedcode+data,EXACTtrackedsize,to compilerentry0x40150000;cachemaintenance,publishsize,prints installed LF. Noapp ->no program LF. Currentappunchanged. load/loadfile/asm/as/buildsuccessestracksize;errorspreserveit. Compiler must be position-independent(ADR/relativebranches);copydoesnotrelocateabsoluteinternalpointers.
build NAME: filesystemlookup,theninstalledcompilercall:
 x0=consoleputc0x402008a8;
 x1=EXACTsourcebytepointer(nonNULterminated,readonlycontract),w2=sourcebytecount0..4096;
 x3=temporaryoutput0x40141000,w4=capacity2048bytes;
 alignedSP/same4KiBstack,normalx19..29/SPcallee-save,RET withw0generatedBYTElength,0=rejection.
KernelrestoresUARTx0/linebufferx8. Returns4..2048multiple4 ->transactionalCOMMIT/tracksize/ built LF. Anyotherreturn ->build error LF,PREVIOUSAPP/code/flag/sizeUNCHANGED. Partialstagingwritesokay. Compilerremainsinstalledacrossbuilds/appassemblies/loads. Itsstaticdatapersistsbetweenbuilds;resetownper-buildstate. Errorpriority:nodisk->no disk LF;missingfile->not found LF;thenabsentcompiler->no compiler LF. InstalledslotisRAM-only,bootcleared;sourcefilepersists.
Nextstage needs NOkernelchanges: writecompilerassemblyfile,as NAME;install;build SOURCE;run N. Do not run compilerwithnormalrun ABIunlessitexplicitlyhandlesnumericargumentinsteadsourcepointer. Trustedcode:noisolation/boundswriteenforcement/faultrecovery/timeouts;kernelvalidatesonlyreportedlength.

MEMORY:
Appx19=0x40140000..407ff,staging0x40141000..417ff. Loadedflagu32at0x40142000,NEWloadedsizeu32at0x40142004,bootzero. Compiler0x40150000..507ff,NEWinstalledsizeu32at0x40150800(0=none),bootzero. Separatefromapp/staging/workspace. Mode0x40145000,labels0x40146000..467ff,fixups0x40147000..48fff. Compilerpreservingcalleesprotectsx19appbase,x22diskbase,x23device,w24queueidx.

NEW CODE (offsetsfrom0x40200000):
1d78 install/run-space/build-spaceintercept;fallback14fc. Build flagw17=4/readw18=0/start6 ->B20lookup. Plainrun838->1e10(w1=0),parsedrun1e20uint32parser,1e90 commonrun(setconsole,BLRx19,tail848exit).
1ea8 bootclearsappflag/size/compilerflag,returns704. 1ebc rawloadstoresflag+w13size->820;1ec8 sharedCOMMITstoresflag+w13size->144cRET. COMMIT1400thus tracksloadfile/asm/as/build,raw81cseparately.
1ee0 installcopiesappsize,cleansDcacheevery64bytes,DSB SY/IC IALLU/DSB SY/ISB,publishesinstalledsize.
1f44 router flag4->1f54build;othersoriginal1538route. Build checkscompiler,GETFILE12d8,setargs,BLRx20(slot),w13=returnlen,restorevolatileOSstate,validatebounds/alignment,BL1400,printbuilt. 1fb8nocompiler/1fc4builderror/1fd0invalidargument. Help68bytes2015,end2059.
Patchesvsstage012:122cB1d78;838B1e10;700B1ea8;81cB1ebc;1448B1ec8;1534B1f44;730ADR2015/734len68. DraftLDRHprefixoffset4encodedas8;corrected1d98/1dec to79400901 beforeALLsuccessfultests. Final8281byteimageunchangedafterfix.

PERSISTENT COMPILER STUB progBad (assembled in guest with as):
cmp w2,1;b.ne reject;cmp w4,8;b.lt reject;ldrb w5,[x1];sub w5,w5,48;cmp w5,0;b.lt reject;cmp w5,10;b.ge reject;adr x6,words;ldr w7,[x6];lsl w5,w5,10;orr w7,w7,w5;str w7,[x3];ldr w7,[x6,4];str w7,[x3,4];mov w0,8;ret;reject:;mov w0,0;ret;words:;.word 285212704;.word 3596551104
23words/92bytes,acceptsoneASCIIdigit,emits ADDw0,w1,#digit(base11000020)+RET(d65f03c0),returns8. alpha currentlysinglebyte9;generatedrunN=(N+9)mod2^32. Reproduceafterfreshboot:as progBad;install;build alpha;run 3;run 20 ->12,29. No hostassembler used.

FINAL TESTS:
Disk20261103T233014.482642Z:installwithoutapp=noprogram,buildalpha=nocompiler,buildmissing=notfound. Savedstub/as/install;alpha7/build->built,SAMEgeneratedimage run3=10,run20=27,plainrun7. buildbeta(reject0)->builderror/run3still10. alpha9/rebuild->run3=12,run20=29. asprog8/run96thenbuild/run12provedcompilerseparate. loadfileempty(full2048byteswithreturn42attail)/install/build->builderror(return42),run42;provesloadfilefullsizecopy. OldasmprogFwd/install/build->error(return10)/run10. Rawreturn3/install,rawreturnargloaded,build->error/run11=11;return2052alsoerror/preservesapp. Rawconsoleprogramrun123->Zexit0000abcd;buildstillworks. uint32maxpassed;overflow,-1,junkrejected.
Freshdisk20261103T233323.745783Z:installnoprogram/buildnocompiler(bootreset);asprogBad/install/buildalpha,SAMEcompiledimage run3=12/run20=29;buildbetarejected/run3still12. STOPPED.
HTTP20261103T233347.284509Z:BOOT/MAC02:3e:b7:b0:1a:27/Hello, world! 456694ed412b/prompt;buildnodisk/installnoprogram;rawreturnarg run123=7b/plainrun0;installworkswithoutdisk/buildnodisk;helpupdated,echook. STOPPED.

PRESERVED ASSEMBLER/OS:
Help:help echo load run save append cat ls asm loadfile as install build LF. Inline load4..32rawbytes;loadfile4..2048rawbytes,contiguoushex/multiple4,transactional. as512four-bytewords(instructions/data),128labels,512fixups,source4096. Semicolons,standaloneNAME:,optionalspaces,commas,lowercaseforms. Labels1..12alnum/underscorecase-sensitive,4bytealigned;padXliteraldatafor8bytealignment. w/x0..30;movw/ximm16/matchingregmoves;add/subWimm12/reg,Ximm12(SPallowed);cmpWimm/reg;B/BL/B.eq/ne/lt/ge;ret;ldr/strW/X[XB/SP,byteoffset],ldrb/strbW;adrXlabel;blrX;mul/and/orrW3regs;lslW0..31;.worduint32. Wmemaligned4,max16380;Xaligned8,max32760;byte4095;[base]=0. Oldasmimplicitw0,max8words/labels. Errorsassembly error/preservepreviousapp.
GETFILE12d8:x11directoryrecord->x5dataRAM/w4u16len(clobbersx1/x2/x5/w4). COMMIT1400:w13validatedbytecount,staging->code,cachemaintenance/flag/size,RET(clobbersw1/w4/x5/x6/flags),no print. Console8a8;print6a8x5ptr/w4len/x0UART(clobbersx5/w4/w1/w2/flags/LR). Shellline0x40105000..507f128bytes,LF/noecho,overflowdrainsLFtheninvalid program.
Disk8files4096printableASCIIeach,names1..12alnum,no delete,allslotsfull. Savecreates/replaces,appendexactchunkexistingfile,savedLF;cattextLF/lsnamesLF. Directory8x128LBA0..1:byte0namelen0unused,u16len+2,name+4..15,marker80=A5,legacyinlinebootmigrated1450thenstale. Filei diskbyte0x1000+i*4096,RAM0x40121400+i*4096;whole0x9000prefixread/writteneachsave/append. Driverx22=0x40120000(desc0/avail100/used200/request300/status310/cache400..93ff),ID2init940,IOA50w1read0/write1LBA0returnsstatus. Nojournal/FLUSH/crashatomicity/corruptionvalidation/timeout/65535wrap. Oversizecheckedbeforemutation.
DiskFULL:alpha9,beta second text,Abc123xyz789oldASCIItest,empty4096hexNOP/return42,progFwdoldasm,prog8large130instr/32fixupsreturn96,progMathADRdata/stackbyteexit56,progBadcompilerstubabove. ImageSAVED,VMSTOPPED. BOOT/ARP/HTTPprivateFINframing/ACKs unchanged,existingsecurity/reliabilitylimitations.
```

</details>

#### +0:00:20

> 💭 **Designing the C parser**
> 💭 **Implementing lexical template matching**

> 💭 **Refining parser prefix matching**
> 💭 **Refining return boundary rules**

> 💭 **Refining template whitespace rules**
> 💭 **Assigning parser registers**

> 💭 **Calculating opcode constants**

> 💭 **Defining compiler helpers**

> 💭 **Designing factor parsing**
> 💭 **Implementing numeric parsing**

> 💭 **Checking parser loop exits**
> 💭 **Implementing expression loops**

> 💭 **Checking parser stack bounds**

> 💭 **Packing prefix data**

> 💭 **Checking template spacing**
> 💭 **Checking return spacing**

> 💭 **Checking compiler error cleanup**
> 💭 **Checking multiplication precedence**

> 💭 **Selecting parser depth cap**

> 💭 **Writing progBad compiler**

`ccsrc` is absent and all eight disk slots are occupied. I’ll use the reserved test file `progBad` for the compiler source and record that name in the handoff notes.

> 💭 **Writing assembly source**

> 💭 **Verifying parse template**
> 💭 **Verifying function frames**

> 💭 **Checking runtime stack handling**

> 💭 **Preparing source chunks**
> 💭 **Constructing source chunks**

**→ `serial_send_text`**

```
save progBad sub sp,sp,16;str x30,[sp];mov x9,x1;add x10,x1,x2;mov x8,x3;mov x11,x3;add x12,x3,x4;
append progBad adr x13,pool;mov w14,0;mov w15,0;bl skip;adr x6,prefix;pf:;ldrb w2,[x6];add x6,x6,1;
append progBad cmp w2,1;b.eq pend;cmp w2,0;b.eq popt;bl peek;cmp w0,w2;b.ne fail;cmp w2,32;b.eq popt;
append progBad add x9,x9,1;b pf;popt:;bl skip;b pf;pend:;bl peek;cmp w0,32;b.eq parse;cmp w0,40;b.ne fail;
append progBad parse:;bl expr;mov w2,59;bl expect;mov w2,125;bl expect;bl skip;cmp x9,x10;b.ne fail;
```

**← `serial_send_text`**

```
{"sent":509}
```

#### +0:04:13

> 💭 **Re-saving corrected main**

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell>
```

#### +0:04:32

**→ `serial_send_text`**

```
save progBad sub sp,sp,16;str x30,[sp];mov x9,x1;add w10,w1,w2;mov x8,x3;mov x11,x3;add w12,w3,w4;
append progBad adr x13,pool;mov w14,0;mov w15,0;bl skip;adr x6,prefix;pf:;ldrb w2,[x6];add x6,x6,1;
append progBad cmp w2,1;b.eq pend;cmp w2,0;b.eq popt;bl peek;cmp w0,w2;b.ne fail;cmp w2,32;b.eq popt;
append progBad add x9,x9,1;b pf;popt:;bl skip;b pf;pend:;bl peek;cmp w0,32;b.eq parse;cmp w0,40;b.ne fail;
append progBad parse:;bl expr;mov w2,59;bl expect;mov w2,125;bl expect;bl skip;cmp w9,w10;b.ne fail;
append progBad cmp w14,0;b.ne fail;ldr w0,[x13,36];bl emit;cmp w14,0;b.ne fail;sub w0,w11,w8;b finish;
append progBad fail:;mov w0,0;finish:;ldr x30,[sp];add sp,sp,16;ret;expr:;sub sp,sp,16;str x30,[sp];bl term;
append progBad eloop:;cmp w14,0;b.ne eret;bl skip;cmp w0,43;b.eq eplus;cmp w0,45;b.ne eret;mov w2,1;b egot;
append progBad eplus:;mov w2,0;egot:;str w2,[sp,8];add x9,x9,1;bl push;bl term;bl pop;ldr w2,[sp,8];
append progBad cmp w2,0;b.ne esub;ldr w0,[x13,24];b eout;esub:;ldr w0,[x13,28];eout:;bl emit;b eloop;
append progBad eret:;ldr x30,[sp];add sp,sp,16;ret;term:;sub sp,sp,16;str x30,[sp];bl factor;
append progBad tloop:;cmp w14,0;b.ne tret;bl skip;cmp w0,42;b.ne tret;add x9,x9,1;bl push;bl factor;bl pop;
append progBad ldr w0,[x13,32];bl emit;b tloop;tret:;ldr x30,[sp];add sp,sp,16;ret;
```

**← `serial_send_text`**

```
{"sent":1318}
```

#### +0:04:47

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20
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
shell>
```

#### +0:04:50

> 💭 **Implementing factor-depth checks**
> 💭 **Adding initial digit validation**

> 💭 **Testing compiled arithmetic**

**→ `serial_send_text`**

```
append progBad factor:;sub sp,sp,16;str x30,[sp];add w15,w15,1;cmp w15,65;b.ge fbad;cmp w14,0;b.ne fend;
append progBad bl skip;cmp w0,40;b.eq fparen;cmp w0,120;b.eq fx;sub w2,w0,48;cmp w2,0;b.lt fbad;
append progBad cmp w2,10;b.ge fbad;mov w3,0;nloop:;mov w4,10;mul w3,w3,w4;add w3,w3,w2;mov w4,65535;
append progBad cmp w3,w4;b.lt nok;b.eq nok;b fbad;nok:;add x9,x9,1;bl peek;sub w2,w0,48;cmp w2,0;b.lt ndone;
append progBad cmp w2,10;b.lt nloop;ndone:;lsl w3,w3,5;ldr w0,[x13,4];orr w0,w0,w3;bl emit;b fend;
append progBad fx:;add x9,x9,1;ldr w0,[x13];bl emit;b fend;fparen:;add x9,x9,1;bl expr;mov w2,41;bl expect;b fend;
append progBad fbad:;mov w14,1;fend:;sub w15,w15,1;ldr x30,[sp];add sp,sp,16;ret;
append progBad push:;sub sp,sp,16;str x30,[sp];ldr w0,[x13,8];bl emit;ldr w0,[x13,12];bl emit;b pgret;
append progBad pop:;sub sp,sp,16;str x30,[sp];ldr w0,[x13,16];bl emit;ldr w0,[x13,20];bl emit;
append progBad pgret:;ldr x30,[sp];add sp,sp,16;ret;expect:;sub sp,sp,16;str x30,[sp];bl skip;cmp w0,w2;
append progBad b.ne xbad;add x9,x9,1;b xdone;xbad:;mov w14,1;xdone:;ldr x30,[sp];add sp,sp,16;ret;
append progBad skip:;cmp w9,w10;b.ge eof;ldrb w0,[x9];cmp w0,32;b.ne sret;add x9,x9,1;b skip;sret:;ret;
append progBad peek:;cmp w9,w10;b.ge eof;ldrb w0,[x9];ret;eof:;mov w0,0;ret;
append progBad emit:;add x1,x11,4;cmp w12,w1;b.lt full;str w0,[x11];add x11,x11,4;ret;full:;mov w14,1;ret;
```

**← `serial_send_text`**

```
{"sent":1398}
```

#### +0:05:22

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20
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
shell>
```

#### +0:05:26

> 💭 **Sizing code and data**

**→ `serial_send_text`**

```
append progBad prefix:;.word 544501353;.word 2621542;.word 544501353;.word 2687096;
append progBad .word 1701970043;.word 1852994932;.word 1;
append progBad pool:;.word 704709600;.word 1384120320;.word 3506455551;.word 3103785952;
append progBad .word 3107980258;.word 2432713727;.word 184549440;.word 1258291264;
append progBad .word 453016640;.word 3596551104;
as progBad
install
save alpha int f(int x){return x;}
build alpha
run 3
run 20
```

**← `serial_send_text`**

```
{"sent":442}
```

#### +0:05:40

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e20617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030330a7368656c6c3e20657869742030303030303031340a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> assembled
shell> installed
shell> saved
shell> built
shell> exit 00000003
shell> exit 00000014
shell>
```

#### +0:05:43

> 💭 **Testing literal returns**

**→ `serial_send_text`**

```
save alpha int f(int x){return x+2*3;}
build alpha
run 3
run 20
save alpha int f(int x){return (x+2)*3;}
build alpha
run 3
run 20
save alpha int f(int x){return x-2-3;}
build alpha
run 20
save alpha int f(int x){return x*(x+1)-2*(3+x);}
build alpha
run 3
run 20
```

**← `serial_send_text`**

```
{"sent":262}
```

#### +0:05:55

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030390a7368656c6c3e20657869742030303030303031610a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030660a7368656c6c3e20657869742030303030303034320a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030660a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030300a7368656c6c3e20657869742030303030303137360a7368656c6c3e20
```

`text`

```
saved
shell> built
shell> exit 00000009
shell> exit 0000001a
shell> saved
shell> built
shell> exit 0000000f
shell> exit 00000042
shell> saved
shell> built
shell> exit 0000000f
shell> saved
shell> built
shell> exit 00000000
shell> exit 00000176
shell>
```

#### +0:05:58

> 💭 **Checking compiler output capacity**
> 💭 **Verifying emitter instruction encoding**

> 💭 **Preparing compiler handoff**
> 💭 **Testing parser error recovery**

> 💭 **Checking parser edge cases**

> 💭 **Verifying compiler register invariants**

**→ `serial_send_text`**

```
save alpha   int   f ( int   x ) { return((x + 1) * (x - 1)) ; }  
build alpha
run 3
run 20
save alpha int f(int x){return 65535;}
build alpha
run 123
save alpha int f(int x){return x+;}
build alpha
run 20
save alpha int f(int x){return (x+2;}
build alpha
run 20
save alpha int f(int x){return 65536;}
build alpha
run 20
save alpha int f(int x){returnx;}
build alpha
run 20
save alpha int g(int x){return x;}
build alpha
run 20
save alpha int f(int x){return x;}junk
build alpha
run 20
```

**← `serial_send_text`**

```
{"sent":486}
```

#### +0:07:00

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030380a7368656c6c3e20657869742030303030303138660a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030666666660a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030666666660a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030666666660a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030666666660a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030666666660a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030666666660a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030666666660a7368656c6c3e20
```

`text`

```
saved
shell> built
shell> exit 00000008
shell> exit 0000018f
shell> saved
shell> built
shell> exit 0000ffff
shell> saved
shell> build error
shell> exit 0000ffff
shell> saved
shell> build error
shell> exit 0000ffff
shell> saved
shell> build error
shell> exit 0000ffff
shell> saved
shell> build error
shell> exit 0000ffff
shell> saved
shell> build error
shell> exit 0000ffff
shell> saved
shell> build error
shell> exit 0000ffff
shell>
```

#### +0:07:03

> 💭 **Verifying compiled arithmetic**
> 💭 **Checking source line lengths**

> 💭 **Preparing example C files**
> 💭 **Writing alpha test case**

> 💭 **Testing valid compiler builds**

**→ `serial_send_text`**

```
save alpha int f(int x){return (x+2)*3;}
build alpha
run 3
run 20
build beta
run 3
```

**← `serial_send_text`**

```
{"sent":83}
```

#### +0:08:05

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030660a7368656c6c3e20657869742030303030303034320a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030660a7368656c6c3e20
```

`text`

```
saved
shell> built
shell> exit 0000000f
shell> exit 00000042
shell> build error
shell> exit 0000000f
shell>
```

#### +0:08:11

> 💭 **Preparing a fresh boot**

> 💭 **Validates compiler behavior**

> 💭 **Verified kernel size fields**

**→ `serial_send_text`**

```
save alpha int f(int x){return x
append alpha +1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1
append alpha +1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1
append alpha +1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1
append alpha +1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1
append alpha ;}
build alpha
run 3
save alpha int f(int x){return (x+2)*3;}
build alpha
run 3
run 20
```

**← `serial_send_text`**

```
{"sent":445}
```

#### +0:08:58

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
73617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e2073617665640a7368656c6c3e206275696c64206572726f720a7368656c6c3e20657869742030303030303030660a7368656c6c3e2073617665640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030660a7368656c6c3e20657869742030303030303034320a7368656c6c3e20
```

`text`

```
saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> saved
shell> build error
shell> exit 0000000f
shell> saved
shell> built
shell> exit 0000000f
shell> exit 00000042
shell>
```

#### +0:09:01

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:09:06

**→ `vm_boot_disk`**

**← `vm_boot_disk`**

```
{"run_id":"20261103T234615.128435Z"}
```

#### +0:09:10

**→ `serial_read`** `{"wait_ms": 1000}`

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

#### +0:09:13

**→ `serial_send_text`**

```
as progBad
install
build alpha
run 3
run 20
```

**← `serial_send_text`**

```
{"sent":44}
```

#### +0:09:16

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
617373656d626c65640a7368656c6c3e20696e7374616c6c65640a7368656c6c3e206275696c740a7368656c6c3e20657869742030303030303030660a7368656c6c3e20657869742030303030303034320a7368656c6c3e20
```

`text`

```
assembled
shell> installed
shell> built
shell> exit 0000000f
shell> exit 00000042
shell>
```

#### +0:09:19

> 💭 **Stopping before writing notes**

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:09:27

> 💭 **Estimating source byte count**
> 💭 **Checking binary code size**

> 💭 **Validating kernel build**

> 💭 **Verifying parser semantics**
> 💭 **Confirming source persistence**

> 💭 **Checking compiler codegen**
> 💭 **Checking pool immutability**

> 💭 **Preparing handoff notes**

**→ `notes_write`**

<details><summary>text (7,357 chars, 44 lines)</summary>

```
Stage-014 FINAL: first real C-subset compiler is now guest assembly on the persistent disk. Kernel image is FIXED/UNCHANGED from stage013 (8281bytes,entry0x40200000). No image writes, host assembler, external references, load/loadfile, or hand-encoded compiler installation used. Only shell save/append, guest as, install, build and run. VM STOPPED.

IMPORTANT SOURCE FILENAME EXCEPTION:
Compiler assembly source is EXACTLY progBad (case-sensitive), NOT ccsrc. At start ls showed all8slots occupied; cat ccsrc returned not found. Kernel has no delete/rename and store is full, so used the user's permitted reserved-test-filename fallback, overwriting old progBad compiler stub. progBad now contains the complete new compiler assembly (~2.6KiB,under4096); it assembles within2048bytes. No kernel modifications needed. Other than progBad, only alpha test input was overwritten.

REPRODUCE AFTER FRESH BOOT:
vm_boot_disk; serial_send_text:
 as progBad
 install
 build alpha
 run 3
 run 20
Expected assembled/installed/built, exit0000000f and exit00000042. alpha persists as int f(int x){return (x+2)*3;}. Installed compiler/app are RAM-only and must be re-created afterboot; assembly/source files persist.

LANGUAGE:
Exact function grammar int f(int x){return EXPR;} with optionalASCIIspaces at token boundaries and around operators/parentheses/punctuation. Mandatory separation between int andf/int andx. return(x) allowed, returnx rejected. Leading/trailingspaces allowed. EXPR: x runtimeargument, unsigneddecimal literals0..65535 (leadingzerosokay), parentheses, binary+,-,*; normalprecedence,*above+/-;leftassociative. No unaryoperators,otheridentifiers/functions/comments/hex/suffixes/additionalstatements. Requiressemicolon,closingbrace,thenonlyspaces/EOF. Native32-bitW arithmetic (wraps modulo2^32);negative results displayed as hex bykernel. x ALWAYSconsumed atRUNTIME fromw1,not substituted bycompiler/shell. No runtime expressioninterpreter.
Compiler returns generated bytecount on success, zero on syntax/literal/resourceerror. Outputcapacity checked beforeeveryword;partialoutputonfailureallowed, kernel keepspreviousapp. Compiler factor-depthlimit64 avoids4KiBcompilerstackoverflow;generatedprogramsboundedbyoutputcapacity2048bytes. Repeatedinvalidbuilds followedbyvalidbuild verified noSP/global-stateleaks.

IMPLEMENTATION (all in progBad):
Recursive-descent expr -> term ((+|-) term)*, term -> factor (* factor)*, factor -> x | decimal | (expr). Code emitted as parsing happens, no AST or constantfolding. Every binary operator emits native runtime stackcode: pushLHS, compileRHS, popLHS intow2, operatew0=w2 OPw0. Thus precedence/leftassociativity andnestedparentheses preserved. Generatedcode onlywritesw0/w2 andSP,readsw1,neverchangescallee-savedregs orLR;all runtimepush/popframes16bytes andbalanced,thenRET.
Compiler itself onlyusescaller-savedregsx0..18, savesLR in16byteframes inall nonleafroutines,balancesSPoneverypath,preservesx19..29/kernelglobals. No consolecalls; x0consolepointer ignored. Globalregisters: x8outputbase,x9sourcecursor,x10sourceend,x11outputcursor,x12outputend,x13opcodepool,w14stickyerror,w15factordepth. w2/w3/w4temporaries; mainprefixusesx6templatepointer. Pointer addition/comparison useslowWregisters whereXregisterarith/CMPunsupported; safe becauseall ABI RAM pointersarepositive<0x80000000. InputpointerendcheckedbeforeLDRB.
Main entry resetsglobals/error/depth, matchesprefix, calls expr, expects ; and }, requiresEOF, emitsRET, returnsoutcursor-base or0. Labelpf walks packedprefixdata;0templatebyte=skipoptionalspaces,32=requiredspace/skiprest,1=end. Prefixbytes: int f\0(\0int x\0)\0{\0return\1. Literalkeywordcharactersmatchedexactly,no spacesinsidekeywords. Afterreturn requiresSPACEor'(',preventingreturnx/return123.
Labels expr/eloop/eplus/egot/esub/eout/eret implementadditiveleftloop;op0ADD/1SUB saved atcompilerSP+8 acrossrecursivecall. term/tloop/tret implementmultiplication. factor/fx/fparen/fbad/fend implementprimaries,depthbalanced. nloop/nok/ndone checkeddecimalparse,valuealways<=65535 beforemultiply-by10,so nooverflowwrap. push/pop/pgret emitruntimepush/poppairs. expect/xbad/xdone checksonepunctuationafterspaces. skip/sret andpeek/eof boundsafehelpers returnw0charor0. emit checkscandidateout+4<=end,setserroriffull,elseSTRword/advance. fail/finish maincleanexit.
Codepoolx13 offsets (actualAArch64 words, emitted bycompiler as output, NOT hand-loaded compiler):
+0 704709600 = MOVw0,w1 (2a0103e0)
+4 1384120320 = MOVZw0,#0 base52800000;literalOR(imm<<5)
+8 3506455551 = SUBSP,SP,#16 d10043ff
+12 3103785952 = STRw0,[SP] b90003e0
+16 3107980258 = LDRw2,[SP] b94003e2
+20 2432713727 = ADDSP,SP,#16 910043ff
+24 184549440 = ADDw0,w2,w0 0b000040
+28 1258291264 = SUBw0,w2,w0 4b000040
+32 453016640 = MULw0,w2,w0 1b007c40
+36 3596551104 = RET d65f03c0.
Prefixdata packed7words544501353,2621542,544501353,2687096,1701970043,1852994932,1. Both tables are assembler.worddata, addressed withADR, so compilerrelocatescorrectlyfromappslottoinstalledslot.

VERIFIED IN LIVE GUEST:
Diskrun20261103T233709.413409Z: wrote progBad via save/append, as progBad ->assembled,install->installed. buildintfreturnx,run3=3/run20=20(SAME compiledimage). x+2*3 ->9/26. (x+2)*3 ->15/66. x-2-3 with20 ->15(leftassociative). x*(x+1)-2*(3+x) ->0/374 with3/20. Spaced int f declaration and return((x+1)*(x-1)) ->8/399. Literal65535 ->ffff. Everybuilduses actual installedguestcompiler and run executes emittedAArch64.
Malformed x+,unclosedparen,65536,returnx,wrongfunctiong,trailingjunk all ->build error;runstillffff frompriorvalidapp. Rejectedbeta(second text) retainspriorprogram. A validexpressionwith128+1operators exceeded2048outputcap ->build error,previous(x+2)*3 stillreturned15. Restoringvalidsource/rebuildingstill15/66.
STOP thenFRESHBOOT20261103T234615.128435Z: as progBad/install/build alpha ->assembled/installed/built;run3=0000000f,run20=00000042,provingcompiler/sourcepersistencewithoutkernelchangesorrawload. vm_stop completedafterchecks. VMSTOPPED.

FIXED OS ABI / RESOURCES FOR NEXT STAGE:
run N:uint32decimalruntimearg(default0),entry0x40140000 x0=putc0x402008a8,w1=N,SP0x40110000aligned16,4KiBbelow;RET w0exit;preserve19..29/SP,saveLRwhenBL. putcASCIIw0clobbersx1/x2. install copiestrackedloadedsizeinto0x40150000..507ff,installedsize0x40150800(bootzero),PICrequired. build NAME callscompiler x0putc,x1exactsourceptr,w2len,x3output0x40141000,w4cap2048;RET w0length4..2048multiple4 or0reject;kernelpublishestransactionallyandprints built/build error. Source nonNULterminated/read-onlycontract. Loadedflag0x40142000,size42004. Kernelcompiler/appmemorytrusted,noisolation/timeouts/faultrecovery.
Guestas source4096,max512words/128labels/512fixups;supportsall stage012formsincludingSPframes/LDRSTR/ADR/BLR/MUL/AND/ORR/LSL/.word;oldasmimplicitw0still8words. All instructions/datawordaligned;Xliteralalignmentmustbe8whenusingLDRX. Source/programsheldinfixed8filestore(no delete);names1..12alnum,file4096ASCII,commandlines128. save replaces,append exactchunk. Whole0x9000diskprefixpersisted;directoryLBA0..1(8x128records namelenbyte0/u16len+2/name+4/marker80=A5);filei fixeddataLBA8+8i (4096bytes),RAM0x40121400+i*4096. SourceprogBadindex6;alphaindex0. Otherfiles beta,Abc123xyz789,empty,progFwd,progMath,prog8 unchanged. Kernel8281bytesleftuntouched;handoffsourceisprogBad,sampleCisalpha,VMSTOPPED.
```

</details>

**← `notes_write`**

```
{"saved":true}
```

#### +0:11:44

> 💭 **Compiler tests completed**

Built the compiler entirely in guest assembly, stored in reserved file `progBad` because `ccsrc` was absent and the disk was full.

Verified runtime inputs, precedence, parentheses, left associativity, and malformed-source rejection. `(x+2)*3` returned 15 and 66 for inputs 3 and 20.

Kernel unchanged. Handoff notes saved; VM stopped.
