# A minimal deployable agent service

`app.py` is a tiny HTTP service (Python standard library plus the `anthropic` SDK). `GET /health` for the platform's
health check; `POST /ask {"question": "..."}` for the agent. Patterns reused from `site/deploy/` (Dockerfile,
`fly.toml`, `railway.json`). **Humans deploy:** nothing here runs a deploy for you, and Claude never presses the button.

## 1. Run it on your laptop first (no key, no Docker)

```bash
cd demos
DEMO_OFFLINE=1 PORT=8080 python3 week4/deploy/app.py        # leave it running
curl -s localhost:8080/health
curl -s -X POST localhost:8080/ask -H 'Content-Type: application/json' -d '{"question":"What is a health check?"}'
```

Offline mode answers with a canned line. With `ANTHROPIC_API_KEY` set it makes one real call per question, and then
`ASK_TOKEN` is **required** (callers send `Authorization: Bearer <token>`), so a public URL cannot burn your credit.

## 2. Secrets: environment variables only

| Variable | Needed | What |
|---|---|---|
| `ANTHROPIC_API_KEY` | live mode | your key; set it in the platform, never in a file or in the image |
| `ASK_TOKEN` | live mode | a long random string you make up (`python3 -c "import secrets;print(secrets.token_urlsafe(32))"`) |
| `DEMO_MODEL` | no | default `claude-opus-5-5` |
| `APP_VERSION` | no | shown in `/health`; change it per release so you can see a deploy or a rollback happen |
| `PORT` | no | the platform usually sets it; default 8080 |

Type secrets without leaving them in your shell history: `read -rs KEY` then use `"$KEY"`.

## 3. Railway

1. Install the CLI and log in: `railway login` (or use the dashboard, "New project, Deploy from GitHub repo", root folder `demos/week4/deploy`).
2. In this folder: `railway init` (first time), then set the variables in the dashboard, Variables tab:
   `ANTHROPIC_API_KEY`, `ASK_TOKEN`, `APP_VERSION=v1`.
3. `railway up --detach` builds the `Dockerfile`; `railway.json` tells Railway to poll `/health`.
4. Domain: dashboard, Settings, Networking, "Generate domain". Then `curl https://<your-domain>/health`.
5. Logs: `railway logs` or the dashboard. Rollback: dashboard, Deployments, pick the last good one, Redeploy/Rollback.

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

VERIFY: none of the Orgo steps below were checked here. Confirm each against Orgo's current documentation first.

- VERIFY: how Orgo runs a long-lived service (a container image, or a computer you start the process on).
- If it runs a computer/VM: copy `app.py`, `pip install "anthropic>=2.3.0"`, then start it with the variables
  from section 2 set in the environment (VERIFY: where Orgo stores secrets; do not type the key into a shared screen).
- VERIFY: how to expose a port or URL, and how to read logs and stop or roll back.
- Until verified, show Orgo as the "try it, then compare" option and deploy the demo on Railway or Fly.

## 6. After the deploy

```bash
curl -s https://<your-host>/health
curl -s -H "Authorization: Bearer $ASK_TOKEN" "https://<your-host>/ask?q=hello"
```

Check the logs show one JSON line per request. Container build is untested here (no Docker in the authoring
environment): VERIFY with `docker build -t agent-service . && docker run --rm -p 8080:8080 agent-service` before class.
