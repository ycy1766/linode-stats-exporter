# linode_stats_exporter


## Build Usage
````bash
podman build -t linode-stats-exporter:0.1 .
````


## Usage
To run the `linode_stats_exporter` in a container, use the following `podman` command:

````bash
podman run -d --name linode-stats-exporter \
  -p 3915:3915 \
  --env-file linode_token.txt \
  linode-stats-exporter:0.1
````
