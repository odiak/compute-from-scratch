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
| Small OS | Handle the console, memory, and program loading and exit. Start with a single task and define a calling convention between programs and the kernel. Complete (007). Verified assembled, installed, and generated executables up to 8 KiB (026) and then 32 KiB (033). Verified a 53,772-byte self-hosted compiler with a 60,000-byte build limit (038). Verified full 65,532-byte builds/installs and subsequent process I/O (039). |
| Persistent disk and filesystem | Read and write a virtual block device, and save and reload source files and programs across reboots. Complete (008 and 010). Verified raw UART imports up to 8 KiB and byte-for-byte persistence across reboot (022). Verified guest-side migration to 24 files of up to 32 KiB, including assembly and C sources larger than 8 KiB (031). |
| Assembler | Translate AArch64 instructions and labels into machine code inside the guest, then run the result. Verified the instruction coverage and capacity needed to assemble a compiler in the guest (009–014). |
| Compiler | Build a compiler with the guest assembler. Verified a single-function C subset with runtime arguments, integer expressions, local variables, branches, and loops (014–015). Verified helper function definitions and calls (021), and compilation of imported multiline C source with whitespace and comments (023). Verified taking the address of a local integer and reading and writing through a pointer (024). |
| GUI and browser | Framebuffer and keyboard input are complete (016). Verified rendering simple HTML fetched from the host (017). Verified navigation to keyboard-entered paths within one boot (027). Verified keyboard navigation through links extracted from received HTML (028). |
| Self-hosting assembler | Use the kernel assembler to build a seed, then assemble its own source as a guest application. Compare generated code across generations. Complete (019). |
| Processes and system calls | Give each program its own stack and execution state. Support cooperative scheduling, process exit and waiting, and file and console I/O. Cooperative processes and basic file I/O are complete (018 and 020). Verified passing argc and argv to a loaded executable (029), and C command-line programs with string literals, putchar, puts, and strcmp (035). |
| C compiler and minimal libc | Gradually add multiple functions, types, pointers, arrays, strings, and preprocessing. Test the features of the target C standard and provide library routines for I/O and string operations. Verified runtime indexing and byte loads and stores for a local char array (025), and verified up to four named integer locals and independently named function parameters (030). Used a guest-assembled seed with named functions and typed pointers to build and run a compiler written in C (032). Added C pointer arithmetic, short circuit, globals, loops, casts, include processing, and object macros to compile unmodified upstream echo (038). Verified shared descriptor I/O and libc with unmodified echo, cat and basename, plus conditional preprocessing and switch statements (039). |
| Self-hosting C compiler | Have a seed compiler running in the guest build its own C source. Use the resulting compiler to rebuild itself and run regression tests. Verified byte-identical self-builds over two successive C-built generations and execution of a separate test program (034). Verified byte-identical 53,772-byte generations after the native-C extensions (038). Verified 64,624-byte successive generations with the shared CLI environment (039), then 65,412-byte generations with the development shell (040). |
| Open-source CLI | Have the observer supply the source of a small CLI with a pinned version and hash. Build it in the guest, verify its inputs and outputs, and record any porting changes. Verified sbase 0.1 echo with a guest-side portability adapter and an upstream host reference (036). Then compiled the exact upstream echo.c without an adapter and matched the reference (038). Verified unmodified echo, cat and basename with shared libc and matching normal/error behavior (039). |
| External network | Establish offline reproducibility first, then verify the workflow from source retrieval to build with a restricted set of sources. Verified live retrieval of the pinned sbase echo.c through a single-source host relay and a subsequent offline guest build matching the upstream reference (037). |

The later campaign built a self-hosted C compiler and a small CLI runtime, built an existing open-source command offline, then verified restricted external retrieval and a guest build. Browser navigation was implemented in stages 027–028 and verified again on the final kernel.

### Next milestones

Each stage below delivers a working development workflow, including the language and OS changes it needs. Completion is recorded only after independent verification. Stages 039–041 allow 16,384 characters in handoff notes to retain build steps and implementation limits.

| Experiment | Goal and acceptance criteria |
| --- | --- |
| 038 — Unmodified upstream echo (complete) | Verified in [038](experiments/038-campaign.md). Compile the exact pinned upstream `echo.c` in the guest with guest headers, libc, and startup code. No source-specific adapter or compiler special cases. Compare output and exit status with the upstream reference, and verify compiler self-rebuilds and byte-identical successive generations. |
| 039 — Multiple upstream commands (complete) | Verified unmodified sbase echo, cat, and basename with shared libc, file and console I/O, reference error outputs, and compiler self-hosting in [039](experiments/039-campaign.md). Build several unmodified commands covering string processing, standard input, and file I/O. Share headers and libc across commands and provide a repeatable build path for multiple source files. Compare normal and error cases with upstream references. |
| 040 — Develop inside the guest (complete) | Verified a guest-written editor, protected build/run workflow, redirection, append, binary pipelines and reboot reproduction in [040](experiments/040-campaign.md). Edit source, build, run, fix, save, reboot, and rebuild inside the guest. Provide a usable editor, redirection, and pipes; demonstrate commands processing each other's output and persistent files. |
| 041 — Rebuild the environment from source | Starting with a documented minimal boot environment and compiler seed, automatically rebuild the compiler, libc, and command set from exact saved sources. Boot or load the rebuilt environment, repeat the workflow tests, and compare successive compiler generations. |

For all four stages, keep upstream `.c` files byte-for-byte intact. Guest-specific headers, library implementations, startup code, and ordinary preprocessing are allowed; source-specific rewriting is not. Maintain compiler self-hosting, preserve reproducible inputs, and independently verify outputs. Record unsupported features and any build limits. Favor coherent reusable interfaces and reproducible rebuilds over elapsed time; fix regressions before advancing. Memory protection, preemptive scheduling, a fuller browser, and direct HTTPS are later, separate milestones.

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
| 小さなOS | コンソール、メモリ、プログラムのロードと終了を扱う。最初は単一タスクで、プログラムとカーネルの呼び出し規約を定める。完了（007）。アセンブル・インストール・ビルドで8 KiB（026）、続いて最大32 KiB（033）の実行コードを扱えることを確認済み。ビルド上限60,000バイトで53,772バイトの自己ホストしたコンパイラも確認済み（038）。上限65,532バイトのビルド・インストールと、その後のプロセスI/Oも確認済み（039） |
| 永続ディスクとファイルシステム | 仮想ブロックデバイスを読み書きし、再起動をまたいでソースとプログラムを保存・再読込する。完了（008・010）。UARTから最大8 KiBのファイルを取り込み、再起動後もバイト単位で一致することを確認済み（022）。ゲスト内で24ファイル・各32 KiBの形式に移行し、8 KiBを超えるアセンブリとCソースを処理できることを確認済み（031） |
| アセンブラ | ゲスト内でAArch64の命令とラベルを機械語に変換し、生成物を実行する。コンパイラをゲスト内で組み立てられる命令と容量を確認済み（009–014） |
| コンパイラ | ゲスト内アセンブラでコンパイラを組む。実行時引数・整数式・局所変数・分岐・ループを含むCサブセットを確認済み（014–015）。補助関数の定義と呼び出し（021）、空白やコメントを含む複数行のCソースを取り込んでコンパイルする処理（023）、ローカル整数のアドレス取得とポインタ経由の読み書き（024）を確認済み |
| GUIとブラウザ | フレームバッファとキー入力は完了（016）。ホストから取得したシンプルなHTMLの描画を確認済み（017）。キーボードで入力したパスで、同じ起動中にページを遷移できることを確認済み（027）。受信したHTMLから抽出したリンクをキー操作でたどれることを確認済み（028） |
| アセンブラの自己ホスト | カーネル内のアセンブラで種を作り、ゲストアプリとして自分のソースを組み立て直す。世代間で生成コードを照合する。完了（019） |
| プロセスとシステムコール | 複数のプログラムに独立したスタックと実行状態を持たせ、協調スケジューリング、終了・待機、ファイルやコンソールの入出力を扱う。協調プロセスと基本ファイル入出力は完了（018・020）。ロード済みプログラムへの argc と argv の引き渡し（029）、文字列リテラルと putchar・puts・strcmp を使うCコマンドの実行（035）を確認済み |
| Cコンパイラと最小libc | 複数関数、型、ポインタ、配列、文字列、前処理などを段階的に追加する。対象とするC規格の機能をテストし、入出力・文字列操作などのライブラリを用意する。ローカルの文字配列を実行時の添字で読み書きできること（025）と、最大4個の名前付き整数ローカル変数および関数ごとの引数名（030）を確認済み。名前付き関数と型付きポインタを扱う種コンパイラで、C製コンパイラのビルドと動作を確認済み（032）。Cのポインタ演算・短絡評価・グローバル変数・ループ・キャスト・include処理・オブジェクト形式マクロを追加し、原本のechoを無改変でビルドできることを確認済み（038）。共通のFD入出力とlibcで原本のecho・cat・basenameを動かし、条件付き前処理とswitchも確認済み（039） |
| Cコンパイラの自己ホスト | ゲストで動く種コンパイラがコンパイラ自身のCソースをビルドできるようにし、生成したコンパイラで再ビルドと回帰テストを行う。C製コンパイラによる2世代の自己ビルドがバイト単位で一致し、別のCプログラムも実行できることを確認済み（034）。言語機能の拡張後も53,772バイトの連続世代のバイト一致を確認済み（038）。共通CLI環境の64,624バイトの連続世代も一致（039）。開発シェルを含む環境でも65,412バイトの連続世代が一致（040） |
| オープンソースCLI | 観測側が版とハッシュを固定した小さなCLIのソースを投入し、ゲスト内でビルドして入出力を照合する。必要な移植差分を記録する。sbase 0.1のechoをゲスト内で移植・ビルドし、ホストでビルドした原本と入出力を照合済み（036）。続いて原本のecho.cを変換器なしでビルドし、上流版と照合済み（038）。原本のecho・cat・basenameを共通libcでビルドし、正常系・異常系を照合済み（039） |
| 外部ネットワーク | オフラインでの再現を確立した後、まず取得先を限定してソース取得からビルドまで検証する。取得先を1件に固定したホストの中継を経由してsbaseのecho.cを取得し、オフラインでビルドして上流版と照合済み（037） |

後半はCコンパイラの自己ホスト、OSと最小libcによるCコマンドの実行、既存OSSコマンドのオフラインビルドを経て、取得先を限定した外部通信とゲストでのビルドまで確認した。段階027・028で作ったブラウザのページ遷移も最終カーネルで再検証した。

### 今後のマイルストーン

今後は、必要な言語機能やOS機能をまとめて実装し、一通り使える開発手順を1段階とする。合格条件を示し、観測側の独立検証を通った段階だけ完了と記す。039〜041ではビルド手順と制約を省かず残すため、引き継ぎノートを16,384文字まで扱う。

| 実験 | 目標と合格条件 |
| --- | --- |
| 038 — 上流のechoを無改変でビルド（完了） | [038](experiments/038-campaign.md)で確認済み。版を固定した原本の`echo.c`を、ゲストのヘッダ・libc・起動処理とともにゲスト内でコンパイルする。ソース固有の変換器やコンパイラの特別扱いは使わない。出力・終了コードを上流版と照合し、コンパイラの自己ビルドと連続世代のバイト一致も確認する。 |
| 039 — 複数のOSSコマンドを動かす（完了） | [039](experiments/039-campaign.md)で原本のecho・cat・basename、共通libc、ファイルとコンソールI/O、上流版のエラー出力、自己ホストを確認済み。文字列処理・標準入力・ファイルI/Oを使う複数のコマンドを無改変でビルドする。ヘッダとlibcを共有し、複数ソースを再現可能な手順でビルドする。正常系・異常系を上流版と照合する。 |
| 040 — ゲスト内で日常的に開発する（完了） | [040](experiments/040-campaign.md)でゲスト製エディタ、失敗時に旧コードを保持するビルド・実行、リダイレクト、追記、バイナリのパイプ、再起動後の再現を確認済み。 ゲスト内でソースの編集・ビルド・実行・修正・保存・再起動後の再ビルドを完結する。使えるエディタ、リダイレクト、パイプを用意し、コマンド同士の出力と永続ファイルを処理する。 |
| 041 — ソース一式から環境を再構築する | 明記した最小起動環境と種コンパイラから、保存した正確なソースを使ってコンパイラ・libc・コマンド群を自動ビルドする。再構築した環境を起動またはロードして一連の検証を繰り返し、コンパイラの連続世代も照合する。 |

4段階を通じて、上流の`.c`はバイト単位で保持する。ゲスト向けヘッダ・ライブラリ実装・起動処理と通常のプリプロセッサは認め、ソース固有の書き換えは使わない。自己ホストを維持し、入力を再現できる形で保存して、観測側が出力を独立検証する。未対応機能とビルド容量の制約も記録する。所要時間より、再利用できる一貫した設計と再構築の確実さを優先し、回帰を直してから次へ進む。メモリ保護・プリエンプティブなプロセス・本格的なブラウザ・直接のHTTPSは、その後の別のマイルストーンとする。

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
