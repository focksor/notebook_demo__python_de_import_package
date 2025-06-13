import os
import pickle
import socket


def run_in_other_process(func, *args, **kwargs):
    """
    Run a function in another process using os.fork and socket.socketpair.
    """
    parent_sock, child_sock = socket.socketpair()
    pid = os.fork()

    if pid == 0:  # Child process
        parent_sock.close()
        try:
            result = func(*args, **kwargs)
            child_sock.sendall(pickle.dumps(result))
        except Exception as e:
            child_sock.sendall(pickle.dumps(e))
        finally:
            child_sock.close()
        os._exit(0)
    else:  # Parent process
        child_sock.close()
        result = pickle.loads(parent_sock.recv(4096))
        parent_sock.close()
        if isinstance(result, Exception):
            raise result
        return result


def a_task_using_asyncio(a):
    with open('/proc/self/status') as f:
        print('task init', ''.join(line for line in f if line.startswith('VmRSS')).strip())
    import asyncio  # noqa: F401
    with open('/proc/self/status') as f:
        print('imported', ''.join(line for line in f if line.startswith('VmRSS')).strip())
    return a ** a


with open('/proc/self/status') as f:
    print('init', ''.join(line for line in f if line.startswith('VmRSS')).strip())

assert run_in_other_process(a_task_using_asyncio, 3) == 27

with open('/proc/self/status') as f:
    print('task done', ''.join(line for line in f if line.startswith('VmRSS')).strip())
