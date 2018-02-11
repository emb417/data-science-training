# MapReduce
The MapReduce programming model (and a corresponding system) was proposed in a 2004 paper from a team at Google as a simpler abstraction for processing very large datasets in parallel.  This exercise uses small datasets that you can inspect directly to determine the correctness of your results and to internalize how MapReduce works.

## Python MapReduce Framework

The python library MapReduce.py implements the MapReduce programming model. The framework faithfully implements the MapReduce programming model, but it executes entirely on a single machine -- it does not involve parallel computation.

Here is the word count example implemented as a MapReduce program using the framework:

```
# Part 1
mr = MapReduce.MapReduce()
# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
        mr.emit_intermediate(w, 1)
# Part 3
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0
    for v in list_of_values:
        total += v
    mr.emit((key, total))
# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
```

In Part 1, we create a MapReduce object that is used to pass data between the map function and the reduce function; you won’t need to use this object directly.

In Part 2, the mapper function tokenizes each document and emits a key-value pair. The key is a word formatted as a string and the value is the integer 1 to indicate an occurrence of word.

In Part 3, the reducer function sums up the list of occurrence counts and emits a count for word. Since the mapper function emits the integer 1 for each word, each element in the list_of_values is the integer 1.

The list of occurrence counts is summed and a (word, total) tuple is emitted where word is a string and total is an integer.

In Part 4, the code loads the json file and executes the MapReduce query which prints the result to stdout.


## Inverted Index
Given a set of documents, an inverted index is a dictionary where each word is associated with a list of the document identifiers in which that word appears.

### Mapper Input

The input is a 2-element list: [document_id, text], where document_id is a string representing a document identifier and text is a string representing the text of the document. The document text may have words in upper or lower case and may contain punctuation. Treat each token as if it was a valid word; use value.split() to tokenize the string.

### Reducer Output

The output should be a (word, document ID list) tuple where word is a String and document ID list is a list of Strings.

The inverted_index.py script can input books.json to generate the expected output:

```
$ python inverted_index.py books.json
```

## Relational Join as a MapReduce Query

Consider the following query:

```
SELECT *
FROM Orders, LineItem
WHERE Order.order_id = LineItem.order_id
```

The script join.py is a MapReduce query that produces the same result as this SQL query executed against an appropriate database.

You can consider the two input tables, Order and LineItem, as one big concatenated bag of records that will be processed by the map function record by record.

### Map Input

Each input record is a list of strings representing a tuple in the database. Each list element corresponds to a different attribute of the table

* The first item (index 0) in each record is a string that identifies the table the record originates from, with two possible values:
  * "line_item" indicates that the record is a line item.
  * "order" indicates that the record is an order.
* The second element (index 1) in each record is the order_id
* LineItem records have 17 attributes including the identifier string
* Order records have 10 elements including the identifier string

### Reduce Output

The output should be a joined record: a single list of length 27 that contains the attributes from the order record followed by the fields from the line item record. Each list element should be a string.

The script join.py can input records.json to generate the expected output:

```
$ python join.py records.json
```

## Generate a Psuedo-Graph

Consider a simple social network dataset consisting of a set of key-value pairs (person, friend) representing a friend relationship between two people.

The script friend_count.py is a MapReduce algorithm that counts the number of friends for each person.

### Map Input

Each input record is a 2 element list [personA, personB] where personA is a string representing the name of a person and personB is a string representing the name of one of personA's friends.
* Note that it may or may not be the case that the personA is a friend of personB.

### Reduce Output

The output should be a pair (person, friend_count) where person is a string and friend_count is an integer indicating the number of friends associated with person.

The script friend_count.py can input friends.json to generate the expected output:

```
$ python friend_count.py friends.json
```

## Asymmetric Friendships

The relationship "friend" is often symmetric, meaning that if I am your friend, you are my friend.

The asymmetric_friendships.py script is a MapReduce algorithm to check whether this property holds.

### Map Input

Each input record is a 2 element list [personA, personB] where personA is a string representing the name of a person and personB is a string representing the name of one of personA's friends.
* Note that it may or may not be the case that the personA is a friend of personB.

### Reduce Output

The output should be all pairs (friend, person) such that (person, friend) appears in the dataset but (friend, person) does not.

The script friends.json can input friends.json to generate the expected output:

```
$ python asymmetric_friendships.py friends.json
```

## Unique Trims

Consider a set of key-value pairs where each key is sequence id and each value is a string of nucleotides, e.g., GCTTCCGAAATGCTCGAA....

The script unique_trims.py is a MapReduce query that removes the last 10 characters from each string of nucleotides, then removes any duplicates generated.

### Map Input

Each input record is a 2 element list [sequence id, nucleotides] where sequence id is a string representing a unique identifier for the sequence and nucleotides is a string representing a sequence of nucleotides.

### Reduce Output

The output from the reduce function should be the unique trimmed nucleotide strings.

The script unique_trims.py can input dna.json to generate the expected output:

```
$ python unique_trims.py dna.json
```

## Multiply Matrix

Assume you have two matrices A and B in a sparse matrix format, where each record is of the form i, j, value.

The script multiple.py is a MapReduce algorithm that computes the matrix multiplication A x B.

### Map Input

The input to the map function will be a row of a matrix represented as a list. Each list will be of the form [matrix, i, j, value] where matrix is a string and i, j, and value are integers.

The first item, matrix, is a string that identifies which matrix the record originates from with two possible values:
* "a" indicates that the record is from matrix A
* "b" indicates that the record is from matrix B

### Reduce Output

The output from the reduce function will also be a row of the result matrix represented as a tuple. Each tuple will be of the form (i, j, value) where each element is an integer.

The script multiply.py can input matrix.json to generate the expected output:

```
$ python multiply.py matrix.json
```
