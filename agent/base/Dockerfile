# Shared by every step: Python and the agent libraries. Each step adds only its
# agent.py and prompts on top, so pulling another step costs a few KB.
FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && pip uninstall -y pip setuptools wheel >/dev/null 2>&1 || true
EXPOSE 8080
CMD ["python", "agent.py"]
