# Example code that can be called with the `run_script` management command
from app.models import Writer
print(Writer.objects.all())
