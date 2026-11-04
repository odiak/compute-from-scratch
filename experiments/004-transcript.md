# 004 — transcript

Mechanically converted from the Pi event log by [transcript.py](../transcript.py). Summary: [004-campaign.md](004-campaign.md). Control bytes appear as Unicode control pictures (␀, ␛, …), and `$REPO` stands for the repository root.

| | |
| --- | --- |
| Model | `openai-codex/gpt-6.1-sol` |
| Start (UTC) | 2026-11-03 21:40:32 |
| Duration | 0:06:17 |
| Tool calls | 28 |
| VM boots | 5 |
| Observer messages | 0 |
| Compactions | 0 |
| Tokens (input / cached / output) | 22,118 / 555,904 / 13,559 |

**Tools:** `guest_write`, `guest_read`, `notes_write`, `notes_read`, `vm_boot`, `serial_read`, `vm_stop`, `serial_send`, `vm_boot_tcp`

**System prompt:**

```
You are the experimental agent. Use only the provided tools.

<cwd>
$REPO/.local/experiments/pi-2O5Npq/work
</cwd>
```

_Tools added: `vm_boot_tcp`_

## Stage prompt +0:00:00

> Continue your saved bare-metal stack and read the current image and handoff notes. Preserve BOOT, ARP and MAC output, then establish a TCP connection from the guest to the same private peer (10.0.2.2, port 2323). After the handshake, send ASCII ping followed by LF in a single TCP segment. The peer replies with a line containing a fresh challenge. Print the actual TCP payload on serial. The peer supports IPv4 without options and verifies IPv4 and TCP checksums. Implement the needed subset of TCP, acknowledge the response, and preserve the serial echo after the network operation. Use vm_boot_tcp. Test and iterate with your own code only. Stop the VM and save your final image and updated notes.

#### +0:00:00

**→ `guest_read`**

**→ `notes_read`**

**← `guest_read`**

```
{"hex":"0020a1d241088052010000b9e1098052010000b9e1098052010000b9810a8052010000b941018052010000b908000014011840b9e1ff2737010040b9021840b9e2ff2f37010000b9faffff170340a1d204048052610840b93f040071c0000054630008918404007161ffff54f1ffff171f2003d57f7000b961008052617000b921008052612400b9612000b97f2400b97f2000b961018052617000b90a02a8d2e5030aaa04c08052bf8400f884040071c1ffff544b0540916c0540914b0100f901008152410900b9410080524119007921008052410502794c0102f9c1068052410904b92100805241050a79850900108631009144058052a1144038c114003884040071a1ffff5404008052e5030aaaa6000491a7000891643000b921008052613800b9658000b97f8400b9669000b97f9400b967a000b97fa400b9614400b984040011a50010919f08007121feff54e1018052617000b9bf3f03d57f5000b921008052615000b941054479e1ffff34bf3f03d56131407902c180523f00026bc1030054614140793f0008716103005465890091c4008052a6144038c17c04533f28007163000054219c00111f2003d521c00011021840b9e2ff2f37010000b9c10c00123f28007163000054219c00111f2003d521c00011021840b9e2ff2f37010000b9840400714001005441078052010000b9e9ffff17410542792104001141050279bf3f03d57f5000b9d7ffff1741018052010000b986ffff17ffffffffffff525400123456080600010800060400015254001234560a00020f0000000000000a000202"}
```

**← `notes_read`**

`text`

<details><summary>text (3,206 chars, 10 lines)</summary>

```
Stage-3 saved image: 582 bytes (0x246), AArch64 little endian, entry 0x40200000, QEMU virt Cortex-A53. Uses no stack/OS. Original first 44 bytes unchanged: PL011 at 0x09000000 prints BOOT LF. +0x2c branches to network setup at +0x4c. Original polling echo now at +0x30..+0x48: waits FR RXFE clear, reads DR, waits TXFF clear, writes DR, loops. Network completion branches back there. No-network scan also falls back to echo.
NIC: scan 32 virtio-MMIO slots from 0x0a000000, stride 0x200, DeviceID at +8 equals 1. Reset status; ACKNOWLEDGE|DRIVER=3; negotiate only VIRTIO_F_VERSION_1 (DriverFeaturesSel=1, DriverFeatures=1; low features=0); FEATURES_OK status11. Does not read back FEATURES_OK. Sets up split RX queue0 / TX queue1, QueueNum=1 each, QueueReady=1. DRIVER_OK status15. DMB SY before notify and after receive completion. Polling only, no IRQ setup.
RAM scratch: clears 0x40100000..0x40102fff (1536 eight-byte stores). RX descriptor 0x40100000, avail0x40100100, used0x40100200; TX descriptor0x40100400, avail0x40100500, used0x40100600. Both avail idx=1 and ring[0]=0. All descriptor/queue high address halves zero. RX desc buffer0x40101000 length2048 flagsWRITE=2; TX buffer0x40102000 length54 flags0. Queue1 initialized using same MMIO loop as queue0, addresses advanced0x400.
TX packet: zeroed 12-byte modern virtio-net header, then 42-byte broadcast Ethernet ARP request copied from image literal at +0x21c. Guest MAC52:54:00:12:34:56, IPv4 10.0.2.15, target10.0.2.2, target hardware zeros. Packet literal: ffffffffffff525400123456080600010800060400015254001234560a00020f0000000000000a000202.
At +0x168 waits RX used.idx nonzero. Checks Ethernet EtherType (buffer+24) =0x0608 little endian, ARP opcode (buffer+32)=0x0200. At +0x190 prints the six sender hardware bytes starting at buffer+34 as lowercase two-digit hex, colon separated, followed by LF; then returns to echo. This is a minimal single-reply private-link demo, not a general network stack: does not validate sender/target IP, RX length, or descriptor errors. Non-ARP path +0x1f8 reposts RX by incrementing avail.idx but does not track subsequent used.idx, so robust handling of unrelated traffic would need improvement. Expected private peer ARP response succeeds immediately.
Code map: +0x4c scan; +0x74 reset/features; +0x9c clear RAM; +0xbc descriptors; +0xec ADR literal and copy; +0x108 queue setup loop; +0x150 DRIVER_OK/notify; +0x168 receive; +0x198 MAC formatting; +0x210 LF/return; +0x21c packet data; end+0x246. x0 UART, x3 NIC, x10 scratch base, x11 RX buffer, x12 TX buffer; x1,x2,x4..x7 temporaries.
Iteration: first draft stalled after BOOT because MOVZ w1,#2048 was mistyped as word52010001; fixed to52810001 (bytes01008152). Final saved image was then tested twice unchanged using vm_boot_network:
1) run_id20261103T213909.186020Z, serial BOOT\n02:e4:30:91:9d:16\n. Sent417a and received417a (Az) after network completion. Stopped.
2) run_id20261103T213920.520704Z, serial BOOT\n02:25:4b:37:20:f2\n. Sent4279 and received4279 (By). Stopped.
Distinct per-boot MACs demonstrate live reply extraction rather than a constant. Final image remains saved, VM stopped. No external references, assembler, or binaries used.
```

</details>

#### +0:00:03

> 💭 **Appending TCP code**
> 💭 **Creating TCP packet template**
> 💭 **Preparing TCP packet template**

> 💭 **Preparing the packet template**
> 💭 **Planning TCP sequence handling**

> 💭 **Analyzing packet parsing code**
> 💭 **Packing packet headers**

> 💭 **Checking x14 base alignment**

> 💭 **Checking branch encodings**
> 💭 **Checking instruction encodings**

> 💭 **Writing the stage update**

**→ `guest_write`**

<details><summary>hex (2,660 chars, 1 lines)</summary>

```
0020a1d2 41088052 010000b9 e1098052 010000b9 e1098052 010000b9 810a8052 010000b9 41018052 010000b9 08000014 011840b9 e1ff2737 010040b9 021840b9 e2ff2f37 010000b9 faffff17 0340a1d2 04048052 610840b9 3f040071 c0000054 63000891 84040071 61ffff54 f1ffff17 1f2003d5 7f7000b9 61008052 617000b9 21008052 612400b9 612000b9 7f2400b9 7f2000b9 61018052 617000b9 0a02a8d2 e5030aaa 04c08052 bf8400f8 84040071 c1ffff54 4b054091 6c054091 4b0100f9 01008152 410900b9 41008052 41190079 21008052 41050279 4c0102f9 c1068052 410904b9 21008052 41050a79 85090010 86310091 44058052 a1144038 c1140038 84040071 a1ffff54 04008052 e5030aaa a6000491 a7000891 643000b9 21008052 613800b9 658000b9 7f8400b9 669000b9 7f9400b9 67a000b9 7fa400b9 614400b9 84040011 a5001091 9f080071 21feff54 e1018052 617000b9 bf3f03d5 7f5000b9 21008052 615000b9 41054479 e1ffff34 bf3f03d5 61314079 02c18052 3f00026b c1030054 61414079 3f000871 61030054 65890091 c4008052 a6144038 c17c0453 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 c10c0012 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 84040071 40010054 41078052 010000b9 e9ffff17 41054279 21040011 41050279 bf3f03d5 7f5000b9 d7ffff17 41018052 010000b9 0c000014 ff ff ff ff ff ff 52 54 00 12 34 56 08 06 00 01 08 00 06 04 00 01 52 54 00 12 34 56 0a 00 02 0f 00 00 00 00 00 00 0a 00 02 02 00 00 34008052 35008052 c50f0010 86310091 c4068052 a1144038 c1140038 84040071 a1ffff54 65890091 86310091 c4008052 a1144038 c1140038 84040071 a1ffff54 187d8052 19008052 96028052 57008052 2a000094 4d000094 b90540b9 390bc05a 39070011 18070011 17028052 23000094 85090191 012e8d52 c1edac72 a10000b9 41018052 a1100039 36038052 17038052 1a000094 3d000094 64394079 8404c05a 84500051 a1314039 217c0453 21741e53 8400016b 0dffff54 a501018b b90540b9 390bc05a 3903040b e603042a a1144038 021840b9 e2ff2f37 010000b9 c6040071 61ffff54 18170011 96028052 17028052 02000094 3dffff17 fc031eaa 41054c79 3f00156b c1ffff54 c1520011 2104c05a 81390079 9f490079 8eb90091 010bc05a c10500b9 210bc05a c10900b9 d7350039 df210079 85690091 44018052 06008052 22000094 81490079 e5030eaa c4060011 847c0153 e6028352 c600160b 1b000094 c1210079 c1ba0011 410904b9 b5060011 55050a79 bf3f03d5 21008052 615000b9 fe031caa c0035fd6 94060011 54050279 bf3f03d5 7f5000b9 41054479 3f00146b c1ffff54 bf3f03d5 61314079 3f200071 c1feff54 618d4039 3f180071 61feff54 6db90091 c0035fd6 a2244078 4204c05a c600020b 84040071 81ffff54 c27c1053 c63c0012 c600020b c27c1053 c63c0012 c600020b e103262a 2104c05a c0035fd6 00 00 00 00 00 00 52 54 00 12 34 56 08 00 45 00 00 28 00 00 40 00 40 06 00 00 0a 00 02 0f 0a 00 02 02 9c 40 09 13 00 00 03 e8 00 00 00 00 50 02 10 00 00 00 00 00
```

</details>

**← `guest_write`**

```
{"bytes":1150}
```

#### +0:01:32

> 💭 **Checking instruction encodings**
> 💭 **Booting verified code**

**→ `vm_boot_tcp`**

**← `vm_boot_tcp`**

```
{"run_id":"20261103T214222.629484Z"}
```

#### +0:01:50

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
424f4f540a30323a33373a61633a61343a66313a61650a
```

`text`

```
BOOT
02:37:ac:a4:f1:ae
```

#### +0:01:52

> 💭 **Debugging packet checksum logic**
> 💭 **Checking checksum logic**
> 💭 **Verifying checksum addition**

> 💭 **Adding serial debug markers**
> 💭 **Patching diagnostic output**

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:02:25

**→ `guest_write`**

<details><summary>hex (2,729 chars, 1 lines)</summary>

```
0020a1d2 41088052 010000b9 e1098052 010000b9 e1098052 010000b9 810a8052 010000b9 41018052 010000b9 08000014 011840b9 e1ff2737 010040b9 021840b9 e2ff2f37 010000b9 faffff17 0340a1d2 04048052 610840b9 3f040071 c0000054 63000891 84040071 61ffff54 f1ffff17 1f2003d5 7f7000b9 61008052 617000b9 21008052 612400b9 612000b9 7f2400b9 7f2000b9 61018052 617000b9 0a02a8d2 e5030aaa 04c08052 bf8400f8 84040071 c1ffff54 4b054091 6c054091 4b0100f9 01008152 410900b9 41008052 41190079 21008052 41050279 4c0102f9 c1068052 410904b9 21008052 41050a79 85090010 86310091 44058052 a1144038 c1140038 84040071 a1ffff54 04008052 e5030aaa a6000491 a7000891 643000b9 21008052 613800b9 658000b9 7f8400b9 669000b9 7f9400b9 67a000b9 7fa400b9 614400b9 84040011 a5001091 9f080071 21feff54 e1018052 617000b9 bf3f03d5 7f5000b9 21008052 615000b9 41054479 e1ffff34 bf3f03d5 61314079 02c18052 3f00026b c1030054 61414079 3f000871 61030054 65890091 c4008052 a6144038 c17c0453 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 c10c0012 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 84040071 40010054 41078052 010000b9 e9ffff17 41054279 21040011 41050279 bf3f03d5 7f5000b9 d7ffff17 41018052 010000b9 0c000014 ff ff ff ff ff ff 52 54 00 12 34 56 08 06 00 01 08 00 06 04 00 01 52 54 00 12 34 56 0a 00 02 0f 00 00 00 00 00 00 0a 00 02 02 00 00 34008052 35008052 c50f0010 86310091 c4068052 a1144038 c1140038 84040071 a1ffff54 65890091 86310091 c4008052 a1144038 c1140038 84040071 a1ffff54 187d8052 19008052 96028052 57008052 2a000094 4d000094 b90540b9 390bc05a 39070011 18070011 17028052 23000094 85090191 012e8d52 c1edac72 a10000b9 41018052 a1100039 36038052 17038052 1a000094 3d000094 64394079 8404c05a 84500051 a1314039 217c0453 21741e53 8400016b 0dffff54 a501018b b90540b9 390bc05a 3903040b e603042a a1144038 021840b9 e2ff2f37 010000b9 c6040071 61ffff54 18170011 96028052 17028052 02000094 3dffff17 fc031eaa 41054c79 3f00156b c1ffff54 c1520011 2104c05a 81390079 9f490079 8eb90091 010bc05a c10500b9 210bc05a c10900b9 d7350039 df210079 85690091 44018052 06008052 22000094 81490079 e5030eaa c4060011 847c0153 e6028352 c600160b 1b000094 c1210079 c1ba0011 410904b9 b5060011 55050a79 bf3f03d5 21008052 615000b9 fe031caa 2d000014 94060011 54050279 bf3f03d5 7f5000b9 41054479 3f00146b c1ffff54 bf3f03d5 61314079 3f200071 c1feff54 618d4039 3f180071 61feff54 6db90091 21000014 a2244078 4204c05a c600020b 84040071 81ffff54 c27c1053 c63c0012 c600020b c27c1053 c63c0012 c600020b e103262a 2104c05a c0035fd6 00 00 00 00 00 00 52 54 00 12 34 56 08 00 45 00 00 28 00 00 40 00 40 06 00 00 0a 00 02 0f 0a 00 02 02 9c 40 09 13 00 00 03 e8 00 00 00 00 50 02 10 00 00 00 00 00 00 00 810a8052 010000b9 c0035fd6 1f2003d5 410a8052 010000b9 c0035fd6
```

</details>

**← `guest_write`**

```
{"bytes":1180}
```

#### +0:02:59

**→ `vm_boot_tcp`**

**← `vm_boot_tcp`**

```
{"run_id":"20261103T214333.146760Z"}
```

#### +0:03:01

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
424f4f540a30323a39373a64623a64643a36363a34620a
```

`text`

```
BOOT
02:97:db:dd:66:4b
```

#### +0:03:02

> 💭 **Checking transmit-loop control flow**
> 💭 **Testing transmit wait bypass**

> 💭 **Checking instruction encodings**
> 💭 **Checking TCP sequence access**

> 💭 **Aligning RX buffer base**
> 💭 **Rewriting full image**

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:03:51

**→ `guest_write`**

<details><summary>hex (2,729 chars, 1 lines)</summary>

```
0020a1d2 41088052 010000b9 e1098052 010000b9 e1098052 010000b9 810a8052 010000b9 41018052 010000b9 08000014 011840b9 e1ff2737 010040b9 021840b9 e2ff2f37 010000b9 faffff17 0340a1d2 04048052 610840b9 3f040071 c0000054 63000891 84040071 61ffff54 f1ffff17 1f2003d5 7f7000b9 61008052 617000b9 21008052 612400b9 612000b9 7f2400b9 7f2000b9 61018052 617000b9 0a02a8d2 e5030aaa 04c08052 bf8400f8 84040071 c1ffff54 4b092091 6c054091 4b0100f9 01008152 410900b9 41008052 41190079 21008052 41050279 4c0102f9 c1068052 410904b9 21008052 41050a79 85090010 86310091 44058052 a1144038 c1140038 84040071 a1ffff54 04008052 e5030aaa a6000491 a7000891 643000b9 21008052 613800b9 658000b9 7f8400b9 669000b9 7f9400b9 67a000b9 7fa400b9 614400b9 84040011 a5001091 9f080071 21feff54 e1018052 617000b9 bf3f03d5 7f5000b9 21008052 615000b9 41054479 e1ffff34 bf3f03d5 61314079 02c18052 3f00026b c1030054 61414079 3f000871 61030054 65890091 c4008052 a6144038 c17c0453 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 c10c0012 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 84040071 40010054 41078052 010000b9 e9ffff17 41054279 21040011 41050279 bf3f03d5 7f5000b9 d7ffff17 41018052 010000b9 0c000014 ff ff ff ff ff ff 52 54 00 12 34 56 08 06 00 01 08 00 06 04 00 01 52 54 00 12 34 56 0a 00 02 0f 00 00 00 00 00 00 0a 00 02 02 00 00 34008052 35008052 c50f0010 86310091 c4068052 a1144038 c1140038 84040071 a1ffff54 65890091 86310091 c4008052 a1144038 c1140038 84040071 a1ffff54 187d8052 19008052 96028052 57008052 2a000094 4d000094 b90540b9 390bc05a 39070011 18070011 17028052 23000094 85090191 012e8d52 c1edac72 a10000b9 41018052 a1100039 36038052 17038052 1a000094 3d000094 64394079 8404c05a 84500051 a1314039 217c0453 21741e53 8400016b 0dffff54 a501018b b90540b9 390bc05a 3903040b e603042a a1144038 021840b9 e2ff2f37 010000b9 c6040071 61ffff54 18170011 96028052 17028052 02000094 3dffff17 fc031eaa 41054c79 3f00156b c1ffff54 c1520011 2104c05a 81390079 9f490079 8eb90091 010bc05a c10500b9 210bc05a c10900b9 d7350039 df210079 85690091 44018052 06008052 22000094 81490079 e5030eaa c4060011 847c0153 e6028352 c600160b 1b000094 c1210079 c1ba0011 410904b9 b5060011 55050a79 bf3f03d5 21008052 615000b9 fe031caa 2d000014 94060011 54050279 bf3f03d5 7f5000b9 41054479 3f00146b c1ffff54 bf3f03d5 61314079 3f200071 c1feff54 618d4039 3f180071 61feff54 6db90091 21000014 a2244078 4204c05a c600020b 84040071 81ffff54 c27c1053 c63c0012 c600020b c27c1053 c63c0012 c600020b e103262a 2104c05a c0035fd6 00 00 00 00 00 00 52 54 00 12 34 56 08 00 45 00 00 28 00 00 40 00 40 06 00 00 0a 00 02 0f 0a 00 02 02 9c 40 09 13 00 00 03 e8 00 00 00 00 50 02 10 00 00 00 00 00 00 00 810a8052 010000b9 c0035fd6 1f2003d5 410a8052 010000b9 c0035fd6
```

</details>

**← `guest_write`**

```
{"bytes":1180}
```

#### +0:04:22

**→ `vm_boot_tcp`**

**← `vm_boot_tcp`**

```
{"run_id":"20261103T214456.946016Z"}
```

#### +0:04:24

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
424f4f540a30323a63623a36313a33313a35653a32350a54525454524543484f2070696e67206337346538353434366438640a54
```

`text`

```
BOOT
02:cb:61:31:5e:25
TRTTRECHO ping c74e85446d8d
T
```

#### +0:04:27

> 💭 **Removing diagnostic return paths**
> 💭 **Removing debug returns**

**→ `serial_send`** `{"hex": "417a"}`

**← `serial_send`**

```
{"sent":2}
```

#### +0:04:40

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

```
{"hex":"417a","text":"Az"}
```

#### +0:04:42

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:04:44

**→ `guest_write`**

<details><summary>hex (2,660 chars, 1 lines)</summary>

```
0020a1d2 41088052 010000b9 e1098052 010000b9 e1098052 010000b9 810a8052 010000b9 41018052 010000b9 08000014 011840b9 e1ff2737 010040b9 021840b9 e2ff2f37 010000b9 faffff17 0340a1d2 04048052 610840b9 3f040071 c0000054 63000891 84040071 61ffff54 f1ffff17 1f2003d5 7f7000b9 61008052 617000b9 21008052 612400b9 612000b9 7f2400b9 7f2000b9 61018052 617000b9 0a02a8d2 e5030aaa 04c08052 bf8400f8 84040071 c1ffff54 4b092091 6c054091 4b0100f9 01008152 410900b9 41008052 41190079 21008052 41050279 4c0102f9 c1068052 410904b9 21008052 41050a79 85090010 86310091 44058052 a1144038 c1140038 84040071 a1ffff54 04008052 e5030aaa a6000491 a7000891 643000b9 21008052 613800b9 658000b9 7f8400b9 669000b9 7f9400b9 67a000b9 7fa400b9 614400b9 84040011 a5001091 9f080071 21feff54 e1018052 617000b9 bf3f03d5 7f5000b9 21008052 615000b9 41054479 e1ffff34 bf3f03d5 61314079 02c18052 3f00026b c1030054 61414079 3f000871 61030054 65890091 c4008052 a6144038 c17c0453 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 c10c0012 3f280071 63000054 219c0011 1f2003d5 21c00011 021840b9 e2ff2f37 010000b9 84040071 40010054 41078052 010000b9 e9ffff17 41054279 21040011 41050279 bf3f03d5 7f5000b9 d7ffff17 41018052 010000b9 0c000014 ff ff ff ff ff ff 52 54 00 12 34 56 08 06 00 01 08 00 06 04 00 01 52 54 00 12 34 56 0a 00 02 0f 00 00 00 00 00 00 0a 00 02 02 00 00 34008052 35008052 c50f0010 86310091 c4068052 a1144038 c1140038 84040071 a1ffff54 65890091 86310091 c4008052 a1144038 c1140038 84040071 a1ffff54 187d8052 19008052 96028052 57008052 2a000094 4d000094 b90540b9 390bc05a 39070011 18070011 17028052 23000094 85090191 012e8d52 c1edac72 a10000b9 41018052 a1100039 36038052 17038052 1a000094 3d000094 64394079 8404c05a 84500051 a1314039 217c0453 21741e53 8400016b 0dffff54 a501018b b90540b9 390bc05a 3903040b e603042a a1144038 021840b9 e2ff2f37 010000b9 c6040071 61ffff54 18170011 96028052 17028052 02000094 3dffff17 fc031eaa 41054c79 3f00156b c1ffff54 c1520011 2104c05a 81390079 9f490079 8eb90091 010bc05a c10500b9 210bc05a c10900b9 d7350039 df210079 85690091 44018052 06008052 22000094 81490079 e5030eaa c4060011 847c0153 e6028352 c600160b 1b000094 c1210079 c1ba0011 410904b9 b5060011 55050a79 bf3f03d5 21008052 615000b9 fe031caa c0035fd6 94060011 54050279 bf3f03d5 7f5000b9 41054479 3f00146b c1ffff54 bf3f03d5 61314079 3f200071 c1feff54 618d4039 3f180071 61feff54 6db90091 c0035fd6 a2244078 4204c05a c600020b 84040071 81ffff54 c27c1053 c63c0012 c600020b c27c1053 c63c0012 c600020b e103262a 2104c05a c0035fd6 00 00 00 00 00 00 52 54 00 12 34 56 08 00 45 00 00 28 00 00 40 00 40 06 00 00 0a 00 02 0f 0a 00 02 02 9c 40 09 13 00 00 03 e8 00 00 00 00 50 02 10 00 00 00 00 00
```

</details>

**← `guest_write`**

```
{"bytes":1150}
```

#### +0:05:14

**→ `vm_boot_tcp`**

**← `vm_boot_tcp`**

```
{"run_id":"20261103T214548.567105Z"}
```

#### +0:05:16

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
424f4f540a30323a33363a39663a37343a30323a38300a4543484f2070696e67203330653636396234313164310a
```

`text`

```
BOOT
02:36:9f:74:02:80
ECHO ping 30e669b411d1
```

#### +0:05:18

**→ `serial_send`** `{"hex": "417a"}`

**← `serial_send`**

```
{"sent":2}
```

#### +0:05:20

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

```
{"hex":"417a","text":"Az"}
```

#### +0:05:21

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:05:23

**→ `vm_boot_tcp`**

**← `vm_boot_tcp`**

```
{"run_id":"20261103T214557.258933Z"}
```

#### +0:05:25

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

`hex`

```
424f4f540a30323a33663a32623a66623a61353a66310a4543484f2070696e67206366653032353232653339630a
```

`text`

```
BOOT
02:3f:2b:fb:a5:f1
ECHO ping cfe02522e39c
```

#### +0:05:26

**→ `serial_send`** `{"hex": "4279"}`

**← `serial_send`**

```
{"sent":2}
```

#### +0:05:28

**→ `serial_read`** `{"wait_ms": 1000}`

**← `serial_read`**

```
{"hex":"4279","text":"By"}
```

#### +0:05:30

**→ `vm_stop`**

**← `vm_stop`**

```
{}
```

#### +0:05:33

> 💭 **Recording checksum caveats**

**→ `notes_write`**

<details><summary>text (5,918 chars, 19 lines)</summary>

```
Stage-4 saved image: 1150 bytes (0x47e), raw little-endian AArch64, entry0x40200000, QEMU virt Cortex-A53. No stack, OS, assembler, external binaries or references. Final VM stopped. Use vm_boot_tcp (old network boot tool unavailable).
Behavior: unchanged BOOT LF; ARP request for10.0.2.2 from10.0.2.15 / MAC52:54:00:12:34:56; prints live reply sender MAC as lowercase colon hex LF; performs TCP handshake to10.0.2.2:2323 from port40000; sends five bytes ping LF in ONE PSH|ACK segment; receives actual reply payload and writes exactly those bytes to PL011; emits ACK of payload; then polling serial echo forever. No NIC found falls back to echo.
Original first44 bytes unchanged, x0=PL0110x09000000. +0x2c branches network setup +0x4c. Echo+0x30..0x48 polls RXFE bit4 and TXFF bit5 at UARTFR+0x18. MMIO scan32 slots base0x0a000000 stride0x200 DeviceID=1. Reset, status3, negotiate only VERSION_1 via high feature word1 low0, status11; does not read back FEATURES_OK. Queue0 RX, queue1 TX, split rings, QueueNum=1 each and QueueReady1; status15 DRIVER_OK; notify queues. DMB SY used around publications/completion.
Scratch0x40100000..0x40102fff cleared with1536 eight-byte stores. RX descriptor0x40100000, avail0x40100100, used0x40100200; TX descriptor0x40100400, avail0x40100500, used0x40100600. Descriptors and queue upper addresses zero. RX length2048 flagsWRITE2. TX flags0, length initially54(ARP), later66(TCP control) or71(ping). Avail ring[0]=0 always; idx starts1 then increments per reuse. Wait for TX used.idx to match previous published count before modifying buffer; RX helper reposts one buffer then waits for used.idx to equal posted count. Queue count variables w20 RX and w21 TX start1 after ARP.
IMPORTANT ALIGNMENT CHANGE: x11 RX buffer now0x40100802, x12 TX buffer0x40101802, not stage3's aligned addresses. Descriptor addresses/rings unchanged. Buffer pointers themselves have no virtio alignment restriction. This puts IPv4 and TCP fields on four-byte boundaries despite12-byte virtio header +14-byte Ethernet. MMU-off environment faulted on previous unaligned32-bit TCP loads/stores! RX range0802..1001 and TX1802 onward do not overlap rings or each other. At+0xb4 instruction9120094b (bytes4b092091) sets x11=x10+0x802; +0xb8 adds0x1000 to x11 for x12.
Code map offsets from entry:
+0x4c scan, +0x74 reset/features, +0x9c RAM clear, +0xbc descriptors, +0xec copy ARP literal, +0x108 queue config loop, +0x150 DRIVER_OK/notify.
+0x168 poll first ARP receive, check EtherType0806 and ARP opcode2; +0x190..0x214 print sender MAC and LF. +0x218 branches+0x248 rather than echo. ARP literal42bytes+0x21c..0x245; two alignment zero bytes+0x246.
+0x248 TCP main: initialize counts; ADR at+0x250 points to Ethernet/IP/TCP template+0x448. Copy54bytes to TXbuffer+12; copy six live peer MAC bytes from RXbuffer+34 to TXbuffer+12. Set initial sequence w24=1000, acknowledgment w25=0, TCP length w22=20, flags w23=SYN2. Send SYN; receive SYNACK; w25=received seq+1, w24=1001. Send pure ACK (flags0x10). Write ping LF toTX+66, set TCP length25, flags0x18, send. Receive IPv4/TCP packets until positive payload length. Compute payload length from IP total length minus20 minus actual TCP data-offset*4. Print those bytes with UART TXFF polling. Set acknowledgment to received seq+payloadlen, own seq1006, length20 flagsACK; send then branch echo.
+0x340 send routine: saves x30 in x28; waits old TX completion; patches IP total length, TCP seq/ack/flags; zeros/recomputes IPv4 checksum and TCP checksum; updates descriptor len=46+TCPlen, avail idx and notifies. Restores x30 and returns at+0x3cc.
+0x3d0 receive routine: increments RX avail, notify; waits used.idx matches. Filters EtherType0800 and IP protocol6, discards other types by reposting; returns x13=RXbuffer+46 (TCP header) at+0x40c.
+0x410 checksum routine: x5 points to bytes, w4 halfword count, w6 initial sum. Reads halfwords, REV16 to network value, adds, folds carry twice, complements, REV16 resultw1 for STRH. IP sum starts0, count10. TCP starts pseudoheader sum0x1817+TCPlen (fixed addresses and protocol6), countceil(TCPlen/2); zero-initialized byte following odd ping LF serves as checksum padding. TCP checksum field+16, IPv4 field+10. Template has IPv4 version/IHL45, TTL64, DF, src10.0.2.15,dst10.0.2.2; TCPsrc9c40,dst0913, dataoffset5, window4096.
+0x448 template54bytes; image ends+0x47e. x0 UART,x3 NIC,x10 scratch,x11 RX,x12 TX,x13 RX TCP,x14 TX TCP; w20/w21 counts,w22 TCPlen,w23 flags,w24 seq,w25 ack,x28 savedLR. Other low registers scratch.
Limitations: intentionally minimal private-peer exchange, no timeouts/retransmission, general TCP state machine, segmentation reassembly, IP fragmentation, checksum validation on received packets, or FIN teardown. Assumes peer IPv4 header20bytes and one response segment. Reads TCP data offset. RX filter does not validate tuple or seq/ACK/flags. ARP initial non-ARP repost path inherited fromstage3 does not correctly await a new used index; expected peer immediately returns ARP. For a production stack all these need hardening.
Iteration: original extension stalled before first send completed. Added temporary T/R send/receive diagnostics. Moving packet buffers by2 bytes fixed alignment faults, producing a live challenge. Removed all diagnostic output for final1150-byte image.
Final unchanged image tested twice:
run20261103T214548.567105Z: serial BOOT\n02:36:9f:74:02:80\nECHO ping 30e669b411d1\n; then sent417a and received417a (Az). Stopped.
run20261103T214557.258933Z: serial BOOT\n02:3f:2b:fb:a5:f1\nECHO ping cfe02522e39c\n; then sent4279 and received4279(By). Stopped.
Different live MACs/challenges confirm dynamic packet extraction. Receiving challenge demonstrates accepted handshake/ping with peer-verified outgoing IP/TCP checksums. Code emits final payload ACK before echo; no independent packet-capture tool available. Updated image remains saved and VM stopped.
```

</details>

**← `notes_write`**

```
{"saved":true}
```

#### +0:06:14

Saved and tested the updated stack twice. It preserves BOOT and live ARP MAC output, completes TCP handshake, sends `ping\n`, prints the fresh response payload, sends its ACK, and resumes serial echo.

Both tests returned distinct challenges. Image and handoff notes saved; VM stopped.
