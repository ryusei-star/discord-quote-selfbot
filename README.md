# discord-quote-selfbot

返信されたメッセージを画像として投稿する Discord selfbot です。  
VoidAPI を使って "Make it a Quote" 風の画像を生成します。

## 注意

セルフボットの使用は Discord の利用規約に反する可能性があります。使用は自己責任で行ってください。

## セットアップ

1. 依存をインストール：

```bash
pip install -r requirements.txt
````

2. `.env` を `.env.example` から作成：

```bash
cp .env.example .env
```

3. 起動：

```bash
python3 bot.py
```

## 使い方

返信した状態で `.miq` と送信すると、元メッセージの画像を投稿します。

## ライセンス

MIT
