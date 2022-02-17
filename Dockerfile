FROM python:3.10.2-alpine3.15

RUN apk update && apk upgrade && /usr/local/bin/python -m pip install --upgrade pip && \ 
    addgroup -S slacker && adduser -S slacker -G slacker
COPY code/config.py code/slacker.py code/main.py /usr/src/slacker/
COPY code/requirements.txt /tmp/

RUN chown -R slacker:slacker /usr/src/slacker/ && pip install -r /tmp/requirements.txt

USER slacker

ENTRYPOINT [ "/usr/local/bin/python", "/usr/src/slacker/main.py" ]

