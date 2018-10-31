# Clear-Site-Data demo
## Introduction

This directory contains an example Clear-Site-Data implementation.
It consists of

- server.py, a Python server than returns the header when requested
- index.html, a single-page website served by the server that allows users
  to add site data, inspect it, and request its deletion
- README.md - this file

## Setup instructions

1. Download the `demo/` directory.
2. Run `python server.py` in that directory (Use Python 3.5 or higher).
3. Navigate to `localhost:8000`. (**NOTE:** Clear-Site-Data only works on
   `localhost` and `https`. Since `server.py` is HTTP-only, navigating to other
   hosts than `localhost` will not work.)
4. Add various site data, using the UI in `index.html` or manually.
5. Use the UI to request a Clear-Site-Data header.
6. Observe that requested data types were cleared.

## Notes

As of 2016-11-15, this only works in Chromium. Tested in Chromium 56.0.2889.0.
