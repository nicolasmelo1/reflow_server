def is_integer(value):
    try:
        value = int(value)
        return True
    except:
        return False

def is_string(value):
    return isinstance(value, str)

def is_boolean(value):
    return isinstance(value, bool)

def is_float(value):
    try:
        value = float(value)
        return True
    except:
        return False


class DynamicArray:
    """
    This is a dynamic array that is similar to a Python List.
    Yes it is kinda dumb since we already have python List that basically does the job already.
    But since performance is not actually an issue and the possibility to translate this code to another language
    is. This is needed so in other languages we can just translate the implementation

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
    
    def __len__(self):
        """
        Return number of elements in the array
        """
        return self.number_of_elements
      
    def __getitem__(self, index):
        """
        Return element at index
        """
        if index < 0:
            index = self.number_of_elements + index
        
        if index >= self.number_of_elements:
            raise Exception('index is out of bounds') 
        
        return self.array[index] # Retrieve from the array at index
          
    def append(self, element):
        """
        Add element to end of the array
        """
        if self.number_of_elements == self.capacity:
            # Double capacity if not enough room
            self.__resize(2 * self.capacity) 
        
        last_index_of_array = self.number_of_elements
        self.array[last_index_of_array] = element # Set self.n index to element
        self.number_of_elements += 1
  
    def insert_at(self,item,index):
        """
        This function inserts the item at any specified index.
        """
        is_index_less_than_0 = index < 0
        is_index_bigger_than_number_of_elements = index >= self.number_of_elements
        
        is_capacity_at_limit = self.number_of_elements == self.capacity


        if is_index_less_than_0 or is_index_bigger_than_number_of_elements:
            raise Exception('index is out of bounds') 
          
        if is_capacity_at_limit:
            self.__resize(2 * self.capacity) # Double capacity if not enough room

        for i in range(self.number_of_elements - 1, index - 1, -1):
            self.array[i+1]=self.array[i]
              
        self.array[index] = item
        self.number_of_elements += 1
          
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
            self.array[index] = 0
            self.number_of_elements -= 1
        else:
            for i in range(index, self.number_of_elements - 1):
                self.array[i]=self.array[i + 1]            
                
            
            self.array[self.number_of_elements-1]=0
            self.number_of_elements -= 1
          
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
          
    def make_array(self, new_capacity):
        """
        Returns a new array with new_capacity capacity
        """
        return [None] * new_capacity