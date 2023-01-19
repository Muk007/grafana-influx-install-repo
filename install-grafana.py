#!/usr/bin/python3

import sys
import os
import json
import logging

logging.basicConfig(filename='/var/log/grafana-install.log', format='%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def load_config (config_file_path):
    config_data = {}
    with open(config_file_path) as config_file:
        config_data = json.load(config_file)
    return config_data

def download_binary(url, grafana_home):
    cmd = "sudo apt update -y  \ncurl -o "+grafana_home+"grafana-9.3.2.tar.gz "+url
    os.system(cmd)
    logging.info("System updated & grafana binary downloaded.")

def grafana_config(grafana_home):
    cmd = "tar -xvf "+grafana_home+"grafana-9.3.2.tar.gz -C "+grafana_home+" \nmv "+grafana_home+"grafana-9.3.2 "+grafana_home+"grafana  \nsudo cp -R "+grafana_home+"grafana/bin/grafana-server /usr/local/bin/grafana-server  \nsudo chmod +x /usr/local/bin/grafana-server"
    os.system(cmd)
    logging.info("grafana-server binary configured.")
     
def start_script(service_name, grafana_home):
    with open("/etc/systemd/system/grafana.service", "w") as file:
        lines = ["[Unit]\n", "Description=Grafana Service\n", "Documentation=https://grafana.com/docs/grafana/latest/\n\n", "[Service]\n","ExecStart=grafana-server -homepath "+grafana_home+"grafana\n\n", "[Install]\n", "WantedBy=multi-user.target\n", "Alias=grafana.service\n"]
        file.writelines(lines)
        file.close()
    cmd = "sudo systemctl start "+service_name
    os.system(cmd)
    logging.info("Grafana started...")
    
config_data = {}

try:
    config_data = load_config(sys.argv[1])
    download_binary(config_data['url'], config_data['grafana_home']) 
    grafana_config(config_data['grafana_home'])
    start_script(config_data['service_name'], config_data['grafana_home'])
    
except Exception as exp:
    logging.exception("Grafana installation failed.")
