# -*- coding: utf-8 -*-


def mc(a):
    ret = ""
    b = "0123456789ABCDEF"
    if a == ord(' '):
        ret = "+"
    elif (a < ord('0') and a != ord('-') and a != ord('.')) or (a < ord('A') and a > ord('9')) or (a > ord('Z') and a < ord('a') and a != ord('_')) or (a > ord('z')):
        ret = "%" + b[a >> 4] + b[a & 15];
    else:
        ret = chr(a)
    return ret
    
def m(a):
    return (((a & 1) << 7) | ((a & (0x2)) << 5) | ((a & (0x4)) << 3) | ((a & (0x8)) << 1) | ((a & (0x10)) >> 1) | ((a & (0x20)) >> 3) | ((a & (0x40)) >> 5) | ((a & (0x80)) >> 7))

def md6(a):
    b = ""
    c = 0xbb
    for i  in range(0,len(a)):
        c = m(ord(a[i])) ^ (0x35 ^ (i & 0xff))
        d = hex(c)
        b += mc(c)
    return b
    