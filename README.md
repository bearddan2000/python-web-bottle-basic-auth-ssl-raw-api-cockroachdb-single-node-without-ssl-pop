# python-web-bottle-basic-auth-ssl-raw-api-cockroachdb-single-node-without-ssl-pop

## Description
Simple web app that serves an api
for a bottle project.

Uses sqlalchemy with raw sql to query a table `pop`.

Remotely tested with *testify*, ssl not verified.
Requires basic authentication for endpoints.

| username | password |
| -------- | -------- |
| *user* | *pass* |

## Tech stack
- python
  - bottle
  - sqlalchemy
  - testify
  - requests
- cockroachdb

## Docker stack
- alpine:edge
- python:latest
- cockroachdb/cockroach:v19.2.4

## To run
`sudo ./install.sh -u`
- Get all pops: http://localhost/pop
  - Schema id, name, and color
- CRUD opperations
  - Create: curl -i -X PUT localhost/pop/<id> -u 'user:pass'
  - Read: http://localhost/pop/<id> -u 'user:pass'
  - Update: curl -i -X POST localhost/pop/<id>/<name>/<color> -u 'user:pass'
  - Delete: curl -i -X DELETE localhost/pop/<id> -u 'user:pass'

## To stop
`sudo ./install.sh -d`

## For help
`sudo ./install.sh -h`
