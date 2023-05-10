JQ="      .nodes.ethereum.latest   = \"${{ secrets.NODE_ETH }}\""
JQ=$JQ" | .nodes.ethereum.archival = \"${{ secrets.NODE_ETH }}\""
JQ=$JQ" | .nodes.xdai.archival     = \"${{ secrets.NODE_XDAI }}\""
JQ=$JQ" | .nodes.polygon.archival  = \"${{ secrets.NODE_POLYGON }}\""
JQ=$JQ" | .nodes.optimism.archival = \"${{ secrets.NODE_OPTIMISM }}\""
JQ=$JQ" | .apikeys.etherscan       = \"${{ secrets.APIKEYS_ETHERSCAN }}\""
JQ=$JQ" | .apikeys.polscan         = \"${{ secrets.APIKEYS_POLSCAN }}\""
echo $JQ 

jq "$JQ" < defi_protocols/config.json > /tmp/tmp_config.json
