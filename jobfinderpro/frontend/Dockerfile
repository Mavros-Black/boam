FROM node:20-alpine AS base
WORKDIR /app

COPY frontend/package.json frontend/tsconfig.json frontend/vite.config.ts frontend/index.html frontend/postcss.config.js frontend/tailwind.config.js /app/
COPY frontend/src /app/src
COPY frontend/public /app/public

RUN npm install && npm run build

EXPOSE 5173
CMD ["npm", "run", "preview", "--", "--host"]