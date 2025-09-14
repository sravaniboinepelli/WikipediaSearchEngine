import math
import multiprocessing
import sys

def merge(*args):
    # This function merges two sorted lists, `left` and `right`, into a single sorted list.
    # It can accept the lists as two separate arguments or as a single two-item tuple,
    # which is useful for parallel processing with `multiprocessing.Pool`.
    left, right = args[0] if len(args) == 1 else args
    left_length, right_length = len(left), len(right)
    left_index, right_index = 0, 0
    merged = []

    # Iterate through both lists, appending the smaller element to `merged`.
    while left_index < left_length and right_index < right_length:
        ltemp = left[left_index].split(":")
        rtemp = right[right_index].split(":")
        if ltemp[0] < rtemp[0]:
            merged.append(left[left_index])
            left_index += 1
        elif ltemp[0] > rtemp[0]:
            merged.append(right[right_index])
            right_index += 1
        else:
            # If the keys are identical, combine the values and append to `merged`.
            merged.append(ltemp[0] + ":" + ltemp[1].rstrip() + "|" + rtemp[1].rstrip() + "\n")
            left_index += 1
            right_index += 1

    # Append any remaining elements from the list that hasn't been fully processed.
    if left_index == left_length:
        merged.extend(right[right_index:])
    else:
        merged.extend(left[left_index:])
    return merged


def merge_sort(data):
    # Divides the list in half, recursively sorts each half, and then merges them.
    length = len(data)
    if length <= 1:
        return data
    middle = length // 2
    left = merge_sort(data[:middle])
    right = merge_sort(data[middle:])
    return merge(left, right)


def merge_sort_parallel(data):
    # This function performs a parallel merge sort by utilizing multiple CPU cores.
    # It first divides the data into chunks, sorts each chunk in parallel,
    # and then merges the sorted chunks sequentially.

    # Initialize a pool of worker processes, one for each CPU core.
    processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=processes)
    
    # Partition the data into equal-sized chunks for each worker process.
    size = int(math.ceil(float(len(data)) / processes))
    data = [data[i * size:(i + 1) * size] for i in range(processes)]
    
    # Use the worker pool to sort each partition in parallel.
    data = pool.map(merge_sort, data)
    
    # Sequentially merge the sorted partitions in pairs until only one remains.
    while len(data) > 1:
        # Handle cases with an odd number of partitions by setting aside the last one and appending it later.
        extra = data.pop() if len(data) % 2 == 1 else None
        
        # Pair up the remaining partitions for merging.
        data = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]
        
        # Merge the pairs in parallel and re-add the extra partition if it exists.
        data = pool.map(merge, data) + ([extra] if extra else [])
        
    return data[0]