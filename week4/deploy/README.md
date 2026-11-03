# Deploy kit: a minimal agent service

`app.py` is a tiny HTTP service (Python standard library plus the `anthropic` SDK). `GET /health` is for the
platform's health check; `POST /ask {"question": "..."}` is the agent. **Humans deploy:** nothing in this kit runs a
deploy for you, and you press the button yourself. Your trainer shows the path in Thursday's Session 2.

Make it yours: replace `SYSTEM` and the body of `answer()` in `app.py` with your capstone's agent (call your own
function there), keep `/health` cheap (no model call), and keep the log line free of questions and secrets.

## 1. Run it on your laptop first (no key, no Docker)

```bash
cd deploy
DEMO_OFFLINE=1 PORT=8080 python3 app.py        # leave it running
curl -s localhost:8080/health
curl -s -X POST localhost:8080/ask -H 'Content-Type: application/json' -d '{"question":"What is a health check?"}'
```

Offline mode answers with a canned line. With `ANTHROPIC_API_KEY` set it makes one real call per question, and then
`ASK_TOKEN` is **required** (callers send `Authorization: Bearer <token>`), so a public URL cannot burn your credit.

## 2. Secrets: environment variables only

| Variable | Needed | What |
|---|---|---|
| `ANTHROPIC_API_KEY` | live mode | your key; set it in the platform, never in a file or in the image |
| `ASK_TOKEN` | live mode | a long random string: `python3 -c "import secrets;print(secrets.token_urlsafe(32))"` |
| `MODEL` | no | model id (VERIFY the id you will use) |
| `APP_VERSION` | no | shown in `/health`; change it each release so you can see a deploy or rollback happen |
| `PORT` | no | the platform usually sets it; default 8080 |

Type secrets without leaving them in your shell history: `read -rs KEY`, then use `"$KEY"`. Never commit a `.env`.

## 3. Railway

1. Install the CLI and log in: `railway login` (or use the dashboard: New project, Deploy from GitHub repo, root folder `deploy`).
2. In this folder: `railway init` (first time). In the dashboard, Variables tab, set `ANTHROPIC_API_KEY`, `ASK_TOKEN`, `APP_VERSION=v1`.
3. `railway up --detach` builds the `Dockerfile`; `railway.json` tells Railway to poll `/health`.
4. Domain: dashboard, Settings, Networking, Generate domain. Then `curl https://<your-domain>/health`.
5. Logs: `railway logs` or the dashboard. Rollback: dashboard, Deployments, pick the last good one, redeploy it.

VERIFY: menu names and CLI flags move; check Railway's current docs.

## 4. Fly.io

```bash
fly auth login
fly launch --copy-config --no-deploy        # edit the app name in fly.toml first; say no to a database
read -rs KEY; fly secrets set ANTHROPIC_API_KEY="$KEY" ASK_TOKEN="$(python3 -c 'import secrets;print(secrets.token_urlsafe(32))')"
fly deploy
fly status && fly logs
curl https://<your-app>.fly.dev/health
```

Rollback: `fly releases --image` lists releases with their images; deploy the last good one with
`fly deploy --image <image>` (VERIFY the flag on the current Fly docs). Scale to zero is on in `fly.toml`
(`min_machines_running = 0`): the first request after idle is slow.

## 5. Orgo

VERIFY: none of the Orgo steps below were checked. Confirm each against Orgo's current documentation first.

- VERIFY: how Orgo runs a long-lived service (a container image, or a computer you start the process on).
- If it runs a computer or VM: copy `app.py`, `pip install "anthropic>=2.3.0"`, then start it with the variables from
  section 2 set in the environment (VERIFY: where Orgo stores secrets; do not type the key into a shared screen).
- VERIFY: how to expose a port or URL, how to read logs, how to stop or roll back.
- Until verified, treat Orgo as the "try it and compare" option and deploy the demo on Railway or Fly.

## 6. After the deploy

```bash
curl -s https://<your-host>/health
curl -s -H "Authorization: Bearer $ASK_TOKEN" "https://<your-host>/ask?q=hello"
```

Check the logs show one JSON line per request. The Dockerfile has not been built by the author of this kit (no Docker
there): VERIFY with `docker build -t agent-service . && docker run --rm -p 8080:8080 agent-service` before you rely on it.
