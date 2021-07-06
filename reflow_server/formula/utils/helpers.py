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
    This is a dynamic array that is similar to a Python List.
    Yes it is kinda dumb since we already have python List that basically does the job already.
    But since performance is not actually an issue and the possibility to translate this code to another language
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
        
        return self.array[index] # Retrieve from the array at index
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


class HashTable:
    class HashNode:
        def __init__(self,number_of_removed_elements_when_added, order_added, hasher, key, value):
            """
            This is each node of the HashTable.

            Args:
                hasher (bool): [description]
                key ([type]): [description]
                value ([type]): [description]
            """
            self.number_of_removed_elements_when_added = number_of_removed_elements_when_added
            self.order_added = order_added
            self.hasher = hasher
            self.key = key
            self.value = value
            self.next = None

    
    def __init__(self, hashes_keys_and_values=[]):
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

    def __add_at_index_and_handle_collision(self, table, index, hash_node):
        if index < len(table) and table[index] != None and table[index].key != hash_node.key:
            node = table[index]
            while node.next is not None and node.key != hash_node.key:
                node = node.next
            node.next = hash_node
        else:
            hash_node.next = None
            table[index] = hash_node

    def search(self, hasher, key):
        hash_index = hasher % self.capacity
        node = self.table[hash_index]
        while node != None and node.key != key and node.next is not None:
            node = node.next
        if node == None:
            raise Exception('Key does not exist in dict')
        else:
            return node
        
    def remove(self, hasher, key):
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

    def append(self, hasher, key, value):
        """
        
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

    def make_table(self, new_capacity):
        """
        Returns a new array with new_capacity capacity
        """
        return [None] * new_capacity
