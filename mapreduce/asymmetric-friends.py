import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework

$ python asymmetric_friends.py friends.json
"""

mr = MapReduce.MapReduce()

def mapper(record):
    composite_key = '_'.join(sorted(record))
    mr.emit_intermediate(composite_key, record)

def reducer(key, list_of_values):
    for tuple in list_of_values:
        if len(list_of_values) == 1 :
            mr.emit((tuple))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
