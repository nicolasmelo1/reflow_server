# ------------------------------------------------------------------------------------------
def is_integer(value):
    try:
        value = int(value)
        return True
    except:
        return False
# ------------------------------------------------------------------------------------------
def is_string(value):
    return isinstance(value, str)
# ------------------------------------------------------------------------------------------
def is_boolean(value):
    return isinstance(value, bool)
# ------------------------------------------------------------------------------------------
def is_float(value):
    try:
        value = float(value)
        return True
    except:
        return False
# ------------------------------------------------------------------------------------------

############################################################################################
class DynamicArray:
    """
    This is a dynamic array that is similar to a Python List. Yes, this does the same job as if you used [].
    
    Since performance is not actually an issue and the possibility to translate this code to another language
    is. This is needed so in other languages we can just translate the implementation.

    This is agnostic to the formulas, since this is a HELPER. So try to keep ._representation_() and other stuff in
    The actual primitive objects

    Reference: https://www.geeksforgeeks.org/implementation-of-dynamic-array-in-python/
               https://stackoverflow.com/a/3917632
    """
      
    def __init__(self, elements=[]):
        self.number_of_elements = 0 # Count actual elements (Default is 0)
        self.capacity = 1 # Default Capacity
        self.array = self.make_array(self.capacity)
        if elements:
            for element in elements:
                self.append(element)
    # ------------------------------------------------------------------------------------------
    def __len__(self):
        """
        Return number of elements in the array
        """
        return self.number_of_elements
    # ------------------------------------------------------------------------------------------
    def __getitem__(self, index):
        """
        Return element at index
        """
        if index < 0:
            index = self.number_of_elements + index
        
        if index >= self.number_of_elements:
            raise Exception('index is out of bounds') 
        # Retrieve from the array at index
        return self.array[index]
    # ------------------------------------------------------------------------------------------   
    def append(self, element):
        """
        Add element to end of the array
        """
        if self.number_of_elements == self.capacity:
            # Double capacity if not enough room
            self.__resize(2 * self.capacity) 
        
        # Set self.number_of_elements index to element
        last_index_of_array = self.number_of_elements
        self.array[last_index_of_array] = element
        self.number_of_elements += 1
    # ------------------------------------------------------------------------------------------
    def insert_at(self, item, index, delete_element_at_index=False):
        """
        This function inserts the item at any specified index.
        """
        is_index_less_than_0 = index < 0
        is_index_bigger_than_number_of_elements = index >= self.number_of_elements
        
        is_capacity_at_limit = self.number_of_elements == self.capacity

        if is_index_less_than_0 or is_index_bigger_than_number_of_elements:
            raise Exception('index is out of bounds') 
          
        if is_capacity_at_limit:
            # Double capacity if not enough room
            self.__resize(2 * self.capacity)

        if not delete_element_at_index:
            for i in range(self.number_of_elements - 1, index - 1, -1):
                self.array[i+1]=self.array[i]

        self.array[index] = item
        self.number_of_elements += 1
    # ------------------------------------------------------------------------------------------   
    def pop(self):
        """
        This function deletes item from the end of array
        """
        is_array_empty = self.number_of_elements == 0

        if is_array_empty:
            raise Exception("Array is empty deletion not Possible")
        element = self.array[self.number_of_elements - 1]

        self.array[self.number_of_elements - 1] = 0
        self.number_of_elements -= 1
        return element
    # ------------------------------------------------------------------------------------------
    def remove_at(self,index):
        """
        This function deletes item from a specified index..
        """        
        is_array_empty = self.number_of_elements == 0
        is_index_less_than_0 = index < 0
        is_index_bigger_than_number_of_elements = index >= self.number_of_elements

        if is_array_empty:
            raise Exception("Array is empty deletion not Possible")
                  
        if is_index_less_than_0 or is_index_bigger_than_number_of_elements:
            raise Exception("index is out of bounds")        

        is_last_index = index == self.number_of_elements - 1

        if is_last_index:
            self.array[index] = None
            self.number_of_elements -= 1
        else:
            for i in range(index, self.number_of_elements - 1):
                self.array[i] = self.array[i + 1]            
                
            self.array[self.number_of_elements-1] = None
            self.number_of_elements -= 1
    # ------------------------------------------------------------------------------------------
    def __resize(self, new_capacity):
        """
        Resize internal array to capacity new_capacity

        Args:
            new_capacity (int): Resizes the capacity of the array
        """
        new_array = self.make_array(new_capacity) # New bigger array
        for i in range(self.number_of_elements): # Reference all existing values
            new_array[i] = self.array[i]
              
        self.array = new_array # Call A the new bigger array
        self.capacity = new_capacity # Reset the capacity
    # ------------------------------------------------------------------------------------------
    def make_array(self, new_capacity):
        """
        Returns a new array with new_capacity capacity
        """
        return [None] * new_capacity
    # ------------------------------------------------------------------------------------------
############################################################################################
class HashTable:
    ############################################################################################
    class HashNode:
        def __init__(self,number_of_removed_elements_when_added, order_added, hasher, key, value):
            """
            This is each node of the HashTable. Each node of the hash table is also a linked list.
            So in the worst cenario, if it has a collision we will not take up memory creating new list
            we just append the next node to the first node. This way we can keep our code more efficient.

            Args:
                number_of_removed_elements_when_added (int): it is not straight forward but we use this so when we remove
                                                             by the 'order_added' index we can subtract by this number
                                                             so it can give us the actual index. Read '.remove()' method for further
                                                             explanation.
                order_added (int): The order that the node was added, with this we can get the 'key', 'value' and
                                   'index' for the given node respectively from 'keys', 'values' and 'indexes' list
                                   in the HashTable                                            
                hasher (int): The original hashing number. Sometimes the number can be '1231231231' so when we 
                              fill the space in the hashing table we devide this big integer by the capacity and get
                              the remainder.
                key (any): This key can be of any type, this is the actual value yu are storing as key (NOT THE HASH OF THE VALUE)
                           This way we can prevent duplicate keys from being added
                value (any): The actual value you want to store.
            """
            self.number_of_removed_elements_when_added = number_of_removed_elements_when_added
            self.order_added = order_added
            self.hasher = hasher
            self.key = key
            self.value = value
            self.next = None
    ############################################################################################
    # ------------------------------------------------------------------------------------------
    def __init__(self, hashes_keys_and_values=[]):
        """
        This is a HashTable object that uses Chaining as resolution for collisions, it also has a dynamic size, and works similar to DynamicArray. 
        So you probably don't know what hashtables are, so let me try to explain.
        First things first, you've probably seen HashTables and you've problably have been using for a LONG LONG time.
        Have you ever used a Python Dict ({"chave": "valor"}) ? Or even, you've ever seen a JSON? 
        They are all examples of a HashTable. 

        But you might be asking yourself, "okay, but why do we use it?"

        While on lists/arrays we can retrieve a value by it's index always in a constant speed O(1), people wanted to retrieve 
        values using other stuff other than a index.

        In a list we access stuff like 
        
        >>> lista = [1, 2, 3] 
        
        if we want to retrieve value 3 we do
        lista[2], but what if i wanted to retrieve the value 3 using something that makes more sense for me, like a string?
        I wanted to access this value by making lista['age_of_lucas']. How do we do it? For that, if you are following along
        we use a HashTable, that in our beloved python is a dict.
        we would end up with something like:

        >>> dictionary = {"age_of_amanda": 1, "age_of_bruna": 2, "age_of_lucas": 3}

        ^ This, is a Hash Table.

        But what are Hash Tables and how they are constructed? Simple, sorry to break it to you but a Hash Table is actually
        a list/array. Nothing else. Only arrays for most programming languages give us the ability of finding an item in O(1).
        The compiler mostly knows only how to deal with arrays (can be in C, in Erlang or others, the compiler understand only arrays)

        In other words, the 'dictionary' variable above would be something like
        
        >>> [None, None, None, ["age_of_amanda", 1], None, None, ["age_of_bruna", 2], ["age_of_lucas", 3]]
        
        And that's it, now you understand the "Table" part of the name "HashTable" but when does "Hash" comes into play?

        So if you see, there is a lot of vacant space in the list above with the value of None. Where we add Each Node or
        key/value pair is not random. We use the power of Hashing and cryptography to solve this. Python also uses it.
        check 
        >>> print(hash('Testar_valor_hash_de_string'))
        >>> print(hash(123.9))
        >>> print(hash(19))
        >>> print(hash(True))

        If you know python you know that the classes has those Dunder (Doube Underscore) methods like __init__. But we also got
        __hash__ that is used when we use the hash() function on the object. 

        Anyway, have you noticed something while printing this? All of those return INTEGERS, and that's actually really important.
        because those integers will be the position we will add the element in the array. Of course we WILL NOT have an array of 
        550040178637243895 elements just to add one element this is a waste of memory. So what we do is get the remainder of the total
        capacity of the array.

        If we start with an array of 4 elements we will have 550040178637243895 % 4 which is equal 3. So we add this value to the index 3.
        A nice thing about hashes is that on the same context and runtime, doesn't matter how many times you've generated a hash for an
        element, it will ALWAYS be the same (for the same context).

        There are many hashing functions out there that returns a integer: https://www.geeksforgeeks.org/string-hashing-using-polynomial-rolling-hash-function/
        To understand how those functions work you will need to have a deep knowledge in Maths, but this is out of the scope here.
        To choose one hashing function you will want to use a hashing that has the least number of collisions (we will explain that in a sec)

        Okay, so now we've understood the "Hash" part of the algorithm.

        Last but not least, what are collisions?

        A collision is when for different values the hash is the same. So let's suppose that 
        
        >>> hash('Testar_valor_hash_de_string')
        
        and 
        
        >>> hash(550040178637243895)

        generates the same hash 550040178637243895 (which is actually true if the hash generated by the string was this). Don't you agree that 
        'Testar_valor_hash_de_string' is a string and 550040178637243895 is an int so they are completly different values?

        What do we do in this case? Both values will be stored in the index 3 as we saw before and this is collision. 
        There are two ways of fixing this issue:
        Linear Probing and Chaining.

        Linear Probing will try to fill all of the elements in the array so we will end up with
        >>> [None, None, ["Testar_valor_hash_de_string", 1], [550040178637243895, 2]] 
        notice that one of the elements was move to the index BEFORE (to the index 2) the actual index it should be.
        
        One of the most efficient ways to do this is to use the robin hood hashing algorithm https://programming.guide/robin-hood-hashing.html
        
        Chaining is what we do here, because in the worst case scenario you will end up with something like:
        >>> [None, None, None, [["Testar_valor_hash_de_string", 1], [550040178637243895, 2]]]
        Notice that for the array of 4 elements, on the last position we have also an array.
        So in the worst case scenario to get the value of 550040178637243895
        we will need to loop through all elements in the array at position 3 just to find the element with the key i'm looking for. So now
        the efficiency will not be O(1) anymore.

        Now you understand why trying to minimize collisions is extremely important for your hashing function.
        
        Last but not least, some material for further reading:
        - https://stephenagrice.medium.com/how-to-implement-a-hash-table-in-python-1eb6c55019fd This is mostly what i used.
        - https://www.sebastiansylvan.com/post/robin-hood-hashing-should-be-your-default-hash-table-implementation/
        - http://blog.chapagain.com.np/hash-table-implementation-in-python-data-structures-algorithms/#:~:text=Standard%20Implementation&text=Python's%20built%2Din%20%E2%80%9Chash%E2%80%9D,be%2020%2C%20and%20so%20on.
        The last one explains linear probing and chaining better.
        """
        self.number_of_removed_elements = 0
        self.number_of_elements = 0
        self.capacity = 8

        self.indexes = DynamicArray()
        self.keys = DynamicArray()
        self.values = DynamicArray()

        self.table = self.make_table(self.capacity)

        for hash_key_and_value in hashes_keys_and_values:
            the_hash = hash_key_and_value[0]
            the_key = hash_key_and_value[1]
            the_value = hash_key_and_value[2]
            self.append(the_hash, the_key, the_value)
    # ------------------------------------------------------------------------------------------
    def __add_at_index_and_handle_collision(self, table, index, hash_node):
        """
        This is responsible for adding a HashNode object in a 'table' list at a specific index.
        If there is a collision we handle it by appending the hash_node to the last node of the linked list

        Args:
            table (list): This is the list we will append the hash_node on
            index (int): This the index of the list you will append hash_node to the table
            hash_node (self.HashNode): A HashNode objects that holds itself and the reference for the others
                                       it is linked to.
        """
        if index < len(table):
            if table[index] != None and table[index].key != hash_node.key:
                node = table[index]
                while node.next is not None and node.key != hash_node.key:
                    node = node.next
                node.next = hash_node
            else:
                # we are adding a fresh new node in the index, we clean hash_node.next for when resizing.
                hash_node.next = None
                table[index] = hash_node
        else:
            raise Exception('Index to add is out of bounds, resize the array')
    # ------------------------------------------------------------------------------------------
    def search(self, hasher, key):
        """
        Tries to get the node using the hasher, if it is chained then loop through all nodes to find the key

        Args:
            hasher (int): The actual hashing value of the key your are searching, the hashing is done outside of the hashing table.
            key (any): The value you are searching

        Raises:
            Exception: If key does not exist in the hash table we throw an error.

        Returns:
            self.NodeType: Returns the node object that holds the value.
        """
        hash_index = hasher % self.capacity
        node = self.table[hash_index]
        while node != None and node.key != key and node.next is not None:
            node = node.next
        if node == None:
            raise Exception('Key does not exist in dict')
        else:
            return node
    # ------------------------------------------------------------------------------------------    
    def remove(self, hasher, key):
        """
        Removes a certain key from the array.

        It is actually really simple but you might not understand this line
        
        >>> remove_key_index_and_value_at = node.order_added - self.number_of_removed_elements + node.number_of_removed_elements_when_added

        order_added in each node holds the order the element was added starting at index 0. This actually uses the `self.number_of_removed_elements`
        variable. So if you add a node, let's say, position 4, remove this node then add a new node. The new node will have order_added as 4.

        So why do we use it? To remove the node from the lists 'keys', 'indexes' and 'values'.
        
        okay, so what does we do in 'remove_key_index_and_value_at'
        """
        hash_index = hasher % self.capacity
        node = self.table[hash_index]
        
        if node != None:
            if node.key == key:
                remove_key_index_and_value_at = node.order_added - self.number_of_removed_elements + node.number_of_removed_elements_when_added

                self.indexes.remove_at(remove_key_index_and_value_at)
                self.keys.remove_at(remove_key_index_and_value_at)
                self.values.remove_at(remove_key_index_and_value_at)

                self.table[hash_index] = None
            else:
                previous = node
                while node.key != key:
                    previous = node
                    node = node.next
                
                remove_key_index_and_value_at = node.order_added - self.number_of_removed_elements + node.number_of_removed_elements_when_added
                self.indexes.remove_at(remove_key_index_and_value_at)
                self.keys.remove_at(remove_key_index_and_value_at)
                self.values.remove_at(remove_key_index_and_value_at)

                previous.next = None

            self.number_of_removed_elements += 1
            self.number_of_elements -= 1
        else:
            raise Exception('Key does not exist in dict')
    # ------------------------------------------------------------------------------------------
    def append(self, hasher, key, value):
        """
        Appends a new value to the HashTable, we send a hasher, the key and the value, the key is the actual value
        you want to store as list. The value is the value you are storing in this key, and the hasher is the key hashed.

        Args:
            hasher (int): This is the 'key' value hashed. Some other implementations of the hashtable you will see that
                          the hashing is handled inside of the hashtable, on this we let each builtin object implement their own
                          hashing algorithm
            key ([float, int, string, boolean]): The Key can be of type bool, int, str or float.
            value (any): The actual value you are holding can be of any type, there are no limitations.
        """
        hash_node = self.HashNode(self.number_of_removed_elements, self.number_of_elements, hasher, key, value)
        hash_index = hasher % self.capacity
        
        if self.number_of_elements + 1 > self.capacity:
            self.__resize(2 * self.capacity)

        self.indexes.append(hash_index)
        self.keys.append(key)
        self.values.append(value)

        self.__add_at_index_and_handle_collision(self.table, hash_index, hash_node)
        
        self.number_of_elements += 1
    # ------------------------------------------------------------------------------------------
    def __resize(self, new_capacity):
        """
        Resize internal table to new_capacity.

        The idea is simple:
        1º we set a new indexes list to update all of the indexes
        2º we set the new capacity, create a new table with the new capacity and last but not least define a nodes_to_fix array

        3º we need One loop only to update the table. I try to make it as efficient as possible but try to make as least resizes as possible.
        4º we iterate by each index in the indexes array of course filtering by everything that is not None.
        5º Then we get the node to update and add this node to the previous variable. This 'previous' variable might not be all clear for everybody
        6º The 'previous' variables holds the previous node reference, this way we can get the next node WITHOUT LOSING REFERENCE to the previous.
        7º If node.next is a node, then we will lopp again, but we will not need 'previous' for anything else so we can update this node safely
        8º We calculate the new index by using the original hash value and retrieving the remainder for the new array
        9º Update the index and add node at index handling collision. Finish by updating everything.

        Args:
            new_capacity (int): The new capacity of the hash table table.
        """
        new_indexes = DynamicArray()
        new_table = self.make_table(new_capacity) 

        for node_index in self.indexes.array:
            if node_index != None:
                node = self.table[node_index]
                previous = node
                while node is not None:
                    previous = node
                    node = node.next

                    new_index = previous.hasher % new_capacity
                    new_indexes.append(new_index)

                    self.__add_at_index_and_handle_collision(new_table, new_index, previous)

        self.indexes = new_indexes
        self.table = new_table 
        self.capacity = new_capacity
    # ------------------------------------------------------------------------------------------
    def make_table(self, new_capacity):
        """
        Returns a new array with new_capacity capacity
        """
        return [None] * new_capacity
