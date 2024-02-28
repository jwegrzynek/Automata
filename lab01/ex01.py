def bin_from_int(x, n):
    return [int(bit) for bit in format(x, f'0{n}b')]


print(bin_from_int(25, 8))
print(bin_from_int(50, 10))
print(bin_from_int(111, 9))


def int_from_bin(bits_list):
    return int(''.join(str(bit) for bit in bits_list), 2)


print(int_from_bin(bin_from_int(25, 8)))
print(int_from_bin(bin_from_int(50, 10)))
print(int_from_bin(bin_from_int(111, 9)))

print('-------------------------')


def my_bin_from_int(x, n):
    result = []

    while x != 0:
        result.append(x % 2)
        x = x // 2

    if len(result) > n:
        return "n is too small"
    else:
        while len(result) < n:
            result.append(0)
    return result[::-1]


print(my_bin_from_int(25, 8))
print(my_bin_from_int(50, 10))
print(my_bin_from_int(111, 9))


def my_int_from_bin(bits_list):
    res = 0
    for step, b in enumerate(bits_list[::-1]):
        res += b * 2 ** step

    return res


print(my_int_from_bin(my_bin_from_int(25, 8)))
print(my_int_from_bin(my_bin_from_int(50, 10)))
print(my_int_from_bin(my_bin_from_int(111, 9)))
