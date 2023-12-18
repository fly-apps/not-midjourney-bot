FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3 python3-pip python3-virtualenv && \
    apt-get install --no-install-recommends -y libopencv-dev python3-opencv && \
    rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY ./Fooocus-API /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
RUN pip3 install install torch==2.1.0 torchvision==0.16.0

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

CMD ["bash", "/start.sh"]
