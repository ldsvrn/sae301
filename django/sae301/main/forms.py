from django.forms import Form, TimeField, MultipleChoiceField, TimeInput

# truc trouvé sur internet pour que le forms ne soit pas dégeu
class TimePickerInput(TimeInput):
    input_type = 'time'

class ScheduleForm(Form):
    prise = MultipleChoiceField(choices=[("prise1", "prise1"), ("prise2", "prise2")])
    start = TimeField(required=True, label="Heure de début", widget=TimePickerInput)
    end = TimeField(required=True, label="Heure de fin", widget=TimePickerInput)
