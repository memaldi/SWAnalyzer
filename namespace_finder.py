import time
import json
import copy
import multiprocessing

PERCENT = 0.1 # PERCENT

def _map_impl(urls):
    data = {}
    for url in urls:
        previous_dict = data
        for c in filter(None, url.split('/')):
            if c in previous_dict:
                pos, d = previous_dict[c]
                previous_dict[c] = (pos + 1, d)
            else:
                previous_dict[c] = (1, {})

            previous_dict = previous_dict[c][1]
    return data

def _search_base(datas, parent):
    valued_keys = {}

    value = 0

    for data in datas:
        if isinstance(data, dict):
            continue

        current_value, data_dict = data
        value += current_value

        if not isinstance(data_dict, dict):
            print "ERROR: data_dict is a %s; data was %s with len = %s; data_dict len = %s; cur_value is %s" % (str(type(data_dict)), type(data), len(data), len(data_dict), type(current_value))

        for key in data_dict:
            child_value, _ = data_dict[key]
            if key not in valued_keys:
                valued_keys[key] = child_value
            else:
                valued_keys[key] += child_value

    valued_keys = valued_keys.items()
    if len(valued_keys) == 0:
        return 0, parent

    next_key, max_pos = max(valued_keys, key = lambda x : x[1])

    new_datas = [ data[1][next_key] for data in datas if next_key in data[1] ]
    
    child_value, route = _search_base(new_datas, parent + next_key + '/')
    if parent == 'http:/':
        return child_value, route
    elif child_value * (1.0 + PERCENT) >= value:
        return child_value, route
    else:
        return value, parent
       
def _search(datas):
    return _search_base([(0, data) for data in datas], '')

def find_pattern(dataset, branches = 5, subprocesses = False, verbose = False):
    if branches > len(dataset):
        branches = len(dataset)

    

    slot_size = len(dataset) / branches
    current_slot = 0
    datasets = [[]]
    current_dataset = datasets[0]
    for url in dataset:
        current_dataset.append(url)

        current_slot += 1
        current_slot %= branches
        if current_slot == 0:
            current_dataset = []
            datasets.append(current_dataset)
    
    if verbose:
        initial_map = time.time()

    if subprocesses:
        pool = multiprocessing.Pool(branches)
        results = pool.map(_map_impl, datasets)
    else:
        results = map(_map_impl, datasets)

    if verbose:
        initial_search = time.time()
        print "Map finished: %.2f " % (initial_search - initial_map)

    result = _search(results)

    if verbose:
        end_search = time.time()
        print "Search finished: %.2f" % (end_search - initial_search)

    result = (result[0], result[1].replace('http:/', 'http://'))
    return result


