FROM node:lts-alpine

WORKDIR /code

RUN chmod 755 /code

COPY ./src /code/src

COPY ./public /code/public

COPY ./package.json /code/package.json

COPY ./jsconfig.json /code/jsconfig.json

COPY ./next.config.js /code/next.config.js

RUN yarn install

RUN echo "API_ENDPOINT=http://34.22.87.179" > /code/.env

RUN yarn build

EXPOSE 3000

CMD ["yarn", "start"]
