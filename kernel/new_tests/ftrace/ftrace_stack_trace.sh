#!/bin/sh
LOOP=400
TRACING_PATH="/sys/kernel/debug/tracing"
while true; do
	i=0
	while [ $i -lt $LOOP ]; do
		cat "$TRACING_PATH"/stack_trace > /dev/null
		i=$((i + 1))
	done

	sleep 1

	i=0
	while [ $i -lt $LOOP ]; do
		echo 0 > /proc/sys/kernel/stack_tracer_enabled
		echo 1 > /proc/sys/kernel/stack_tracer_enabled
		i=$((i + 1))
	done

	sleep 1
done
