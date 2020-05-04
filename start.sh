#!/bin/bash

if [ ! -d "$HOME/.ssh" ]
then
    echo "Creating .ssh dir"
    mkdir "$HOME/.ssh"
fi

if [ ! -z "$SSH_KEY" ] && [ ! -f "$HOME/.ssh/id_rsa" ];
then
    echo "Copying key to .ssh/id_rsa"
    echo -e $SSH_KEY > "$HOME/.ssh/id_rsa"
    chmod 600 $HOME/.ssh/id_rsa
fi

git config --global user.email "$GIT_EMAIL"
git config --global user.name "$GIT_USERNAME"

gunicorn --bind=0.0.0.0:5000 wsgi
