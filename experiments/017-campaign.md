# 017 — ホストから取得したHTMLを画面に描画

2026-11-04 JST。016を引き継ぎ、[ステージ指示](017-campaign-prompt.txt)を実行した。Piは既存TCPコードを使ってホストの `/index.html` を取得し、`h1` と `p` の内容を自作のビットマップフォントで描いた。[レンダラー](017-renderer.s) と [統合用コード](017-integration.s) はゲストのアセンブラで組み立て、[カーネルイメージ](017-campaign.hex) に統合した。

観測側は同一イメージで異なるページを受信した。PCAPのGET、ホストのアクセスログ、FINへのACKを照合し、スクリーンショットの文字をOCRと目視で確認した。シリアルシェル、通常のGUIナビゲーション、従来の `/hello` 起動も維持された。

| 表示内容 | スクリーンショット |
| --- | --- |
| GREEN FIELD / OPEN WINDOW | [画面](017-green-field.png) |
| BLUE MOON / FRESH PAGE | [画面](017-blue-moon.png) |

最終テスト後のWebSocketエラーで引き継ぎメモが未保存だったため、観測結果を添えて1回続行を依頼した。[引き継ぎメモ](017-handoff.txt)にソースとイメージの配置を残した。再現は `python3 verify_browser.py experiments/017-campaign.hex`（ImageMagickとTesseractが必要）。
