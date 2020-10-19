from tests.models import TestModel

model = TestModel.objects.first()
model.script2.run_script()