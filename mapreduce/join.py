import MapReduce
import sys

"""
The output should be a joined record: a single list of length 27 that contains
the attributes from the order record followed by the fields from the line item
record. Each list element should be a string.

$ python join.py records.json
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: order_id
    key = record[1]
    mr.emit_intermediate(key, record)

def reducer(key, items):
    order_item = []
    for item in items:
      if item[0] == "order":
        order_item = item
      elif item[0] == "line_item":
	    mr.emit(order_item + item)

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
