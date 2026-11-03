# 006 — シリアルシェル

2026-11-04 JST。005のセッションと成果物を再開し、[ステージ指示](006-campaign-prompt.txt)を渡した。モデルは [HTTPゲストのイメージを拡張](006-campaign.hex)し、行入力と `help`、`echo`、未知のコマンドへの応答を実装した。モデルによるVM起動は2回、続行指示は0回。

観測側は保存した同一イメージをNICなしとHTTP付きで起動した。それぞれ同じVMで任意の文字列を `echo` でき、長い入力を破棄した後に `help` が動いた。HTTP付きではホストの本文とFINへのACKも照合した。

再現は `python3 verify_shell.py experiments/006-campaign.hex`。[引き継ぎメモ](006-handoff.txt)に入口と行バッファの配置がある。生ログは `.local/experiments/pi-2O5Npq/` と `.local/shell-check/`。
