def gap_compressor(line):
    temp = line.split(":")
    word = temp[0]
    posting_list = temp[1].split("|")
    posting_list = [[int(i.split("-")[0][1:]), i.split("-")[1]] for i in posting_list]
    for i in range(len(posting_list)-1, 0, -1):
        posting_list[i][0] = posting_list[i][0] - posting_list[i-1][0]

    posting_list = [str(i[0]) + "-" + i[1] for i in posting_list]
    compressed_line = word + "-" + str(len(posting_list)) + ":" + "|".join(posting_list)
    return compressed_line


def si_creator(index):
    second_index = {}
    with open(index, "r") as fp:
        cnt = 1
        for line in fp:
            head = line[0]
            if head not in second_index:
                second_index[line[0]] = [cnt, 0]
            else:
                second_index[line[0]][1] += 1
            cnt += 1
    secodary_filename = index.split("index.txt")[0] + 'secondary_' + index.split("/")[-1]
    fs = open(secodary_filename, "w+")
    fp = open(index, "r")
    for k, v in second_index.items():
        fs.write(k + ":" + str(v[0]) + "-" + str(v[0]+v[1]) + "\n")
        f = open(index.split("index.txt")[0] + k + ".txt", "w+")
        for i in range(v[0], v[0] + v[1] + 1):
            f.write(fp.readline())


def index_compressor(infile, outfile):
    fi = open(infile, "r")
    with open(outfile, "w+") as fo:
        for line in fi:
            fo.write(gap_compressor(line))
