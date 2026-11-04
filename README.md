# Compute from Scratch

[English](#english) · [日本語](#日本語)

## English

An experiment to see how far GPT-6.1 Sol can build a software stack from machine code in a bare-metal environment.

### Milestones

| Stage | Success criteria |
| --- | --- |
| Boot and serial I/O | Boot from raw machine code and verify character input and output. Complete (001–002). |
| Ethernet, TCP, and HTTP | Implement ARP and TCP, then retrieve the body of an HTTP response from the host. Complete (003–005). |
| Serial shell | Enter and run multiple commands in the same VM and receive their results and a prompt. Complete (006). |
| Small OS | Handle the console, memory, and program loading and exit. Start with a single task and define a calling convention between programs and the kernel. Complete (007). |
| Persistent disk and filesystem | Read and write a virtual block device, and save and reload source files and programs across reboots. Complete (008 and 010). |
| Assembler | Translate AArch64 instructions and labels into machine code inside the guest, then run the result. Verified the instruction coverage and capacity needed to assemble a compiler in the guest (009–014). |
| Compiler | Build a compiler with the guest assembler. Verified a single-function C subset with runtime arguments, integer expressions, local variables, branches, and loops (014–015). |
| GUI and browser | Framebuffer and keyboard input are complete (016). Render simple HTML fetched from the host. Complete (017). |
| Self-hosting assembler | Use the kernel assembler to build a seed, then assemble its own source as a guest application. Compare generated code across generations. Complete (019). |
| Processes and system calls | Give each program its own stack and execution state. Support cooperative scheduling, process exit and waiting, and file and console I/O. Cooperative processes and basic file I/O are complete (018 and 020). |
| C compiler and minimal libc | Gradually add multiple functions, types, pointers, arrays, strings, and preprocessing. Test the features of the target C standard and provide library routines for I/O and string operations. |
| Self-hosting C compiler | Have a seed compiler running in the guest build its own C source. Use the resulting compiler to rebuild itself and run regression tests. |
| Open-source CLI | Have the observer supply the source of a small CLI with a pinned version and hash. Build it in the guest, verify its inputs and outputs, and record any porting changes. |
| External network | Establish offline reproducibility first, then verify the workflow from source retrieval to build with a restricted set of sources. |

Each stage builds on the previous artifacts and adds the tools it needs. The observer supplies the public source code initially and keeps both the agent and the guest offline. Record build inputs separately from the environment available for researching solutions.

### Continuing experiments with Pi

Node.js 24, Python 3, QEMU, and an authenticated Codex CLI are required.

```sh
npm ci --prefix pi --ignore-scripts
node pi/run.mjs 001
node pi/run.mjs 002 "$campaign"
```

Set `campaign` to the directory printed by stage 001. Stage 001 starts a new campaign, and stage 002 resumes the same Pi session and workspace. The next stage reads the `guest.hex` saved by the model and extends it while preserving existing behavior.

QEMU uses the `virt` machine with a single Cortex-A53 core, TCG, and 64 MiB of RAM. It loads raw bytes at `0x40200000` and starts execution there. The NIC and display are disabled.

Stage 001 exposes tools to read and write the image and handoff notes, start and stop the VM, and read serial output. Stage 002 adds serial input. The experimental VM runs until the model stops it or the host ends the experiment. The observer's boot test CLI can stop the VM after a specified duration.

The campaign directory stores the conversation, artifacts, each stage's tool list and events, and the image and serial log for each boot.

### Evaluation and resuming

The observer checks the logs against the artifacts to decide whether a stage is complete. The number of attempts can vary. If the model finishes before meeting the criteria, use `node pi/run.mjs 002 "$campaign" --continue "Unmet success criterion" "Actual observation"` to ask it to continue in the same session. Describe the expected output and observed facts, such as the actual bytes or whether the PCAP shows traffic in each direction. For each stage, record the number of entries where `mode == "--continue"` in `*-prompts.jsonl` separately from the number of VM boots.

Pi records the start and end of compaction as timestamped SDK events in `*-events.jsonl`, including the reason and result.

To switch conversations, use `node pi/run.mjs 002 "$campaign" --fresh` to start a new session with the saved image and notes. A serial read can wait up to five seconds while the VM continues running.

### Observer boot test

Python 3 and `qemu-system-aarch64` are required. On macOS, install QEMU with `brew install qemu`.

```sh
run=$(python3 runner.py fixtures/serial-smoke.hex)
cat "$run/serial.log"
```

The test passes when it prints `O` followed by a newline. The sample loops after printing, so the runner stops QEMU after two seconds by default. The binary, serial output, QEMU standard error, and run configuration for each execution are saved under `.local/runs/`.

### Verifying ARP

```sh
node pi/run.mjs 003 "$campaign"
python3 verify_arp.py "$campaign/work/guest.hex"
```

Stage 003 adds a dedicated Ethernet link. The host-side peer responds to ARP with a different MAC address on each boot. A socket connects QEMU directly to the peer on an isolated link. The observer boots the same image twice, verifies that both PCAPs contain an ARP request and reply, and checks that the responder MAC matches the serial output. The observer also verifies the boot message and serial echo.

To check the reference guest, run `python3 verify_arp.py fixtures/arp-reference.hex --reference`. To regenerate the reference binary, run `python3 fixtures/build-arp-reference.py > fixtures/arp-reference.hex`.

### Verifying TCP

```sh
node pi/run.mjs 004 "$campaign"
python3 verify_tcp.py "$campaign/work/runs/$run_id"
```

The dedicated peer in stage 004 receives `ping\n` on port 2323 and returns a different response on each boot. The observer checks TCP checksums, the handshake, the request, the acknowledgment of the response, and the serial output.

### Verifying HTTP

```sh
node pi/run.mjs 005 "$campaign"
python3 verify_http.py "$campaign/work/runs/$run_id"
```

Stage 005 forwards the guest's `GET /hello HTTP/1.0` to a fixed local HTTP origin. The observer cross-checks the PCAP, the host access log, and the serial output. The origin includes a different identifier in the response body on each boot.

### Verifying the GUI

```sh
node pi/run.mjs 016 "$campaign"
python3 verify_gui.py experiments/016-campaign.hex
```

Stage 016 uses ramfb and a virtio keyboard. The observer checks screenshot colors, changes after keyboard input, and the serial shell response.

### Verifying the browser

```sh
node pi/run.mjs 017 "$campaign"
python3 verify_browser.py experiments/017-campaign.hex
```

Stage 017 renders headings and paragraphs from HTML fetched from the host. The observer compares the PCAP and HTTP log and verifies the rendered output with ImageMagick and Tesseract. See the screenshots in [experiment 017](experiments/017-campaign.md).

### License

This project is licensed under the [MIT License](LICENSE).

## 日本語

GPT-6.1 Solが、ベアメタル環境で機械語からどこまでソフトウェアスタックを構築できるかを観察する実験。

### マイルストーン

| 段階 | 到達条件 |
| --- | --- |
| 起動・シリアル | 生の機械語から起動し、文字の出力と入力を確認する。完了（001–002） |
| Ethernet・TCP・HTTP | ARPとTCPを実装し、ホストのHTTP応答本文を取得する。完了（003–005） |
| シリアルシェル | 同じVMで複数のコマンドを入力・実行し、結果とプロンプトを返す。完了（006） |
| 小さなOS | コンソール、メモリ、プログラムのロードと終了を扱う。最初は単一タスクで、プログラムとカーネルの呼び出し規約を定める。完了（007） |
| 永続ディスクとファイルシステム | 仮想ブロックデバイスを読み書きし、再起動をまたいでソースとプログラムを保存・再読込する。完了（008・010・022） |
| アセンブラ | ゲスト内でAArch64の命令とラベルを機械語に変換し、生成物を実行する。コンパイラをゲスト内で組み立てられる命令と容量を確認済み（009–014） |
| コンパイラ | ゲスト内アセンブラでコンパイラを組む。実行時引数・整数式・局所変数・分岐・ループを含むCサブセットを確認済み（014–015）。補助関数の定義と呼び出しを追加済み（021） |
| GUIとブラウザ | フレームバッファとキー入力は完了（016）。ホストから取得したシンプルなHTMLを画面に描画する。完了（017） |
| アセンブラの自己ホスト | カーネル内のアセンブラで種を作り、ゲストアプリとして自分のソースを組み立て直す。世代間で生成コードを照合する。完了（019） |
| プロセスとシステムコール | 複数のプログラムに独立したスタックと実行状態を持たせ、協調スケジューリング、終了・待機、ファイルやコンソールの入出力を扱う。協調プロセスと基本ファイル入出力は完了（018・020） |
| Cコンパイラと最小libc | 複数関数、型、ポインタ、配列、文字列、前処理などを段階的に追加する。対象とするC規格の機能をテストし、入出力・文字列操作などのライブラリを用意する |
| Cコンパイラの自己ホスト | ゲストで動く種コンパイラがコンパイラ自身のCソースをビルドできるようにし、生成したコンパイラで再ビルドと回帰テストを行う |
| オープンソースCLI | 観測側が版とハッシュを固定した小さなCLIのソースを投入し、ゲスト内でビルドして入出力を照合する。必要な移植差分を記録する |
| 外部ネットワーク | オフラインでの再現を確立した後、まず取得先を限定してソース取得からビルドまで検証する |

各段階で前段の成果物を引き継ぎ、その段階で必要なツールを追加する。公開ソースの初回投入は観測側が行い、エージェントとゲストにインターネットへの経路を渡さない。ビルド時の入力と、解法を調べられる環境を分けて記録する。

### Piの継続実験

Node.js 24、Python 3、QEMU、ログイン済みのCodex CLIが必要。

```sh
npm ci --prefix pi --ignore-scripts
node pi/run.mjs 001
node pi/run.mjs 002 "$campaign"
```

`campaign` に001が表示したディレクトリを指定する。001で新しいキャンペーンを開始し、002では同じPiセッションと作業領域を再開する。モデルが保存した `guest.hex` を次のステージで読み、既存の振る舞いを保ちながら拡張する。

QEMUは `virt`、Cortex-A53、1コア、TCG、RAM 64 MiB。生バイト列を `0x40200000` に置き、そこから実行する。NICと画面は無効。

001ではイメージと引き継ぎメモの読み書き、VMの起動・停止、シリアル出力の読み取りを公開する。002ではシリアル入力を追加する。実験用VMに固定の実行時間はなく、モデルが停止するか、ホストが実験を終了すると停止する。観測側の起動テスト用CLIは時間を指定して終了できる。

会話と成果物、各ステージのツール一覧・イベント、起動ごとのイメージとシリアルログはキャンペーンディレクトリに保存する。

### 判定と再開

観測側がログと成果物を照合して完了を判定する。試行回数は固定しない。モデルが作業を終えても条件を満たしていなければ、`node pi/run.mjs 002 "$campaign" --continue "未達の合格条件" "実際に観測した結果"` で同じセッションに続きを依頼する。原因の推測や修正方法は書かず、期待した出力と観測したバイト列、PCAPの送受信の有無などの確認事実に限る。各ステージの結果には `*-prompts.jsonl` の `mode == "--continue"` の件数と、VM起動回数を別々に記録する。

Piの圧縮開始・終了は、理由と結果を含むSDKイベントとして時刻付きで `*-events.jsonl` に残す。

会話を切り替えるときは `node pi/run.mjs 002 "$campaign" --fresh` で新規セッションを作り、保存済みのイメージとメモを引き継ぐ。シリアル読み取りには最大5秒の待ち時間を指定でき、VM自体は動き続ける。

### 観測側の起動テスト

Python 3と `qemu-system-aarch64` が必要。macOSでは `brew install qemu` で入手できる。

```sh
run=$(python3 runner.py fixtures/serial-smoke.hex)
cat "$run/serial.log"
```

`O` と改行が出れば成功。サンプルは出力後にループするので、既定の2秒でランナーがQEMUを停止する。各実行のバイナリ、シリアル、QEMUの標準エラー、実行条件は `.local/runs/` に保存する。

### ARPの観測

```sh
node pi/run.mjs 003 "$campaign"
python3 verify_arp.py "$campaign/work/guest.hex"
```

003では専用のEthernetリンクを追加する。ホスト側の応答役は起動ごとに異なるMACでARPに応答する。リンクはQEMUと応答役をソケットで直結し、外部への転送経路を持たない。観測側は同一イメージを2回起動し、両方のPCAPにARP要求・応答があり、応答元MACがシリアル出力と一致することを確認する。起動メッセージとシリアルエコーも検証する。

観測側の参照ゲストは `python3 verify_arp.py fixtures/arp-reference.hex --reference` で確認できる。参照バイナリを再生成する場合は `python3 fixtures/build-arp-reference.py > fixtures/arp-reference.hex` を実行する。

### TCPの観測

```sh
node pi/run.mjs 004 "$campaign"
python3 verify_tcp.py "$campaign/work/runs/$run_id"
```

004の専用応答役は、ポート2323で `ping\n` を受け、起動ごとに異なる応答を返す。観測側はTCPのチェックサム、ハンドシェイク、要求、応答のACK、シリアル表示を照合する。

### HTTPの観測

```sh
node pi/run.mjs 005 "$campaign"
python3 verify_http.py "$campaign/work/runs/$run_id"
```

005ではゲストの `GET /hello HTTP/1.0` を固定のローカルHTTPオリジンへ渡す。観測側はPCAP、ホストのアクセスログ、シリアル出力を照合する。オリジンは起動ごとに異なる識別子を本文に含める。

### GUIの観測

```sh
node pi/run.mjs 016 "$campaign"
python3 verify_gui.py experiments/016-campaign.hex
```

016はramfbとvirtioキーボードを使う。観測側はスクリーンショットの色、キー入力での変化、シリアルシェルの応答を確認する。

### ブラウザの観測

```sh
node pi/run.mjs 017 "$campaign"
python3 verify_browser.py experiments/017-campaign.hex
```

017はホストから取得したHTMLの見出しと段落を描画する。観測側はPCAPとHTTPログを照合し、ImageMagickとTesseractで画面を検証する。スクリーンショットは [実験017](experiments/017-campaign.md) に掲載している。

### ライセンス

このプロジェクトは [MITライセンス](LICENSE) で公開しています。
