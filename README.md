# Vikas Madgula — Portfolio

Personal portfolio for **Vikas Madgula**, AI/ML Engineer & Full Stack Developer.

- **Frontend** — Plain HTML/CSS/JS, hosted on GitHub Pages
- **Backend** — FastAPI (Python), deployed on Render (free tier)

---

## Project structure

```
vikas-portfolio/
├── frontend/
│   ├── index.html          # Main single-page portfolio
│   ├── css/
│   │   └── style.css       # All styles (dark theme, responsive)
│   └── js/
│       └── main.js         # Nav, blog fetch, contact form
│
├── backend/
│   ├── main.py             # FastAPI app entry point
│   ├── requirements.txt
│   ├── .env.example        # Copy to .env with your SMTP credentials
│   └── routers/
│       ├── blog.py         # GET /blog, GET /blog/{slug}, POST /blog
│       └── contact.py      # POST /contact (sends email in background)
│
└── README.md
```

---

## Local development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # Edit .env with your SMTP credentials
uvicorn main:app --reload       # Runs on http://localhost:8000
```

API docs auto-generated at: `http://localhost:8000/docs`

### Frontend

Open `frontend/index.html` with [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) in VS Code, or:

```bash
cd frontend
python -m http.server 5500
# Open http://localhost:5500
```

> **Note:** The blog and contact form will hit `API_BASE` in `js/main.js`.
> Change it to `http://localhost:8000` for local development.

---

## Deployment

### Backend → Render

1. Push the repo to GitHub.
2. Go to [render.com](https://render.com) → **New Web Service**.
3. Connect your repo, set **Root Directory** to `backend`.
4. **Build command:** `pip install -r requirements.txt`
5. **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `.env.example` under **Environment**.
7. Note your Render URL (e.g. `https://vikas-portfolio-api.onrender.com`).

### Frontend → GitHub Pages

1. In `frontend/js/main.js`, set `API_BASE` to your Render URL.
2. In `backend/main.py`, update `allow_origins` with your GitHub Pages URL.
3. Push to GitHub.
4. Go to **Settings → Pages**, set source to the `main` branch, `/frontend` folder (or root if you move files).
5. Your site will be live at `https://<your-username>.github.io/<repo-name>/`.

---

## Adding blog posts

**Option A — Edit `blog.py` directly** (simplest):
Add entries to the `_posts` list in `backend/routers/blog.py` and redeploy.

**Option B — Use the API**:
```bash
curl -X POST https://your-api.onrender.com/blog \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "my-new-post",
    "title": "My new post",
    "excerpt": "A short summary.",
    "content": "Full markdown content here.",
    "tag": "LLMs"
  }'
```
> Add an API key check to `POST /blog` before exposing this publicly.

---

## Customisation checklist

- [ ] `backend/main.py` — Replace `allow_origins` URL with your GitHub Pages URL
- [ ] `frontend/js/main.js` — Set `API_BASE` to your Render backend URL
- [ ] `backend/.env` — Add your Gmail app password for contact form emails
- [ ] `frontend/index.html` — Add links to your GitHub / LinkedIn profiles
- [ ] `frontend/index.html` — Add real GitHub links to project cards

---

## Stack

| Layer | Tech |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Python 3.12, FastAPI, Uvicorn |
| Email | Python smtplib (Gmail SMTP) |
| Frontend hosting | GitHub Pages |
| Backend hosting | Render (free tier) |
| Fonts | Syne, DM Mono, DM Sans (Google Fonts) |

---

## License

MIT — free to use as a base for your own portfolio.
