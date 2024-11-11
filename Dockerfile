FROM python:3.12.1 AS builder

RUN --mount=type=bind,source=requirements.txt,target=/app/requirements.txt \
  pip wheel --no-cache-dir --no-deps -r /app/requirements.txt --wheel-dir /app/wheels



FROM python:3.12.1-alpine

RUN apk add --no-cache shadow

RUN --mount=type=bind,source=requirements.txt,target=/app/requirements.txt \
  pip install -r /app/requirements.txt

COPY . /app/

RUN addgroup --system app \
  && adduser --system --ingroup app app \
  && chown -R app:app /app/
USER app

WORKDIR /app

CMD ["python", "main.py"]


