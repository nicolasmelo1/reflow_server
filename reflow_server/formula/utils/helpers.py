from datetime import datetime


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
    try:
        value = bool(value)
        return True
    except Exception as e:
        return False
# ------------------------------------------------------------------------------------------
def is_float(value):
    try:
        value = float(value)
        return True
    except:
        return False
# ------------------------------------------------------------------------------------------
############################################################################################
class DatetimeHelper:
    valid_formats = [
        'YYYY',
        'MM',
        'DD',
        'hh',
        'HH',
        'mm',
        'ss',
        'SSS',
        'AA'
    ]
    
    valid_attributes = [
        'year',
        'month',
        'day',
        'hour',
        'minute',
        'second',
        'microsecond'
    ]

    def validate_format(self, datetime_format):
        if datetime_format not in self.valid_formats:
            raise Exception('Not a valid datetime format')
    
    def get_regex(self, datetime_format):
        self.validate_format(datetime_format)

        if datetime_format == 'YYYY':
            return r'(\d{4})'
        elif datetime_format == 'MM':
            return r'(0[1-9]|1[0-2]|[1-9])'
        elif datetime_format == 'DD':
            return r'(0[1-9]|1[0-9]|2[0-9]|3[0-1]|[1-9])'
        elif datetime_format == 'hh':
            return r'(0[0-9]|1[0-9]|2[0-3]|[1-9])'
        elif datetime_format == 'HH':
            return r'(0[1-9]|1[0-2]|[1-9])'
        elif datetime_format == 'mm':
            return r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])?'
        elif datetime_format == 'ss':
            return r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])?'
        elif datetime_format == 'AA':
            return r'(am|pm|AM|PM)?'
        else:
            return r'(\d{3})?'

    @staticmethod
    def to_python_format(date_format, time_format):
        """
        Converts a date_format and a time_format to something that Python can actually understand and convert

        Args:
            date_format (str): The format of the date to be used.
            time_format (str): The format of the time to be used and converted.
        
        Returns:
            str: Returns the date and time formated to something that python can actually understand.
        """
        date_format = date_format.replace('YYYY', '%Y')
        date_format = date_format.replace('MM', '%m')
        date_format = date_format.replace('DD', '%d')

        time_format = time_format.replace('hh', '%H')
        time_format = time_format.replace('HH', '%I')
        time_format = time_format.replace('mm', '%M')
        time_format = time_format.replace('ss', '%S')
        time_format = time_format.replace('SSS', '%f')
        time_format = time_format.replace('AA', '%p')

        return f'{date_format} {time_format}'
    
    def append_values(self, datetime_format, value):
        """
        This might doesn't make any sense at all, but this is how we retrieve the values using this function.

        We DO NOT append and retrieve the values directly you will see is that we create some attributes in the class
        'date_year', 'date_month' and so on. All of those attributes are a dict that holds the data needed for retrieving the
        value you appended.

        But why do we do this you might ask. So suppose the format have the AM/PM part in the date. This comes last in the hour it will be
        something like 11:20:52 PM, this means this time is 23:20:52 in the 24hour date format. So what we need? We store the value of the hour
        which is 11, with this value we also store the `am_or_pm` in the dict that we will use for adding by 12. So, like i said before, 11 PM is actually
        23 in the 24 hour time format. So it is 11 + 12. That's why we need to store the values BEFORE retrieving the actual value. This way
        when we retrieve the value we can format a to something python actually can understand and interpret

        Args:
            datetime_format: must comply with `valid_formats` list, but we do not validate here, this is because we send everything to be evaluated here
                             but we only save what is needed.
            value: The value to be appended.
        """
        if datetime_format == 'YYYY':
            self.date_year = {
                'format': datetime_format,
                'value': int(value) if value != '' else 0
            }
        elif datetime_format == 'MM':
            self.date_month = {
                'format': datetime_format,
                'value': int(value) if value != '' else 0
            }
        elif datetime_format == 'DD':
            self.date_day = {
                'format': datetime_format,
                'value': int(value) if value != '' else 0
            }
        elif datetime_format == 'hh':
            self.date_hour = getattr(self, 'date_hour', {}) 
            self.date_hour.update({
                'format': datetime_format,
                'value': int(value) if value != '' else 0
            })
        elif datetime_format == 'HH':
            self.date_hour = getattr(self, 'date_hour', {})
            self.date_hour.update({
                'format': datetime_format,
                'value': int(value) if value != '' else 0
            })
        elif datetime_format == 'mm':
            self.date_minute = {
                'format': datetime_format,
                'value': int(value) if value != '' else 0
            }
        elif datetime_format == 'ss':
            self.date_second = {
                'format': datetime_format,
                'value': int(value) if value != '' else 0
            }
        elif datetime_format == 'AA':
            self.date_hour = getattr(self, 'date_hour', {}) 
            self.date_hour.update({
                'am_or_pm': 'pm' if value.lower() == 'pm' else 'am'
            })
        elif datetime_format == 'SSS':
            self.date_microsecond = {
                'format': datetime_format,
                'value': int(value) if value != '' else 0
            }

    def append_values_by_definition(self, datetime_definition, value):
        """
        Different from `append_values` method, this method will append the values by the datetime definition.
        This means that here we have less `elif` case statements. Also the format of the object is somewhat different
        from one another. But keep in mind that we append the values to the same instance variables.

        Args:
            datetime_definition ('year', 'month', 'day',  'hour', 'minute', 'second', 'microsecond'): The datetime definition to be used.
            value (int | str): The value to append to datetimehelper instance.
        """
        if datetime_definition == 'year':
            self.date_year = {
                'value': int(value) if value != '' else 0
            }
        elif datetime_definition == 'month':
            self.date_month = {
                'value': int(value) if value != '' else 0
            }
        elif datetime_definition == 'day':
            self.date_day = {
                'value': int(value) if value != '' else 0
            }
        elif datetime_definition == 'hour':
            self.date_hour = {
                'value': int(value) if value != '' else 0
            }
        elif datetime_definition == 'minute':
            self.date_minute = {
                'value': int(value) if value != '' else 0
            }
        elif datetime_definition == 'second':
            self.date_second = {
                'value': int(value) if value != '' else 0
            }
        elif datetime_definition == 'microsecond':
            self.date_microsecond = {
                'value': int(value) if value != '' else 0
            }
    
    def get_value_stringfied_by_format(self, format):
        """
        This gets each value as string by the actual format. Generally this will be used in conjunction with 
        the `.append_values_by_definition()` method. Different from the `.get_value` this returns the value stringfied and
        not the actual number. This will also use the format and not the datetimeDefinition like the other method.
        
        Args: 
            format ('YYYY', 'MM', 'DD', 'hh', 'HH', 'mm', 'ss', 'SSS', 'AA'): The format to use for retrieving the value.
            Needs to exist in the `valid_formats` array.

        Returns:
            str | Npne: The value as string. The value of the format as a string. Or return None if No value is found.
        """
        if format == 'YYYY':
            return str(self.date_year['value'])
        elif format == 'MM':
            return f'0{self.date_month["value"]}' if self.date_month['value'] < 10 else str(self.date_month['value'])
        elif format == 'DD':
            return f'0{self.date_day["value"]}' if self.date_day['value'] < 10 else str(self.date_day['value'])
        elif format == 'hh':
            return f'0{self.date_hour["value"]}' if self.date_hour['value'] < 10 else str(self.date_hour['value'])
        elif format == 'HH':
            hour_value = self.date_hour['value'] - 12 if self.date_hour['value'] >= 12 else self.date_hour['value']
            hour_value = 12 if self.hour_value == 0 else hour_value
            return f'0{hour_value}' if hour_value < 10 else str(hour_value)
        elif format == 'mm':
            return f'0{self.date_minute["value"]}' if self.date_minute['value'] < 10 else str(self.date_minute['value'])
        elif format == 'ss':
            return f'0{self.date_second["value"]}' if self.date_second['value'] < 10 else str(self.date_second['value'])
        elif format == 'SSS':
            return f'00{self.date_microsecond["value"]}' if self.date_microsecond['value'] < 10 else \
                   f'0{self.date_microsecond["value"]}' if self.date_microsecond['value'] < 100 else \
                       str(self.date_microsecond['value'])
        elif format == 'AA':
            return 'PM' if self.date_hour['value'] >= 12 else 'AM'
        else:
            return None
    
    def get_value(self, datetime_definition):
        """
        Returns the actual value from the values appended in the `append_values()` method.

        Here we actually transform the date value to something that python can understand. Sometimes you can convert something while appending
        and sometimes you need to convert while retrieving the value. So it needs some thinking before you come up with a solution.

        Args:
            datetime_definition (str): One of the strings defined in `valid_attributes` array in the instantiation of this class.

        Returns:
            int: returns an int needed refering for the value you are trying to retrieve  
        """
        if datetime_definition == 'year' and hasattr(self, 'date_year'):
            return self.date_year['value']
        elif datetime_definition == 'month' and hasattr(self, 'date_month'):
            return self.date_month['value']
        elif datetime_definition == 'day' and hasattr(self, 'date_day'):
            return self.date_day['value']
        elif datetime_definition == 'hour' and hasattr(self, 'date_hour'):
            if self.date_hour.get('am_or_pm'):
                return self.date_hour['value'] + 12 if self.date_hour['am_or_pm'] == 'pm' else self.date_hour['value']
            else:
                return self.date_hour['value']
        elif datetime_definition == 'minute' and hasattr(self, 'date_minute'):
            return self.date_minute['value']
        elif datetime_definition == 'second' and hasattr(self, 'date_second'):
            return self.date_second['value']
        elif datetime_definition == 'microsecond' and hasattr(self, 'date_microsecond'):
            return self.date_microsecond['value']
        else:
            return 0
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
        def __init__(self, order_added, hasher, raw_key, key, value):
            """
            This is each node of the HashTable. Each node of the hash table is also a linked list.
            So in the worst cenario, if it has a collision we will not take up memory creating new list
            we just append the next node to the first node. This way we can keep our code more efficient.

            Args:
                order_added (int): The order that the node was added, with this we can get the 'key', 'value' and
                                   'index' for the given node respectively from 'keys', 'values' and 'indexes' list
                                   in the HashTable                                            
                hasher (int): The original hashing number. Sometimes the number can be '1231231231' so when we 
                              fill the space in the hashing table we devide this big integer by the capacity and get
                              the remainder.
                raw_key (any): The key you are storing, this is the actual value you want to store.
                key (any): This key can be of any type, this is the actual value yu are storing as key (NOT THE HASH OF THE VALUE)
                           This way we can prevent duplicate keys from being added
                value (any): The actual value you want to store.
            """
            self.order_added = order_added
            self.hasher = hasher
            self.raw_key = raw_key
            self.key = key
            self.value = value
            self.next = None
    ############################################################################################
    # ------------------------------------------------------------------------------------------
    def __init__(self, raw_keys_hashes_keys_and_values=[]):
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
        self.number_of_elements = 0
        self.capacity = 8

        self.raw_keys = DynamicArray()
        self.indexes = DynamicArray()
        self.keys = DynamicArray()
        self.values = DynamicArray()

        self.table = self.make_table(self.capacity)

        for raw_key_hash_key_and_value in raw_keys_hashes_keys_and_values:
            the_raw_key = raw_key_hash_key_and_value[0]
            the_hash = raw_key_hash_key_and_value[1]
            the_key = raw_key_hash_key_and_value[2]
            the_value = raw_key_hash_key_and_value[3]
            self.append(the_raw_key, the_hash, the_key, the_value)
    # ------------------------------------------------------------------------------------------
    def length(self):
        """"
        Returns the number of elements in the Hash Table.

        Returns:
            int: The number of elements in the Hash Table.
        """
        return self.number_of_elements
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
                already_existing_hash_node = table[index]
                while already_existing_hash_node.next is not None and already_existing_hash_node.next.key != hash_node.key:
                    already_existing_hash_node = already_existing_hash_node.next
                already_existing_hash_node.next = hash_node
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
        is_hash_index_a_valid_index = hash_index < len(self.table)
        if is_hash_index_a_valid_index:
            existing_hash_node_at_index = self.table[hash_index]
            while(
                existing_hash_node_at_index is not None and \
                existing_hash_node_at_index.key != key and \
                existing_hash_node_at_index.next is not None
            ):
                existing_hash_node_at_index = existing_hash_node_at_index.next
            if existing_hash_node_at_index is None:
                raise Exception(f'Key "{key}" does not exist in dict')
            else:
                return existing_hash_node_at_index
        else:
            raise Exception(f'Key "{key}" does not exist in dict')
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
        is_hash_index_a_valid_index = hash_index < len(self.table)
        if is_hash_index_a_valid_index:
            hash_node_to_be_removed = self.table[hash_index]
            does_key_and_hash_node_exists = key in self.indexes.array and hash_node_to_be_removed is not None
            
            if does_key_and_hash_node_exists:
                # he hash_node_to_be_removed is the first node in the linked list but is not the element we are looking for
                if hash_node_to_be_removed.key != key:
                    previous_node_to_update_linked_list = hash_node_to_be_removed
                    while hash_node_to_be_removed.key != key and hash_node_to_be_removed.next is not None:
                        previous_node_to_update_linked_list = hash_node_to_be_removed
                        hash_node_to_be_removed = hash_node_to_be_removed.next

                    if hash_node_to_be_removed is None:
                        raise Exception(f'Key {key} does not exist in dict')

                    # We kept track of the last node in the linked list so we can update the reference and delete it.
                    # the hashNodeToBeRemoved will lose reference
                    previous_node_to_update_linked_list.next = hash_node_to_be_removed.next
                else:
                    self.table[hash_index] = hash_node_to_be_removed.next
            
                for index in range(len(self.keys.array)):
                    if self.keys.array[index] == key:
                        self.raw_keys.remove_at(index)
                        self.indexes.remove_at(index)
                        self.keys.remove_at(index)
                        self.values.remove_at(index)
                
                self.number_of_elements -= 1
            else:
                raise Exception(f'Key {key} does not exist in dict')
    # ------------------------------------------------------------------------------------------
    def append(self, raw_key, hasher, key, value):
        """
        Appends a new value to the HashTable, we send a hasher, the key and the value, the key is the actual value
        you want to store as list. The value is the value you are storing in this key, and the hasher is the key hashed.

        Args:
            raw_key (any): The key you are storing, this is the actual value you want to store.
            hasher (int): This is the 'key' value hashed. Some other implementations of the hashtable you will see that
                          the hashing is handled inside of the hashtable, on this we let each builtin object implement their own
                          hashing algorithm
            key ([float, int, string, boolean]): The Key can be of type bool, int, str or float.
            value (any): The actual value you are holding can be of any type, there are no limitations.
        """
        # we first check to see if the key was already inserted, if it was this means we are actually changing the value
        # of an existing key so we need to insert again.
        # WHY DON'T YOU JUST UPDATE THE EXISTING KEY? Because by doing so we would need to separate logic in this method: 
        # one for updating an existing node and other for inserting a new node. To keep it simple, just consider everything
        # as adding a new node.
        if key in self.keys.array:
            self.remove(hasher, key)

        # we should resize before retrieving the hashIndex, i was running trough an error and it was hard to debug.
        # The bug happened because we got the index after resizing. This means the hashIndex would be wrong because after we resize
        # we change the capacity of the array generating a new hashIndex that should be used in the insertion.
        if self.number_of_elements + 1 > self.capacity:
            self.__resize(2 * self.capacity)
            
        hash_node = self.HashNode(self.number_of_elements, hasher, raw_key, key, value)
        hash_index = hasher % self.capacity
        
        self.raw_keys.append(raw_key)
        self.indexes.append(hash_index)
        self.keys.append(key)
        self.values.append(value)

        self.__add_at_index_and_handle_collision(self.table, hash_index, hash_node)
        
        self.number_of_elements += 1
        return value
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
        new_keys = DynamicArray()
        new_raw_keys = DynamicArray()
        new_values = DynamicArray()
        
        new_table = self.make_table(new_capacity) 

        for node_index in self.indexes.array:
            if node_index != None:
                hash_index = node_index % self.capacity
                
                node = self.table[hash_index]
                previous = node
                while node is not None:
                    previous = node
                    node = node.next
                    
                    new_hash_index = previous.hasher % new_capacity
                    
                    self.__add_at_index_and_handle_collision(new_table, new_hash_index, previous)
                    
                    new_indexes.append(new_hash_index)
                    new_keys.append(previous.key)
                    new_raw_keys.append(previous.raw_key)
                    new_values.append(previous.value)
        
        self.indexes = new_indexes
        self.keys = new_keys
        self.raw_keys = new_raw_keys
        self.values = new_values
        
        self.table = new_table 
        self.capacity = new_capacity
    # ------------------------------------------------------------------------------------------
    def make_table(self, new_capacity):
        """
        Returns a new array with new_capacity capacity
        """
        return [None] * new_capacity
############################################################################################
class Conversor:
    def __init__(self, settings):
        from reflow_server.formula.utils.builtins import objects
        self.objects = objects
        self.settings = settings

    def python_value_to_flow_object(self, python_value):
        if isinstance(python_value, str):
            return self.__python_str_to_flow_string(python_value)
        elif isinstance(python_value, float):
            return self.__python_float_to_flow_float(python_value)
        elif isinstance(python_value, int):
            return self.__python_int_to_flow_integer(python_value)
        elif isinstance(python_value, bool):
            return self.__python_bool_to_flow_boolean(python_value)
        elif isinstance(python_value, list):
            return self.__python_list_to_flow_list(python_value)
        elif isinstance(python_value, dict):
            return self.__python_dict_to_flow_dict(python_value)
        elif isinstance(python_value, datetime):
            return self.__python_datetime_to_flow_datetime(python_value)
        elif python_value == None:
            return self.__python_none_to_flow_null()
        else:
            return python_value
        
    def __python_str_to_flow_string(self, value):
        new_string = self.objects.String(self.settings)
        return new_string._initialize_(value)
    
    def __python_float_to_flow_float(self, value):
        new_float = self.objects.Float(self.settings)
        return new_float._initialize_(value)

    def __python_int_to_flow_integer(self, value):
        new_integer = self.objects.Integer(self.settings)
        return new_integer._initialize_(value)
    
    def __python_none_to_flow_null(self):
        new_none = self.objects.Null(self.settings)
        return new_none._initialize_()

    def __python_bool_to_flow_boolean(self, value):
        new_boolean = self.objects.Boolean(self.settings)
        return new_boolean._initialize_(value)
    
    def __python_datetime_to_flow_datetime(self, value):
        new_datetime = self.objects.Datetime(self.settings)
        return new_datetime._initialize_(value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond)
        
    def __python_list_to_flow_list(self, values):
        new_list = self.objects.List(self.settings)

        array = []
        for value in values:
            array.append(self.python_value_to_flow_object(value))
        
        new_list._initialize_(array)
        return new_list

    def __python_dict_to_flow_dict(self, value):
        new_dict = self.objects.Dict(self.settings)
        
        values = []
        for key, value in value.items():
            key = self.python_value_to_flow_object(key)
            value = self.python_value_to_flow_object(value)
            values.append([key, value])
        new_dict._initialize_(values)
        return new_dict