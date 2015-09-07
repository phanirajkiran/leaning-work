criu
lxc
cgroup
======
http://coolshell.cn/articles/17049.html
root@ISG_WalnutCanyonII-2:~# mkdir cgroup
root@ISG_WalnutCanyonII-2:~# mount -t tmpfs cgroup_root ./cgroup
root@ISG_WalnutCanyonII-2:~# mkdir cgroup/cpuset
root@ISG_WalnutCanyonII-2:~# mount -t cgroup -ocpuset cpuset ./cgroup/cpuset/
root@ISG_WalnutCanyonII-2:~# mkdir cgroup/cpu
root@ISG_WalnutCanyonII-2:~# mount -t cgroup -ocpu cpu ./cgroup/cpu/
root@ISG_WalnutCanyonII-2:~# mkdir cgroup/memory
root@ISG_WalnutCanyonII-2:~# mount -t cgroup -omemory memory ./cgroup/memory/
root@ISG_WalnutCanyonII-2:~# ls ./cgroup/cpuset/
cgroup.clone_children  cpuset.cpu_exclusive  cpuset.mem_hardwall     cpuset.memory_pressure_enabled  cpuset.mems		      notify_on_release
cgroup.procs	       cpuset.cpus	     cpuset.memory_migrate   cpuset.memory_spread_page	     cpuset.sched_load_balance	      release_agent
cgroup.sane_behavior   cpuset.mem_exclusive  cpuset.memory_pressure  cpuset.memory_spread_slab	     cpuset.sched_relax_domain_level  tasks
root@ISG_WalnutCanyonII-2:~# ls ./cgroup/cpu/
cgroup.clone_children  cgroup.procs  cgroup.sane_behavior  cpu.shares  notify_on_release  release_agent  tasks
root@ISG_WalnutCanyonII-2:~# ls ./cgroup/memory/
cgroup.clone_children  memory.force_empty	       memory.kmem.tcp.failcnt		   memory.limit_in_bytes	    memory.memsw.usage_in_bytes      memory.soft_limit_in_bytes  notify_on_release
cgroup.event_control   memory.kmem.failcnt	       memory.kmem.tcp.limit_in_bytes	   memory.max_usage_in_bytes	    memory.move_charge_at_immigrate  memory.stat		 release_agent
cgroup.procs	       memory.kmem.limit_in_bytes      memory.kmem.tcp.max_usage_in_bytes  memory.memsw.failcnt		    memory.numa_stat		     memory.swappiness		 tasks
cgroup.sane_behavior   memory.kmem.max_usage_in_bytes  memory.kmem.tcp.usage_in_bytes	   memory.memsw.limit_in_bytes	    memory.oom_control		     memory.usage_in_bytes
memory.failcnt	       memory.kmem.slabinfo	       memory.kmem.usage_in_bytes	   memory.memsw.max_usage_in_bytes  memory.pressure_level	     memory.use_hierarchy
root@ISG_WalnutCanyonII-2:~# 


root@ISG_WalnutCanyonII-2:~# ls cgroup/cpu/lyang0
cgroup.clone_children  cgroup.procs  cpu.shares  notify_on_release  tasks
root@ISG_WalnutCanyonII-2:~# ls cgroup/cpu/      
cgroup.clone_children  cgroup.procs  cgroup.sane_behavior  cpu.shares  lyang0  notify_on_release  release_agent  tasks


xfs
kprobe
uprobe
ftrace
mem hotplug 
kmemleak
lttng2
oprofile
perf
perf kvm

ptrace
trace-cmd
unionfs
latencytop
docker
sysrq
Event Trigger
Histograms
eBPF ---> kernel/bpf/

./kernel/trace/trace.c
./kernel/trace/trace_stack.c
./kernel/trace/trace_clock.c
./kernel/trace/trace_printk.c
./kernel/trace/trace_output.c
./kernel/trace/trace_nop.c
./kernel/trace/trace_benchmark.c
./kernel/trace/trace_syscalls.c
./kernel/trace/trace_event_perf.c
./kernel/trace/trace_probe.h
./kernel/trace/trace_seq.c
./kernel/trace/trace.h
./kernel/trace/trace_output.h
./kernel/trace/trace_events_filter_test.h
./kernel/trace/trace_selftest.c
./kernel/trace/trace_probe.c
./kernel/trace/trace_branch.c
./kernel/trace/trace_benchmark.h
./kernel/trace/trace_entries.h
./kernel/trace/trace_selftest_dynamic.c
./kernel/trace/trace_stat.h
./kernel/trace/trace_kprobe.c
./kernel/trace/trace_sched_switch.c
./kernel/trace/trace_uprobe.c
./kernel/trace/trace_functions_graph.c
./kernel/trace/trace_export.c
./kernel/trace/trace_events.c
./kernel/trace/trace_sched_wakeup.c
./kernel/trace/trace_mmiotrace.c
./kernel/trace/trace_irqsoff.c
./kernel/trace/trace_stat.c



Tracefs 
=======
New tracefs File System
• Added in 4.1, by Steve Rostedt
• Used by ftrace
• Instead of debugfs (usually /sys/kernel/debug/tracing), tracing has now its own file system, under /sys/kernel/tracing
To be compatible with old systems, it is also mounted under
debugfs
New include file /include/linux/tracefs.h
Ftrace and perf use it
No changes in functionality
See articles:
• https://lwn.net/Articles/632519/ (perf support)
• https://lwn.net/Articles/630526/ (kernel patch)

Now when mounting /sys/kernel/debug, tracefs is automatically mounted
in /sys/kernel/debug/tracing such that old tools will still see that
path as expected. But now system admins can mount tracefs directly
and not need to mount debugfs, which can expose security issues.
A new directory is created when tracefs is configured such that
system admins can now mount it separately (/sys/kernel/tracing).


1)CONFIG_TRACING=y
2)
root@ISG_WalnutCanyonII-2:~# mount -t tracefs none /sys/kernel/tracing/
root@ISG_WalnutCanyonII-2:~# ls /sys/kernel/tracing/
README		      free_buffer     saved_cmdlines	   trace_pipe
available_events      instances       saved_cmdlines_size  tracing_cpumask
available_tracers     kprobe_events   set_event		   tracing_on
buffer_size_kb	      kprobe_profile  trace		   tracing_thresh
buffer_total_size_kb  options	      trace_clock
current_tracer	      per_cpu	      trace_marker
events		      printk_formats  trace_options

ktap
====
---------------------------------------------------
Ktap, end of story?
• In kernel tracer by Jovi Zhangwei of Huawei
• Project started in 2013
• Hosted on https://github.com/ktap/ktap.git
• http://www.ktap.org/doc/tutorial.html
• Presentation:
http://events.linuxfoundation.org/sites/events/files/lcjpcojp13_zhangwei.p
df
• In kernel interpreter
• Scripting language is based on Lua
• Targeted to embedded community
• Virtual machine in kernel
• Architectures supported: x86, x86-64, powerpc, arm
• Was merged in 3.13 staging tree, then pulled
• Development stopped
• Last public statement (dec 2014):
http://comments.gmane.org/gmane.comp.linux.ktap/377

------------------------------------------------------------------

live patch 
==========
DYNAMIC_FTRACE_WITH_REGS [=n] && MODULES [=y] && SYSFS [=y] && KALLSYMS_ALL [=n] && HAVE_LIVEPATCH [=y]
DYNAMIC_FTRACE_WITH_REGS
Depends on: TRACING_SUPPORT [=y] && FTRACE [=y] && DYNAMIC_FTRACE [=n] && HAVE_DYNAMIC_FTRACE_WITH_REGS [=y]

1)enable CONFIG_LIVEPATCH and CONFIG_SAMPLE_LIVEPATCH
2)make modules 
3)

4)
  $ cat /proc/cmdline
  <your cmdline>
 
  $ insmod livepatch-sample.ko
  $ cat /proc/cmdline
  this has been live patched
 
  $ echo 0 > /sys/kernel/livepatch/livepatch_sample/enabled
  $ cat /proc/cmdline
  <your cmdline>
logs:
root@ISG_WalnutCanyonII-2:/# modprobe livepatch-sample
[   45.387225] livepatch: tainting kernel with TAINT_LIVEPATCH
[   45.393541] livepatch: enabling patch 'livepatch_sample'
root@ISG_WalnutCanyonII-2:~# cat /proc/cmdline
this has been live patched
root@ISG_WalnutCanyonII-2:~# echo 0 > /sys/kernel/livepatch/livepatch_sample/enabled
root@ISG_WalnutCanyonII-2:~# cat /proc/cmdline
console=ttyS0,115200 root=/dev/nfs rw nfsroot=128.224.165.20:/export/pxeboot/vlm-boards/22574/rootfs rw ip=dhcp intel_iommu=off no_console_suspend=1 crashkernel=512M@64M
root@ISG_WalnutCanyonII-2:~# 


-------------------------------------------------------------------------
crypto
======
commit 53f52d7aecb4cb3772872c902b73e0c685a56901
Author: Tim Chen <tim.c.chen@linux.intel.com>
Date:   Wed Dec 11 14:28:47 2013 -0800

    crypto: tcrypt - Added speed tests for AEAD crypto alogrithms in tcrypt test suite

brtfs
=====

https://www.howtoforge.com/a-beginners-guide-to-btrfs

criu
=====
root@ISG_WalnutCanyonII-2:~# ./test.sh  < /dev/null &> test.log &
[1] 1564
root@ISG_WalnutCanyonII-2:~# criu dump -D mnt/ -t 1564 --shell-job -vvvv -o dump.log
#dump.log is located in /mnt, --vvvv is the debug info 
Warn  (sk-unix.c:420): Relative bind path 'public/pickup' unsupported
Warn  (sk-unix.c:420): Relative bind path 'public/cleanup' unsupported
Warn  (sk-unix.c:420): Relative bind path 'public/qmgr' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/tlsmgr' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/rewrite' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/bounce' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/defer' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/trace' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/verify' unsupported
Warn  (sk-unix.c:420): Relative bind path 'public/flush' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/proxymap' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/proxywrite' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/smtp' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/relay' unsupported
Warn  (sk-unix.c:420): Relative bind path 'public/showq' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/error' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/retry' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/discard' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/local' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/virtual' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/lmtp' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/anvil' unsupported
Warn  (sk-unix.c:420): Relative bind path 'private/scache' unsupported
[1]+  Killed                  ./test.sh < /dev/null &> test.log

------------------------------------------------------------------------------
root@ISG_WalnutCanyonII-2:~# crashkernel=512M@32M
root@ISG_WalnutCanyonII-2:~# cat /proc/cmdline > kexec_args
root@ISG_WalnutCanyonII-2:~# kexec -l /bzImage --append="`cat kexec_args`"
my_load:669: do
------------------------------------------------------------------------------

root@ISG_WalnutCanyonII-2:~# criu restore -d -D /mnt/ -vvvv -o restore.log --shell-job
#restore.log is located in /mnt, --vvvv is the debug info, --shell-job must be used here 



root@ISG_WalnutCanyonII-2:~# tail -f test.log
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31

root@ISG_WalnutCanyonII-2:~# cat test.ol 
#!/bin/sh
for i in {1..300}
do
	echo $i
	sleep 1
done

or
   #!/bin/sh
   while :; do
       sleep 1
       date
   done


注意：这里的脚本缩进一定要对齐，我用粘贴到终端的方式 不好
http://www.mailbrowse.com/linux-kernel/1501690.html
http://lwn.net/Articles/557046/

QA:
Q:Pid $number do not match expected $another_number
A:http://criu.org/When_C/R_fails and http://lists.openvz.org/pipermail/criu/2015-January/018504.html
  #before restore
  $unshare -p --fork --mount-proc 


Q: (00.039360) Error (cr-restore.c:943): Can't open -1/sys/kernel/ns_last_pid on procfs: No such file or directory
(00.039365) Error (cr-restore.c:945): 1153: Can't open sys/kernel/ns_last_pid: No such file or directory

A:
│ Symbol: CHECKPOINT_RESTORE [=n]                                                                                                                                                                      │  
  │ Type  : boolean                                                                                                                                                                                      │  
  │ Prompt: Checkpoint/restore support                                                                                                                                                                   │  
  │   Location:                                                                                                                                                                                          │  
  │ (1) -> General setup                                                                                                                                                                                 │  
  │   Defined at init/Kconfig:1156                                                                                                                                                                       │  
  │   Selects: PROC_CHILDREN [=n]

There is no  "Checkpoint/restore support" becasue : bool "Checkpoint/restore support" if EXPERT

 Symbol: EXPERT [=n]                                                                                                                                                                                  │  
  │ Type  : boolean                                                                                                                                                                                      │  
  │ Prompt: Configure standard kernel features (expert users)                                                                                                                                            │  
  │   Location:                                                                                                                                                                                          │  
  │ (1) -> General setup                                                                                                                                                                                 │  
  │   Defined at init/Kconfig:1355                                                                                                                                                                       │  
  │   Selects: DEBUG_KERNEL [=y]                                                                                                                                                                         │  
  │   Selected by: EMBEDDED [=n] 
