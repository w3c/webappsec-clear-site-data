# Clear-Site-Data performance demo
## Introduction

This directory contains an example Clear-Site-Data implementation.
It consists of

- server.py, a Python server that serves various resources (an HTML page,
  an SVG image, both potentially with the Set-Cookie and/or Clear-Site-Data
  headers)
- index.html, a single-page website served by the server that allows users
  to load multiple resources at the same time, with or without Clear-Site-Data
- README.md - this file

## Setup instructions

1. Download the `performance_demo/` directory.
2. Run `python server.py` in that directory.
3. Navigate to `localhost:8000`. (**NOTE:** Clear-Site-Data only works on
   `localhost` and `https`. Since `server.py` is HTTP-only, navigating to other
   hosts than `localhost` will not work.)
4. Use the controls to load resources which add cookies and storage entries,
   and presumably will be cached.
5. Use the controls to load resources with the Clear-Site-Data header.
6. Observe the deletion performance as many instances of headers are processed
   at the same time.
