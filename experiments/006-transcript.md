# 006 — transcript

Mechanically converted from the Pi event log by [transcript.py](../transcript.py). Summary: [006-campaign.md](006-campaign.md). Control bytes appear as Unicode control pictures (␀, ␛, …), and `$REPO` stands for the repository root.

| | |
| --- | --- |
| Model | `openai-codex/gpt-6.1-sol` |
| Start (UTC) | 2026-11-03 21:57:11 |
| Duration | 0:03:03 |
| Tool calls | 18 |
| VM boots | 2 |
| Observer messages | 0 |
| Compactions | 0 |
| Tokens (input / cached / output) | 20,002 / 968,320 / 7,124 |

**Tools:** `guest_write`, `guest_read`, `notes_write`, `notes_read`, `vm_boot`, `serial_read`, `vm_stop`, `serial_send`, `vm_boot_http`

**System prompt:**

```
You are the experimental agent. Use only the provided tools.

<cwd>
$REPO/.local/experiments/pi-2O5Npq/work
</cwd>
```

## Stage prompt +0:00:00

> Extend your saved stage-005 AArch64 machine-code image into a small serial shell. Read the current image and handoff notes. Preserve BOOT and the existing HTTP fetch on a network boot. After boot (and after the fetch when a NIC is present), show the prompt "shell&gt; " and repeatedly accept lines terminated by LF. Implement these commands:
> - help: output "help echo\n"
> - echo followed by a space and arbitrary text: output the text followed by LF
> - any unrecognized command: output "unknown command\n"
> After each command show the prompt again. Raw input echo is optional. Bound your line buffer and recover to the next prompt after an overlong line. Test multiple commands in one live VM and test the HTTP-boot path. Keep the updated image, leave handoff notes about entry points and line buffer layout, and stop the VM. Use only your campaign artifacts and provided tools; no external references.

#### +0:00:00

**→ `guest_read`**

**→ `notes_read`**

**← `guest_read`**

<details><summary>result (2,944 chars, 1 lines)</summary>

```
{"hex":"0020a1d241088052010000b9e1098052010000b9e1098052010000b9810a8052010000b941018052010000b908000014011840b9e1ff2737010040b9021840b9e2ff2f37010000b9faffff170340a1d204048052610840b93f040071c0000054630008918404007161ffff54f1ffff171f2003d57f7000b961008052617000b921008052612400b9612000b97f2400b97f2000b961018052617000b90a02a8d2e5030aaa04c08052bf8400f884040071c1ffff544b0920916c0540914b0100f901008152410900b9410080524119007921008052410502794c0102f9c1068052410904b92100805241050a79850900108631009144058052a1144038c114003884040071a1ffff5404008052e5030aaaa6000491a7000891643000b921008052613800b9658000b97f8400b9669000b97f9400b967a000b97fa400b9614400b984040011a50010919f08007121feff54e1018052617000b9bf3f03d57f5000b921008052615000b941054479e1ffff34bf3f03d56131407902c180523f00026bc1030054614140793f0008716103005465890091c4008052a6144038c17c04533f28007163000054219c00111f2003d521c00011021840b9e2ff2f37010000b9c10c00123f28007163000054219c00111f2003d521c00011021840b9e2ff2f37010000b9840400714001005441078052010000b9e9ffff17410542792104001141050279bf3f03d57f5000b9d7ffff1741018052010000b90c000014ffffffffffff525400123456080600010800060400015254001234560a00020f0000000000000a00020200003400805235008052c50f001086310091c4068052a1144038c114003884040071a1ffff546589009186310091c4008052a1144038c114003884040071a1ffff54187d80521900805296028052570080522a0000944d000094b90540b9390bc05a3907001118070011170280522300009472000014012e8d52c1edac72a10000b941018052a110003936038052170380521a0000943d000094643940798404c05a84500051a1314039217c045321741e538400016b0dffff54a501018bb90540b9390bc05a3903040be603042aa1144038021840b9e2ff2f37010000b9c604007161ffff54181700119602805217028052020000943dffff17fc031eaa41054c793f00156bc1ffff54c15200112104c05a813900799f4900798eb90091010bc05ac10500b9210bc05ac10900b9d7350039df2100798569009144018052060080522200009481490079e5030eaac4060011847c0153e6028352c600160b1b000094c1210079c1ba0011410904b9b506001155050a79bf3f03d521008052615000b9fe031caac0035fd69406001154050279bf3f03d57f5000b9410544793f00146bc1ffff54bf3f03d5613140793f200071c1feff54618d40393f18007161feff546db90091c0035fd6a22440784204c05ac600020b8404007181ffff54c27c1053c63c0012c600020bc27c1053c63c0012c600020be103262a2104c05ac0035fd600000000000052540012345608004500002800004000400600000a00020f0a0002029c401f90000003e800000000500210000000000000002509001086090191e4028052a1144038c114003884040071a1ffff547605805217038052a7ffff97185f00115a0d4091fb031aaa13008052c6ffff97a10540b92108c05a3f00196be1020054643940798404c05a84500051a1314039217c045321741e538400016b8bfeff54a501018b3903040bc4000034a11440386117003884040071a1ffff541f2003d5a1354039a100003639070011330080521f2003d51f2003d5960280521702805285ffff9753fcff3441054c793f00156bc1ffff54e5031aaa06008052bf001beba2020054a1144038c65c1853c600012a42a1815242a1a172df00026b01ffff54bf001bebc2000054a1144038021840b9e2ff2f37010000b9faffff173f28007120d5ff5441018052021840b9e2ff2f37010000b9a4feff17474554202f68656c6c6f20485454502f312e300d0a0d0a"}
```

</details>

**← `notes_read`**

`text`

<details><summary>text (6,319 chars, 24 lines)</summary>

```
Stage-005 FINAL saved image:1467 bytes (0x5bb), raw little-endian AArch64, entry0x40200000, QEMU virt Cortex-A53. VM STOPPED. Use vm_boot_http; vm_boot_tcp/network unavailable. No OS/stack, external references, assembler or binaries used.
Behavior: BOOT LF unchanged; broadcast ARP for10.0.2.2 from guest10.0.2.15 MAC52:54:00:12:34:56; prints live peer sender MAC lowercase colon hex LF. TCP connection from port40000 to10.0.2.2:8080, SYN seq1000; handshake then ONE PSH|ACK segment containing exact23bytes GET /hello HTTP/1.0 CR LF CR LF. Accumulates in-order actual HTTP response payload, ACKs payload and FIN, waits final ACK's TX used completion, scans CRLFCRLF boundary, prints only body (adds LF only if body doesn't end LF), returns to PL011 polling echo. Two final boots gave different bodies and MACs.
Common stage004 machinery retained:
First44bytes produce BOOT LF, x0=PL0110x09000000. +0x2c branches+0x4c. Echo+0x30..0x48 polls UARTFR+0x18 RXFEbit4/TXFFbit5 and echoesDR. No NIC scan match returns echo.
Virtio MMIO: scan32slots base0x0a000000 stride0x200 DeviceID=1. Reset, status3, negotiate only VERSION_1 via high features1 low0; status11, no FEATURES_OK readback. Queue0RX/1TX split queues, QueueNum1 each, QueueReady1; status15; notify. DMB SY around publication/completion.
Clear RAM0x40100000..0x40102fff. RX desc0x40100000 avail0x40100100 used0x40100200; TX desc0x40100400 avail0x40100500 used0x40100600. Queue/descriptor high address halves0, availring[0]=0, idx starts1. RX desc len2048 flagsWRITE2, TX flags0 and dynamic len. x10=0x40100000, x11 RXbuffer0x40100802, x12 TXbuffer0x40101802. IMPORTANT: buffer offsets2mod4 put IP/TCP32-bit fields on aligned addresses after12-byte virtioheader+14-byteEthernet. MMU-off unaligned32-bit accesses faulted in stage004, so preserve this buffer layout. Buffers don't overlap each other/rings.
Stage004 code map retained:
+0x4c scan; +0x74 reset/features; +0x9c clear; +0xbc descriptors; +0xec copy ARP literal; +0x108 queue config; +0x150 DRIVER_OK/notify; +0x168 firstARP receive, checks EtherType0806/opcode2; +0x190..214 MAC formatting/LF. +0x218 branches+0x248. ARPliteral42bytes at+0x21c..245 then2zero alignment bytes.
+0x248 initializes w20 RXavail and w21 TXavail=1. Copy54-byte Ethernet/IP/TCP template at+0x448 toTX+12, then copy six peer MAC bytes fromARP RX+34 toTX+12. w24 seq1000,w25ack0,w22TCPlen20,w23flagsSYN2; send, receiveSYNACK, w25=peerseq+1,w24=1001, flagsACK16,send. +0x2b8 NOW branches+0x480 (word14000072); old stage004 ping/response code+0x2bc..33c remains SAVED BUT UNREACHABLE.
+0x340 send routine savesLRx28, waits previousTXused.idx=w21, patchesIPtotal and TCPseq/ack/flags, computes both checksums, descriptorlen=46+TCPlen, incrementsw21/TXavail, notifies, restoresLR/returns+0x3cc.
+0x3d0 receive incrementsw20/RXavail, notifies, waitsRXused.idx=w20. Filters EtherType0800/IPprotocol6, reposts others; returnsx13=RX+46 (TCP header), +0x40cRET.
+0x410 checksum: pointerx5,w4halfwordcount,w6initialsum; read16bits REV16 add, fold twice, complement thenREV16w1 forSTRH. IPsum0 count10; TCPpseudo sum0x1817+TCPlen (fixedIPs/protocol6), countceil(TCPlen/2). Zeroed padding byte after odd request provides odd checksum padding. TCPchecksum+16, IPchecksum+10. +0x448template54bytes, TCPdst NOW1f90(8080) instead of0913(2323); IPv4header20bytes, TTL64, DF, TCPdataoffset5 window4096. +0x47e two alignment zeros.
New HTTP code map:
+0x480 ADRx5 request at+0x5a4, copy23bytes toTX+66; TCP length43 flagsPSHACK24; BLsend+0x4a4; own seq+=23 =>1024.
+0x4ac x26=0x40103000 accumulation start (not precleared, every stored byte initialized); x27current write pointer; w19FINseen0.
+0x4b8 BLreceive. LoadreceivedTCPseq to w1, REV w1,w1 at+0x4c0 (word5ac00821!), comparew25 expected. Mismatching sequence skips consumption and sends current ACK+0x524. Matching segment: IPtotal-20-TCPdataoffset*4 yields payloadlen; negative drops/reposts. Addlen tow25; copy bytes fromRX TCP+headerlen to[x27++] bytewise. +0x50c readTCPflags bit0; ifFIN incrementackw25 by1, setw19=1. +0x524 setTCPlen20flagsACK, send. +0x530 loop+0x4b8 unlessFINseen. Handles separate segments, pureACK, separateFIN or combinedpayloadFIN; no retransmission timer.
+0x534 waitTXused=w21 for finalACKcompletion. +0x540 startscan atx26 withrolling32-bit CRLFCRLF matcher0x0d0a0d0a, boundedbyx27. +0x56c bodyprint untilx27 withUARTTXFFpolling. +0x588 iflastbyteLF goecho, else appendLFthen echo. +0x5a4literal23bytes:474554202f68656c6c6f20485454502f312e300d0a0d0a. End+0x5bb.
Registers: x0UART,x3NIC,x10scratch,x11RX,x12TX,x13RX TCP,x14TX TCP,w20/w21queuecounts,w22TCPlen,w23flags,w24seq,w25ack,x28savedLR; neww19FINseen,x26responsebase,x27responseend. Lowregs scratch.
HTTP framing: this HTTP/1.0 origin closes withFIN. Accumulation throughFIN gives response length; CRLFCRLF split extractsbody. Does NOT parse Content-Length numerically; origin's actual body length was27 in diagnostics and no bytes beyondbody were present. Not a general keepalive/chunked client. No boundcheck on responseaccumulation (expectedshortresponse), receivedchecksum validation, IPfragment handling, tuplefilter, outboundFIN/close handshake, or timeout/retransmit. Sequence mismatch causes duplicateACK but no out-of-order buffer. InitialARP non-ARP repost path inheritedfromstage003 has weak usedidx handling; expectedlink immediately repliesARP. Small queue indices not wrap-safe. Hardening required before general traffic.
Iteration: firstHTTP draft completed handshake/request but never consumeddata. TemporaryT/R diagnostics then actualIPdatagram serialdump showed host returned validHTTP200 includingpayload+FIN(flags0x19). Fault: +0x4c0 mistakenly REVw1,w25 rather thanREVw1,w1, causingexpectedsequence comparison alwaysfail. Correctedto5ac00821, removed ALLdiagnosticcode/output. No other changes after successful finaltests.
Two unchanged FINALimage tests:
run_id20261103T215354.883880Z: BOOT\n02:c4:d8:f6:95:ba\nHello, world! b9599fa89536\n. Sent417a, read417a(Az). vm_stop completed.
run_id20261103T215405.459172Z: BOOT\n02:fb:20:3a:11:c3\nHello, world! 9dc91081bd3c\n. Sent4279, read4279(By). vm_stop completed.
Live differentorigin bodies, noHTTPheaders onfinalserial. Code ACKs payload+FIN beforebodyprinting and waitsTXcompletion. Updated1467-byte image remains saved; VMstopped.
```

</details>

#### +0:00:03

> 💭 **Preparing shell branch patch**
> 💭 **Patching shell input loop**

> 💭 **Tracing the help branch**

> 💭 **Calculating ADR encodings**
> 💭 **Verifying branch encodings**

> 💭 **Appending the huge image**

**→ `guest_write`**

<details><summary>hex (4,106 chars, 1 lines)</summary>

```
0020a1d2 41088052 010000b9 e1098052 010000b9 e1098052 010000b9 810a8052 010000b9 41018052 010000b9 08000014 63010014 e1ff2737 010040b9 021840b9 e2ff2f37 010000b9 faffff17 0340a1d2 04048052 610840b9 3f040071 c0000054 63000891 84040071 61ffff54 f1ffff17 1f2003d5 7f7000b9 61008052 617000b9 21008052 612400b9 612000b9 7f2400b9 7f2000b9 61018052 617000b9 0a02a8d2 e5030aaa 04c08052 bf8400f8 84040071 c1ffff54 4b092091 6c054091 4b0100f9 01008152 410900b9 41008052 41190079 21008052 41050279 4c0102f9 c1068052 410904b9 21008052 41050a79 85090010 86310091 44058052 a1144038 c1140038 84040071 a1ffff54 04008052 e5030aaa a6000491 a7000891 643000b9 21008052 613800b9 658000b9 7f8400b9 669000b9 7f9400b9 67a000b9 7fa400b9 614400b9 84040011 a5001091 9f080071 21feff54 e1018052 617000b9 bf3f03d5 7f5000b9 21008052 615000b9 41054479 e1ffff34 bf3f03d5 61314079 02c18052 3f00026b c1030054 61414079 3f000871 61030054 65890091 c4008052 a6144038 c17c0453 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 c10c0012 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 84040071 40010054 41078052 010000b9 e9ffff17 41054279 21040011 41050279 bf3f03d5 7f5000b9 d7ffff17 41018052 010000b9 0c000014 ff ff ff ff ff ff 52 54 00 12 34 56 08 06 00 01 08 00 06 04 00 01 52 54 00 12 34 56 0a 00 02 0f 00 00 00 00 00 00 0a 00 02 02 00 00 34008052 35008052 c50f0010 86310091 c4068052 a1144038 c1140038 84040071 a1ffff54 65890091 86310091 c4008052 a1144038 c1140038 84040071 a1ffff54 187d8052 19008052 96028052 57008052 2a000094 4d000094 b90540b9 390bc05a 39070011 18070011 17028052 23000094 72000014 012e8d52 c1edac72 a10000b9 41018052 a1100039 36038052 17038052 1a000094 3d000094 64394079 8404c05a 84500051 a1314039 217c0453 21741e53 8400016b 0dffff54 a501018b b90540b9 390bc05a 3903040b e603042a a1144038 021840b9 e2ff2f37 010000b9 c6040071 61ffff54 18170011 96028052 17028052 02000094 3dffff17 fc031eaa 41054c79 3f00156b c1ffff54 c1520011 2104c05a 81390079 9f490079 8eb90091 010bc05a c10500b9 210bc05a c10900b9 d7350039 df210079 85690091 44018052 06008052 22000094 81490079 e5030eaa c4060011 847c0153 e6028352 c600160b 1b000094 c1210079 c1ba0011 410904b9 b5060011 55050a79 bf3f03d5 21008052 615000b9 fe031caa c0035fd6 94060011 54050279 bf3f03d5 7f5000b9 41054479 3f00146b c1ffff54 bf3f03d5 61314079 3f200071 c1feff54 618d4039 3f180071 61feff54 6db90091 c0035fd6 a2244078 4204c05a c600020b 84040071 81ffff54 c27c1053 c63c0012 c600020b c27c1053 c63c0012 c600020b e103262a 2104c05a c0035fd6 00 00 00 00 00 00 52 54 00 12 34 56 08 00 45 00 00 28 00 00 40 00 40 06 00 00 0a 00 02 0f 0a 00 02 02 9c 40 1f 90 00 00 03 e8 00 00 00 00 50 02 10 00 00 00 00 00 00 00 25090010 86090191 e4028052 a1144038 c1140038 84040071 a1ffff54 76058052 17038052 a7ffff97 185f0011 5a0d4091 fb031aaa 13008052 c6ffff97 a10540b9 2108c05a 3f00196b e1020054 64394079 8404c05a 84500051 a1314039 217c0453 21741e53 8400016b 8bfeff54 a501018b 3903040b c4000034 a1144038 61170038 84040071 a1ffff54 1f2003d5 a1354039 a1000036 39070011 33008052 1f2003d5 1f2003d5 96028052 17028052 85ffff97 53fcff34 41054c79 3f00156b c1ffff54 e5031aaa 06008052 bf001beb a2020054 a1144038 c65c1853 c600012a 42a18152 42a1a172 df00026b 01ffff54 bf001beb c2000054 a1144038 021840b9 e2ff2f37 010000b9 faffff17 3f280071 20d5ff54 41018052 021840b9 e2ff2f37 010000b9 a4feff17 47 45 54 20 2f 68 65 6c 6c 6f 20 48 54 54 50 2f 31 2e 30 0d 0a 0d 0a 00 0802a8d2 08154091 45080010 e4008052 37000094 07008052 09008052 011840b9 e1ff2737 010040b9 211c0012 3f280071 a0010054 49ffff35 ff000271 e2000054 0601078b c1000039 e7040011 f4ffff17 1f2003d5 1f2003d5 29008052 f0ffff17 1f2003d5 a9030035 ff100071 21010054 010140b9 02ad8c52 820dae72 3f00026b c1020054 85040070 44018052 16000014 ff140071 23020054 010140b9 a26c8c52 02edad72 3f00026b 81010054 01114039 3f800071 21010054 05150091 e4140051 0b000094 41018052 021840b9 e2ff2f37 010000b9 cdffff17 45020030 04028052 1f2003d5 02000094 c8ffff17 04010034 a1144038 021840b9 e2ff2f37 010000b9 84040071 61ffff54 1f2003d5 c0035fd6 73 68 65 6c 6c 3e 20 68 65 6c 70 20 65 63 68 6f 0a 75 6e 6b 6e 6f 77 6e 20 63 6f 6d 6d 61 6e 64 0a
```

</details>

**← `guest_write`**

```
{"bytes":1773}
```

#### +0:01:22

> 💭 **Checking instruction encodings**

**→ `vm_boot`**

**← `vm_boot`**

```
{"run_id":"20261103T215840.834691Z"}
```

#### +0:01:28

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

#### +0:01:30

**→ `serial_send`** `{"hex": "68656c700a6563686f2068656c6c6f20776f726c640a6e6f70650a6563686f200a"}`

**← `serial_send`**

```
{"sent":33}
```

#### +0:01:33

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
68656c70206563686f0a7368656c6c3e2068656c6c6f20776f726c640a7368656c6c3e20756e6b6e6f776e20636f6d6d616e640a7368656c6c3e200a7368656c6c3e20
```

`text`

```
help echo
shell> hello world
shell> unknown command
shell> 
shell>
```

#### +0:01:35

> 💭 **Preparing overflow input**
> 💭 **Preparing overflow payload**

**→ `serial_send`**

```
4142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f
```

**← `serial_send`**

```
{"sent":63}
```

#### +0:01:48

**→ `serial_send`**

```
4142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f
```

**← `serial_send`**

```
{"sent":63}
```

#### +0:01:52

**→ `serial_send`**

```
4142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f0a68656c700a6563686f207265636f76657265640a
```

**← `serial_send`**

```
{"sent":84}
```

#### +0:01:56

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
756e6b6e6f776e20636f6d6d616e640a7368656c6c3e2068656c70206563686f0a7368656c6c3e207265636f76657265640a7368656c6c3e20
```

`text`

```
unknown command
shell> help echo
shell> recovered
shell>
```

#### +0:01:59

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:02:01

**→ `vm_boot_http`**

**← `vm_boot_http`**

```
{"run_id":"20261103T215915.283073Z"}
```

#### +0:02:03

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
424f4f540a30323a64633a38343a34353a37663a64330a48656c6c6f2c20776f726c6421203739376437373937393533350a7368656c6c3e20
```

`text`

```
BOOT
02:dc:84:45:7f:d3
Hello, world! 797d77979535
shell>
```

#### +0:02:05

**→ `serial_send`** `{"hex": "68656c700a6563686f206e6574776f726b207368656c6c0a3f0a"}`

**← `serial_send`**

```
{"sent":26}
```

#### +0:02:07

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
68656c70206563686f0a7368656c6c3e206e6574776f726b207368656c6c0a7368656c6c3e20756e6b6e6f776e20636f6d6d616e640a7368656c6c3e20
```

`text`

```
help echo
shell> network shell
shell> unknown command
shell>
```

#### +0:02:09

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:02:11

> 💭 **Updating HTTP notes**

**→ `notes_write`**

<details><summary>text (6,592 chars, 20 lines)</summary>

```
Stage-006 FINAL saved image:1773bytes (0x6ed), raw little-endian AArch64, entry0x40200000, QEMU virt Cortex-A53. VM STOPPED. No OS or initialized stack, assembler, external reference or binary. Read/update via guest tools only. vm_boot for noNIC; vm_boot_http for private ARP + hostHTTP origin. Old vm_boot_tcp/network unavailable.
Behavior: BOOT LF unchanged; ifNIC exists, perform existing ARP/MAC print + TCP/HTTP GET/responsebody print, then shell. WithoutNIC, shell immediately afterscan. Prompt exact sevenbytes shell> space. LF-terminatedcommands: exact help -> help echo LF; echo followedbyspace -> remaining arbitrarybytes thenLF (emptytextallowed); everythingelse -> unknown command LF. Repeats prompt. No raw inputecho, CRstripping, editing, quoting, tokenexpansion or NULtermination. Emptyline and helpwithtrailingtext unknown. All128bytes oflinebuffer usable;129thnonLF marks overflow, drains untilLF then unknowncommand andfreshprompt. Length-based output preserves embeddedNULs too.
SHELL ENTRY/LAYOUT:
Stage005 first1467bytes preserved EXCEPT wordat+0x30 replaced by14000163 (bytes63010014), a branchto+0x5bc. Original network/noNIC returntargets+0x30 therefore all funnel into shell instead of raw echo. Old echo instructions+0x34..48 nowunreachable. Stage005 ends+0x5bb; zeroalignmentbyteat+0x5bb; shellstarts+0x5bc (absolute0x402005bc).
+0x5bc MOVZx8,#0x4010,LSL16; +0x5c0 ADDx8,#0x5000 =>linebuffer0x40105000. This initialization is independent of x10/NIC/RAMclear. Buffer128bytes range0x40105000..0x4010507f inclusive, separatefromrings/RX/TX/HTTPaccumulation. Notprecleared orNULterminated, everyreadgovernedbylength. x8bufferbase,w7length0..128,w9overflowboolean.
+0x5c4 promptentry: ADRx5,promptstring+0x6cc; w4=7; BLprint; resetw7/w9; pollinput+0x5d8. PL011 x0=0x09000000 inheritedBOOT; FRoffset0x18 RXFEbit4; DRoffset0; receivedvalue masked8bits. LFbranchesdispatch+0x620. OverflowflagdrainsnonLF. Otherwisecomparelength128; atcapacitynextbyte setsflag+0x614; belowcapacity storebyteatbuffer+length, incrementlength.
+0x620 dispatch: overflow ->unknown+0x694. Ifexactlength4, alignedLDRw1,[x8], comparelittleendianword706c6568(help); matchoutputshelpstring+0x6d3 length10 via+0x6a0. Elseunknown. Otherlengths: require>=5, firstword6f686365(echo), byte4space. Echo at+0x674 pointsx5=buffer+5,w4=length-5, callsprint, explicitlywritesLFthenbranchprompt. Thus echoaloneunknown, echo-space emitsLF.
+0x694 unknownADRstring+0x6dd,w4=16. +0x6a0 callprint thenprompt.
+0x6a8 print routine (absolute0x402006a8): x5bytepointer,w4length; returnsimmediatelyif0, elseLDRBpostincrement, waitTXFFbit5clear, writeDR, decrementlengthandloop. RET+0x6c8. Clobbersx5,w4,w1,w2,flags, usesx30 link; leavesx8,w7,w9intact. No nestedcalls orstack.
+0x6cc prompt7bytes(shell> space), +0x6d3 help10bytes(help echo LF), +0x6dd unknown16bytes(unknown command LF). Endexclusive+0x6ed. Shellonlyusesx0,x1,x2,x4,x5,x6,x7,x8,x9,x30; networkregistersnotneededonceentered.
VERIFICATION final1773-byteimageunchangedbetweentests:
NoNIC vm_boot run_id20261103T215840.834691Z -> BOOT\nshell> . One serial_send contained help\necho hello world\nnope\necho \n; output help echo\nshell> hello world\nshell> unknown command\nshell> \nshell> . SameVM: sentthree63bytechunks(eachbytes41..7f) thenLF,helpLF,echo recoveredLF. 189-byteoverlonglineproducedsingleunknown command LF+prompt; followingcommandsproducedhelp echo LF+prompt and recovered LF+prompt. vm_stopcompleted.
HTTPboot vm_boot_http run_id20261103T215915.283073Z -> BOOT\n02:dc:84:45:7f:d3\nHello, world! 797d77979535\nshell> . SenthelpLF,echo network shellLF,?LF inonewrite; gothelp echo LF+prompt,network shell LF+prompt,unknown command LF+prompt. vm_stopcompleted. ShellpromptappearsAFTERactualHTTPbody. Updatedimageissaved; VMstopped.
PRESERVED NETWORK STACK REFERENCE:
MMIOscan32slots0x0a000000 stride0x200 DeviceID1; reset,status3,VERSION_1only highfeatures1 low0,status11(no readback),queuesRX0/TX1 QueueNum1 Ready1,status15. DMB SY publications/completions. RAMclear0x40100000..0x40102fff. x10scratchbase. RXdesc0x40100000 avail0100 used0200; TXdesc0400 avail0500 used0600 (relativex10). Allhighaddresshalveszero,ring[0]=0,idxstarts1. RXlen2048 WRITE2, TXflags0dynamiclen. x11RX0x40100802,x12TX0x40101802. IMPORTANTbufferalignment2mod4 ensuresIP/TCP32bitfieldsalignedafter12bytevirtio+14byteEthernet; MMUoffunalignedwordaccessfaultspreviouslyobserved. Neverrestorealignedbufferpointerswithoutrewritingpacketaccesses.
+0x4c scan,+0x74 features,+0x9c clear,+0xbcdescriptors,+0xeccopyARP,+0x108queues,+0x150notify,+0x168ARPreceivechecks0806/opcode2,+0x190..214 printsMAC/LF,+0x218branches+0x248. ARP42byteliteral+0x21c..245 then2zeros; guest52:54:00:12:34:56 /10.0.2.15 targeting10.0.2.2.
+0x248 w20RXavail/w21TXavail=1,copy54bytetemplate+0x448 toTX+12,copyARPpeerMACtoEthernetdestination. TCPport40000 ->8080(1f90), seqw24=1000, ackw25=0. SYNsend, receiveSYNACK, peerack=seq+1, ownseq1001, ACKsend. +0x2b8branches+0x480(word14000072); obsoletepingcode+0x2bc..33cunreachable.
+0x340send savesLRx28, waitsusedTX=w21,patchesIPtot/seq/ack/flags,recomputeschecksums,descriptorlen46+TCPlen,w21++/publishnotify,return+0x3cc. w22TCPlen,w23flags,w24ownseq,w25ack,x14TXTCP. +0x3d0receive postsRXw20++,waitsused=w20,filtersIPv4/protocol6,returnsx13=RX+46,RET+0x40c. +0x410checksumx5pointer,w4halfwordcount,w6initialsum;REV16reads,add,foldtwice,complement,REV16resultw1forSTRH. IPsum0 count10; TCPpseudo0x1817+TCPlen countceil(TCPlen/2),oddpaddingzero. +0x44854bytetemplate; IPv4IHL5 TTL64 DF,src10.0.2.15 dst10.0.2.2; TCPdataoffset5 window4096; twoalignmentzeros+0x47e.
+0x480copy23bytesGET /hello HTTP/1.0 CRLFCRLF fromliteral+0x5a4 toTX+66, TCPlen43flagsPSHACK,send,ownseq+=23=1024. x26responsebase0x40103000,x27writepointer,w19FINseen0. +0x4b8receive; REVreceivedseqat+0x4c0 MUSTword5ac00821(REVw1,w1),compareexpectedw25. Sequence mismatchdupACK. IPtotal-20-actualTCPdataoffset yieldslen,appendpayloadbytewiseto[x27++],ack+=len; ifFINbit0 at+0x50c ack++/FINseen1; +0x524sendACKTCPlen20. LoopuntilFIN,+0x534waitfinalTXcompletion,+0x540boundedCRLFCRLFrollingmatch,+0x56cprintremainingbody,+0x588appendLFifnecessary,branch+0x30(NOWshelltrampoline). HTTP/1.0closeframed; Content-Lengthnotparsednumerically. Hostshortbodypreviously27bytes.
Networklimitationsinherited: noresponseaccumulationbounds, timeouts,retransmissiontimers,IPfragments,inboundchecksumvalidation,tuplefilter,generalTCPstate/FINteardown/keepalive/chunking. InitialARPnonARPpathusedidxweak. Queueindicesnotwrapsafe. Intendedprivateoriginonly. Shellbufferboundsareindependentandexplicit.
```

</details>

**← `notes_write`**

```
{"saved":true}
```

#### +0:02:59

Saved the serial shell with `help`, `echo`, unknown-command handling, and a bounded 128-byte line buffer.

Verified multiple commands and overlong-line recovery in one VM, plus the HTTP boot path followed by shell commands. BOOT and HTTP output preserved. Handoff notes updated; VM stopped.
