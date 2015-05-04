__author__ = 'cmotevasselani'

from abc import ABCMeta, abstractmethod


class BaseRace:
  __metaclass__ = ABCMeta

  @abstractmethod
  def get_fighter_component(self):
    raise NotImplementedError('subclasses must override foo()!')
