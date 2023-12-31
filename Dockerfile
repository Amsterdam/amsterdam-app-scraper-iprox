FROM python:3.9-alpine

# Install python requirements
COPY FetchData/* /code/FetchData/
COPY GenericFunctions/* /code/GenericFunctions/
COPY unittests/* /code/unittests/
COPY init.sh /code/
COPY main.py /code/
COPY requirements.txt /code
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
 && python3 -m pip \
      --no-cache-dir install \
      -r /code/requirements.txt \
 && rm -rf /tmp/* \
 && find / -name "*.c" -delete \
 && find / -name "*.pyc" -delete \
 && apk del .build-deps \
 && chmod +x /code/init.sh

WORKDIR /code
ENTRYPOINT /code/init.sh
