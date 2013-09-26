def iter_prefix(l, prefix_len=1):
    # Break a sequence into prefix_len prefixes and what follows them
    return (
        (
            tuple(l[i:i + prefix_len]),
            l[i + prefix_len]
        ) for i in range(len(l) - prefix_len)
    )

if __name__ == "__main__":
    for i in iter_prefix(range(10), 1):
        print i
    for i in iter_prefix(range(10), 2):
        print i
    for i in iter_prefix(range(10), 3):
        print i
