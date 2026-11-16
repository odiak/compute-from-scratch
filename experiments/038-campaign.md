# 038 — 上流のechoを無改変でビルド

2026-11-16 JST。[ステージ指示](038-campaign-prompt.txt)に沿って、原本のsbase 0.1 `echo.c`を変換器なしでゲスト内ビルドした。コンパイラは構文を処理し、includeとオブジェクト形式マクロを展開する。上流ソース固有の書き換え・ファイル名やハッシュによる特別扱いはない。

## 独立検証

観測側は空のディスクに、保存した種・Cコンパイラ・ヘッダ・上流ソースをUARTで投入して検証した。

- アセンブリの種、034、035、中継コンパイラを経て、最終コンパイラを3回ビルド。すべて53,772バイトで、後ろの2世代がバイト一致した。SHA-256は`7bc5230bf99540f4f909ff17c53c77bbbb87a9747e435f62e9ba8ecbf6f87460`。インストールされたコードとの一致もQMPで確認した。
- 421バイトの原本`echo.c`を直接ビルド。同じ上流版をホストでビルドした参照と、引数なし、ランダムな引数、`-n`のみ、先頭・途中の`-n`、`--`について出力と終了コードを比較した。同じバイナリを繰り返し実行しても一致した。
- 別名の入力で改行リテラルをタブへ変更すると、出力の終端も変わった。原本は変更されなかった。
- [独立したCコード](../fixtures/c-native/semantics.c)で短絡評価と副作用、ポインタ演算、条件演算子、代入式、カンマ式、ループを確認した。不正ソースの拒否後も、直前の実行ファイルのバイト列と実行結果は維持された。
- 再起動後も入力が全バイト一致し、種からの再ビルドと上流版との比較を再現した。
- ABIのゼロ・短すぎるサイズ・非整列サイズ・渡した容量超過の拒否と、前のプログラム維持を確認した。引数渡し、協調プロセスのファイルI/O、HTMLリンク移動も回帰検証を通った。

## 成果物と再現

[最終イメージ](038-campaign.hex)と[037からのパッチ一覧](038-kernel-patches.json)を保存する。カーネルは18,576バイト。コンパイラを含む実行コードの生成はすべてゲスト内で行った。

| ゲスト名 | 保存した入力 | 役割 |
| --- | --- | --- |
| new1 / extra1 / extra3 | [032-seed.s](032-seed.s)、[034-compiler.c](034-compiler.c)、[035-compiler.c](035-compiler.c) | 既存の種と中継 |
| raw | [038-bootstrap-compiler.c](038-bootstrap-compiler.c) | 新しい構文を扱う中継コンパイラ |
| extra2 | [038-compiler.c](038-compiler.c) | 自己ホストする最終コンパイラ |
| stdioh / stringh / utilh | [038-stdio.h](038-stdio.h)、[038-string.h](038-string.h)、[038-util.h](038-util.h) | ゲストで書いた共通のコンソール用定義 |
| extra5 | [echo.c](../fixtures/sbase-0.1/echo.c) | 無改変の上流ソース |

`raw`は以前のecho変換器を置き換えたコンパイラで、上流ソースを変換しない。ライブラリ実装はすべてゲストで書いたもので、上流ライブラリの無改変移植ではない。平坦なファイル名へ対応するため、include名からドットを除いて完全一致で検索する（`stdio.h`→`stdioh`）。特定のヘッダ名や枠による分岐はない。

ゲストでは次を1コマンドずつ別の行で実行する。

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
build extra5
exec echo hello world
```

観測側の再現手順は以下。ホストのビルドは比較用で、ゲストの生成物には使わない。

```sh
cc -o .local/echo-reference fixtures/sbase-0.1/echo.c \
  fixtures/sbase-0.1/libutil/putword.c fixtures/sbase-0.1/libutil/fshut.c \
  fixtures/sbase-0.1/libutil/eprintf.c
python3 verify_native_echo.py experiments/038-campaign.hex \
  experiments/038-bootstrap-compiler.c experiments/038-compiler.c \
  experiments/038-stdio.h experiments/038-string.h experiments/038-util.h \
  .local/echo-reference
python3 verify_build_abi.py experiments/038-campaign.hex
python3 verify_exec_argv.py experiments/038-campaign.hex
python3 verify_process_io.py experiments/038-campaign.hex
python3 verify_browser_links.py experiments/038-campaign.hex
```

## 制約と試行経緯

ビルド上限60,000バイト、状態領域2,048バイトで、生成コードの実質上限は57,952バイト。ファイルは各32 KiB、前処理出力は30,000バイトまで。32関数、16グローバル、関数ごと32ローカル、4引数まで。現在のメモリ配置に合わせて32ビットの整数でもアドレスを保持し、argvのポインタ枠は64ビット。コンパイラのポインタ・整数変換は明示的キャストへ移行した。固定作業領域を使い、再入可能ではない。

依然としてCのサブセットで、構造体・typedef・プロトタイプ・可変長引数・sizeof・ローカル配列・関数形式マクロ・条件付き前処理などは未対応。関数は使用前に定義する。標準C全体への適合を示す実験ではない。

ライブラリは即時シリアル出力を扱う最小構成。`stdout`は唯一のストリームで、バッファと出力エラー通知がないため`fshut`は成功を返す。通常のファイルstdio・標準入力・標準エラーは039の対象となる。

最初はポインタ拡張だけで原本をコンパイルできず、未達条件を渡して続行した。[中間コンパイラ](038-pointer-compiler.c)、[移行用ユーティリティ](038-compiler-migration.c)、[中間引き継ぎ](038-pointer-handoff.txt)も保存した。`verify_c_pointer_bootstrap.py`でこの中間成果を再現できる。

続行中に、命令補正処理が新しい命令を壊す問題、作業領域の重複、繰り返し実行時のグローバル状態残存を修正した。無改変ビルドが通った候補でも、観測側がABIの容量超過を誤って受理する回帰を発見し、追加の続行で修正した。新しいコード生成命令定数は手計算を含む。カーネルの容量比較に使う命令はゲストのアセンブラでも確認した。

Piへの続行指示は2回、PiのVM起動は18回。観測側の独立検証の起動は別に数える。詳細は[引き継ぎ](038-handoff.txt)と[トランスクリプト](038-transcript.md)を参照。生ログ・生成コード・パケット・回帰スクリーンショットは`.local/`にある。
