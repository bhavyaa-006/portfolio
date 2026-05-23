FROM node:20-alpine

WORKDIR /app

ENV HOST=0.0.0.0 \
	PORT=5173 \
	CHOKIDAR_USEPOLLING=true \
	VITE_DEV_SERVER_PORT=5173 \
	VITE_HMR_HOST=localhost \
	VITE_HMR_CLIENT_PORT=5173 \
	VITE_API_PROXY_TARGET=http://backend:8000

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
