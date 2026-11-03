# 007 — 小さなOSとプログラムローダー

2026-11-04 JST。006を引き継ぎ、[ステージ指示](007-campaign-prompt.txt)に沿って `load` と `run` を追加した。単一タスクでアプリを呼び、コンソールサービスと終了コードの受け渡しを実装した。モデルによるVM起動は2回、続行指示は0回。

観測側は [最終イメージ](007-campaign.hex) を通常起動とHTTP付き起動の両方で検証した。ランダムな終了コードを返すプログラム、文字を出してから別のコードを返すプログラム、不正なロード後の再実行、実行後のシェルへの復帰がいずれも成功した。HTTP付き起動では従来のHTTP本文取得も照合した。

再現は `python3 verify_os.py experiments/007-campaign.hex`。[引き継ぎメモ](007-handoff.txt)にABIとメモリ配置を記録した。生ログは `.local/experiments/pi-2O5Npq/` と `.local/os-check/`。
