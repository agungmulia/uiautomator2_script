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
  PAYLOAD=$(jq -c -n --arg name "$TUNNEL_NAME" --arg userId "$USER_ID" --argjson timestamp "$TIMESTAMP" \
  '{name: $name, userId: $userId, timestamp: $timestamp}')

  SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')
  SIGNATURE_HEADER="-H \"X-Signature: $SIGNATURE\""
else
  PAYLOAD="{\"name\": \"$TUNNEL_NAME\"}"
fi

# Setup paths
TUNNEL_DIR="$HOME/.cloudflared"
TUNNEL_META="$TUNNEL_DIR/tunnel-meta.json"

SECRET_DIR="$HOME/.secret"
SECRET_FILE="$SECRET_DIR/secret.key"
TOKEN_FILE="$SECRET_DIR/token.key"

# Create tunnel directory if not exists
mkdir -p "$TUNNEL_DIR"

# Check if we already have a saved tunnel
if [ -f "$TOKEN_FILE" ]; then
  echo "[✓] Existing tunnel token found."
else
  echo "[+] No tunnel found. Requesting setup from backend..."

  # Call backend to create tunnel with given name

  echo "$PAYLOAD"

  RESPONSE=$(curl -s -X POST https://1wzpbwv2-3000.asse.devtunnels.ms/cloudflare \
  -H "Content-Type: application/json" \
  -H "X-Signature: $SIGNATURE" \
  -d "$PAYLOAD")

  echo "$RESPONSE"

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

  echo "[✓] Tunnel '$TUNNEL_NAME' initialized."
fi


echo "[DEBUG] HOME=$HOME"
echo "[DEBUG] SECRET_FILE=$SECRET_FILE"

mkdir -p "$SECRET_DIR"
chmod 700 "$SECRET_DIR"

# Try writing
echo "$SECRET" > "$SECRET_FILE"
echo "$TUNNEL_TOKEN" > "$TOKEN_FILE"

# Check success/failure of write
if [ $? -ne 0 ]; then
  echo "[✗] Failed to write to $SECRET_FILE"
else
  chmod 600 "$SECRET_FILE"
  echo "[✓] Secret saved at $SECRET_FILE"
fi

echo "[*] Launching tunnel with cloudflared..."
cloudflared tunnel run --token $TUNNEL_TOKEN