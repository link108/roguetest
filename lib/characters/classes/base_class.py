__author__ = 'cmotevasselani'

from abc import ABCMeta, abstractmethod

class BaseClass:

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_caster_component(self):
        raise NotImplementedError('subclasses must override foo()!')
