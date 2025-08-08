FROM nginx:1.24.0 as base

# Remove the default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy the modified Nginx config as a template
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf.template

RUN apt-get update \
  && apt-get install -y dumb-init

FROM base AS development

ENV NGINX_PUBLIC_PORT=8080
ENV FRONTEND_HOST="172.17.0.1:5180/"
ENV API_HOST="backend:3003/api"

RUN envsubst '$FRONTEND_HOST $API_HOST $NGINX_PUBLIC_PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
RUN cat /etc/nginx/conf.d/default.conf
RUN env

ENTRYPOINT ["dumb-init", "--"]
CMD ["bash", "-c", "exec nginx"]