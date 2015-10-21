
AGENT="br-ex"
CONTROL_IP="127.0.0.1"
CONTROL_PORT="6343"
SAMPLE_SIZE="1024"
POLLING_INTERVAL="10"
TARGET_BRIDGE="br-int"

ovs-vsctl -- --id=@s create sFlow agent=$AGENT \
    target=\"$CONTROL_IP:$CONTROL_PORT\" header=128 sampling=$SAMPLE_SIZE \
    polling=$POLLING_INTERVAL -- set Bridge $TARGET_BRIDGE sflow=@s

