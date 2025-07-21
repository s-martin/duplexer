FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends -qq \
    pdftk \ 
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 --quiet install flask

RUN mkdir -p /app/uploads /app/outputs

# add app and website
COPY app.py /app/app.py 
COPY index.html /app/templates/index.html

WORKDIR /app

EXPOSE 5000

CMD ["python3", "app.py"]
