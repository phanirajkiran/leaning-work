#!/bin/sh
MAX_STACK_SIZE=8192
TRACING_PATH="/sys/kernel/debug/tracing"
while true; do
	i=0
	while [ $i -lt $MAX_STACK_SIZE ]; do
		echo $i > "$TRACING_PATH"/stack_max_size
		cat "$TRACING_PATH"/stack_max_size > /dev/null
		i=$((i + 1))
	done
	sleep 1
done
