# Tunnel Check

Tunnel Check is an open-source Python utility that continuously monitors and maintains an SSH tunnel. It verifies the tunnel's status at a defined interval and automatically reestablishes the tunnel in case of any failure. It can change the network location setting in the operating system. This project is designed for MacOS due to the networksetup utility used in the script.

## Features

- Monitors the status of an SSH tunnel.
- Automatic reestablishment of the tunnel in case of failure.
- Changes the network location setting in MacOS.
- Configurable checking interval.
- Colorful and timestamped logs for easier debugging.

## Getting Started

These instructions will guide you on how to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.x
- Packages: os, socks, socket, requests, time, datetime, subprocess, colorama

You can install the necessary packages using pip:

```bash
pip install PySocks requests colorama
```

### Installing

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/tunnel-check.git
cd tunnel-check
```

### Configuration

You need to replace the SSH credentials in the `main()` function with your own:

```python
ssh_user = 'your_username'
ssh_host = 'your_host'
```

Set your desired check interval (in seconds) in the `main()` function:

```python
interval = 2  # Change this to your preferred check interval
```

### Usage

Run the script:

```bash
python3 tunnel_check.py
```

Press `Ctrl+C` to stop the script.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Acknowledgments

This script uses the `colorama` library for colorful, easy-to-read logs and the `PySocks` library for setting up and testing the SOCKS proxy. The `subprocess` library is used for running terminal commands inside the script, and the `requests` library for making HTTP requests to test the proxy connection.
