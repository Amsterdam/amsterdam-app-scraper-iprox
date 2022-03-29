FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on

# Install python requirements
ADD . /code/
RUN apk add --update --no-cache netcat-openbsd \
 && python3 -m pip install -r /code/build-docker-image/requirements.txt \
 && rm -rf /tmp/* /code/build \
 && chmod +x /code/init.sh

WORKDIR /code
ENTRYPOINT /code/init.sh
