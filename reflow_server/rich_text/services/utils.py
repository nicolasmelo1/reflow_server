def ordered_list_from_serializer_data_for_page_data(rich_text_page_data):
    """
    Returns a ordered list so you can easily insert the list to create a new PageData object so you can save your rich text.

    Make sure your block serializer have both the 'uuid' field and the 'rich_text_depends_on_blocks' field

    Args:
        rich_text_page_data (dict): This is will be a dict starting of a rich_text Page.
        Make sure your Page serializer has the 'rich_text_page_blocks' field and your Block serializer has the 'uuid' 
        and 'rich_text_depends_on_blocks' field.

    Returns:
        list(dict): The dict will have the following structure: 
        {
            'depends_on_uuid': str,
            'data': dict -> This is each BLOCK data
        }
    """
    blocks_to_add = []
    blocks_to_check = [{'depends_on_uuid': None, 'data': block } for block in rich_text_page_data.get('rich_text_page_blocks', [])]
    while len(blocks_to_check) > 0:
        first_block = blocks_to_check.pop(0)
        blocks_to_add.append(first_block)
        if first_block['data'].get('rich_text_depends_on_blocks', None):
            blocks_to_check.extend([{
                'depends_on_uuid': first_block['data']['uuid'], 
                'data': block 
            } for block in first_block['data'].get('rich_text_depends_on_blocks', [])])

    return blocks_to_add