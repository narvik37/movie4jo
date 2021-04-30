from import_export import resources
from .models import Test

class TestResources(resources.ModelResources):
    class Meta:
        model = Test