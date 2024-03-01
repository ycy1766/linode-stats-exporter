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

## Metrics
The following metrics/labels are being exported:
````bash
# HELP linode_instance_cpu_usage CPU usage of the Linode instance in percent
linode_instance_cpu_usage{linode_id="00000000",linode_label="test-linoe-001"} 0.0
linode_instance_cpu_usage{linode_id="00000000",linode_label="test-linoe-002"} 0.28
# HELP linode_instance_netv4_in IPv4 incoming traffic of the Linode instance in bytes
linode_instance_netv4_in{linode_id="00000000",linode_label="test-linoe-001"} 0.0
linode_instance_netv4_in{linode_id="00000000",linode_label="test-linoe-002"} 343.79
# HELP linode_instance_netv4_out IPv4 outgoing traffic of the Linode instance in bytes
linode_instance_netv4_out{linode_id="00000000",linode_label="test-linoe-001"} 0.0
linode_instance_netv4_out{linode_id="00000000",linode_label="test-linoe-002"} 304.75
# HELP linode_instance_io_swap Swap IO of the Linode instance in IO ops
linode_instance_io_swap{linode_id="00000000",linode_label="test-linoe-001"} 0.0
linode_instance_io_swap{linode_id="00000000",linode_label="test-linoe-002"} 0.0
# HELP linode_instance_io_io IO of the Linode instance in IO ops
linode_instance_io_io{linode_id="00000000",linode_label="test-linoe-001"} 0.0
linode_instance_io_io{linode_id="00000000",linode_label="test-linoe-002"} 0.19
````