import re

s = "00115faabbcc"
s2 = "".join(reversed(s))
print(s2)
"""s2 = re.sub(r'(.{2})', r':\1', s)[1:]
print(s2)"""