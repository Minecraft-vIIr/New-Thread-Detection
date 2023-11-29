import wmi
import os
import sys
import time

def getpath():
    if getattr(sys, "frozen", False):
        application_path = sys.executable
    elif __file__:
        application_path = os.path.abspath(__file__)
    return application_path

save_path = os.path.join(os.path.dirname(getpath()), "log")
try:
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
except Exception as err:
    print(err)

c = wmi.WMI()
raw_wql = "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_Process'"
watcher = c.watch_for(raw_wql=raw_wql)

while True:
    process_created = watcher()

    print(f'\033[1;0m{time.strftime("[%Y.%m.%d %H:%M:%S]")}')
    print(f'\033[0mProcess Name: \033[1;32m{getattr(process_created, "Name", None)}')
    print(f'\033[0mParent PID: \033[1;32m{getattr(process_created, "ParentProcessId", None)}')
    print(f'\033[0mPID: \033[1;32m{getattr(process_created, "ProcessId", None)}')
    print(f'\033[0mCommand Line: \033[1;32m{getattr(process_created, "CommandLine", None)}')
    print()

    with open(os.path.join(save_path, f'{time.strftime("%Y%m%d-%H%M")}.txt'), "a", encoding="utf-8") as f:
        f.write(f'{time.strftime("[%Y.%m.%d %H:%M:%S]")}\n')
        f.write(f'Process Name: {getattr(process_created, "Name", None)}\n')
        f.write(f'Parent PID: {getattr(process_created, "ParentProcessId", None)}\n')
        f.write(f'PID: {getattr(process_created, "ProcessId", None)}\n')
        f.write(f'Command Line: {getattr(process_created, "CommandLine", None)}\n\n')
