# Inspired from https://albertauyeung.github.io/2020/06/15/python-trie.html/
# Hamming distance from https://github.com/volpato30/hamming-d-search/blob/master/trie.py


class TrieNode:
    """
    Node objects that is stored in the Trie
    Stores its children in a dictionary
    """

    def __init__(self, char: str) -> None:
        self.char = char
        self.is_end = False  # Set to true only at the final character of a word/sequence
        self.counter = 0  # Number of times a sequence has been added to the trie
        self.children = {}


class Trie:
    """
    Trie object storing TrieNodes
    Starts with empty root TrieNode, children of each node can be found
    Methods starting with a '_' are private functions and should not be used outside the class
    """

    def __init__(self) -> None:
        self.root = TrieNode("")  # Root node

    def insert(self, word: str) -> None:
        """
        Inserts a word/sequence into the Trie
        """

        node = self.root  # Start at the root

        # Check if there is a child containing the character
        # If not, create new child with the character
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

    def _depth_first_search(self, node: TrieNode, prefix: str):
        """
        Depth-first traversal of Trie

        Node: Current node in the Trie
        Prefix: Current path taken through the trie, stores word
        """

        # The end of a word has been reached
        # Add word and counter to output list
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))

        # Start a new depth first search for each of the children
        for child in node.children.values():
            self._depth_first_search(child, prefix + node.char)

    def query(self, prefix: str) -> list[tuple[str, int]]:
        """
        Finds all words that starts with the prefix
        Returns a list containing of words and the number of times they have been inserted
        """

        # Create new empty list each time function is called
        self.output = []

        # start at the root of the trie
        node = self.root

        # Checks that the word actually exists in the trie
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []

        # Do depth first search, starting at last node in prefix (x)
        self._depth_first_search(node, prefix[:-1])

        # return all words starting with prefix (x), ordered by most number of occurrence
        return sorted(self.output, key=lambda x: x[1], reverse=True)

    def search_hamming_dist(self, query_seq: str, max_dT: int):
        """
        Returns a sequence if a it has a deltaT higher than max_dist compared with query_sequence
        Stops if a sequence that is not identical to the query sequence is found
        """
        result = []  #
        current_index = 0
        current_cost = 0

        node = self.root  # Gets the root node

        # Searches each of the children to the current node recursively
        for child in node.children:
            if not result:
                self._search_recursive(node.children[child], child, query_seq, current_index, current_cost, max_dT,
                                       child, result)

        return result

    def _search_recursive(self, current_node: TrieNode, base: str, query_seq: str, current_index: int,
                          current_cost: int, max_dT: int, prefix: str, result: list[str]):
        """
        Recursive search function that checks if the current index of the
        query sequence matches current node in the trie.
        If more than max_dist mismatches are found, the search will not continue
        """

        if result:
            return
        # Checks query_seq against current base
        # Note that query seq needs to be checked (not base) to get correct deltaT
        if not (base == query_seq[current_index]):
            if query_seq[current_index] in ["A", "T"]:
                current_cost += 2
            if query_seq[current_index] in ["C", "G"]:
                current_cost += 4

        # If too high cost, terminate this branch
        if current_cost > max_dT:
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
            self._search_recursive(current_node.children[base], base, query_seq, current_index, current_cost, max_dT,
                                   prefix + base, result)
