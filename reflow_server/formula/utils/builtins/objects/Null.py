from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import NONE_TYPE


class Null(Object):
    def __init__(self, settings):
        super().__init__(NONE_TYPE, settings)
    # ------------------------------------------------------------------------------------------
    def _initialize_(self):
        self.value = None
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------
    def _representation_(self):
        return self.value
    # ------------------------------------------------------------------------------------------
    def _string_(self, **kwargs):
        return self.new_string(self.settings.null_keyword)
    # ------------------------------------------------------------------------------------------
    def _safe_representation_(self):
        return self.value