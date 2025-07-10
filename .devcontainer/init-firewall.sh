#!/bin/bash
# Firewall initialization script for Synthetic Plastic Transformer dev container
# Adapted from verbatim-ai setup with ML/chemistry specific domains

set -e

echo "🔒 Initializing firewall for secure development environment..."

# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Set default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow all loopback traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow DNS
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Allow SSH (for git operations)
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT

# Create ipsets for allowed domains
ipset create allowed_domains hash:net -exist

# Function to add domain IPs to ipset
add_domain_ips() {
    local domain=$1
    local ips=$(dig +short $domain A | grep -E '^[0-9]')
    for ip in $ips; do
        ipset add allowed_domains $ip -exist
    done
}

# Essential domains for development
ALLOWED_DOMAINS=(
    # Package registries
    "pypi.org"
    "files.pythonhosted.org"
    "registry.npmjs.org"
    "conda.anaconda.org"
    "repo.anaconda.com"
    
    # ML/Data science
    "download.pytorch.org"
    "data.pyg.org"
    "huggingface.co"
    "cdn-lfs.huggingface.co"
    
    # Chemistry/Materials
    "www.rdkit.org"
    "materialsproject.org"
    
    # Version control
    "github.com"
    "api.github.com"
    "raw.githubusercontent.com"
    "gitlab.com"
    
    # AI/ML services
    "api.anthropic.com"
    "api.openai.com"
    
    # Container registries
    "registry.docker.io"
    "ghcr.io"
    "quay.io"
    
    # Development tools
    "code.visualstudio.com"
    "marketplace.visualstudio.com"
    
    # Database/Cache
    "hub.docker.com"
)

# Add domain IPs to ipset
echo "📡 Resolving allowed domains..."
for domain in "${ALLOWED_DOMAINS[@]}"; do
    echo "  - Adding $domain"
    add_domain_ips $domain
done

# Allow traffic to ipset members
iptables -A OUTPUT -m set --match-set allowed_domains dst -j ACCEPT

# GitHub Meta API for dynamic IPs
echo "🐙 Fetching GitHub IP ranges..."
GITHUB_META=$(curl -s https://api.github.com/meta || echo '{}')
if [ ! -z "$GITHUB_META" ] && [ "$GITHUB_META" != "{}" ]; then
    # Extract IPs from various GitHub services
    for service in "web" "api" "git" "packages" "pages" "importer" "actions" "dependabot"; do
        ips=$(echo $GITHUB_META | jq -r ".$service[]? // empty" 2>/dev/null)
        for ip in $ips; do
            if [ ! -z "$ip" ]; then
                ipset add allowed_domains $ip -exist
            fi
        done
    done
fi

# Allow Docker internal communication
iptables -A INPUT -s 172.16.0.0/12 -j ACCEPT
iptables -A OUTPUT -d 172.16.0.0/12 -j ACCEPT

# Allow host.docker.internal
HOST_IP=$(getent hosts host.docker.internal | awk '{ print $1 }')
if [ ! -z "$HOST_IP" ]; then
    iptables -A OUTPUT -d $HOST_IP -j ACCEPT
fi

# Log dropped packets (for debugging)
iptables -A OUTPUT -m limit --limit 1/sec -j LOG --log-prefix "DROPPED: " --log-level 4

echo "✅ Firewall initialized successfully!"

# Test connectivity
echo ""
echo "🧪 Testing connectivity..."
test_connection() {
    local host=$1
    local port=$2
    timeout 5 bash -c "echo >/dev/tcp/$host/$port" && echo "✅ $host:$port - OK" || echo "❌ $host:$port - BLOCKED"
}

test_connection github.com 443
test_connection pypi.org 443
test_connection download.pytorch.org 443
test_connection api.anthropic.com 443

echo ""
echo "🔒 Firewall rules applied. Only allowed connections will work."
echo "📝 Check /var/log/syslog for dropped connection attempts."