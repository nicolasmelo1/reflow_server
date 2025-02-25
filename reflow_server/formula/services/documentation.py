from django.conf import settings

from reflow_server.formula.models import FormulaContextBuiltinLibrary, FormulaBuiltinLibraryModuleAttributeType, FormulaContextType, \
    FormulaBuiltinLibraryModuleType


class DocumentationService:
    def __init__(self):
        """
        This is the service responsible for documenting the formulas. First i was thinking about documenting on all languages
        we support and will support. But later i found that it's not a programmers responsability to translate everything. So we
        default this documentation to a default language on which is english. So every programmer should provide a documentation at
        least in english.

        This is supposed to run when you start your application and only that, so everytime you run your app this run and creates or
        updates the documentation for the formulas.
        """
        builtin_modules = FormulaBuiltinLibraryModuleType.objects.all()
        self.__builtin_modules = { builtin_module.module_name: builtin_module.id for builtin_module in builtin_modules }
        attribute_context_types = FormulaBuiltinLibraryModuleAttributeType.objects.all()
        self.__attribute_types = { attribute_context_type.attribute_name: attribute_context_type.id for attribute_context_type in attribute_context_types }
        context_types = FormulaContextType.objects.all()
        self.__context_types = { context_type.name: context_type.id for context_type in context_types }

    def update_documentation(self):
        """
        This is the function used to update the documentation for the formulas, be aware that this is the method you run when you
        start the application, the idea is simple: When we run the command we get all of the formulas in `FORMULA_MODULES` setting and 
        creates the documentation for it in the database.
        """
        for formulas_for_context in settings.FORMULA_MODULES.values():
            for formula_module_name in formulas_for_context:
                path = "%s.%s" % (settings.FORMULA_BUILTIN_MODULES_PATH, formula_module_name)
                module = __import__(path, fromlist=[formula_module_name])
                kls = getattr(module, formula_module_name)
                formula_builtin_module = kls(None)
                module_documentation = formula_builtin_module._documentation_()
                self.document(formula_module_name, module_documentation)

    def document(self, module_name, documentation):
        """
        Document the formulas to the users, the required translation and documentation is only english since this
        is the default language we are using. For portuguese and other languages we translate everything by hand.

        Args:
            module_name (str): The name of the formula.
            documentation (dict): Please, follow the following format:
            >>> {
                'description' (str): The description of the module
                'translation' (str): The translation of the module. Defaults to the module_name
                'struct_parameters': {
                    '<struct_parameter_name>': {
                        'description' (str): The description of the struct parameter,
                        'translation' (str): The translation of the struct parameter. Defaults to the struct_parameter_name,
                        'is_required' (bool): True if this struct_parameter is required or False if optional. Defaults to True.
                    }
                },
                'methods': {
                    '<method_name>': {
                        'description' (str): The description of the method,
                        'translation' (str): The translation of the method. Defaults to the method_name,
                        'attributes' : {
                            '<method_parameter_name>': {
                                'description' (str): The description of the method.
                                'translation' (str): The translation of the method. Defaults to the method_name.
                                'is_required' (bool): True if this method_parameter is required or False if optional. Defaults to True.
                            }
                        }
                    }
                },
                'structs': {
                    '<struct_name>': {
                        'description' (str): The description of the struct,
                        'translation' (str): The translation of the struct. Defaults to the struct_name,
                        'attributes': {
                            '<struct_attribute_name>': {
                                'description' (str): The description of the struct_attribute.
                                'translation' (str): The translation of the struct_attribute. Defaults to the struct_attribute_name.
                                'is_required' (bool): True if this struct_attribute is required or False if optional. Defaults to True.
                            }
                        }
                    }
                }
            }
        """
        added_or_updated_formula_context_builtin_library_type = []
        
        if module_name not in self.__builtin_modules.keys():
            module_instance = FormulaBuiltinLibraryModuleType.objects.create(module_name=module_name)
            module_instance_id = module_instance.id
        else:
            module_instance_id = self.__builtin_modules[module_name]

        module_description = documentation['description']
        module_translation = documentation.get('translation', module_name)

        module_instance, __ = FormulaContextBuiltinLibrary.objects.update_or_create(
            attribute_type_id=self.__attribute_types['module'],
            context_type_id=self.__context_types['default'],
            module_type_id=module_instance_id,
            original_value=module_name,
            defaults={
                'description': module_description,
                'translation': module_translation
            }
        )
        added_or_updated_formula_context_builtin_library_type.append(module_instance.id)

        # retrieve and work on struct parameters
        for struct_parameter_key, struct_parameter_value in documentation.get('struct_parameters', {}).items():
            struct_parameter_name = struct_parameter_key
            struct_parameter_description = struct_parameter_value['description']
            struct_parameter_translation = struct_parameter_value.get('translation', struct_parameter_name)
            struct_parameter_is_required = struct_parameter_value.get('is_required', True)

            struct_parameter_instance, __ = FormulaContextBuiltinLibrary.objects.update_or_create(
                attribute_type_id=self.__attribute_types['module_struct_parameter'],
                context_type_id=self.__context_types['default'],
                module_type_id=module_instance_id,
                original_value=struct_parameter_name,
                defaults={
                    'description': struct_parameter_description,
                    'translation': struct_parameter_translation,
                    'is_required_attribute': struct_parameter_is_required,
                    'related_to': module_instance
                }
            )
            added_or_updated_formula_context_builtin_library_type.append(struct_parameter_instance.id)

        # handles methods
        for method_key, method_value in documentation.get('methods', {}).items():
            method_name = method_key
            method_description = method_value['description']
            method_translation = method_value.get('translation', method_name)
            
            method_instance, __ = FormulaContextBuiltinLibrary.objects.update_or_create(
                attribute_type_id=self.__attribute_types['method'],
                context_type_id=self.__context_types['default'],
                module_type_id=module_instance_id,
                original_value=method_name,
                related_to=module_instance,
                defaults={
                    'description': method_description,
                    'translation': method_translation
                }
            )
            added_or_updated_formula_context_builtin_library_type.append(method_instance.id)

            # handles methods attributes
            for method_attribute_key, method_attribute_value in method_value.get('attributes', {}).items():
                method_attribute_name = method_attribute_key
                method_attribute_description = method_attribute_value['description']
                method_attribute_translation = method_attribute_value.get('translation', method_attribute_name)
                method_attribute_is_required = method_attribute_value.get('is_required', True)

                method_attribute_instance, __ = FormulaContextBuiltinLibrary.objects.update_or_create(
                    attribute_type_id=self.__attribute_types['method_parameter'],
                    context_type_id=self.__context_types['default'],
                    module_type_id=module_instance_id,
                    original_value=method_attribute_name,
                    related_to=method_instance,
                    defaults={
                        'description': method_attribute_description,
                        'translation': method_attribute_translation,
                        'is_required_attribute': method_attribute_is_required
                    }
                )
                added_or_updated_formula_context_builtin_library_type.append(method_attribute_instance.id)

        # handles structs
        for struct_key, struct_value in documentation.get('structs', {}).items():
            struct_name = struct_key
            struct_description = struct_value['description']
            struct_translation = struct_value.get('translation', struct_name)

            struct_instance, __ = FormulaContextBuiltinLibrary.objects.update_or_create(
                attribute_type_id=self.__attribute_types['struct'],
                context_type_id=self.__context_types['default'],
                module_type_id=module_instance_id,
                original_value=struct_name,
                related_to=module_instance,
                defaults={
                    'description': struct_description,
                    'translation': struct_translation
                }
            )
            added_or_updated_formula_context_builtin_library_type.append(struct_instance.id)

            # handles structs attributes
            for struct_attribute_key, struct_attribute_value in struct_value.get('attributes', {}).items():
                struct_attribute_name = struct_attribute_key
                struct_attribute_description = struct_attribute_value['description']
                struct_attribute_translation = struct_attribute_value.get('translation', struct_attribute_name)

                struct_instance, __ = FormulaContextBuiltinLibrary.objects.update_or_create(
                    attribute_type_id=self.__attribute_types['struct_attribute'],
                    context_type_id=self.__context_types['default'],
                    module_type_id=module_instance_id,
                    original_value=struct_attribute_name,
                    related_to=struct_instance,
                    defaults={
                        'description': struct_attribute_description,
                        'translation': struct_attribute_translation
                    }
                )
                added_or_updated_formula_context_builtin_library_type.append(struct_instance.id)

        # deletes the translation that was not created or updated.
        FormulaContextBuiltinLibrary.objects\
            .filter(context_type_id=self.__context_types['default'], module_type_id=module_instance_id)\
            .exclude(id__in=added_or_updated_formula_context_builtin_library_type)\
            .delete()
