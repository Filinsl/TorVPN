# TorVPN

**TorVPN** is software that allows you to use the Tor network as a VPN outside of the Tor Browser. The program creates a SOCKS5 proxy using TorSocks and redirects all traffic through the Tor network, ensuring online anonymity.

## Description

TorVPN uses TorSocks to create a SOCKS5 proxy server through which all your internet traffic is routed. This allows you to take advantage of the Tor network for anonymous browsing without being limited to just the Tor Browser.

### Benefits of using TorVPN:
- **Anonymity:** All connections are routed through the Tor network, hiding your identity.
- **Ease of use:** No complicated setup required, just run the program and connect to Tor.
- **Security:** The program provides a high level of security by hiding your real IP address and protecting your data from tracking.

## How it works?

TorVPN runs a SOCKS5 proxy server using TorSocks. All internet traffic, including HTTP, HTTPS requests, as well as DNS queries, is routed through the Tor network. This allows you to stay anonymous online and bypass censorship and geo-blocking.

## Installation

### Requirements:
- **Operating System:** Linux (tested on GNOME).
- **Required packages:** Tor must be installed and running on your device.

### Installation Instructions:

1. Go to the [Releases](https://github.com/Filinsl/TorVPN/releases) page to download the latest version of the program.
2. Download the file (`.deb`).
3. Install the program:
    ```bash
    sudo dpkg -i TorVPN-1.0.deb
    ```
4. Run the program:
    ```bash
    TorVPN
    ```
6. Ensure that the Tor service is running before launching the program.
7. Verify that your connection is successful by running the following command:
    ```bash
    curl --socks5 127.0.0.1:9050 https://check.torproject.org
    ```

If you see a message stating that you are using Tor, it means the program is working correctly.

### Planned Updates

Future versions of the program will add support for bridges for countries where Tor is blocked. This will help bypass censorship and ensure access to the Tor network even in countries with restrictions on using Tor.

You can read more about Tor bridges and how they work [here](https://bridges.torproject.org).

### Notes

Currently, the program is only available for Linux.

Make sure the Tor service is running before launching the program.

The program automatically configures all necessary SOCKS5 settings to work.

### License

This project is licensed under the MIT License. See the LICENSE file for details.
