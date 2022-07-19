import pickle

import pickle

# An arbitrary collection of objects supported by pickle.
data = {
    'count': [0, 0, 0],
}

print(data['count'][0])
with open('data.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

with open('data.pickle', 'rb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    print(pickle.load(f))