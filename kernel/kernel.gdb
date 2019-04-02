https://lkml.org/lkml/2012/12/23/94


I get segmentation faults when running one of these commands:
perf report -g --sort symbol_to
perf report -g --sort symbol_from
perf report -g --sort dso_from
perf report -g --sort dso_to

I am running uname -a
Linux sb 3.5.0-21-generic #32-Ubuntu SMP Tue Dec 11 18:51:59 UTC 2012 x86_64 x86_64 x86_64 GNU/Linux

The perf utility crashes in both the version installed perf version 3.5.7.1
and as well in the self compiled version from the kernel repository v3.8-rc1

gdb output from the perf version included at kernel v3.8-rc1

gdb ../linux/tools/perf/perf 
GNU gdb (GDB) 7.5-ubuntu
Copyright (C) 2012 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /home/sb/OSS/linux/tools/perf/perf...done.
(gdb) r report -g --sort dso_to
Starting program: /home/sb/OSS/linux/tools/perf/perf report -g --sort dso_to
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
# ========
# captured on: Sun Dec 23 20:57:02 2012
# hostname : sb
# os release : 3.5.0-21-generic
# perf version : 3.5.7.1
# arch : x86_64
# nrcpus online : 8
# nrcpus avail : 8
# cpudesc : Intel(R) Core(TM) i7-2760QM CPU @ 2.40GHz
# cpuid : GenuineIntel,6,42,7
# total memory : 8133288 kB
# cmdline : /usr/bin/perf_3.5.0-21 record -g ./flare 
# event : name = cycles, type = 0, config = 0x0, config1 = 0x0, config2 = 0x0, excl_usr = 0, excl_kern = 0, excl_host = 0, excl_guest = 1, precise_
# HEADER_CPU_TOPOLOGY info available, use -I to display
# HEADER_NUMA_TOPOLOGY info available, use -I to display
# ========
#
[kernel.kallsyms] with build id 4d9cff231d947ccf8f1cd1cf504a682cad29cae4 not found, continuing without symbols

Program received signal SIGSEGV, Segmentation fault.
sort__dso_to_cmp (left=0x7fffffffcd70, right=0x24a3320) at util/sort.c:372
372		return _sort__dso_cmp(left->branch_info->to.map,
(gdb) bt
#0  sort__dso_to_cmp (left=0x7fffffffcd70, right=0x24a3320) at util/sort.c:372
#1  0x000000000047bc22 in hist_entry__cmp (right=0x24a3320, left=0x7fffffffcd70) at util/hist.c:386
#2  add_hist_entry (hists=hists@entry=0x79eac0, entry=entry@entry=0x7fffffffcd70, period=1, al=<optimized out>) at util/hist.c:288
#3  0x000000000047cbd6 in __hists__add_entry (self=self@entry=0x79eac0, al=al@entry=0x7fffffffceb0, sym_parent=<optimized out>, 
    period=<optimized out>) at util/hist.c:376
#4  0x0000000000429d6f in perf_evsel__add_hist_entry (machine=<optimized out>, sample=0x7fffffffcff0, al=0x7fffffffceb0, evsel=0x79ea20)
    at builtin-report.c:149
#5  process_sample_event (tool=0x7fffffffd3d0, event=0x7fffed436e08, sample=0x7fffffffcff0, evsel=0x79ea20, machine=<optimized out>)
    at builtin-report.c:216
#6  0x000000000046a331 in perf_session_deliver_event (session=session@entry=0x79cd60, event=<optimized out>, sample=sample@entry=0x7fffffffcff0, 
    tool=tool@entry=0x7fffffffd3d0, file_offset=<optimized out>) at util/session.c:1075
#7  0x000000000046a93f in flush_sample_queue (s=s@entry=0x79cd60, tool=tool@entry=0x7fffffffd3d0) at util/session.c:729
#8  0x000000000046c059 in __perf_session__process_events (session=session@entry=0x79cd60, data_offset=<optimized out>, data_size=<optimized out>, 
    file_size=63901304, tool=tool@entry=0x7fffffffd3d0) at util/session.c:1459
#9  0x000000000046c56e in perf_session__process_events (self=self@entry=0x79cd60, tool=tool@entry=0x7fffffffd3d0) at util/session.c:1476
#10 0x000000000042aee0 in __cmd_report (rep=0x7fffffffd3d0) at builtin-report.c:371
#11 cmd_report (argc=<optimized out>, argv=<optimized out>, prefix=<optimized out>) at builtin-report.c:765
#12 0x0000000000412c23 in run_builtin (p=p@entry=0x6cb9c8 <commands+168>, argc=argc@entry=4, argv=argv@entry=0x7fffffffe140) at perf.c:318
#13 0x00000000004123bb in handle_internal_command (argv=0x7fffffffe140, argc=4) at perf.c:366
#14 run_argv (argv=0x7fffffffdf30, argcp=0x7fffffffdf3c) at perf.c:410
#15 main (argc=4, argv=0x7fffffffe140) at perf.c:51
