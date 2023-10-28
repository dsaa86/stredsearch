#!/bin/bash

sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl start redis-server
source Scripts/activate
