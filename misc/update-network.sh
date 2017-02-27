#!/bin/bash

echo "Generating new configuration …"
curl -o - https://members.atilla.org/network/render/dhcp
curl -o - https://members.atilla.org/network/render/dns
curl -o - https://members.atilla.org/network/render/dns/reverse

sleep 3

echo "Removing old files …"
mv -f /etc/bind/db.members.salle106.atilla.org /etc/bind/db.members.salle106.atilla.org.back
mv -f /etc/bind/db.rev.192.168.253 /etc/bind/db.rev.192.168.253.back
mv -f /etc/dhcp/members.conf /etc/dhcp/members.conf.back

echo "Gathering new configuration files …"
scp members@members-prod.prod.infra.atilla.org:~/dns.conf /etc/bind/db.members.salle106.atilla.org
scp members@members-prod.prod.infra.atilla.org:~/dhcp.conf /etc/dhcp/members.conf
scp members@members-prod.prod.infra.atilla.org:~/rev.dns.conf /etc/bind/db.rev.192.168.253

echo "Dumping infra reverse DNS configuration to reverse DNS file …"
cat /etc/bind/infra.db >> /etc/bind/db.rev.192.168.253

echo "Restarting services …"
systemctl restart isc-dhcp-server
systemctl restart bind9
