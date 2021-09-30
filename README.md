# freegroups
Some scripts for working with finitely generated free groups and their automorphisms, Stallings graphs, Whitehead graphs, and determining geometricity/virtual geometricity of (multi)words and imprimitivity rank.

This requires, and is a subtree of:
https://github.com/cashenchris/grouptheory.git

Includes two command line scripts vg.py, for determining virtual geometricity, and irank.py for computing imprimitivity rank.

$ ./freegroups/vg.py a aabAAAB

True

This says the multiword {a, aabAAAB} in the free group <a,b> is virtually geomtric.

$ ./freegroups/irank.py aabbcc

3

This says the word aabbcc in the free group <a,b,c> has imprimitivity rank 3.


The geometricity and virtual geometricity code requires the program 'heegaard', available at:
 https://t3m.math.uic.edu/
From the heegaard root directory, the following commands should install the 'heegaard' python module.

$ cd python
$ python setup.py install --user


