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

def _reduce_impl(urls_base, urls_new):
    for key in urls_new:

        if not key in urls_base:
            urls_base[key] = copy.deepcopy(urls_new[key])

        else:
            val1, dict_urls_new  = urls_new[key]
            val2, dict_urls_base = urls_base[key]
            urls_base[key] = (val1 + val2, _reduce_impl(dict_urls_base, dict_urls_new))

    return urls_base

def _search_base(data, parent):
    if isinstance(data, dict) or len(data[1].keys()) == 0:
        return 0, parent
    
    value, new_data = data

    valued_keys = []
    
    for key in new_data:
        child_value, _ = new_data[key]
        valued_keys.append( (key, child_value) )

    next_key, max_pos = max(valued_keys, key = lambda x : x[1])
    
    child_value, route = _search_base(new_data[next_key], parent + next_key + '/')
    if parent == 'http:/':
        return child_value, route
    elif child_value * (1.0 + PERCENT) >= value:
        return child_value, route
    else:
        return value, parent


def _search(data):
    return _search_base((0, data), '')

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
        initial_reduce = time.time()
        print "Map finished: %.2f " % (initial_reduce - initial_map)

    reduced_results = reduce(_reduce_impl, results, {})

    if verbose:
        end_reduce = time.time()
        print "Reduce finished: %.2f" % (end_reduce - initial_reduce)
        # print "Processing: ", json.dumps(reduced_results, indent = 4)


    result = _search(reduced_results)

    if verbose:
        end_search = time.time()
        print "Search finished: %.2f" % (end_search - end_reduce)

    result = (result[0], result[1].replace('http:/', 'http://'))
    return result

