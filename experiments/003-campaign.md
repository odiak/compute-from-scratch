# 003 — ARPの送受信

2026-11-04 JST。002のPiセッション、イメージ、メモを再開した。[ステージ指示](003-campaign-prompt.txt)に従い、モデルは既存のシリアル動作を保ちながらvirtio-netの送受信を追加した。

最初の起動ではPCAPにARPの要求と応答があったが、シリアルには `BOOT\n` だけが出た。モデルはイメージを修正し、同じ更新版で2回起動して異なる応答MACを表示した。続行指示は0回、モデルによるVM起動は3回。

観測側でも [最終イメージ](003-campaign.hex) を二度起動した。PCAPの要求と応答、応答元MACとシリアル表示、`BOOT\n` と入力 `A` のエコーが全て一致した。応答MACは `02:70:be:39:a7:9e` と `02:9a:ac:54:95:dc`。ネットワーク環境の準備時に参照ゲストでも同じ判定を通した。

再現は `python3 verify_arp.py experiments/003-campaign.hex`。モデルは [引き継ぎメモ](003-handoff.txt) を更新した。生ログは `.local/experiments/pi-2O5Npq/` と `.local/arp-check/` にある。
