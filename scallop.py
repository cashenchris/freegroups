
import pexpect, re

scallop_program = "/Users/chris/Research/Software/scallop/scallop"

# scallop is going to expect that the input words are written with group generators a-z.

def scl(*words,**kwargs):
    chain=" ".join([w() for w in words])
    H=pexpect.spawn(scallop_program + " " + chain)
    if 'maxtime' in kwargs:
        H.timeout = kwargs['maxtime']
    else:
        H.timeout=10
    try:
        raw_data = H.read()
        H.close()
        ans = re.search("scl_.*=(.*)\r", raw_data)
        if ans:
            thescl=float(ans.groups(1)[0])
        else:
            raise InputError, "scallop could not compute, maybe input not in commutator group"
    except pexpect.TIMEOUT:
        raise RuntimeError, "scallop timed out"

    return thescl

