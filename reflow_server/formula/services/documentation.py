class DocumentationService:
    def __init__(self, language):
        valid_documentation_languages = ['english', 'portuguese']
        if language not in valid_documentation_languages:
            raise Exception('Not a valid language, use one of the following: %s' % valid_documentation_languages)
        else:
            self.language = language
        
    def document(self, documentation):
        module_name = documentation['module_name']
        module_description = documentation['description']
        module_translation = documentation.get('translation', module_name)
        
        