FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Instalar el Angular CLI globalmente
RUN npm install -g @angular/cli

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0", "--poll", "2000"]