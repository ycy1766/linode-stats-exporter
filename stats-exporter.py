from prometheus_client import make_wsgi_app, Gauge
from wsgiref.simple_server import make_server
from datetime import datetime
import time
import requests
import random
import os
import argparse
import threading

parser = argparse.ArgumentParser(description='Linode Metrics Exporter')
parser.add_argument('--port', type=int, default=3915, help='Port to serve on (default: 3915)')
parser.add_argument('--path', type=str, default='/metrics', help='Path to serve metrics on (default: /metrics)')
args = parser.parse_args()

def log_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


linode_tokens = os.getenv("LINODE_TOKENS", "").split(",")

CPU_USAGE = Gauge('linode_instance_cpu_usage', 'CPU usage of the Linode instance in percent', ['linode_id', 'linode_label'])
NETV4_IN = Gauge('linode_instance_netv4_in', 'IPv4 incoming traffic of the Linode instance in bytes', ['linode_id', 'linode_label'])
NETV4_OUT = Gauge('linode_instance_netv4_out', 'IPv4 outgoing traffic of the Linode instance in bytes', ['linode_id', 'linode_label'])
IO_SWAP = Gauge('linode_instance_io_swap', 'Swap IO of the Linode instance in IO ops', ['linode_id', 'linode_label'])
IO_IO = Gauge('linode_instance_io_io', 'IO of the Linode instance in IO ops', ['linode_id', 'linode_label'])

def fetch_all_instances_stats():
    while True:
        api_token = random.choice(linode_tokens)
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get("https://api.linode.com/v4/linode/instances", headers=headers)
        if response.status_code == 200:
            instances = response.json()
            for instance in instances['data']:
                fetch_instance_stats(str(instance['id']), instance['label'], headers)
        else: 
            log_with_timestamp(f"Failed to fetch instances. Status code: {response.status_code}")
        time.sleep(300)

def fetch_instance_stats(linode_id, linode_label, headers):
    stats_url = f"https://api.linode.com/v4/linode/instances/{linode_id}/stats"
    response = requests.get(stats_url, headers=headers)
    if response.status_code == 200:
        stats = response.json()['data']
        CPU_USAGE.labels(linode_id=linode_id, linode_label=linode_label).set(stats['cpu'][-1][1] if stats['cpu'] else 0)
        NETV4_IN.labels(linode_id=linode_id, linode_label=linode_label).set(stats['netv4']['in'][-1][1] if stats['netv4']['in'] else 0)
        NETV4_OUT.labels(linode_id=linode_id, linode_label=linode_label).set(stats['netv4']['out'][-1][1] if stats['netv4']['out'] else 0)
        IO_SWAP.labels(linode_id=linode_id, linode_label=linode_label).set(stats['io']['swap'][-1][1] if stats['io']['swap'] else 0)
        IO_IO.labels(linode_id=linode_id, linode_label=linode_label).set(stats['io']['io'][-1][1] if stats['io']['io'] else 0)
        
        log_with_timestamp(f"Updated metrics for instance {linode_label} ({linode_id}).")
    else:
        log_with_timestamp(f"Failed to fetch stats for instance {linode_label} ({linode_id}). Status code: {response.status_code}")

app = make_wsgi_app()

def custom_wsgi_app(environ, start_response):
    if environ['PATH_INFO'] == args.path:
        return app(environ, start_response)
    else:
        message = f"Invalid path. Please use {args.path} to access metrics."
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [message.encode('utf-8')]

if __name__ == '__main__':
    threading.Thread(target=fetch_all_instances_stats, daemon=True).start()
    httpd = make_server('', args.port, custom_wsgi_app)
    log_with_timestamp(f"Serving on port {args.port} with metrics path {args.path}...")
    httpd.serve_forever()

