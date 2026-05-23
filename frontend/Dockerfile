FROM node:20-alpine AS base
WORKDIR /app

FROM base AS deps
COPY package*.json ./
RUN npm install --no-audit --no-fund

FROM base AS development
ENV NODE_ENV=development \
    HOST=0.0.0.0 \
    PORT=5173 \
    CHOKIDAR_USEPOLLING=true \
    VITE_DEV_SERVER_PORT=5173 \
    VITE_API_PROXY_TARGET=http://backend:8000
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev"]

FROM base AS build
ARG VITE_API_URL=/api/v1
ENV NODE_ENV=production \
    VITE_API_URL=$VITE_API_URL
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM nginx:1.27-alpine AS production
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
