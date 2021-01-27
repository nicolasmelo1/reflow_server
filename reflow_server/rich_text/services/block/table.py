from reflow_server.rich_text.models import TextTableOption, TextTableOptionColumnDimension, \
    TextTableOptionRowDimension


class RichTextTableBlockService:
    def save_table_block(self, border_color, row_dimensions, column_dimensions, table_option_id=None):
        """
        Saves the table block options, the block option of the table is simple: we just save the border color in it
        Besides that we need to save row_dimensions and column_dimensions. With both we can handle the size of each column
        individually and the size of each row of the table. We also use column_dimensions and row_dimensions to know the
        size of the table, if it has 3 row dimensions and 2 column dimensions it's a table 3x2. 

        We always create the row and column dimensions so when updating make sure you delete the old values first.

        Args:
            border_color (str): Can be also None, this is the color of the borders of the table
            row_dimensions (list(int)): Can also be a list of None, this is the height in pixels of each row.
            column_dimensions (list(int)): Can also be a list of None, this is the width in percentage of each column.
            table_option_id (int, optional): The TextTableOption instance id, only needs to be set when updating an instance. 
                                             Defaults to None.

        Returns:
            reflow_server.rich_text.models.TextTableOption: The created or updated TextTableOption instance.
        """
        table_option_instance = TextTableOption.rich_text_.update_or_create(border_color, table_option_id)
        if table_option_id:
            TextTableOptionColumnDimension.rich_text_.delete_column_dimensions_by_table_option_id(table_option_id)
            TextTableOptionRowDimension.rich_text_.delete_row_dimensions_by_table_option_id(table_option_id)

        TextTableOptionRowDimension.rich_text_.bulk_create_row_dimensions(table_option_instance.id, row_dimensions)
        TextTableOptionColumnDimension.rich_text_.bulk_create_column_dimensions(table_option_instance.id, column_dimensions)

        return table_option_instance