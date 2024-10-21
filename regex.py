import re
from fuzzywuzzy import process


def gettext(file, mode='normal') -> list:
    templines = []
    if mode == 'normal':
        with open(file, 'r') as f:
            for line in f.readlines():
                # templines.append(line.strip().split(']')[1])
                templines.append(line.strip())
    elif mode == 'debug':
        with open(file, 'r') as f:
            for line in f.readlines():
                templines.append(line.strip())

    return templines


def result_format(result):
    n = 1
    for mainstr, substr in result:
        print(f"\nResult {n}: {substr}\n{mainstr}")
        n += 1


def main():
    filepath = input("Please input the filepath: ").strip()
    keystrs = input("Please input the keystrs [default: 'flag']: ").strip()
    if not keystrs:
        keystrs = "flag"
    keychar = list(keystrs)
    pattern = '[^a-zA-Z0-9]*'.join(keychar) + ".*"
    # pattern = "f[^a-zA-Z0-9]+l[^a-zA-Z0-9]+a[^a-zA-Z0-9]+g.+"
    bytelimit = input("Please set the bytelimit [default: 10]: ").strip()
    bytelimit = int(bytelimit) if bytelimit.isdigit() else 10

    logs = []
    results = []
    contents = gettext(filepath)
    for text in contents:
        strings = re.findall(pattern, text)
        if strings:
            logs.append(strings[0])

    if not logs:
        print("No flags found.")
        return 0

    for log in logs:
        normalized_log = log.lower()

        # 遍历日志中的每一个可能的10个字节序列
        for i in range(len(normalized_log) - bytelimit - 1):
            substring = normalized_log[i:i + bytelimit]

            # 检查是否包含所有要搜索的字符
            if all(char in substring for char in keychar):
                # 记录结果（可以记录原始日志和匹配的子字符串）
                results.append((log, substring))

    results = sorted(results, key=lambda x: x[1])
    result_format(results)
    best_result = process.extractOne(keystrs, results)
    print("")
    print(f"Possibility: {best_result[1]}%")
    print(best_result[0])
    print("")


if __name__ == '__main__':
    main()
