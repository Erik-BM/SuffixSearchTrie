# SuffixSearchTrie

Input format 
```
n
word_1
...
word_n
...
word_n+m
```

where words 1 to n is to be inserted into trie. The remaining words are going to be searched for.

The output is first the structure of the trie after every word inserted. Thereafter, a list of words n+1 to m and a boolean to indicate if suffix is in trie.

## Example
```
python3 Trie.py test1.txt out.txt
```
