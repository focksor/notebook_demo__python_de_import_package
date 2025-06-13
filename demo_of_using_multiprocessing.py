import multiprocessing


def run_in_other_process(func, *args, **kwargs):
    """
    Run a function in another process.
    """
    with multiprocessing.Pool(1) as pool:
        result = pool.apply(func, args, kwargs)
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
