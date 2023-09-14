FROM alpine:latest as base

RUN apk add --no-cache zsh cryptsetup pinentry sudo gpg e2fsprogs findmnt

# download and unpack tomb
RUN wget https://files.dyne.org/tomb/Tomb-2.9.tar.gz
RUN tar xvfz Tomb-2.9.tar.gz
RUN ln -s /Tomb-2.9/tomb /usr/bin/tomb


