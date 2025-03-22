# Docker Usage Guide for Oracle Downloader

This guide explains how to use the Oracle Downloader module with Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)

## Quick Start

### Using Docker Compose (Recommended)

1. Navigate to the Docker directory inside the downloader directory:
   ```bash
   cd downloader/Docker
   ```

2. Build and run the container:
   ```bash
   docker-compose up --build
   ```

3. To run in the background:
   ```bash
   docker-compose up -d
   ```

### Using Docker Directly

1. Navigate to the Docker directory:
   ```bash
   cd downloader/Docker
   ```

2. Build the image:
   ```bash
   docker build -t oracle-downloader -f Dockerfile ..
   ```

3. Run the container:
   ```bash
   docker run -v $(pwd)/../downloads:/downloads oracle-downloader
   ```

## Configuration

### Environment Variables

You can configure the downloader using environment variables:

| Variable           | Description                          | Default                        |
| ------------------ | ------------------------------------ | ------------------------------ |
| URL                | Single URL to download               | None                           |
| FORMAT             | Format selection for yt-dlp          | "bestvideo+bestaudio/best"     |
| OUTPUT_TEMPLATE    | Output filename template             | "/downloads/%(title)s.%(ext)s" |
| ADDITIONAL_OPTIONS | Additional options to pass to yt-dlp | ""                             |

Example:
```bash
docker run -v $(pwd)/../downloads:/downloads -e "URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" -e "FORMAT=bestvideo[height<=720]+bestaudio/best" oracle-downloader
```

### Using a URL File

You can provide a file with URLs (one per line):

```bash
docker run -v $(pwd)/../downloads:/downloads -v $(pwd)/../my-urls.txt:/app/urls.txt oracle-downloader
```

### Configuration Files

Mount the configuration directory to customize settings:

```bash
docker run -v $(pwd)/../downloads:/downloads -v $(pwd)/../script/downloader-conf:/app/script/downloader-conf oracle-downloader
```

## Advanced Usage

### Customizing the Docker Compose File

Edit the `docker-compose.yml` file in the Docker directory to customize volumes, environment variables, and other settings.

### Running with GPU Support (for faster processing)

```bash
docker run --gpus all -v $(pwd)/../downloads:/downloads oracle-downloader
```

## Troubleshooting

### Permission Issues

If you encounter permission issues with the downloaded files:

```bash
sudo chown -R $(id -u):$(id -g) ../downloads
```

### Container Won't Start

Check logs:
```bash
docker logs oracle-downloader
```

### Can't Access Files

Make sure you're mounting the volume correctly:
```bash
docker run -v "$(pwd)/../downloads:/downloads" oracle-downloader
``` 