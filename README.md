# qbit-ci
A micro CI/CD framework for qBittorrent Web.

## Example
```yml
name: test
type: pipeline
steps:
  - name: "Notify completed uncategorized torrents"
    commands:
      - >
        curl
          -H "Content-Type: application/json"
          -d '{"username": "Botterboy", "content": "{{ torrent.name }} complete"}'
          <webhook_url>
    when:
      - '{{ changes.completion_on not in [None, -1] }}'
      - '{{ torrent.state == "uploading" }}'
```

## Usage
Python:
```py
# Copy and update settings
cp .env.sample .env
nano .env

# Install requirements
pip install -r requirements.txt
pip install -e .

# Create a qbit-ci config file
nano .qbit-ci.yaml

# Start the app
python qbit_ci
```

Docker:
```sh
# Copy and update settings
cp .env.sample .env
nano .env

# Create a qbit-ci config file
nano .qbit-ci.yaml

# Run qbit-ci
docker run \
  --env-file .env \
  --mount type=bind,source=$(pwd)/.qbit-ci.yaml,target=/app/.qbit-ci.yaml \
  git.cesium.pw/niku/qbit-ci:latest
```
