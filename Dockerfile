FROM ubuntu:latest
LABEL authors="ponom"

ENTRYPOINT ["top", "-b"]