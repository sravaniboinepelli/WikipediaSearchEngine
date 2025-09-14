import os
from merge_sort import merge_sort_parallel


class FileSplitter(object):
    BLOCK_FILENAME_FORMAT = 'block_{0}.dat'

    def __init__(self, filename):
        self.filename = filename
        self.block_filenames = []

    def write_block(self, data, block_number):
        filename = self.BLOCK_FILENAME_FORMAT.format(block_number)
        file = open(filename, 'w')
        file.write(data)
        file.close()
        self.block_filenames.append(filename)

    def get_block_filenames(self):
        return self.block_filenames

    def split(self, block_size, sort_key=None):
        file = open(self.filename, 'r')
        i = 0

        while True:
            lines = file.readlines(block_size)

            if lines == []:
                break

            lines = merge_sort_parallel(lines)

            self.write_block(''.join(lines), i)
            i += 1

    def cleanup(self):
        map(lambda f: os.remove(f), self.block_filenames)


class NWayMerge(object):
    def select(self, choices):
        min_index = -1
        min_str = None

        for i in range(len(choices)):
            if min_str is None or choices[i].split(":")[0] < min_str.split(":")[0]:
                min_index = i
                min_str = choices[i]

        return min_index


class FilesArray(object):
    def __init__(self, files):
        self.files = files
        self.empty = set()
        self.num_buffers = len(files)
        self.buffers = {i: None for i in range(self.num_buffers)}

    def get_dict(self):
        return {i: self.buffers[i] for i in range(self.num_buffers) if i not in self.empty}

    def refresh(self):
        for i in range(self.num_buffers):
            if self.buffers[i] is None and i not in self.empty:
                self.buffers[i] = self.files[i].readline()

                if self.buffers[i] == '':
                    self.empty.add(i)

        if len(self.empty) == self.num_buffers:
            return False

        return True

    def unshift(self, index):
        value = self.buffers[index]
        self.buffers[index] = None

        return value


class FileMerger(object):
    def __init__(self, merge_strategy):
        self.merge_strategy = merge_strategy

    def merge(self, filenames, outfilename, buffer_size):
        outfile = open(outfilename, 'w', buffer_size)
        buffers = FilesArray(self.get_file_handles(filenames, buffer_size))

        while buffers.refresh():
            min_index = self.merge_strategy.select(buffers.get_dict())
            outfile.write(buffers.unshift(min_index))

    def get_file_handles(self, filenames, buffer_size):
        files = {}

        for i in range(len(filenames)):
            files[i] = open(filenames[i], 'r', buffer_size)

        return files


class ExternalSort(object):
    def __init__(self, block_size):
        self.block_size = block_size

    def sort(self, filename, sort_key=None):
        num_blocks = self.get_number_blocks(filename, self.block_size)
        splitter = FileSplitter(filename)
        splitter.split(self.block_size, sort_key)

        merger = FileMerger(NWayMerge())
        buffer_size = self.block_size // (num_blocks + 1)
        merger.merge(splitter.get_block_filenames(), filename + '.out', int(buffer_size))

        splitter.cleanup()

    def get_number_blocks(self, filename, block_size):
        return (os.stat(filename).st_size / block_size) + 1


def parse_memory(string):
    if string[-1].lower() == 'k':
        return int(string[:-1]) * 1024
    elif string[-1].lower() == 'm':
        return int(string[:-1]) * 1024 * 1024
    elif string[-1].lower() == 'g':
        return int(string[:-1]) * 1024 * 1024 * 1024
    else:
        return int(string)


def sort_file(filename, memory):
    sorter = ExternalSort(parse_memory(memory))
    sorter.sort(filename)
