#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "========== Cloudflare Tunnel Launcher =========="

# Accept tunnel name from argument or fallback to default
TUNNEL_NAME="${1:-termux-agent-default}"
USER_ID="${2:-userId}"
SECRET="${3:-DEFAULT_KEY}"

SIGNATURE_HEADER=""
if [ -n "$USER_ID" ]; then
  TIMESTAMP=$(date +%s)
  PAYLOAD="{\"name\": \"$TUNNEL_NAME\", \"userId\": \"$USER_ID\", \"timestamp\": $TIMESTAMP}"
  SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')
else
  PAYLOAD="{\"name\": \"$TUNNEL_NAME\"}"
fi

# Setup paths
TUNNEL_DIR="$HOME/.cloudflared"
TUNNEL_META="$TUNNEL_DIR/tunnel-meta.json"

# Create tunnel directory if not exists
mkdir -p "$TUNNEL_DIR"

# Check if we already have a saved tunnel
if [ -f "$TUNNEL_META" ]; then
  echo "[✓] Existing tunnel metadata found."
  TUNNEL_ID=$(jq -r '.tunnel_id' "$TUNNEL_META")
else
  echo "[+] No tunnel found. Requesting setup from backend..."

  # Call backend to create tunnel with given name

  RESPONSE=$(curl -s -X POST https://1wzpbwv2-3000.asse.devtunnels.ms/cloudflare \
  -H "Content-Type: application/json" \
  -H "X-signature: $SIGNATURE" \
  -H "x-custom-signature: $SIGNATURE" \
  -d "$(echo "$PAYLOAD" | jq -c .)")

  

  # Extract fields
  TUNNEL_ID=$(echo "$RESPONSE" | jq -r '.tunnel_id')
  TUNNEL_NAME=$(echo "$RESPONSE" | jq -r '.tunnel_name')
  CREDENTIALS=$(echo "$RESPONSE" | jq -r '.credentials_file')
  CONFIG_YAML=$(echo "$RESPONSE" | jq -r '.config_yaml')
  TUNNEL_TOKEN=$(echo "$RESPONSE" | jq -r '.token')

  if [[ -z "$TUNNEL_ID" || "$TUNNEL_ID" == "null" ]]; then
    echo "[✗] Failed to create tunnel. Response:"
    echo "$RESPONSE"
    exit 1
  fi

  # Save credentials and config
  echo "$CREDENTIALS" > "$TUNNEL_DIR/$TUNNEL_ID.json"
  chmod 400 "$TUNNEL_DIR/$TUNNEL_ID.json"

  echo "$CONFIG_YAML" > "$TUNNEL_DIR/config.yml"
  chmod 400 "$TUNNEL_DIR/config.yml"

  echo "{\"tunnel_id\": \"$TUNNEL_ID\"}" > "$TUNNEL_META"
  chmod 600 "$TUNNEL_META"

  echo "[✓] Tunnel '$TUNNEL_NAME' initialized."
fi

SECRET_DIR="$HOME/.secret"
SECRET_FILE="$SECRET_DIR/secret.key"

echo "[DEBUG] HOME=$HOME"
echo "[DEBUG] SECRET_FILE=$SECRET_FILE"

mkdir -p "$SECRET_DIR"
chmod 700 "$SECRET_DIR"

# Try writing
echo "$SECRET" > "$SECRET_FILE"

# Check success/failure of write
if [ $? -ne 0 ]; then
  echo "[✗] Failed to write to $SECRET_FILE"
else
  chmod 600 "$SECRET_FILE"
  echo "[✓] Secret saved at $SECRET_FILE"
fi

echo "[*] Launching tunnel with cloudflared..."
cloudflared tunnel --config "$TUNNEL_DIR/config.yml" run