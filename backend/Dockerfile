# Base stage for shared environment setup
FROM python:3.13-slim-bookworm AS base

WORKDIR /usr/app
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
RUN apt-get update \
  && apt-get -y install gcc python3-dev libpcre3 libpcre3-dev libpq-dev git

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /usr/app

# Development stage
FROM base AS development

COPY ./scripts/run-dev.sh /usr/app/run-dev.sh
RUN chmod +x /usr/app/run-dev.sh

EXPOSE 3003
#USER appuser

CMD ["/usr/app/run-dev.sh"]