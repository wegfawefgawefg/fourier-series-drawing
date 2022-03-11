'''
resample path to parameterize it
'''

import json
from pprint import pprint
from vec2 import Vec2

num_samples = 1000
start = 0

# get path from json
with open('path.json') as f:
    path = json.load(f)

# path = [(0, 0), (0, 18), (16, 22), (20, 0), (0, 0)]
lines = [(Vec2(*path[i]), Vec2(*path[i + 1])) for i in range(len(path) - 1)]

line_lengths = [(line[1] - line[0]).mag() for line in lines]
smallest_line_length = min(line_lengths)
total_distance = sum(line_lengths)
step_length = total_distance / num_samples
if step_length > smallest_line_length:
    print("Warning: step length is greater than smallest line length")
    print("increase num_samples or decrease step_length")
    quit()

print("total distance:", total_distance)
print("step length:", step_length)

p_path = []
p = Vec2(*path[0]) # start at the first point
for line in lines:
    line_length = (line[1] - line[0]).mag()
    num_samples_in_line = int(line_length / step_length)

    end_point = line[1]
    for _ in range(num_samples_in_line):
        direction = (end_point - p).norm()
        p += direction * step_length
        p_path.append(p)
    
# save the path
p_path = [p.as_tuple() for p in p_path]
print("output path length:", len(p_path))
with open('tpath.json', 'w') as f:
    json.dump(p_path, f)
