FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Installiere die benötigten Pakete
RUN apt-get update && apt-get install -y --no-install-recommends -qq \
    pdftk \ 
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installiere Flask
RUN pip3 --quiet install flask

# Erstelle Verzeichnisse für Uploads und Outputs
RUN mkdir -p /app/uploads /app/outputs

# Kopiere die Flask-Anwendung und die HTML-Datei in den 
# Container
COPY app.py /app/app.py 
COPY index.html /app/templates/index.html

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Mache den Port 5000 verfügbar
EXPOSE 5000

# Starte die Flask-Anwendung
CMD ["python3", "app.py"]
