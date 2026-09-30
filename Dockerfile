# STAGE 1: Builder
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# STAGE 2: Hardened Runtime
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.10/site-packages"

WORKDIR /app

COPY --from=builder /install /install
COPY --chown=pwuser:pwuser . /app

RUN mkdir -p /app/allure-results /app/artifacts /app/state /tmp && \
    chown -R pwuser:pwuser /app /tmp

USER pwuser

CMD ["pytest", "--env=qa", "--alluredir=allure-results"]
