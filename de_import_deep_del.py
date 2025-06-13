import gc


def delete_module(modname, paranoid=None):
    from sys import modules
    try:
        thismod = modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(thismod)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except:  # noqa: E722
            raise ValueError('must supply a finite list for paranoid')
        else:
            these_symbols = paranoid[:]
    del modules[modname]
    for mod in modules.values():
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == '__':  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                    pass


with open('/proc/self/status') as f:
    print('init', ''.join(line for line in f if line.startswith('VmRSS')).strip())

import asyncio  # noqa: E402

with open('/proc/self/status') as f:
    print('imported', ''.join(line for line in f if line.startswith('VmRSS')).strip())

del asyncio
delete_module('asyncio')
gc.collect()

with open('/proc/self/status') as f:
    print('de-imported', ''.join(line for line in f if line.startswith('VmRSS')).strip())
