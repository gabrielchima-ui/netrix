# Display NETRIX Online (public URL)

Choose **one** path. **Render** is the simplest for Flask. **Vercel** works if you already use it.

> Production needs **PostgreSQL** (not SQLite). Free options: Neon, Supabase, Render Postgres.

---

## Option A — Render.com (recommended)

### 1. Push code to GitHub
```bash
cd netrix
git init
git add .
git commit -m "NETRIX online"
git branch -M main
git remote add origin https://github.com/YOUR_USER/netrix.git
git push -u origin main
```

### 2. Create web service on Render
1. Go to https://render.com → **New** → **Web Service**
2. Connect your GitHub `netrix` repo
3. Settings:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt -r requirements-prod.txt`
   - **Start command:** `gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`
4. Add **PostgreSQL** (New → PostgreSQL) and copy the **Internal/External Database URL**

### 3. Environment variables on Render
| Key | Value |
|-----|--------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | long random string |
| `DATABASE_URL` | Postgres URL from Render/Neon |
| `BOOTSTRAP_ADMIN_EMAIL` | your private admin email |
| `BOOTSTRAP_ADMIN_PASSWORD` | your private strong password |

### 4. Deploy
Click **Deploy**. When live, open:
`https://YOUR-SERVICE.onrender.com`

Health check: `https://YOUR-SERVICE.onrender.com/health`

### 5. Custom domain (Namecheap etc.)
Render → Settings → Custom Domains → add your domain.  
At Namecheap Advanced DNS, add the **CNAME** Render shows (e.g. `www` → `your-service.onrender.com`).

---

## Option B — Vercel

1. Import the GitHub repo at https://vercel.com
2. Set the same environment variables as above (`DATABASE_URL` must be Postgres, e.g. Neon)
3. Deploy → open `https://your-project.vercel.app`
4. Add domain under Project → Domains; point Namecheap DNS to Vercel

Entrypoint: `api/index.py` + `vercel.json`

---

## Option C — Railway

1. https://railway.app → New Project → Deploy from GitHub
2. Add Postgres plugin
3. Variables: `SECRET_KEY`, `FLASK_ENV=production`, `DATABASE_URL` (auto from plugin)
4. Start command: `gunicorn run:app --bind 0.0.0.0:$PORT`

---

## After it is online

1. Open the public URL
2. Users: **Register** / **Login**
3. You: login with the **admin** email/password you set in env vars (never published on the page)
4. Admin Console → monitor users & projects; Site Settings → update frontend text

---

## Local still works

```bash
python run.py
```
→ http://127.0.0.1:5000 (SQLite)

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| 500 on first load | Check `DATABASE_URL` is Postgres and reachable |
| Login cookie issues | Ensure site is **https**; `SESSION_COOKIE_SECURE` is on in production |
| Build fails on psycopg2 | Use `requirements-prod.txt` only on the host; local can use `requirements.txt` alone |
| Sleeping free tier | Render free services sleep; first request may take ~30s |
