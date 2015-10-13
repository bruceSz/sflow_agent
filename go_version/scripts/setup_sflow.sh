
AGENT="br-ex"
CONTROL_IP="127.0.0.1"
CONTROL_PORT="6343"
SAMPLE_SIZE="1024"
POLLING_INTERVAL="10"
TARGET_BRIDGE="br-int"

ovs-vsctl -- --id=@s create sFlow agent=$AGENT \
    target=\"$CONTROL_IP:$CONTROL_PORT\" header=128 sampling=$SAMPLE_SIZE \
    polling=$POLLING_INTERVAL -- set Bridge $TARGET_BRIDGE sflow=@s


chmod +x ./sflowtool

cur_dir=$(dirname $0)
etc_dir="$cur_dir/../etc"
sed -i 's/10.58.193.18/10.16.82.210/' $etc_dir/sflow.conf