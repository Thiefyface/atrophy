from sys import maxsize
from ctypes import *

def syscall_byname(name):
    for i in syscalls:
        if i[0] == name:
            return i 
    return  

def syscall_bynum(num):
    try: 
        return syscalls[num]
    except:
        return ("Undefined",)

# takes a reg struct and returns a list of correctly casted tuples
# First tuple will be (orig_eax,"syscall_name") 
# Rest will be of the format (c_type,value)
# since we know the order of the calls
def syscall_lookup(reg_struct):
    retlist = []
    name,c_type,value = "","",""
        
    if maxsize < 2**32:
        syscall_num_reg = "orig_eax"
        syscall_arg_reg = ("orig_eax","ebx","ecx","edx","esi","edi")
    else: 
        syscall_num_reg = "rax"
        syscall_arg_reg = ("rax","rdi","rsi","rdx","r10","r8","r9")  

    syscall_num = reg_struct.get_register(syscall_num_reg) 
    syscall = syscall_bynum(syscall_num)
    retlist.append(syscall[0])

    if len(syscall) == 1:
        return retlist
    
    # - iterate over all parameters of the syscall
    # - grab the appropriate register from the regstruct
    # - assign the ctype this value
    # - return list of tuples
    for i in range(1,len(syscall)): # start at 1 to ignore syscall name
        name = syscall_arg_reg[i]
        c_type = syscall[i] 
        value = reg_struct.get_register(name)
        retlist.append((c_type,value))

    return retlist


# Begin the syscall definitions
# x86

if maxsize < 2**32:
    syscalls = [
        ("restart_syscall",), # not used : 0
        ("exit",c_int),
        ("fork",c_void_p), 
        ("read",c_uint,c_char_p,c_uint),
        ("write",c_uint,c_char_p,c_uint),
        ("open",c_char_p,c_int,c_int),
        ("close",c_uint),
        ("waitpid",c_uint,pointer(c_int(0)),c_int),
        ("creat",c_char_p,c_int),
        ("link",c_char_p,c_char_p),
        ("unlink", c_char_p), 
        ("execve", c_void_p),
        ("chdir", c_char_p),
        ("time", pointer(c_int(0))),
        ("mknod", c_char_p,c_int,c_ushort),
        ("chmod", c_char_p,c_ushort),
        ("lchown", c_char_p,c_ushort,c_ushort),
        ("break",), # not used : 17
        ("oldstat", c_char_p,c_void_p), 
        ("lseek", c_uint,c_long,c_uint),
        ("getpid",),
        ("mount", c_char_p,c_char_p,c_char_p),
        ("umount", c_char_p),
        ("setuid", c_ushort),
        ("getuid",),
        ("stime",pointer(c_int(0)) ),
        ("ptrace",c_long,c_long,c_long,c_long ),
        ("alarm", c_uint),
        ("oldfstat", c_uint,c_void_p),
        ("pause",),# 29
        ("utime", c_char_p,c_void_p),
        ("stty",), # 31 unused
        ("gtty",), # 32 unused
        ("access",c_char_p,c_int),
        ("nice", c_int),
        ("ftime",), # 35 unused
        ("sync", ),
        ("kill", c_int,c_int),
        ("rename", c_char_p, c_char_p ),
        ("mkdir", c_char_p, c_int),
        ("rmdir", c_char_p ),
        ("dup", c_uint),
        ("pipe", c_ulong),
        ("times", c_void_p),
        ("prof",), # 44 unused
        ("brk",c_ulong ),
        ("setgid", c_ushort),
        ("getgid",),
        ("signal",c_int, c_void_p ),
        ("geteuid",),
        ("getegid",),
        ("acct", c_char_p ),
        ("umount2", c_char_p, c_int ),
        ("lock", ), # 53 unused
        ("ioctl", c_uint, c_uint, c_ulong ),
        ("fcntl", c_uint, c_uint, c_ulong ),
        ("mpx", ), # 56 unused
        ("setpgid", c_ushort, c_ushort),
        ("ulimit",) , # 58 unused
        ("oldolduname",c_void_p ),
        ("umask",c_int ),
        ("chroot",c_char_p ),
        ("ustat",c_ushort,c_void_p ),
        ("dup2", c_uint,c_uint),
        ("getppid",),
        ("getpgrp",),
        ("setsid",),
        ("sigaction",c_int,c_void_p,c_void_p ),
        ("sgetmask",),
        ("ssetmask", c_int ),
        ("setreuid", c_ushort,c_ushort),
        ("setregid", c_ushort,c_ushort),
        ("sigsuspend", c_int,c_int,c_ulong),
        ("sigpending", pointer(c_ulong(0)) ),
        ("sethostname", c_char_p,c_int ),
        ("setrlimit", c_uint,c_char_p),
        ("getrlimit", c_uint,c_char_p),
        ("getrusage", c_int,c_void_p),
        ("gettimeofday", c_void_p,c_void_p),
        ("settimeofday", c_void_p,c_void_p),
        ("getgroups",c_int,pointer(c_ushort(0))),
        ("setgroups",c_int,pointer(c_ushort(0))),
        ("select", c_void_p),
        ("symlink", c_char_p,c_char_p),
        ("oldlstat", c_char_p,c_void_p),
        ("readlink", c_char_p,c_char_p,c_int),
        ("uselib", c_char_p),
        ("swapon", c_char_p,c_int),
        ("reboot", c_int,c_int,c_int,c_void_p),
        ("readdir", c_uint,c_void_p,c_uint),
        ("mmap", c_void_p),
        ("munmap", c_ulong,c_ushort),
        ("truncate", c_char_p,c_ulong),
        ("ftruncate", c_uint,c_ulong),
        ("fchmod", c_uint,c_ushort),
        ("fchown", c_uint,c_ushort,c_ushort),
        ("getpriority", c_int,c_int),
        ("setpriority", c_int,c_int,c_int),
        ("profil",), # 98 unused
        ("statfs", c_char_p,c_void_p),
        ("fstatfs", c_uint,c_void_p),
        ("ioperm", c_ulong,c_ulong,c_int),
        ("socketcall", c_int,c_ulong),
        ("syslog", c_int,c_char_p,c_int),
        ("setitimer", c_int,c_void_p,c_void_p),
        ("getitimer", c_int,c_void_p),
        ("stat", c_char_p,c_void_p),
        ("lstat", c_char_p,c_void_p),
        ("fstat", c_uint,c_void_p),
        ("olduname", c_void_p ),
        ("iopl", c_ulong),
        ("vhangup",),
        ("idle",),
        ("vm86old",c_ulong,c_void_p ),
        ("wait4",c_ushort,pointer(c_ulong(0)),c_int,c_void_p),
        ("swapoff",c_char_p),
        ("sysinfo", c_void_p),
        #("ipc", c_uint,c_int,c_int,c_int,c_void_p,c_long), # six args => ptr of array of args in ebx
        ("ipc",c_void_p),
        ("fsync", c_uint),
        ("sigreturn", c_ulong),
        ("clone", c_void_p),
        ("setdomainname",c_char_p,c_int),
        ("uname", c_void_p),
        ("modify_ldt", c_int,c_void_p,c_ulong),
        ("adjtimex", c_void_p),
        ("mprotect", c_ulong,c_ushort,c_ulong),
        ("sigprocmask", c_int,pointer(c_ulong(0)),pointer(c_ulong(0))),
        ("create_module", c_char_p,c_ushort),
        ("init_module", c_char_p,c_void_p),
        ("delete_module", c_char_p),
        ("get_kernel_syms", c_void_p),
        ("quotactl", c_int,c_char_p,c_int,c_char_p),
        ("getpgid",c_int ),
        ("fchdir", c_uint),
        ("bdflush", c_int,c_long),
        ("sysfs", c_int,c_ulong,c_ulong),
        ("personality", c_ulong),
        ("afs_syscall", c_ushort),
        ("setfsuid", c_ushort),
        ("setfsgid", c_ushort),
        ("_llseek", c_uint,c_ulong,c_ulong,pointer(c_long(0)),c_uint),
        ("getdents", c_uint,c_void_p,c_uint),
        ("_newselect", c_int,c_void_p,c_void_p,c_void_p,c_void_p),
        ("flock", c_uint,c_uint),
        ("msync", c_ulong,c_ushort,c_int),
        ("readv", c_ulong,c_void_p,c_ulong),
        ("writev", c_ulong,c_void_p,c_ulong),
        ("getsid", c_ushort),
        ("fdatasync", c_uint),
        ("_sysctl", c_void_p),
        ("mlock", c_ulong,c_ushort),
        ("munlock", c_ulong,c_ushort),
        ("mlockall", c_int),
        ("munlockall",),
        ("sched_setparam",c_ushort,c_void_p),
        ("sched_getparam", c_ushort,c_void_p),
        ("sched_setscheduler", c_ushort,c_int,c_void_p),
        ("sched_getscheduler", c_ushort),
        ("sched_yield",),
        ("sched_get_priority_max", c_int),
        ("sched_get_priority_min", c_int),
        ("sched_rr_get_interval", c_ushort,c_void_p),
        ("nanosleep", c_void_p,c_void_p),
        ("mremap", c_ulong,c_ulong,c_ulong,c_ulong),
        ("setresuid", c_ushort,c_ushort,c_ushort),
        ("getresuid", pointer(c_ushort(0)),pointer(c_ushort(0)),pointer(c_ushort(0))),
        ("vm86", c_void_p),
        ("query_module", c_char_p,c_int,c_char_p,c_ushort,pointer(c_ushort(0))),
        ("poll", c_void_p,c_uint,c_long),
        ("nfsservctl", c_int,c_void_p,c_void_p),
        ("setresgid", c_ushort,c_ushort,c_ushort),
        ("getresgid", pointer(c_ushort(0)),pointer(c_ushort(0)),pointer(c_ushort(0))),
        ("prctl", c_int,c_ulong,c_ulong,c_ulong,c_ulong),
        ("rt_sigreturn", c_ulong),
        ("rt_sigaction", c_int,c_void_p,c_void_p,c_ushort),
        ("rt_sigprocmask", c_int,pointer(c_ulong(0)),pointer(c_ulong(0)),c_ushort),
        ("rt_sigpending", pointer(c_ulong(0)),c_ushort),
        ("rt_sigtimedwait", pointer(c_ulong(0)),c_void_p,c_void_p,c_ushort),
        ("rt_sigqueueinfo", c_int,c_int,c_void_p),
        ("rt_sigsuspend", pointer(c_ulong(0)),c_ushort),
        ("pread64", c_uint,c_char_p,c_uint,c_long),
        ("pwrite64", c_int,c_char_p,c_uint,c_long),
        ("chown", c_char_p,c_ushort,c_uint),
        ("getcwd", c_char_p,c_ulong),
        ("capget", c_void_p,c_void_p),
        ("capset", c_void_p,c_void_p),
        ("sigaltstack", c_void_p,c_void_p),
        ("sendfile", c_int,c_int,pointer(c_long(0)),c_uint),
        ("getpmsg",),#unused 188 
        ("putpmsg",),#unused 189
        ("vfork",c_void_p), #not sure where the rest of these come from...
        ("ugetrlimit",c_uint,c_void_p),
        ("mmap2", c_void_p,c_uint,c_int,c_int,c_int),
        ("truncate64", c_char_p, c_uint),
        ("ftruncate64", c_int, c_uint),
        ("stat64", c_char_p, c_void_p),
        ("lstat64", c_char_p,c_void_p),
        ("fstat64", c_char_p,c_void_p),
        ("lchown32", c_char_p,c_ushort,c_ushort),
        ("getuid32",),
        ("getgid32",),
        ("geteuid32",),
        ("getegid32",),
        ("setreuid32", c_ushort,c_ushort),
        ("setregid32", c_ushort,c_ushort),
        ("getgroups32", c_int,pointer(c_ushort(0))),
        ("setgroups32", c_int,pointer(c_ushort(0))),
        ("fchown32", ),
        ("setresuid32",pointer(c_ushort(0)),pointer(c_ushort(0)),pointer(c_ushort(0))),
        ("getresuid32", pointer(c_ushort(0)),pointer(c_ushort(0)),pointer(c_ushort(0))),
        ("setresgid32",c_ushort,c_ushort,c_ushort),
        ("getresgid32",pointer(c_ushort(0)),pointer(c_ushort(0)),pointer(c_ushort(0))),
        ("chown32", c_char_p,c_ushort,c_ushort),
        ("setuid32", c_ushort),
        ("setgid32", c_ushort),
        ("setfsuid32", c_ushort),
        ("setfsgid32", c_ushort),
        ("pivot_root", c_char_p,c_char_p),
        ("mincore", c_ulong,c_uint,c_char_p),
        ("madvise", c_ulong,c_uint,c_int),
        ("getdents64", c_uint,c_void_p,c_uint),
        ("fcntl64", c_uint,c_uint,c_ulong),
        ("unimplimented_222",),
        ("unimplimented_223",),
        ("gettid",), 
        ("readahead",c_int,c_uint,c_uint),
        ("setxattr",c_char_p,c_char_p,c_void_p,c_uint,c_int),
        ("lsetxattr",c_char_p,c_char_p,c_void_p,c_uint,c_int),
        ("fsetxattr",c_int,c_char_p,c_void_p,c_uint,c_int),
        ("getxattr",c_char_p,c_char_p,c_void_p,c_uint),
        ("lgetxattr",c_char_p,c_char_p,c_void_p,c_uint),
        ("fgetxattr",c_int,c_char_p,c_void_p,c_uint),
        ("listxattr", c_char_p,c_char_p,c_uint),
        ("llistxattr", c_char_p,c_char_p,c_uint),
        ("flistxattr", c_char_p,c_char_p,c_uint),
        ("removexattr",c_char_p,c_char_p),
        ("lremovexattr",c_char_p,c_char_p ),
        ("fremovexattr",c_int,c_char_p ),
        ("tkill", c_int,c_int),
        ("sendfile64",c_int,c_int,c_uint,c_uint),
        ("futex",),
        ("sched_setaffinity",c_ushort,c_uint,pointer(c_ulong(0))),
        ("sched_getaffinity",c_ushort,c_uint,pointer(c_ulong(0))),
        ("set_thread_area", c_void_p),
        ("get_thread_area", c_void_p),
        ("io_setup", c_ulong,pointer(c_ulong(0))),
        ("io_destroy", c_ulong),
        ("io_getevents",c_ulong,c_long,c_long,c_void_p,c_void_p ),
        ("io_submit", c_ulong,c_long,pointer(c_void_p(0))),
        ("io_cancel", c_ulong,c_void_p,c_void_p),
        ("fadvise64", c_int,c_void_p,c_uint,c_int),
        ("unimplimented_251",),
        ("exit_group",c_int),
        ("lookup_dcookie",c_ulonglong,c_char_p,c_uint),
        ("epoll_create",c_int),
        ("epoll_ctl", c_int,c_int,c_int,c_void_p),
        ("epoll_wait",c_int,c_void_p,c_int,c_int),
        ("remap_file_pages",c_ulong,c_ulong,c_ulong,c_ulong,c_ulong),
        ("set_tid_address",pointer(c_int(0))),
        ("timer_create",c_int,c_void_p,c_void_p),
        ("timer_settime", c_int,c_int,c_void_p,c_void_p),
        ("timer_gettime",c_int,c_void_p),
        ("timer_getoverrun",c_int),
        ("timer_delete", c_int),
        ("clock_settime", c_int,c_void_p),
        ("clock_gettime", c_int,c_void_p),
        ("clock_getres", c_int,c_void_p),
        ("clock_nanosleep", c_int,c_int,c_void_p,c_void_p),
        ("statfs64", c_char_p,c_uint,c_void_p),
        ("fstatfs64", c_uint,c_uint,c_void_p),
        ("tgkill", c_int,c_int,c_int),
        ("utimes", c_char_p,c_void_p),
        ("fadvise64_64",c_int,c_ulonglong,c_ulonglong,c_int),
        ("vserver",), #unimpliemented 273
        ("mbind",),
        ("get_mempolicy",pointer(c_int(0)),pointer(c_ulong(0)),c_ulong,c_ulong,c_ulong),
        ("set_mempolicy",c_int,pointer(c_ulong(0)),c_ulong),
        ("mq_open", c_char_p,c_int,c_uint,c_void_p),
        ("mq_unlink",c_char_p),
        ("mq_timedsend",c_int,c_char_p,c_uint,c_uint,c_void_p),
        ("mq_timedreceive",c_int,c_char_p,c_uint,pointer(c_uint(0)),c_void_p),
        ("mq_notify",c_int,c_void_p),
        ("mq_getsetattr",c_int,c_void_p,c_void_p),
        ("kexec_load",c_ulong,c_ulong,c_void_p,c_ulong),
        ("waitid",c_int,c_ushort,c_void_p,c_int,c_void_p),
        ("add_key",c_char_p,c_char_p,c_void_p,c_uint,c_long),
        ("request_key",c_char_p,c_char_p,c_char_p,c_long),
        ("keyctl",c_int,c_ulong,c_ulong,c_ulong,c_ulong,c_ulong),
        ("ioprio_set",c_int,c_int),
        ("ioprio_get", c_int,c_int),
        ("inotify_init",),
        ("inotify_add_watch", c_int,c_char_p,c_uint),
        ("inotify_rm_watch",c_int,c_uint ),
        ("migrate_pages", c_ushort,c_ulong,pointer(c_ulong(0)),pointer(c_ulong(0))),
        ("openat",c_int,c_char_p,c_int,c_int),
        ("mkdirat",c_int,c_char_p,c_int),
        ("mknodat",c_int,c_char_p,c_int,c_uint),
        ("fchownat",c_int,c_char_p,c_ushort,c_ushort,c_int),
        ("futimesat",c_int,c_char_p,c_void_p),
        ("fstatat64",c_int,c_char_p,c_void_p,c_int),
        ("unlinkat",c_int,c_char_p,c_int),
        ("renameat",c_int,c_char_p,c_int,c_char_p),
        ("linkat",c_int,c_char_p,c_int,c_char_p,c_int),
        ("symlinkat",c_char_p,c_int,c_char_p),
        ("readlinkat",c_int,c_char_p,c_char_p,c_int),
        ("fchmodat", c_int,c_char_p,c_uint),
        ("faccessat", c_int,c_char_p,c_int),
        ("pselect6",),
        ("ppoll", c_void_p,c_uint,c_void_p,c_void_p,c_uint),
        ("unshare",c_ulong ),
        ("set_robust_list",c_void_p,c_uint ),
        ("get_robust_list", c_int,c_void_p,c_void_p),
        ("splice",),
        ("sync_file_range",c_int,c_ulong,c_ulong,c_uint),
        ("tee",c_int,c_int,c_uint,c_uint),
        ("vmsplice", c_int,c_void_p,c_ulong,c_uint),
        ("move_pages",),
        ("getcpu",c_void_p,c_void_p,c_void_p),
        ("epoll_pwait",),
        ("utimensat",c_int,c_char_p,c_void_p,c_int),
        ("signalfd",c_int,c_void_p,c_uint),
        ("timerfd_create",c_int,c_int),
        ("eventfd",c_uint),
        ("fallocate",c_int,c_int,c_ulong,c_ulong),
        ("timerfd_settime",c_int,c_int,c_void_p,c_void_p),
        ("timerfd_gettime",c_int,c_int),
        ("signalfd4",c_int,c_void_p,c_uint,c_int),
        ("eventfd2",c_uint,c_int),
        ("epoll_create1", c_int ),
        ("dup3",c_uint,c_uint,c_int),
        ("pipe2",pointer(c_int(0)),c_int),
        ("inotify_init1",c_int),
        ("preadv",c_ulong,c_void_p,c_ulong,c_ulong,c_ulong),
        ("pwritev",c_ulong,c_void_p,c_ulong,c_ulong,c_ulong),
        ("rt_tgsigqueueinfo",c_ushort,c_ushort,c_int,c_void_p),
        ("perf_event_open",c_void_p,c_ushort,c_int,c_int,c_ulong),
        ("recvmmsg",c_int,c_void_p,c_uint,c_uint,c_void_p)
    ]

    '''
        ("fanotify_init", ),
        ("fanotify_mark", ),
        ("prlimit64", ),
        ("name_to_handle_at", ),
        ("open_by_handle_at", ),
        ("clock_adjtime", ),
        ("syncfs", ),
        ("sendmmsg", ),
        ("setns", ),
        ("process_vm_readv", ),
        ("process_vm_writev", ),
        ("kcmp", ),
        ("finit_module", ),
        ("sched_setattr", ),
        ("sched_getattr", ),
        ("renameat2", ),
        ("seccomp", ),
        ("getrandom", ),
        ("memfd_create", ),
        ("bpf", ),
        ("execveat", ),
        ("socket", ),
        ("socketpair", ),
        ("bind", ),
        ("connect", ),
        ("listen", ),
        ("accept4", ),
        ("getsockopt", ),
        ("setsockopt", ),
        ("getsockname", ),
        ("getpeername", ),
        ("sendto", ),
        ("sendmsg", ),
        ("recvfrom", ),
        ("recvmsg", ),
        ("shutdown", ),
        ("userfaultfd", ),
        ("membarrier", ),
        ("mlock2", ),
    '''

else:

# Begin syscall definitions
# x64
    syscalls = [
        ("read", c_uint,c_char_p,c_ulong),
        ("write", c_uint,c_char_p,c_ulong),
        ("open", c_char_p,c_int,c_int),
        ("close", c_uint),
        ("stat", c_char_p,c_void_p),
        ("fstat", c_uint,c_void_p),
        ("lstat", c_char_p,c_void_p),
        ("poll", c_void_p,c_uint,c_long),
        ("lseek", c_uint,c_ulong,c_uint),
        ("mmap", c_ulong,c_ulong,c_ulong,c_ulong,c_ulong,c_ulong),
        ("mprotect", c_ulong,c_ulong,c_ulong),
        ("munmap",c_ulong,c_ulong),
        ("brk", c_ulong),
        ("rt_sigaction", c_int,c_void_p,c_void_p,c_ulong),
        ("rt_sigprocmask", c_int,c_void_p,c_void_p,c_ulong),
        ("rt_sigreturn",c_ulong),
        ("ioctl", c_uint,c_uint,c_ulong),
        ("pread64",c_ulong,c_char_p,c_ulong,c_ulong ),
        ("pwrite64",c_uint,c_char_p,c_ulong,c_ulong ),
        ("readv",c_ulong,c_char_p,c_ulong),
        ("writev", c_ulong,c_char_p,c_ulong),
        ("access", c_char_p,c_int),
        ("pipe", pointer(c_int(0))),
        ("select", c_int,c_void_p,c_void_p,c_void_p,c_void_p),
        ("sched_yield"),
        ("mremap",c_ulong,c_ulong,c_ulong,c_ulong,c_ulong ),
        ("msync", c_ulong,c_ulong,c_int),
        ("mincore", c_ulong,c_ulong,c_char_p),
        ("madvise", c_ulong,c_ulong,c_int),
        ("shmget", ),
        ("shmat", ),
        ("shmctl", ),
        ("dup", ),
        ("dup2", ),
        ("pause", ),
        ("nanosleep", ),
        ("getitimer", ),
        ("alarm", ),
        ("setitimer", ),
        ("getpid", ),
        ("sendfile", ),
        ("socket",c_int,c_int,c_int ),
        ("connect",c_int,c_void_p,c_int),
        ("accept", c_int,c_void_p,c_int),
        ("sendto", c_int,c_void_p,c_ulong,c_uint,c_void_p,pointer(c_int(0))),
        ("recvfrom",  c_int,c_void_p,c_ulong,c_uint,c_void_p,pointer(c_int(0))),
        ("sendmsg", c_int, c_void_p,c_uint),
        ("recvmsg", c_int,c_void_p,c_uint),
        ("shutdown", c_int,c_int),
        ("bind", c_int,c_void_p,c_int),
        ("listen", c_int,c_int),
        ("getsockname", c_int,c_void_p,c_int),
        ("getpeername", c_int,c_void_p,c_int),
        ("socketpair", c_int,c_int,c_int,pointer(c_int(0))),
        ("setsockopt", c_int,c_int,c_int,c_char_p,c_int),
        ("getsockopt", c_int,c_int,c_int,c_char_p,pointer(c_int(0))),
        ("clone", c_ulong,c_ulong,c_void_p,c_void_p),
        ("fork"),
        ("vfork"),
        ("execve",c_char_p,c_char_p,c_char_p),
        ("exit", c_int),
        ("wait4", c_int),
        ("kill", c_int,c_int),
        ("uname", ),
        ("semget", ),
        ("semop", ),
        ("semctl", ),
        ("shmdt", ),
        ("msgget", ),
        ("msgsnd", ),
        ("msgrcv", ),
        ("msgctl", ),
        ("fcntl", c_uint,c_uint,c_ulong),
        ("flock", ),
        ("fsync", ),
        ("fdatasync", ),
        ("truncate", ),
        ("ftruncate", ),
        ("getdents", ),
        ("getcwd", c_char_p,c_ulong ),
        ("chdir", c_char_p),
        ("fchdir", c_uint),
        ("rename", c_char_p,c_char_p),
        ("mkdir", c_char_p,c_int),
        ("rmdir", c_char_p),
        ("creat", c_char_p,c_int),
        ("link", c_char_p,c_char_p),
        ("unlink", c_char_p),
        ("symlink", c_char_p,c_char_p),
        ("readlink", c_char_p,c_char_p,c_int),
        ("chmod", c_char_p,c_int),
        ("fchmod", c_uint,c_int),
        ("chown", c_char_p,c_int,c_int),
        ("fchown", c_uint,c_int,c_int),
        ("lchown", c_char_p,c_int,c_int),
        ("umask", c_int),
        ("gettimeofday", ),
        ("getrlimit", ),
        ("getrusage", ),
        ("sysinfo", ),
        ("times", ),
        ("ptrace", c_long,c_long,c_ulong,c_ulong),
        ("getuid"),
        ("syslog",c_int,c_char_p,c_int ),
        ("getgid" ),
        ("setuid", ),
        ("setgid", ),
        ("geteuid", ),
        ("getegid", ),
        ("setpgid", ),
        ("getppid", ),
        ("getpgrp", ),
        ("setsid", ),
        ("setreuid", ),
        ("setregid", ),
        ("getgroups", ),
        ("setgroups", ),
        ("setresuid", ),
        ("getresuid", ),
        ("setresgid", ),
        ("getresgid", ),
        ("getpgid", ),
        ("setfsuid", ),
        ("setfsgid", ),
        ("getsid", ),
        ("capget", ),
        ("capset", ),
        ("rt_sigpending", ),
        ("rt_sigtimedwait", ),
        ("rt_sigqueueinfo", ),
        ("rt_sigsuspend", ),
        ("sigaltstack", ),
        ("utime", ),
        ("mknod", ),
        ("uselib", ),
        ("personality", ),
        ("ustat", ),
        ("statfs", ),
        ("fstatfs", ),
        ("sysfs", ),
        ("getpriority", ),
        ("setpriority", ),
        ("sched_setparam", ),
        ("sched_getparam", ),
        ("sched_setscheduler", ),
        ("sched_getscheduler", ),
        ("sched_get_priority_max", ),
        ("sched_get_priority_min", ),
        ("sched_rr_get_interval", ),
        ("mlock", ),
        ("munlock", ),
        ("mlockall", ),
        ("munlockall", ),
        ("vhangup", ),
        ("modify_ldt", ),
        ("pivot_root", ),
        ("_sysctl", ),
        ("prctl", ),
        ("arch_prctl", ),
        ("adjtimex", ),
        ("setrlimit", ),
        ("chroot", ),
        ("sync", ),
        ("acct", ),
        ("settimeofday", ),
        ("mount", ),
        ("umount2", ),
        ("swapon", ),
        ("swapoff", ),
        ("reboot", ),
        ("sethostname", ),
        ("setdomainname", ),
        ("iopl", ),
        ("ioperm", ),
        ("create_module", ),
        ("init_module", ),
        ("delete_module", ),
        ("get_kernel_syms", ),
        ("query_module", ),
        ("quotactl", ),
        ("nfsservctl", ),
        ("getpmsg", ),
        ("putpmsg", ),
        ("afs_syscall", ),
        ("tuxcall", ),
        ("security", ),
        ("gettid", ),
        ("readahead", ),
        ("setxattr", ),
        ("lsetxattr", ),
        ("fsetxattr", ),
        ("getxattr", ),
        ("lgetxattr", ),
        ("fgetxattr", ),
        ("listxattr", ),
        ("llistxattr", ),
        ("flistxattr", ),
        ("removexattr", ),
        ("lremovexattr", ),
        ("fremovexattr", ),
        ("tkill", ),
        ("time", ),
        ("futex", ),
        ("sched_setaffinity", ),
        ("sched_getaffinity", ),
        ("set_thread_area", ),
        ("io_setup", ),
        ("io_destroy", ),
        ("io_getevents", ),
        ("io_submit", ),
        ("io_cancel", ),
        ("get_thread_area", ),
        ("lookup_dcookie", ),
        ("epoll_create", ),
        ("epoll_ctl_old", ),
        ("epoll_wait_old", ),
        ("remap_file_pages", ),
        ("getdents64", ),
        ("set_tid_address", ),
        ("restart_syscall", ),
        ("semtimedop", ),
        ("fadvise64", ),
        ("timer_create", ),
        ("timer_settime", ),
        ("timer_gettime", ),
        ("timer_getoverrun", ),
        ("timer_delete", ),
        ("clock_settime", ),
        ("clock_gettime", ),
        ("clock_getres", ),
        ("clock_nanosleep", ),
        ("exit_group", ),
        ("epoll_wait", ),
        ("epoll_ctl", ),
        ("tgkill", ),
        ("utimes", ),
        ("vserver", ),
        ("mbind", ),
        ("set_mempolicy", ),
        ("get_mempolicy", ),
        ("mq_open", ),
        ("mq_unlink", ),
        ("mq_timedsend", ),
        ("mq_timedreceive", ),
        ("mq_notify", ),
        ("mq_getsetattr", ),
        ("kexec_load", ),
        ("waitid", ),
        ("add_key", ),
        ("request_key", ),
        ("keyctl", ),
        ("ioprio_set", ),
        ("ioprio_get", ),
        ("inotify_init", ),
        ("inotify_add_watch", ),
        ("inotify_rm_watch", ),
        ("migrate_pages", ),
        ("openat", ),
        ("mkdirat", ),
        ("mknodat", ),
        ("fchownat", ),
        ("futimesat", ),
        ("newfstatat", ),
        ("unlinkat", ),
        ("renameat", ),
        ("linkat", ),
        ("symlinkat", ),
        ("readlinkat", ),
        ("fchmodat", ),
        ("faccessat", ),
        ("pselect6", ),
        ("ppoll", ),
        ("unshare", ),
        ("set_robust_list", ),
        ("get_robust_list", ),
        ("splice", ),
        ("tee", ),
        ("sync_file_range", ),
        ("vmsplice", ),
        ("move_pages", ),
        ("utimensat", ),
        ("epoll_pwait", ),
        ("signalfd", ),
        ("timerfd_create", ),
        ("eventfd", ),
        ("fallocate", ),
        ("timerfd_settime", ),
        ("timerfd_gettime", ),
        ("accept4", ),
        ("signalfd4", ),
        ("eventfd2", ),
        ("epoll_create1", ),
        ("dup3", ),
        ("pipe2", ),
        ("inotify_init1", ),
        ("preadv", ),
        ("pwritev", ),
        ("rt_tgsigqueueinfo", ),
        ("perf_event_open", ),
        ("recvmmsg", ),
        ("fanotify_init", ),
        ("fanotify_mark", ),
        ("prlimit64", ),
        ("name_to_handle_at", ),
        ("open_by_handle_at", ),
        ("clock_adjtime", ),
        ("syncfs", ),
        ("sendmmsg", ),
        ("setns", ),
        ("getcpu", ),
        ("process_vm_readv", ),
        ("process_vm_writev", ),
        ("kcmp", ),
        ("finit_module", ),
        ("sched_setattr", ),
        ("sched_getattr", ),
        ("renameat2", ),
        ("seccomp", ),
        ("getrandom", ),
        ("memfd_create", ),
        ("kexec_file_load", ),
        ("bpf", ),
        ("execveat", ),
        ("userfaultfd", ),
        ("membarrier", ),
        ("mlock2", ),
    ]



