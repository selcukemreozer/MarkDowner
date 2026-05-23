---
title: Markdowner
emoji: 🍃
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Markdowner

Convert your files to clean **Markdown** — in the browser or from the terminal. Powered by Microsoft's [markitdown](https://github.com/microsoft/markitdown).

Supports **PDF, Word, Excel, PowerPoint, HTML, CSV, JSON, images, audio** and more.

---

## Vision

AI subscriptions are expensive, and the limits run out faster than you would expect. A student on a tight budget can burn through their daily or monthly quota in a single study session — one long PDF, a few lecture slides, a couple of spreadsheets, and suddenly the assistant stops responding right when it is needed most.

A big part of that cost is hidden in **how** documents are fed to the model. PDFs, Word files, and slide decks carry a lot of formatting overhead. When that bloat is pasted into a chat, it is silently converted into tokens — and tokens are exactly what you pay for, both in money and in rate limits.

**Markdowner exists to fix that.** It turns heavy documents into clean, minimal Markdown that preserves the meaning — headings, tables, lists — while stripping the noise. The same content reaches the model in **fewer tokens**, which means:

- More questions before you hit the limit
- Faster responses
- Lower cost per conversation

The goal is simple: help students (and anyone learning on a budget) get more out of every token, so an expensive subscription stretches further and the limits stop getting in the way of learning.

---

## Two ways to use it

| | Web App | CLI |
|---|---|---|
| **For** | Anyone (no terminal needed) | Terminal users |
| **How** | Drag & drop in the browser | Interactive menu in the terminal |
| **File** | `app.py` | `file_converter.py` |

---

## Web App

A single-page app: drag & drop files, preview the Markdown, download individual `.md` files or all of them as a `.zip`. Files are processed in memory and never stored.

Converting to clean Markdown means **fewer tokens** when you paste content into AI chats — faster responses and lower cost.

### Run locally

```bash
git clone https://github.com/YOUR_USERNAME/markdowner.git
cd markdowner
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5001** in your browser.

> Change the port with `PORT=8080 python app.py`.

---

## CLI

An interactive terminal menu: browse directories, pick files with the spacebar, and convert them. Output goes to a `converted/` folder.

### Install globally with pipx

```bash
pipx install .
```

Now run `markdowner` from **any directory**:

```bash
markdowner
```

- **Convert files to Markdown** — pick files (SPACE to toggle, ENTER to confirm)
- **Change directory** — browse folders before converting
- **Exit**

> After editing the code, refresh the install with `pipx install . --force`.

---

## Deploy (share with anyone via a link)

This repo is ready to deploy to **Render**, **Railway**, or any host that supports Python + gunicorn.

The app is served via `gunicorn` using the `Procfile`:

```
web: gunicorn app:app
```

### Render (free)
1. Push this repo to GitHub.
2. On [render.com](https://render.com) go to **New > Web Service** and connect your repo.
3. **Build command:** `pip install -r requirements.txt`
4. **Start command:** `gunicorn app:app`
5. Deploy — you get a public URL like `https://markdowner.onrender.com`.

---

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt` (`markitdown[all]`, `flask`, `inquirer`, `gunicorn`)
- **Optional:** [ffmpeg](https://ffmpeg.org/) — only needed to transcribe audio/video files (`brew install ffmpeg`)

---

## License

MIT
