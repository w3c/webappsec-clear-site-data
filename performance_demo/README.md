# Clear-Site-Data performance demo
## Introduction

This directory contains an example Clear-Site-Data implementation.
It consists of

- server.py, a Python server that serves various resources (an HTML page,
  an SVG image, both potentially with the Set-Cookie and/or Clear-Site-Data
  headers)
- index.html, a single-page website that allows the user to load multiple
  resources at the same time, with or without Clear-Site-Data
- README.md - this file

## Deployment

The demo is based on [webapp2](https://webapp2.readthedocs.io/), and can be
deployed on [Google App Engine](https://cloud.google.com/appengine/).

It is currently deployed [here](https://clear-site-data-demo.appspot.com).
