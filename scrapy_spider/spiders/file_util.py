def get_list(path):
    array = []
    with open(path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        url = line.strip()
        if len(url) > 0:
            array.append(url)
    return list(set(array))
