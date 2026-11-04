# 035 — Cから引数と標準出力を扱う

2026-11-04 JST。[ステージ指示](035-campaign-prompt.txt)に沿って、自己ホスト済みのCコンパイラをCで拡張した。`main(int argc, char **argv)` はシェルの実際の64ビットポインタ配列を受け取る。文字・文字列リテラルを追加し、`putchar` を既存のコンソール出力に接続した。その上に[再利用可能なCのputsとstrcmp](035-libc.c)を置いた。

観測側は、拡張コンパイラをCから作り、同じソースの自己ビルドを2回繰り返して生成物が一致することを確認した。別のCプログラムでは、`argv[argc]`、引数がない場合、大小文字が異なる場合、一致する場合を試した。ランダムな引数が画面出力に反映され、文字リテラルとエスケープ付き文字列から改行が出て、各ケースで期待する終了コードになった。

初期候補のコンソール呼び出しはシェルへ戻らなかった。通信切断後、観測結果を渡す続行指示を1回行った。カーネルと保護対象の21ファイルはバイト単位で一致した。

再現は `python3 verify_c_cli.py experiments/033-campaign.hex experiments/032-seed.s experiments/034-compiler.c experiments/035-compiler.c experiments/035-libc.c`。[コンパイラ](035-compiler.c)、[実演用プログラム](035-demo.c)、[ABIと文法](035-handoff.txt)、[トランスクリプト](035-transcript.md)を保存した。
