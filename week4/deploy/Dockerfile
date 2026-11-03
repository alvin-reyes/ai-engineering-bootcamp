# Minimal agent service. Build: docker build -t agent-service .
# Run: docker run -p 8080:8080 -e ANTHROPIC_API_KEY -e ASK_TOKEN agent-service
# Secrets are passed as environment variables at run time. Never put them in this file.
#
# TODO: write the image. It needs to:
#   - start FROM a python 3 image (slim is fine)
#   - install the anthropic SDK (pin a minimum version) and create a non-root user
#   - COPY app.py into the image
#   - run as that user (USER) and EXPOSE 8080
#   - HEALTHCHECK by calling /health on the port
#   - CMD that starts app.py
# Reference for the pattern: demos/week4/deploy/Dockerfile (read it, then write your own).
FROM python:3.12-slim
