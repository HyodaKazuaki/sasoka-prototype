FROM raspios-x86_64:buster-20201202
LABEL maintainer="HyodaKazuaki"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["/bin/sh", "-c", "while :; do sleep 10; done"]