import os
import pickle


def run_in_other_process(func, *args, **kwargs):
    """
    Run a function in another process using os.fork and os.pipe.
    """
    read_fd, write_fd = os.pipe()
    pid = os.fork()

    if pid == 0:  # Child process
        os.close(read_fd)
        try:
            result = func(*args, **kwargs)
            with os.fdopen(write_fd, 'wb') as wf:
                wf.write(pickle.dumps(result))
        except Exception as e:
            with os.fdopen(write_fd, 'wb') as wf:
                wf.write(pickle.dumps(e))
        os._exit(0)
    else:  # Parent process
        os.close(write_fd)
        with os.fdopen(read_fd, 'rb') as rf:
            result = pickle.loads(rf.read())
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
