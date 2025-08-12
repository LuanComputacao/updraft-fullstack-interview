FROM nginx:1.24.0 as base

# Remove the default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy the modified Nginx config as a template
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf.template

RUN apt-get update \
  && apt-get install -y dumb-init \
  && rm -rf /var/lib/apt/lists/*

FROM base AS development

ENV NGINX_PUBLIC_PORT=8080 \
    FRONTEND_HOST="frontend:5180" \
    API_HOST="backend:3003"

RUN set -eux; \
  envsubst '$FRONTEND_HOST $API_HOST $NGINX_PUBLIC_PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf; \
  grep proxy_pass /etc/nginx/conf.d/default.conf || true; \
  env | grep -E 'FRONTEND_HOST|API_HOST|NGINX_PUBLIC_PORT'

ENTRYPOINT ["dumb-init", "--"]
CMD ["bash", "-c", "exec nginx"]
