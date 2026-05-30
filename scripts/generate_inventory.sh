#!/bin/bash

cd terraform

IPS=$(terraform output -json web_ips | \
python3 -c "import sys,json; print('\n'.join(json.load(sys.stdin)))")

cd ..

echo "[webservers]" > ansible/inventory.ini

echo "$IPS" | while read ip
do
  echo "$ip ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/ansible-project.pem" \
  >> ansible/inventory.ini
done

echo "Inventory generated!"
