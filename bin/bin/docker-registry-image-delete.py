#!/usr/bin/env python3
import requests
import sys

# curl http://localhost:4000/v2/_catalog to list images
# bin/registry garbage-collect  /etc/docker/registry/config.yml to garbage collect

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0].strip('./')} IMAGE")
    sys.exit(1)

image = sys.argv[1]
headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
r = requests.get(f'http://localhost:4000/v2/{image}/tags/list', headers=headers)

try:
    for tag in r.json()['tags']:
        r = requests.get(f'http://localhost:4000/v2/{image}/manifests/{tag}', headers=headers)
        digest = r.headers['Docker-Content-Digest']
        print(f"Deleting tag {tag} with digest {digest}")
        r2 = requests.delete(f'http://localhost:4000/v2/{image}/manifests/{digest}', headers=headers)
        if r2.status_code == 202:
            print('Success!')
        else:
            print('Failed')
except (KeyError, TypeError):
    print(f'image {image} not found')
    sys.exit(1)
