# Update Cloudflare DNS Record Script

This script automatically updates a Cloudflare DNS record with the current external IP address of the machine running the script. It is designed to be a more readable and maintainable Python version of an older shell script.

## Features

- **Configuration Loading:** Reads configuration parameters from a JSON file.
- **IP Address Handling:** Retrieves the current external IP address and checks if it has changed since the last update.
- **Cloudflare Integration:** Uses Cloudflare API to get Zone ID and Domain ID, and updates the DNS record if the IP address has changed.
- **Error Handling:** Provides error messages and retries for network operations to ensure reliability.
- **Usage:** The script is designed to be run from the command line with a configuration file as an argument.

## Prerequisites

- Python 3.x
- `requests` library (can be installed via `pip install requests`)

## Usage

1. **Install the `requests` library:**
   ```sh
   pip install requests

2. **Create a configuration file (`config.json`) with the following structure:**

```json
{
    "LAST_IP_FILE": "last_ip.txt",
    "CF_EMAIL": "your-email@example.com",
    "CF_TOKEN": "your-cloudflare-api-token",
    "CF_ZONE_NAME": "example.com",
    "CF_DOMAIN_NAME": "sub.example.com"
}
```

3. **Run the script:**

```sh
python update_cloudflare_dns.py config.json
