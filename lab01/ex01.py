def bin_from_int(x, n):
    result = [0 for _ in range(n)]
    step = 0

    if n < len('{0:08b}'.format(x)):
        return "n is too small"

    while x != 0:
        result[len(result) - 1 - step] = x % 2
        x = x // 2
        step += 1
    return result


print(bin_from_int(25, 8))
print(bin_from_int(50, 10))
print(bin_from_int(4, 2))


def int_from_bin(bin_in_list):
    res = 0
    for step, b in enumerate(bin_in_list[::-1]):
        res += b * 2 ** step

    return res


print(int_from_bin(bin_from_int(25, 8)))
print(int_from_bin(bin_from_int(50, 10)))
