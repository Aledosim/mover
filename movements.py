from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Accelerator(Widget):
    """Widget que calcula a 'aceleração' do widget a ser animado"""
    def accelerate(self, obj):
        """Method usado para calcular a aceleração do widget a ser animado"""
        pass


class Oscillator(Accelerator):
    """Oscilador harmônico simples bidimensional"""
    frequency_x = NumericProperty(0)
    frequency_y = NumericProperty(0)
    frequency = ReferenceListProperty(frequency_x, frequency_y)
    amplitude_x = NumericProperty(0)
    amplitude_y = NumericProperty(0)
    amplitude = ReferenceListProperty(amplitude_x, amplitude_y)

    def __init__(self, frequency=(0, 0), frequency_x=0, frequency_y=0, **kwargs):
        super(Oscillator, self).__init__(**kwargs)

        if frequency != (0, 0):
            self.frequency = frequency
        elif frequency_x != 0:
            self.frequency_x = frequency_x
        elif frequency_y != 0:
            self.frequency_y = frequency_y

    def accelerate(self, obj):
        pos = Vector(*obj.center) - Vector(*self.center)
        acc = -pos * Vector(*self.frequency) * Vector(*self.frequency)
        obj.velocity = Vector(*acc) + obj.velocity


class Uniform(Accelerator):
    """Movimento uniforme, com velocidade constante"""

    def accelerate(self, obj):
        pass


class AccUniform(Accelerator):
    acc_x = NumericProperty(0)
    acc_y = NumericProperty(0)
    acc = ReferenceListProperty(acc_x, acc_y)

    def __init__(self, acc=(0, 0), acc_x=0, acc_y=0, **kwargs):
        super(AccUniform, self).__init__(**kwargs)
        if acc != (0, 0):
            self.acc = acc
        elif acc_x != 0:
            self.acc_x = acc_x
        elif acc_y != 0:
            self.acc_y = acc_y

    def accelerate(self, obj):
        obj.velocity = Vector(*self.acc) + obj.velocity