from django.forms.widgets import RadioSelect

class BareRadioSelect(RadioSelect):
    template_name = 'widgets/bare_radio.html'
