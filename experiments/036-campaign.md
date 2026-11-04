# 036 — sbase 0.1のechoをオフラインでビルド

2026-11-04 JST。[ステージ指示](036-campaign-prompt.txt)に沿って、公式リリースの [echo.c](../fixtures/sbase-0.1/echo.c) を観測側からUARTで渡した。アーカイブのSHA-256は `86f6bb67bcc7df3ba7a3f11da72eaeb2cf58c23e9a35a7dbcd316395d934c634`、421バイトのソースは `117c10e0e5a5139a80490673a3f14dd1dfcc45856adb84a83b28e3b301f1b48c`。配布元の[アーカイブ](https://dl.suckless.org/sbase/sbase-0.1.tar.gz)と[ライセンス](../fixtures/sbase-0.1/LICENSE)を参照。

Piは[ゲスト内で動くCの変換器](036-adapter.c)を書いた。変換器は受け取ったソースを読み、対応外の制御構文と引数配列の表現を置き換え、コンソール用の互換関数を先頭に足す。変換後のCは、変換器が出力したシェルコマンドをシリアル経由でそのまま返して保存する。[保存した移植版](036-echo-port.c)を既存のゲストCコンパイラでビルドした。互換層の `fshut` は成功を返す。現在のゲストコンソールには出力エラーを通知する仕組みがない。

観測側は別のVMに原本を再投入して移植版を再生成し、保存した版とバイト単位で照合した。ゲストでビルドしたコマンドと、ホストで同じ版の原本からビルドしたコマンドの出力と終了コードを6パターンで比較した。引数なし、ランダムな引数、先頭の `-n`、途中の `-n` を含む。原本の改行リテラルだけをタブに変える試験では、生成したコマンドの出力もタブに変わった。元のソース、カーネル、保護対象ファイルは維持された。続行指示は0回。

ホストの比較用バイナリはアーカイブを展開し、以下でビルドした。

```sh
cc -o ../echo-reference echo.c libutil/putword.c libutil/fshut.c libutil/eprintf.c
```

```sh
python3 verify_sbase_echo.py experiments/033-campaign.hex experiments/032-seed.s \
  experiments/034-compiler.c experiments/035-compiler.c experiments/036-adapter.c \
  fixtures/sbase-0.1/echo.c /path/to/echo-reference experiments/036-echo-port.c
```

[引き継ぎメモ](036-handoff.txt)と[トランスクリプト](036-transcript.md)を保存した。
