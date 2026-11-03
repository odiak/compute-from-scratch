# Compute from Scratch

GPT-6.1 Solが、ベアメタル環境で機械語からどこまでソフトウェアスタックを構築できるかを観察する実験。

## Piの継続実験

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

## 判定と再開

観測側がログと成果物を照合して完了を判定する。試行回数は固定しない。モデルが作業を終えても条件を満たしていなければ、`node pi/run.mjs 002 "$campaign" --continue "未達の合格条件" "実際に観測した結果"` で同じセッションに続きを依頼する。原因の推測や修正方法は書かず、期待した出力と観測したバイト列、PCAPの送受信の有無などの確認事実に限る。各ステージの結果には `*-prompts.jsonl` の `mode == "--continue"` の件数と、VM起動回数を別々に記録する。

Piの圧縮開始・終了は、理由と結果を含むSDKイベントとして時刻付きで `*-events.jsonl` に残す。

会話を切り替えるときは `node pi/run.mjs 002 "$campaign" --fresh` で新規セッションを作り、保存済みのイメージとメモを引き継ぐ。シリアル読み取りには最大5秒の待ち時間を指定でき、VM自体は動き続ける。

## 観測側の起動テスト

Python 3と `qemu-system-aarch64` が必要。macOSでは `brew install qemu` で入手できる。

```sh
run=$(python3 runner.py fixtures/serial-smoke.hex)
cat "$run/serial.log"
```

`O` と改行が出れば成功。サンプルは出力後にループするので、既定の2秒でランナーがQEMUを停止する。各実行のバイナリ、シリアル、QEMUの標準エラー、実行条件は `.local/runs/` に保存する。

## ARPの観測

```sh
node pi/run.mjs 003 "$campaign"
python3 verify_arp.py "$campaign/work/guest.hex"
```

003では専用のEthernetリンクを追加する。ホスト側の応答役は起動ごとに異なるMACでARPに応答する。リンクはQEMUと応答役をソケットで直結し、外部への転送経路を持たない。観測側は同一イメージを2回起動し、両方のPCAPにARP要求・応答があり、応答元MACがシリアル出力と一致することを確認する。起動メッセージとシリアルエコーも検証する。

観測側の参照ゲストは `python3 verify_arp.py fixtures/arp-reference.hex --reference` で確認できる。参照バイナリを再生成する場合は `python3 fixtures/build-arp-reference.py > fixtures/arp-reference.hex` を実行する。

## TCPの観測

```sh
node pi/run.mjs 004 "$campaign"
python3 verify_tcp.py "$campaign/work/runs/$run_id"
```

004の専用応答役は、ポート2323で `ping\n` を受け、起動ごとに異なる応答を返す。観測側はTCPのチェックサム、ハンドシェイク、要求、応答のACK、シリアル表示を照合する。

## HTTPの観測

```sh
node pi/run.mjs 005 "$campaign"
python3 verify_http.py "$campaign/work/runs/$run_id"
```

005ではゲストの `GET /hello HTTP/1.0` を固定のローカルHTTPオリジンへ渡す。観測側はPCAP、ホストのアクセスログ、シリアル出力を照合する。オリジンは起動ごとに異なる識別子を本文に含める。
