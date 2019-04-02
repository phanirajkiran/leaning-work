#!/bin/sh
TRACING_PATH="/sys/kernel/debug/tracing"
LOOP=200

while true; do
	i=0
	while [ $i -lt $LOOP ]; do
		for tracer in `cat "$TRACING_PATH"/available_tracers`
		do
			if [ "$tracer" = mmiotrace ]; then
				continue
			fi

			echo $tracer > "$TRACING_PATH"/current_tracer 2> /dev/null
		done
		i=$((i + 1))
	done
	sleep 1
done
