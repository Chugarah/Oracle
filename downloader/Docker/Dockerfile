FROM mikenye/yt-dlp:latest as yt-dlp-base

# Use a Python base image for our customizations
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    DOCKER_ENV=true

# Install UV (modern Python package installer/resolver)
RUN pip install uv

# Install FFmpeg and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy yt-dlp executable from the base image
COPY --from=yt-dlp-base /usr/local/bin/yt-dlp /usr/local/bin/yt-dlp

# Create a working directory for our app
WORKDIR /app

# Copy requirements file
COPY ../script/requirements.txt .

# Install dependencies using UV
RUN uv pip install -r requirements.txt

# Copy the rest of the application
COPY .. .

# Create a directory for downloads
RUN mkdir -p /downloads

# Set up volumes for persistent data
VOLUME ["/downloads", "/app/script/downloader-conf"]

# Set environment variables with defaults that can be overridden at runtime
ENV URL="" \
    FORMAT="bestvideo+bestaudio/best" \
    OUTPUT_TEMPLATE="/downloads/%(title)s.%(ext)s" \
    ADDITIONAL_OPTIONS=""

# Create entrypoint script
RUN echo '#!/bin/bash\n\
if [[ -f "/app/urls.txt" ]]; then\n\
    # Use URLs from file\n\
    cat /app/urls.txt | while read url; do\n\
        if [[ ! -z "$url" ]]; then\n\
            echo "Downloading: $url"\n\
            yt-dlp -f "$FORMAT" -o "$OUTPUT_TEMPLATE" $ADDITIONAL_OPTIONS "$url"\n\
        fi\n\
    done\n\
elif [[ ! -z "$URL" ]]; then\n\
    # Use URL from environment variable\n\
    echo "Downloading: $URL"\n\
    yt-dlp -f "$FORMAT" -o "$OUTPUT_TEMPLATE" $ADDITIONAL_OPTIONS "$URL"\n\
else\n\
    # Run the Python script\n\
    echo "Running Python script..."\n\
    cd /app && python script/main.py\n\
fi\n'\
> /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"] 