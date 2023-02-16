#!/bin/zsh
ZSHRC=/Users/tim/.zshrc
SOURCE_DIR=/Users/tim/Documents/workspace/studynotes/docs/src/.vuepress/dist/
source ${ZSHRC}
cd ${SOURCE_DIR}
yarn dev 
