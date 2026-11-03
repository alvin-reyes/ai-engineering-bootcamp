"""Criterion: Ship it. The container and platform files say what the platform needs; no secret is in the repo."""
import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "deploy"


def test_dockerfile_basics():
    df = (D / "Dockerfile").read_text()
    lines = [ln.strip() for ln in df.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    assert any(ln.startswith("FROM python:3.") for ln in lines), "start from a python 3 image"
    assert any(ln.startswith("COPY") and "app.py" in ln for ln in lines), "copy app.py into the image"
    assert any(ln.startswith("CMD") and "app.py" in ln for ln in lines), "start the service with CMD"
    assert any(ln.startswith("EXPOSE") and "8080" in ln for ln in lines)
    assert any(ln.startswith("HEALTHCHECK") and "/health" in ln for ln in lines)
    users = [ln for ln in lines if ln.startswith("USER")]
    assert users and users[-1].split()[1] not in ("root", "0"), "run as a non-root user"


def test_dockerfile_bakes_in_no_secret():
    for ln in (D / "Dockerfile").read_text().splitlines():
        if re.match(r"\s*(ENV|ARG)\b", ln):
            assert not re.search(r"(API_KEY|TOKEN|SECRET)\s*=?\s*\S", ln), f"secret in image: {ln}"


def test_fly_toml():
    cfg = tomllib.loads((D / "fly.toml").read_text())
    assert cfg["app"] and "CHANGE-ME" not in cfg["app"], "pick your own app name"
    svc = cfg["http_service"]
    assert svc["internal_port"] == 8080 and svc["force_https"] is True
    assert any(c["path"] == "/health" for c in svc["checks"])
    assert not any(re.search(r"KEY|TOKEN|SECRET", k, re.I) for k in cfg.get("env", {})), "secrets go in `fly secrets`"


def test_railway_json():
    cfg = json.loads((D / "railway.json").read_text())
    assert cfg["build"]["builder"] == "DOCKERFILE"
    assert cfg["deploy"]["healthcheckPath"] == "/health"
    assert cfg["deploy"]["healthcheckTimeout"] >= 10


def test_deploy_readme_covers_both_platforms_and_humans_deploy():
    text = (D / "README.md").read_text()
    for needle in ("Railway", "Fly", "Orgo", "VERIFY", "/health", "ASK_TOKEN", "ANTHROPIC_API_KEY", "rollback"):
        assert needle.lower() in text.lower(), f"README should mention {needle}"
    assert "you press deploy" in text.lower() or "humans deploy" in text.lower()


def test_no_secrets_anywhere_in_the_repo():
    pattern = re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}|ANTHROPIC_API_KEY\s*=\s*[\"']?[A-Za-z0-9_-]{8,}")
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".md", ".toml", ".json", ".txt", ".ini", ""} and "__pycache__" not in p.parts:
            m = pattern.search(p.read_text(errors="ignore"))
            assert not m, f"possible secret in {p.relative_to(ROOT)}: {m.group(0)[:12]}..."
