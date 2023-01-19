#!/usr/bin/bash

exec > /var/log/influxdb-install.log 2>&1

# Declaring variables
key_url="https://repos.influxdata.com/influxdb.key"
key="23a1c8836f0afc5ed24e0486339d7cc8f6790b83886c4c96995b88a061c5bb5d"
key_path="/etc/apt/trusted.gpg.d/influxdb.gpg"
influx_debian_url="https://repos.influxdata.com/debian"

# Commands to install influxdb
curl -s ${key_url} > influxdb.key
echo "${key} influxdb.key" | sha256sum -c && cat influxdb.key | gpg --dearmor | sudo tee ${key_path} > /dev/null
echo "deb [signed-by=${key_path}] ${influx_debian_url} stable main" | sudo tee /etc/apt/sources.list.d/influxdata.list

sudo apt-get update && sudo apt-get install influxdb
# If you want to install influxdb_v2, replace influxdb (line 16) with influxdb2

sudo service influxdb start

# NOTE: Make sure to enable authentication and create user/paswd in influx which will be used while making influx as data source for the grafana. 
