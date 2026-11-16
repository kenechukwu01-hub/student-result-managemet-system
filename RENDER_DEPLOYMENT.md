# Deploying the web app on Render

1. Push the complete project, including `app.py`, `templates/`, `static/`, `requirements.txt` and `Procfile`, to GitHub.
2. Sign in to Render and create a **New Web Service**.
3. Connect the GitHub repository.
4. Choose a free instance if the free option is available.
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Deploy. Render will provide a public `onrender.com` URL.

The project stores records in `data/students.json`. Free hosting filesystems may be temporary, so records can be lost on restart/redeploy. Use a persistent database before using this for real school records.
