import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration output
DHCP_CONFIG_OUTPUT = os.path.join(BASE_DIR, 'dhcp.conf')
DNS_CONFIG_OUTPUT = os.path.join(BASE_DIR, 'dns.conf')
REV_DNS_CONFIG_OUTPUT = os.path.join(BASE_DIR, 'rev.dns.conf')

# Network IP prefix
IP_NETWORK_PREFIX = "192.168.253."
IP_RANGE_START = 45
IP_RANGE_END = 254

# NS options
TTL = 86400
NEGATIVE_CACHE_TTL = 86400
REFRESH = 21600
RETRY = 3600
EXPIRE = 2419200

DNS_BASE_SERIAL = 42
DNS_DOMAIN = "salle106.atilla.org"
DNS_DOMAIN_SEARCH = "members.salle106.atilla.org"
DNS_SERVER_1 = "192.168.253.1"
DNS_SERVER_2 = "192.168.253.1"

REV_DNS_ORIGIN = "253.168.192.in-addr.arpa"

# General network options
DOMAIN_ROOT_SERVER = "192.168.253.1"
DOMAIN_MAIL_SERVER = "192.168.253.1"
