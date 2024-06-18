import requests
import json
import time
import sys
import os

def load_config(config_file):
    if not os.path.isfile(config_file):
        print("ERROR, CONFIG NOT EXIST.")
        sys.exit(1)
    with open(config_file) as f:
        return json.load(f)

def load_last_ip(last_ip_file):
    if os.path.isfile(last_ip_file):
        with open(last_ip_file) as f:
            return f.read().strip()
    return ""

def save_last_ip(last_ip_file, ip):
    with open(last_ip_file, 'w') as f:
        f.write(ip)

def get_current_ip():
    for _ in range(5):
        try:
            response = requests.get('http://ip.xdty.org')
            ip = response.text.strip()
            if ip:
                return ip
        except requests.RequestException:
            pass
        time.sleep(3)
    return ""

def get_zone_id(cf_email, cf_token, cf_zone_name):
    url = f"https://api.cloudflare.com/client/v4/zones?name={cf_zone_name}"
    headers = {
        "X-Auth-Email": cf_email,
        "X-Auth-Key": cf_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['result'][0]['id'] if data['success'] else ""

def get_domain_id(cf_email, cf_token, cf_zone_id, cf_domain_name):
    url = f"https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records?name={cf_domain_name}"
    headers = {
        "X-Auth-Email": cf_email,
        "X-Auth-Key": cf_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['result'][0]['id'] if data['success'] else ""

def update_domain(cf_email, cf_token, cf_zone_id, cf_domain_id, cf_domain_name, ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records/{cf_domain_id}"
    headers = {
        "X-Auth-Email": cf_email,
        "X-Auth-Key": cf_token,
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": cf_domain_name,
        "content": ip,
        "ttl": 1,
        "proxied": False
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()['success']

def main(config_file):
    config = load_config(config_file)
    last_ip = load_last_ip(config['LAST_IP_FILE'])
    
    current_ip = get_current_ip()
    if not current_ip:
        print("ERROR, COULD NOT RETRIEVE CURRENT IP.")
        return
    
    if current_ip == last_ip:
        print(f"{time.ctime()} -- Already updated.")
        return
    
    cf_zone_id = get_zone_id(config['CF_EMAIL'], config['CF_TOKEN'], config['CF_ZONE_NAME'])
    if not cf_zone_id:
        print("ERROR, COULD NOT RETRIEVE ZONE ID.")
        return
    
    cf_domain_id = get_domain_id(config['CF_EMAIL'], config['CF_TOKEN'], cf_zone_id, config['CF_DOMAIN_NAME'])
    if not cf_domain_id:
        print("ERROR, COULD NOT RETRIEVE DOMAIN ID.")
        return
    
    success = update_domain(config['CF_EMAIL'], config['CF_TOKEN'], cf_zone_id, cf_domain_id, config['CF_DOMAIN_NAME'], current_ip)
    if success:
        print(f"{time.ctime()} -- Update success")
        save_last_ip(config['LAST_IP_FILE'], current_ip)
    else:
        print(f"{time.ctime()} -- Update failed")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <config_file>")
        sys.exit(1)
    main(sys.argv[1])
