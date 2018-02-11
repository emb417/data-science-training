import MapReduce
import sys

"""
The output should be a pair (person, friend_count) where person is a string
and friend_count is an integer indicating the number of friends associated with person.

$ python friend_count.py friends.json
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: person
    person = record[0]
    friend = record[1]
    mr.emit_intermediate(person, friend)

def reducer(key, friends):

	friend_count = 0
	for friend in friends:
		friend_count += 1

	mr.emit((key,friend_count))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
