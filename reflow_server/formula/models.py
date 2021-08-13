from django.db import models

from reflow_server.formula.managers import FormulaContextForCompanyFormulaManager


class FormulaContextForCompany(models.Model):
    company = models.OneToOneField('authentication.Company', on_delete=models.CASCADE, db_index=True)
    context_type = models.ForeignKey('formula.FormulaContextType', on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = 'formula_context_for_company'

    objects = models.Manager()
    formula_ = FormulaContextForCompanyFormulaManager()


class FormulaContextType(models.Model):
    language = models.CharField(max_length=280)
    name = models.CharField(max_length=280)
    order = models.IntegerField(default=1)

    class Meta:
        db_table = 'formula_context_type'
        ordering = ('order',)


class FormulaAttributeType(models.Model):
    name = models.CharField(max_length=280)
    order = models.IntegerField(default=1)

    class Meta:
        db_table = 'formula_attribute_type'
        ordering = ('order',)


class FormulaContextAttributeType(models.Model):
    context_type = models.ForeignKey('formula.FormulaContextType', on_delete=models.CASCADE, db_index=True, related_name='formula_context_type_attributes')
    attribute_type = models.ForeignKey('formula.FormulaAttributeType', on_delete=models.CASCADE, db_index=True, related_name='formula_context_type_attributes')
    translation = models.TextField()

    class Meta:
        db_table = 'formula_context_attribute_type'


class FormulaBuiltinLibraryModuleType(models.Model):
    """
    This is not used by anything actually just for sake of organization in the `FormulaContextBuiltinLibrary`.
    You can define all of the modules you support translation to here. Those are the MODULES, only module names.

    You will study more here, but all builtin modules is, as the name suggests, modules. So you will have lots of handy 
    functions in those modules.

    Those are defined whenever you start a new program to run your formulas on.
    """
    module_name = models.TextField()

    class Meta:
        db_table = 'formula_builtin_library_module_type'


class FormulaBuiltinLibraryModuleAttributeType(models.Model):
    """
    All of the attributes a module can hold for translation, for the present time a module can be defined by

    module - The module itself
    struct_parameter - The parameters for defining the struct (is related to module)
    method - The methods of the module (is related to module)
    method_parameter - The parameters of the method of the module (is related to a method)
    struct - The structs that this module can return (is related to a module)
    struct_attributes - The attributes of the returned struct (is related to a struct)

    This is better explained in `FormulaContextBuiltinLibrary` model so refer to it's documentation.
    """
    attribute_name = models.CharField(max_length=240)
    related_to = models.ForeignKey('self', models.CASCADE, blank=True, null=True, db_index=True,
                                   related_name='formula_builtin_library_module_attribute_type_related_to')
    
    class Meta:
        db_table = 'formula_builtin_library_module_attribute_type'


class FormulaContextBuiltinLibrary(models.Model):
    """
    This might be confusing at first but it is basically how we can change the translation of everything in one single table
    instead of making multiple tables and changing them dynamically.
    
    With a single table we can keep everything concise and clean to use and make changes to:
    For example, suppose the following table
    
    | id | original_value | translation | related_to_id | context_type_id | attribute_type_id | module_type_id | 
    |----|----------------|-------------|---------------|-----------------|-------------------|----------------|
    | 1  | HTTP           | Requisicao  |               | 2               | 1                 | 1              |
    | 6  | request        | requisitar  | 1             | 2               | 3                 | 1              |
    | 2  | get            | pegar       | 1             | 2               | 3                 | 1              |
    | 3  | url            | endereco    | 2             | 2               | 4                 | 1              |
    | 7  | method         | metodo      | 6             | 2               | 4                 | 1              |
    | 8  | url            | endereco    | 6             | 2               | 4                 | 1              |
    | 4  | HTTPResponse   | Resposta    | 1             | 2               | 5                 | 1              |
    | 5  | content        | conteudo    | 4             | 2               | 6                 | 1              |

    Let's start from the last column. First you can see that everything is related to the same module by seing the `module_type_id`
    The module is defined by the `FormulaBuiltinLibraryModuleType`. This is just used for organization and doesn't have any use.

    Second you can see that everything relates to the same context type, so it's quick to make changes to. This translates to
    portuguese, defined by the `FormulaContextType` model.

    Then we can see the relations. The id 1 doesn't relate to anything, that's because this is module. This is can also be identifiable
    by the `attribute_type_id`

    Then the attribute_type_id defined by the `FormulaBuiltinLibraryModuleAttributeType` defines what are those translations
    and to which one they must relate to.

    For example, if we know that the following attribute_type_ids relates_to (This relation can change and vary):
    1 = module
    3 = method
    4 = method_parameter
    5 = struct
    6 = strunct_attribute

    We know that the id 6 row refers to a method, and this method is related to the HTTP module.
    In other words, `request` is a method of the HTTP module and in the flow language for this context it'll be written as `requisitar`

    Then look at ids 7 and 8, we see that they relate to 6, and the attribute_type_id is 4, so it is a method_parameter.
    We can easily identify that 7 and 8 are the parameters/arguments the method 6 will recieve.
    In other words `requisitar` will recieve the `endereco` and `metodo` parameters.

    This makes it really easy to translate and if something changes in the future and we need to change the structure we can
    make it dynamically without the need of modifying tables.

    IMPORTANT: If no translation is defined we will use the default names so just use this if you actually need the translation
    for the formula. You can make translations as needed, so if your original `request` method recieves the `url`, `method` and `headers`
    parameters but you don't want to translate the `headers` parameter, just leaves as is. You just need to add a row if you
    need to add a translation.

    Pretty sick, no?
    """
    context_type = models.ForeignKey(
        'formula.FormulaContextType',  
        on_delete=models.CASCADE, 
        db_index=True,
        related_name='formula_context_builtin_library_type_library_contexts',
        blank=True, 
        null=True
    )
    attribute_type = models.ForeignKey(
        'formula.FormulaBuiltinLibraryModuleAttributeType',  
        on_delete=models.CASCADE, 
        db_index=True,
        related_name='formula_context_builtin_library_type_library_attributes'
    )
    module_type = models.ForeignKey(
        'formula.FormulaBuiltinLibraryModuleType', 
        on_delete=models.CASCADE,
        db_index=True,
        related_name='formula_context_builtin_library_type_library_module'
    )
    original_value = models.TextField()
    translation = models.TextField()
    description = models.TextField(default='', blank=True)
    is_required_attribute = models.BooleanField(default=True)
    related_to = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        db_index=True,
        related_name='formula_context_builtin_library_type_related_to'
    )

    class Meta:
        db_table = 'formula_context_builtin_library_type'
