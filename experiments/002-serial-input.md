# 002 — シリアル入力に応答する

2026-11-04 JST。Pi SDK 1.5.0、GPT-6.1 Sol、QEMU 11.1.2。

[初期プロンプト](002-serial-input-prompt.txt)で、起動直後に `?` を出し、シリアルから1バイトを受けてそのバイトとLFを返すよう依頼した。資料、過去の成果物、会話を渡さず、`run_guest` と `run_guest_with_input` だけを公開した。各呼び出しは新しいVMを起動する。

| 実行ID | 入力 | 出力 |
| --- | --- | --- |
| `20261103T211047.778882Z` | なし | `?` |
| `20261103T211054.006152Z` | `A` | `?A\n` |
| `20261103T211055.080312Z` | `z` | `?z\n` |

入力ありの2回で同じイメージを使い、期待値と出力がバイト単位で一致した。観測側の介入はなかった。保存した [イメージ](002-serial-input.hex) で、モデルが試さなかった入力 `3` も検証した。

```sh
run=$(python3 runner.py experiments/002-serial-input.hex --seconds 1 --serial-byte 51)
printf '?3\n' | cmp - "$run/serial.log"
```

生ログは `.local/experiments/pi-FY1888/` と `.local/runs/` に保存した。
