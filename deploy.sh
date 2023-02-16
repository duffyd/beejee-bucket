#!/bin/zsh
ZSHRC=/Users/tim/.zshrc
SOURCE_DIR=/Users/tim/Documents/workspace/studynotes/docs/src/.vuepress/dist/
APP_DIR=/Users/tim/Documents/workspace/beejee/beejee
source ${ZSHRC}
cd ${SOURCE_DIR}
yarn build
rsync -rmPogv --del ${SOURCE_DIR} ${APP_DIR}/public/
cd ${APP_DIR}
quasar b -m electron
