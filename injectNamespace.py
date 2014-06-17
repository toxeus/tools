#!/usr/bin/env python

# Copyright (C) 2014  Filip Gospodinov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import sys

if len(sys.argv) != 3:
    print("Usage: injectNamespace.py namespaceName file")
    exit()
namespaceName = sys.argv[1]
fileName = sys.argv[2]

f = open(fileName, 'r')
oldFile = f.readlines()
f.close()
for index, line in enumerate(oldFile):
    if re.match("#include.*(\"|<)", line):
        lastIncludeIndex = index
if 'lastIncludeIndex' not in locals():
    print("%s cannot be processed" % fileName)
    exit()
lastIncludeIndex += 1
newFile = oldFile[:lastIncludeIndex]
remainingIndex = 0
for index, line in enumerate(oldFile[lastIncludeIndex:]):
    if re.match("^\s*$", line) or re.match("^\s*//", line) or \
            re.match("^\s*using\s+namespace", line):
        newFile.append(line)
    else:
        if newFile[-1] != "\n":
            newFile.append("\n")
        newFile.append("namespace %s {\n\n" % namespaceName)
        remainingIndex = index
        break
newFile.extend(oldFile[(lastIncludeIndex + remainingIndex):])
newFile.append("\n} // namespace %s\n" % namespaceName)
f = open(fileName, 'w')
f.write("".join(newFile))
f.close()
