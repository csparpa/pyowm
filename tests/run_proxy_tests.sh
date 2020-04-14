#!/usr/bin/env bash

if [ -z "$OWM_API_KEY" ]; then
    echo "*** OWM_API_KEY env variable is not set: aborting"
    exit 1
fi

export OWM_API_KEY

cd proxy

# Build one-off dependency file
DEPS_FILE="$(readlink . -f)/proxyreqs.txt"
echo 'pytest' | cat - ../../requirements.txt > $DEPS_FILE


# Run proxy server
PID_FILE="$(readlink . -f)/proxy.pid"
export PID_FILE

#proxy.py --num-workers 1 --hostname 127.0.0.1 --port 8899 --basic-auth user:pass --pid-file "$PID_FILE" > /dev/null 2>&1 &
pproxy -l http+socks4+socks5://127.0.0.1:8899 --ssl selfsigned.crt > /dev/null 2>&1 &
echo $$ >"$PID_FILE"

# Run tests
echo "*** Running tests... "
tox


# Shut down proxy
echo "*** Killing proxy... "
PID=$(cat $PID_FILE)
rm "$PID_FILE"
rm "$DEPS_FILE"

kill -9 "$PID"

echo "*** End of proxy tests"