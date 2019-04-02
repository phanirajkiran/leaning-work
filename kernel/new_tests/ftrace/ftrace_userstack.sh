#! /bin/sh



LOOP=10
TRACING_PATH="/sys/kernel/debug/tracing"
TSTACK_TRACE_PATH="/proc/sys/kernel/stack_tracer_enabled"
EXC_PAGE_FAULT_ENABLE="$TRACING_PATH/events/exceptions/page_fault_kernel/enable"
MM_PAGE_FAULT_ENABLE="$TRACING_PATH/events/kmem/mm_kernel_pagefault/enable"

ftrace_userstacktrace_test()
{
	if [ ! -e "$TSTACK_TRACE_PATH" ]; then
		tst_brkm TCONF "Stack Tracer is not cofigured in This kernel"
	fi

	for i in $(seq $LOOP); do
		echo 1 >  $TSTACK_TRACE_PATH
		echo userstacktrace > $TRACING_PATH/trace_options
		grep -q "^userstacktrace"  $TRACING_PATH/trace_options
		if [ $? -ne 0 ]; then
			tst_brkm TBROK "Failed to set userstacktrace"
		fi

		if [ -f "$EXC_PAGE_FAULT_ENABLE" ]; then
			exc_page_fault_enable=`cat $EXC_PAGE_FAULT_ENABLE`
			echo 1 > $EXC_PAGE_FAULT_ENABLE
		else
			mm_page_fault_enable=`cat $MM_PAGE_FAULT_ENABLE`
			echo 1 > $MM_PAGE_FAULT_ENABLE
		fi
	done

	if [ -f "$EXC_PAGE_FAULT_ENABLE" ]; then
		echo "$exc_page_fault_enable" > $EXC_PAGE_FAULT_ENABLE
	else
		echo "$mm_page_fault_enable" > $MM_PAGE_FAULT_ENABLE
	fi

	tst_resm TPASS "Finished running the test"
}

ftrace_userstacktrace_test

