import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
output should be a (word, document ID list) tuple where word is
a String and document ID list is a list of Strings

$ python inverted_index.py books.json
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    doc_list = []
    for v in list_of_values:
      doc_list.append(v)
    mr.emit((key, doc_list))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
