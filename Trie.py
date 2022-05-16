# Inspired from https://albertauyeung.github.io/2020/06/15/python-trie.html/
# Hamming distance from https://github.com/volpato30/hamming-d-search/blob/master/trie.py


class TrieNode:
    """Node objects in Trie"""

    def __init__(self, char: str) -> None:
        self.char = char
        self.is_end = False
        self.counter = 0  # Counts number of times inserted, maybe want to change to something else?
        self.children = {}
        # Want to store anything else?
        # Want to insert some check on char?


class Trie:
    """Trie object storing TrieNodes"""

    def __init__(self) -> None:
        self.root = TrieNode("")

    def insert(self, word: str) -> None:
        node = self.root

        # Check if there is a child containing the character
        # If not, create new child with character
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # Create new node
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node  # continue with rest of the word

        # Entire word is inserted, mark that this is end of word, and increase counter
        node.is_end = True
        node.counter += 1

    def _dfs(self, node: TrieNode, prefix: str):
        """Depth-first traversal of Trie

        Args:
            - node: Node to start at
            - prefix: current prefix, stores word while traversing
        """

        # The end of a word has been reached
        # Add word and counter to output list
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))

        for child in node.children.values():
            self._dfs(child, prefix + node.char)

    def query(self, x: str) -> list[tuple[str, int]]:
        """Finds all words that starts with prefix (x)"""

        # Create new empty list each time function is called
        self.output = []

        node = self.root

        # Checks that the word actually exists in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        # Do depth first search, starting at last node in prefix (x)
        self._dfs(node, x[:-1])

        # return all words starting with prefix (x), ordered by least number of occurrence
        return sorted(self.output, key=lambda x: x[1])

    def search_hamming_dist(self, query_seq: str, max_dist: int):
        """
        Returns True if query_sequence have a hamming distance less than max_dist
        Stops if one sequence that is not identical to the query sequence is found
        """
        result = []  #
        current_index = 0
        current_cost = 0

        node = self.root  # Gets the root node

        # Searches each of the children to the current node recursively

        for child in node.children:
            if not result:
                self._search_recursive(node.children[child], child, query_seq, current_index, current_cost, max_dist, child,result)

        return result

    def _search_recursive(self, current_node: TrieNode, base: str, query_seq: str,current_index: int, current_cost: int, max_dist: int, prefix: str, result: list[str]):
        """
        Recursive search function that checks if the current index of the
        query sequence matches current node in the trie.
        If more than max_dist mismatches are found, the search will not continue
        """

        if result:
            return
        # Checks query_seq against current base
        if not (base == query_seq[current_index]):
            current_cost += 1

        # If too many mismatches found, terminate this branch
        if current_cost > max_dist:
            return

        current_index += 1  # Go to next base

        # stopping criteria
        if current_node.is_end:
            if not (prefix == query_seq):  # Only found if not identical to query_seq
                result.append(prefix)
            else:
                return
        
        # Recursive search for all children
        for base in current_node.children:
            self._search_recursive(current_node.children[base], base, query_seq, current_index, current_cost,max_dist, prefix + base, result)


if __name__ == '__main__':
    testTrie = Trie()
    testTrie.insert("yoo")
    testTrie.insert("aoo")
    testTrie.insert("hey")
    testTrie.insert("yeo")
    testTrie.insert("yoy")
    testTrie.insert("hiy")



    print(testTrie.root.char)
    test = testTrie.search_hamming_dist("yoc", 1)

    if test:
        print(test)
