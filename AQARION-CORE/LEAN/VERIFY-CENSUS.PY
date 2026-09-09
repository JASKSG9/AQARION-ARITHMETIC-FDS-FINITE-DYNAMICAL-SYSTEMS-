B = {2:2,3:5,4:15,5:52,6:203,7:877,8:4140,9:21147}
total = sum(B[n]* (n**n) for n in [2,3,4,5])
assert total == 166483, f"got {total}"
assert B[6]* (6**6) == 203*46656
assert 203*202//2 == 20503
assert 21147*21146//2 == 223587231
print("Census 166483 VERIFIED, 166479 KILLED")
