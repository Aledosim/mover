import logging

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.vector import Vector

import movements

logging.basicConfig(filename='mover.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger('root')

kivy.require('1.10.0')


class Rastro(Widget):
    """Widget que cria cópias de outro widget, controlando-as de forma que se cria um rastro dele"""
    decay = NumericProperty(0)
    obj = ObjectProperty(None)
    rastro = ListProperty(())

    def __init__(self, obj=None, decay=0, **kwargs):
        super(Rastro, self).__init__(**kwargs)
        self.obj = obj
        self.decay = decay
        Clock.schedule_interval(self.update, 0.005)

    def update(self, dt):
        # cria cópia
        cp = Mass()
        cp.pos = self.obj.pos
        cp.size = self.obj.size
        cp.velocity= [0, 0]

        self.add_widget(cp)

        # atualiza valores de opacidade das cópias
        for masstemp in self.rastro:
            if masstemp.opacity < 0:
                self.rastro.remove(masstemp)
            else:
                masstemp.opacity = masstemp.opacity - self.decay
        # adiciona uma cópia ao rastro
        self.rastro.append(cp)


class Mass(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        for child in self.children:
            child.pos = Vector(*self.velocity) + child.pos


class Mover(RelativeLayout):
    """Widget que movimenta outros widgets em relação à ele. À ele se relacionam uma classe que
    descreve a dinâmica do movimento (acelerator) e uma outra que representa o widget à ser acoplado"""
    obj = ObjectProperty(None)
    acc = ObjectProperty(None)
    rastro = ObjectProperty(None)
    pos_init_x = NumericProperty(0)
    pos_init_y = NumericProperty(0)
    pos_init = ReferenceListProperty(pos_init_x, pos_init_y)
    vel_init_x = NumericProperty(0)
    vel_init_y = NumericProperty(0)
    vel_init = ReferenceListProperty(vel_init_x, vel_init_y)
    
    def __init__(self, pos_init=(0, 0), pos_init_x=0, pos_init_y=0,
                 vel_init=(0, 0), vel_init_x=0, vel_init_y=0, decay=0, **kwargs):
        super(Mover, self).__init__(**kwargs)
        
        if pos_init != (0, 0):
            self.pos_init = pos_init
        elif pos_init_x != 0:
            self.pos_init_x = pos_init_x
        elif pos_init_y != 0:
            self.pos_init_y = pos_init_y
            
        if vel_init != (0, 0):
            self.vel_init = vel_init
        elif vel_init_x != 0:
            self.vel_init_x = vel_init_x
        elif vel_init_y != 0:
            self.vel_init_y = vel_init_y

        self.rastro = Rastro(obj=self.obj, decay=decay)
        self.add_widget(self.rastro)

    def start(self):
        self.obj.center = Vector(*self.pos_init) + self.center
        self.obj.velocity = self.vel_init

    def update(self, dt):
        logger.debug('Posição: ' + str(self.obj.pos))
        logger.debug('Velocidade: ' + str(self.obj.velocity))
        logger.debug('dt: '+str(dt))
        # move o objeto
        self.obj.move()
        # atualiza a sua velocidade de acordo com a dinâmica escolhida
        self.acc.accelerate(self.obj)
        # cria rastro de widget


class MoverApp(App):
    def build(self):
        mover = Mover(vel_init=[10, 10], decay=0.01)
        osc = movements.Oscillator(frequency=[0.1, 0.11])
        osc.center = mover.center
        mover.acc = osc
        mover.start()
        Clock.schedule_interval(mover.update, 1/60)
        return mover


if __name__ == '__main__':
    MoverApp().run()
