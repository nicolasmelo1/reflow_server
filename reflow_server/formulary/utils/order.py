class Order:
    """
    Utils to reorder the items in the database. This adds space so you can add your order to your objects.

    Example: 
    You have 3 forms:

    - Administração - order 1
    - Negocios - order 2
    - Comercial - order 3

    Then you want to add a new one in order 2, that is already occupied by `Negocios`.
    When you use the `.order()` method you recieve a tuple like the following (2, [1,3,4])
    That means that you have the following order now:
    - Administração - order 1
    - Negocios - order 3
    - Comercial - order 4

    Leaving room to your element being inserted AFTER `Administração`, so in position 2.
    """
    def __init__(self):
        self.insert = 1
    
    def _get_next_indexes(self, current_index, element_to_check, modified_list):
        for index in range(len(modified_list)):
            if modified_list[index] == element_to_check and index != current_index:
                yield index

    def reorder(self, number_to_add, current_order):
        # checks if the order is less than 0 (your element can't have order 0, -1 and so on). And checks if element order is above
        # the length of orders, if you have 3 elements, and want to add in position 5 you can't, the maximum position you can insert
        # is postion 4
        number_to_add = number_to_add if number_to_add > 0 else 1
        number_to_add = number_to_add if number_to_add < len(current_order)+1 else len(current_order)+1

        array = [index+1 for index in range(len(current_order))]

        # this might be a little confusing on start but it makes a lot of sense, next_element_indexes is an array containing all
        # the index that needs to be updated, so, if the `number_to_add` is 2 and the `current_order` is [1,2,3,4]
        # we first get the next_element_indexes, in this case [1]. It means we must update the `current_order` array at index 1.
        # So in the array [1,2,3,4], we are starting updating number 2, which is the value at index 1 in the array.
        # `last_element` holds the number we want to add in this position. In this example, before the while it is 2, inside of the while
        # `last_element` becomes `last_element` + 1, so, number 3.
        # it's important to notice this function also works for reapeated lists or unordered lists
        next_element_indexes = list(self._get_next_indexes(None, number_to_add, array))
        last_element = number_to_add
        while next_element_indexes:
            indexes_to_check = list()
            for next_element_index in next_element_indexes:
                last_element = last_element + self.insert
                indexes_to_check = indexes_to_check + list(self._get_next_indexes(next_element_index, last_element, array))
                array[next_element_index] = last_element
            next_element_indexes = indexes_to_check
        return array
    