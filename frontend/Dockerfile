# Frontend Dockerfile
FROM node:20-alpine AS base
WORKDIR /usr/src/app
# Copy lock/manifests individually to leverage layer caching
COPY package.json ./
# Copy optional lock files if exist (ignored if absent by separate steps)
COPY package-lock.json ./
COPY pnpm-lock.yaml ./

RUN corepack enable && \
    if [ -f pnpm-lock.yaml ]; then pnpm install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    else npm install; fi

COPY . .

FROM base AS development
ENV HOST=0.0.0.0
EXPOSE 5173
CMD ["npm","run","dev"]

FROM base AS build
RUN npm run build

FROM nginx:1.24.0-alpine AS production
COPY --from=build /usr/src/app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
