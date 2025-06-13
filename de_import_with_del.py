import gc
import sys

with open('/proc/self/status') as f:
    print('init', ''.join(line for line in f if line.startswith('VmRSS')).strip())

import asyncio

with open('/proc/self/status') as f:
    print('imported', ''.join(line for line in f if line.startswith('VmRSS')).strip())

del asyncio
del sys.modules['asyncio']
gc.collect()

with open('/proc/self/status') as f:
    print('de-imported', ''.join(line for line in f if line.startswith('VmRSS')).strip())
