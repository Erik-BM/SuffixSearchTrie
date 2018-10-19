"""
Suffix search using tries.
"""

import argparse

class Node():
    """
    Node class
    attributes:
        char :: string, one character of a inserted word.
        children :: list, children of the node.
        word_end :: bool, is the Node the last in a word.
    properties:
        str :: printing structure of trie, parentheses around sub-trees.
        lf :: less than, compare characters.
    """
    def __init__(self, char='*'):
        self.char = char 
        self.children = []
        self.word_end = False
    
    def __str__(self):
        res = ''
        for child in sorted(self.children):
            if len(self.children) < 2: #Compress trie if only one child.
                res += child.char + child.__str__()
            else:
                res += '(' + child.char + child.__str__() + ')'
       
        return res
    
    def __lt__(self, other):
        return self.char < other.char
        
        
def find(root, string):
    """
    Find string (prefix) in trie. 
    args:
        root :: Node, root of trie.
        string :: string, prefix to search for.
    return:
        bool, true if string is found, else return false.
    """
    node = root
    if not node.children: #Only root in trie
        return False
    for char in string: #Traverse trie and compare with characters in string.
        found = False
        for child in node.children:
            """
            Check each child if a match is found. If found move to next character and grandchild, else try next child.
            """
            if child.char == char: 
                found = True
                node = child
                break
        if not found: # No child contains char
            return False
        
    return True

def insert(root, string):
    """
    Insert new string into trie. Similar to find, except, when found insert.
    args:
        root :: Node, trie root.
        string :: string, word to insert.
    return:
        None
    """
    node = root 
    for char in string:
        found = False
        for child in node.children:
            if child.char == char:
                node = child
                found = True
                break
        if not found:
            """
            Search until a mismatch is found, then insert new node with characters missing from trie.
            """
            new_node = Node(char)
            node.children.append(new_node)
            node = new_node
    node.word_end = True

def read_input(filename):
    """
    Read input to program.
    args:
        filename :: string
            path to file containing data on form:
            - N on first line
            - Remaining lines with strings
            - Take N first string as insert set.
            - Remaining string as suffix search string.
    return:
        N :: int, number of strings to insert into trie.
        C :: list, string to insert into trie.
        T :: list, suffixes to search for.
    """
    out = []
    with open(filename, 'r') as f:
        for l in f:
            out.append(str(l).strip())
    
    N = int(out[0])
    C = out[1:N]
    T = out[N:]
    return N,C,T

def save_results(output_filename, d, results):
    """
    Save results to file.
    args:
        filename :: filename to save to.
        d :: dict, key=string, item=structure of trie, parentheses around sub-trees.
        results :: list of bool. Is suffix in string.
    return:
        None
    """
    for k,i in d.items():
        if i[0] != '(':
            d[k] = '('+i+')'
    
    with open(output_filename, 'w') as f:
        for k,i in d.items():
            s = k + ': ' + i + '\n'
            f.write(s)
        f.write('\n')
        for k,i in results.items():
            res = 'NO'
            if i:
                res = 'YES'
            s = k + ' ' + res + '\n'
            f.write(s)
        f.write('\n')
    
    
def main(input_filename, output_filename):
    """
    Construct trie. Search for suffixes. Save results.
    args:
        input_filename :: string, path to input data.
        output_filename :: string, path to save to.
    return:
        None
    """
    N,C,T = read_input(input_filename) 
    
    # Creating string that represents tree structure. Using the prefix tree for that.
    structure = {}
    prefix_trie = Node("prefix")
    for c in C:
        insert(prefix_trie, c)
        structure[c] = str(prefix_trie)
    
    # Creating suffix trie.
    suffix_trie = Node("suffix")
    for c in C:
        insert(suffix_trie, c[::-1]) # reversing string
    
    # Searching for suffix.
    result = {}
    for t in T:
        result[t] = find(suffix_trie, t[::-1]) # reversing string
    
    save_results(output_filename, structure, result)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Suffix trie search')
    parser.add_argument('input_filename', metavar='input', type=str, nargs='?',
                    help='input filename')
    parser.add_argument('output_filename', metavar='output', type=str, nargs='?',
                    help='output filename')
    
    args = parser.parse_args()
    main(args.input_filename, args.output_filename)
    
    
    
