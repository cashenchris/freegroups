#!/usr/bin/env python

## usage:  ./vg.py word1, word2, ...
## decide if wordlist is virtually geometric
## wordi is a string where a-z represent generators of free group and A-Z their inverses

import freegroup
import virtuallygeometric
import sys

####

F=freegroup.FGFreeGroup(numgens=26)
wordlist=[F.word(str(x)) for x in sys.argv[1:]]
print virtuallygeometric.is_virtually_geometric(F,wordlist)
