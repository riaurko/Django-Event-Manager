from django import forms
from events.models import *

#* Form Mixin Styles
class CreateStyles:
    common_classes = "border border-green-900 rounded-md px-3 py-1 focus:outline-none focus:border-2 focus:border-green-700 bg-slate-800 text-slate-100 text-lg md:text-xl"
    def WidgetStyles(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f"{self.common_classes} w-80 sm:w-96",
                    'placeholder': f"Enter the {field.label}"
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': f"{self.common_classes} w-80 sm:w-96",
                    'placeholder': f"Enter the {field.label}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.common_classes} w-80 sm:w-[40rem] overflow-hidden resize-none",
                    'placeholder': f"Enter the {field.label}",
                    'rows': 7
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': f"{self.common_classes} w-28 sm:w-36",
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'type': 'time',
                    'class': f"{self.common_classes} w-12 sm:w-40",
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': f"{self.common_classes} w-48 sm:w-80"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': f"{self.common_classes}"
                })

#* Event Creation ModelForm
class CreateEvent(CreateStyles, forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.TimeInput(attrs={
                'type': 'time'
            }),
        }
    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        self.WidgetStyles()
        self.fields['category'].choices = [(categ.id, categ.name) for categ in categories]

#* Category Creation ModelForm
class CreateCategory(CreateStyles, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WidgetStyles()

#* Participant Registeration ModelForm
class CreateParticipant(CreateStyles, forms.ModelForm):
    class Meta:
        model = Participant
        exclude = ['events']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WidgetStyles()
