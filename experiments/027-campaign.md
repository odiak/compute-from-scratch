# 027 — キーボードでパスを入力してページを移動

2026-11-04 JST。[ステージ指示](027-campaign-prompt.txt)に沿って、物理キーで入力した最大24バイトのパスを、EnterでHTTPリクエストに変換した。Piはゲストのアセンブラで主要部分を組み立て、既存のTCP処理とHTML描画につないだ。取得のたびにネットワークとキーボードを初期化し、VMの起動をまたがず次の入力を受け付ける。

観測側の初回検証で、ピリオドがリクエストから落ちることが分かった。観測結果を伝える続行指示1回で修正した。最終版では、キー入力のみでランダムな2つのパスを「1ページ目 → 2ページ目 → 1ページ目」と移動した。2ページ目は24バイトのパスで、英小文字、数字、ハイフン、ピリオドを含む。PCAPとサーバーログでGETを、OCRで画面表示を照合した。従来のGUI、単一ページ表示、プロセス入出力、8 KiBの実行コード、Cの配列も回帰検証を通った。

| キーボードで入力したパス | 画面 |
| --- | --- |
| `/a8eaedc7` | [GREEN FIELD / OPEN WINDOW](027-first.png) |
| `/b12d9e5130a38a3d97-x.xy` | [BLUE MOON / FRESH PAGE](027-second.png) |
| `/a8eaedc7` | [GREEN FIELD / OPEN WINDOW](027-return.png) |

再現は `python3 verify_browser_paths.py experiments/027-campaign.hex`（ImageMagickとTesseractが必要）。[最終イメージ](027-campaign.hex)、[ゲストアセンブリ](027-navigation.s)、[統合パッチと引き継ぎメモ](027-handoff.txt)、[トランスクリプト](027-transcript.md)を保存した。
