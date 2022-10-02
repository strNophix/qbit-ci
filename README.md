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
```py
# Install requirements
pip install -r requirements.txt
pip install -e .

# Create a qbit-ci config file
nano .qbit-ci.yaml

# Start the app
python qbit_ci
```
