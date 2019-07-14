FROM node:8.16-alpine
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/public
RUN mkdir -p /usr/src/app/src
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install --production --silent 
EXPOSE 3000