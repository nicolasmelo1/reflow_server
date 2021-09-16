from reflow_server.formula.utils.context import Context
from reflow_server.formula.models import FormulaContextBuiltinLibrary, FormulaContextAttributeType


def build_context(context_type_id, flow_context):
    """ 
    This builds the context, the context is a way that we use to translate the formula for many languages like
    portuguese, english, spanish and others. The idea is that the formulas needed to be translatable so it is easier 
    to use for people that do not live in countries like united states, canada. So it becomes easier for non programmers
    to program something complex using our formulas.

    Args:
        context_type_id (int): A FormulaContextType instance id
        flow_context (('formula', 'automation')): This is the context where the flow is running, right now it supports 'formula' 
                                                  or 'automation'.

    Returns:
        reflow_server.formula.utils.context.Context: Returns a Context object
    """
    context = Context()

    if context_type_id:
        formula_context_attributes = FormulaContextAttributeType.objects.filter(context_type_id=context_type_id).values('attribute_type__name', 'translation')
        if formula_context_attributes:
            formula_attributes = {}
            for formula_context_attribute in formula_context_attributes:
                key = formula_context_attribute['attribute_type__name']
                formula_attributes[key] = formula_context_attribute['translation']

            context = Context(**formula_attributes, flow_context=flow_context)

            # the code here might look kinda confusing at first but it's doing basically the same thing
            # basically what we are doing on all those for loops is translating the internal library to something
            # the final user can understand and know.
            formula_context_library_types = FormulaContextBuiltinLibrary.objects.filter(context_type_id=context_type_id)

            # first we translate the module
            for formula_context_library_type_module in formula_context_library_types.filter(
                attribute_type__attribute_name='module'
            ):
                module = context.add_library_module(
                    formula_context_library_type_module.original_value,
                    formula_context_library_type_module.translation
                )
                # translate the module module_struct_parameters
                for formula_context_library_type_struct_parameter in formula_context_library_types.filter(
                    attribute_type__attribute_name='module_struct_parameter', 
                    related_to=formula_context_library_type_module.id
                ):
                    module.add_struct_parameter(
                        formula_context_library_type_struct_parameter.original_value,
                        formula_context_library_type_struct_parameter.translation
                    )
                
                # translate the module methods
                for formula_context_library_type_method in formula_context_library_types.filter(
                    attribute_type__attribute_name='method', 
                    related_to=formula_context_library_type_module.id
                ):
                    method = module.add_method(
                        formula_context_library_type_method.original_value,
                        formula_context_library_type_method.translation
                    )

                    # translate the module method method_parameters
                    for formula_context_library_type_method_parameter in formula_context_library_types.filter(
                        attribute_type__attribute_name='method_parameter', 
                        related_to=formula_context_library_type_method.id
                    ):
                        method.add_parameter(
                            formula_context_library_type_method_parameter.original_value,
                            formula_context_library_type_method_parameter.translation
                        )

                # translate the module structs
                for formula_context_library_type_struct in formula_context_library_types.filter(
                    attribute_type__attribute_name='struct', 
                    related_to=formula_context_library_type_module.id
                ):
                    struct = module.add_struct(
                        formula_context_library_type_struct.original_value,
                        formula_context_library_type_struct.translation
                    )
                    
                    # translate the module struct attribute
                    for formula_context_library_type_struct_attribute in formula_context_library_types.filter(
                        attribute_type__attribute_name='struct_attribute', 
                        related_to=formula_context_library_type_struct.id
                    ):
                        struct.add_attribute(
                            formula_context_library_type_struct_attribute.original_value,
                            formula_context_library_type_struct_attribute.translation
                        )
    
    return context