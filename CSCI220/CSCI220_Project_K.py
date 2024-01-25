import heapq

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    

def build_huffman_tree(char_freq):
    heap = [Node(char, freq) for char, freq in char_freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_node = Node(None, left.freq + right.freq)
        new_node.left = left
        new_node.right = right
        heapq.heappush(heap, new_node)

    return heap[0]

def generate_huffman_codes(root, code="", mapping=None):
    if mapping is None:
        mapping = {}

    if root is not None:
        if root.char is not None:
            mapping[root.char] = code
        generate_huffman_codes(root.left, code + "0", mapping)
        generate_huffman_codes(root.right, code + "1", mapping)

    return mapping

#Encode
def huffman_encode(text, huffman_codes):
    encode_text = ""
    for char in text:
        encode_text += huffman_codes[char]
    
    return encode_text

#Decode
#Iterate through the string
def huffman_decode (text, huffman_tree):
    #Search algorithm
    current_node =huffman_tree
    decode_text = ''
    for bit in text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.char != None:
            decode_text+= current_node.char
            current_node = huffman_tree
    return decode_text
        


# Example usage (based off of the English language)
char_frequencies = {'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 12.7, 'F': 2.2, 'G': 2.0, 'H': 6.1, 'I': 7.0, 'J': 0.2, 'K': 0.8, 'L': 4.0,'M': 2.4, 'N': 6.7, 'O': 7.5, 'P': 1.9, 'Q': 0.1, 'R': 6.0, 'S': 6.3, 'T': 9.1, 'U': 2.8, 'V': 1.0, 'W': 2.4, 'X': 0.2, 'Y': 2.0, 'Z': 0.1}
huffman_tree = build_huffman_tree(char_frequencies)
huffman_codes = generate_huffman_codes(huffman_tree)
print(huffman_codes)

#Get string
text = input("Enter String here: ")
text = text.upper()
try: 
    print(huffman_encode(text, huffman_codes))
except:
    print(huffman_decode(text, huffman_tree))


#Read from a source
    #Get frequencies
    #Get strings/ binary strings

#ChatGPT used to build the Node Object