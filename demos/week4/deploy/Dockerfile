# Minimal agent service. Build: docker build -t agent-service .   Run: docker run -p 8080:8080 -e ANTHROPIC_API_KEY -e ASK_TOKEN agent-service
# Works on Railway, Fly.io and any container host. Secrets are passed as environment variables, never baked in.
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PORT=8080
RUN pip install --no-cache-dir "anthropic>=2.3.0" && useradd --create-home app
WORKDIR /app
COPY app.py .
USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s CMD python -c "import urllib.request,os;urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8080')+'/health',timeout=2)"
CMD ["python", "app.py"]
