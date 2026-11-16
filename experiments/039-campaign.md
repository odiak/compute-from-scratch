# 039 — 複数のOSSコマンドを動かす

2026-11-16 JST。[ステージ指示](039-campaign-prompt.txt)に沿って、原本のsbase 0.1 `echo.c`・`cat.c`・`basename.c`を、ゲスト内の共通ライブラリとヘッダでビルドした。上流ソース固有の変換器は使わず、arg.hも原文のまま読み、ARGBEGIN・ARGENDを通常のオブジェクト形式マクロとして展開する。上流入力の版・ハッシュは[マニフェスト](../fixtures/sbase-0.1/manifest.json)に固定した。

## 独立検証

観測側は空のディスクへ保存ソースを投入して検証した。コンパイラは3世代とも64,624バイトで、各生成物と実際の呼び出し先`0x40150000`へインストールされた全コードが一致した。後ろの2世代も一致した。SHA-256は`d8c8d03ffdf290c2ec3fb77e929cb5e4bd63e2ed4d05d044be57522c25d1d0ae`。

以下を確認した。

- 原本のechoの通常引数、`-n`、引数なしと、basenameの通常パス、接尾辞、ルート、末尾スラッシュ、`--`、引数・オプションエラーを上流参照と比較した。
- 原本のcatの複数ファイル、標準入力との混在、繰り返す`-`、`-u`、NUL・EOT・ランダムなバイナリを含むファイル、存在しないファイルを含めた継続、誤ったオプション、端末入力とCtrl-D、空入力を確認した。正常系・異常系の出力と終了コードが上流参照と一致した。
- [独立した前処理入力](../fixtures/c-native/preprocessor.c)と[言語の意味の入力](../fixtures/c-native/semantics.c)をビルド・実行した。無効分岐の文字列中の`#endif`、空マクロ、継続行、短絡評価と副作用なども通った。
- [独立したCプログラム](../fixtures/c-native/file-io.c)でバイナリファイルの作成・書き込み・読み戻し・EOF・読み取り専用FDへの書き込み拒否を確認した。再起動後も内容が一致した。
- 標準出力と標準エラーを別々にファイルへ振り分け、不正ソースのビルド失敗後も前の実行コードと動作が維持された。再起動後、全ビルド入力がバイト一致し、種からの再ビルドとCLI実行を再現した。
- 上限65,532バイトのプログラム生成・実行・連続ビルド・インストール全体のバイト一致を確認した。その同じVMで協調プロセスのファイルI/Oも通った。ABIの不正サイズ拒否と、HTMLリンク移動の回帰検証も通った。

## 成果物と再現

[カーネル](039-campaign.hex)、[038からのパッチ](039-kernel-patches.json)、[コンパイラ](039-compiler.c)、[中継コンパイラ](039-bootstrap-compiler.c)、[共通libc](039-libc.c)、[引き継ぎ](039-handoff.txt)を保存した。カーネルは18,640バイト。ライブラリ実装はゲストで書いたもので、上流ライブラリを無改変移植したとは主張しない。

| ゲスト名 | 保存した入力 |
| --- | --- |
| new1 / extra1 / extra3 | [032-seed.s](032-seed.s)、[034-compiler.c](034-compiler.c)、[035-compiler.c](035-compiler.c) |
| raw / extra2 | [中継](039-bootstrap-compiler.c)、[最終コンパイラ](039-compiler.c) |
| libc | [039-libc.c](039-libc.c) |
| stdioh / stringh / utilh | [stdio](039-stdio.h)、[string](039-string.h)、[util](039-util.h) |
| fcntlh / libgenh / unistdh | [fcntl](039-fcntl.h)、[libgen](039-libgen.h)、[unistd](039-unistd.h) |
| alpha / beta / extra5 / Abc123xyz789 | 原本のcat.c、basename.c、echo.c、arg.h |
| catbuild / basebuild / Check | [cat](039-cat-build.c)、[basename](039-basename-build.c)、[echo](039-echo-build.c)のビルド入力 |

ビルド入力は共通libcと原本をincludeする通常のCソースで、原本を書き換えない。関数定義を毎回手でコピーせず、複数ソースを同じ前処理・ビルド手順で扱う。ヘッダ名はドットを除いたゲスト名に対応する。ゲストでは次を各コマンド別の行で実行する。

```text
as new1
install
build extra1
install
build extra3
install
build raw
install
build extra2
install
build extra2
install
build catbuild
exec cat FILE
build basebuild
exec basename /dir/file.c .c
build Check
exec echo hello world
```

観測側の参照を作り、空ディスクから検証する手順は以下。ホストでのビルドは比較用だけで、ゲストの生成物には使わない。

```sh
cc -o .local/echo-reference fixtures/sbase-0.1/echo.c \
  fixtures/sbase-0.1/libutil/putword.c fixtures/sbase-0.1/libutil/fshut.c \
  fixtures/sbase-0.1/libutil/eprintf.c
cc -o .local/cat-reference fixtures/sbase-0.1/cat.c \
  fixtures/sbase-0.1/libutil/concat.c fixtures/sbase-0.1/libutil/writeall.c \
  fixtures/sbase-0.1/libutil/eprintf.c
cc -o .local/basename-reference fixtures/sbase-0.1/basename.c \
  fixtures/sbase-0.1/libutil/eprintf.c fixtures/sbase-0.1/libutil/fshut.c
python3 verify_shared_cli.py experiments/039-campaign.hex \
  .local/echo-reference .local/cat-reference .local/basename-reference
python3 verify_large_build.py experiments/039-campaign.hex \
  65532 0x40140000 0x40150000
python3 verify_build_abi.py experiments/039-campaign.hex
python3 verify_browser_links.py experiments/039-campaign.hex
```

## 範囲と試行経緯

ビルド上限は65,532バイト。実行コードは`0x40140000`、インストール先は`0x40150000`、コンパイラの固定作業領域は出力領域の外の`0x409e0000`。ファイル各32 KiB、前処理出力30,000バイト、平坦な24ファイル、名前12文字、FD0〜15という制約がある。Cは依然としてサブセットで、関数形式マクロの呼び出し・構造体・一般のtypedef・プロトタイプ・可変長引数・ローカル配列などは未対応。定義を使用前に置く。関数リンクの単位は結合したC入力であり、独立オブジェクトのリンカはない。

libcはopen・read・write・closeとerrno、標準FD0/1/2を用意する。文字列・パス・フォーマット・エラー処理は共通C実装。固定1文字列引数の`%s`形式で、完全なprintfではない。exit・diskcommit・開始処理は共通の実行ABIにつなぐ。コンソールの標準出力と標準エラーは同じ端末だが、FDとして独立して振り分けられる。

現在のリダイレクトはargv先頭の`< FILE`・`> FILE`・`2> FILE`に限る。`exec`の先頭語は現在の実行コードへ渡すargv0で、パスによるプログラム選択ではない。パイプ・エディタ・日常開発の一連の手順は040の対象。物理ディスクの障害注入とcatの出力容量不足経路はこの段階では未検証。

最初の試行は基準状態だけで終了したため、実装を続けるよう続行した。実装後も観測側が無効分岐の文字列処理とエラー表示の差分を発見し、追加の続行で修正した。容量を128 KiBへ広げた途中候補と配置変更は放棄し、現行レイアウトに整合する上限へ揃えた。末尾には未使用の64バイトの旧配置変更コードがあり、パッチ一覧にも含めた。新しいコード生成命令定数とカーネル差分は手計算を含む。

続行指示2回、PiのVM起動19回。観測側の起動は別に数える。途中から大きな段階の再現手順を省かず残せるよう、引き継ぎノート上限を8,192文字から16,384文字へ広げた。[トランスクリプト](039-transcript.md)を保存し、生成物を確認した。生ログ・生成コード・パケット・回帰スクリーンショットは`.local/`にある。
