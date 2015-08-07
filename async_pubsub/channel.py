#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import multiprocessing

class Channel(collections.defaultdict):
  """
  Channel class.
  """
  def __key(self):
    return tuple(self.name_hierarchy())

  def __eq__(x, y):
    return type(x) == type(y) and x.__key() == y.__key()

  def __hash__(self):
    return hash(self.__key())

  def __str__(self):
    return "<Channel(" + self.name + ")>"

  def __repr__(self):
    return str(self)

  def __init__(self, core=None, name=None, parent=None):
    self.core = core
    self.name = name
    self.parent = parent
    self.listeners = {}

  def __missing__(self, key):
    ret = self[key] = Channel(core=self.core, name=key, parent=self)
    return ret

  def name_hierarchy(self):
    hierarchy = []
    curr_chan = self
    while True:
      hierarchy.append(curr_chan.name)
      if curr_chan.parent is None:
        break
      curr_chan = curr_chan.parent
    return reversed(hierarchy)

  def fully_qualified_name(self):
    return ".".join(self.name_hierarchy())

  def publish(self, message):
    """
    Publishes a given message under the current channel.
    Also publishes under the parent channel, if one exists.
    """
    for listener,queue in self.listeners.iteritems():
      queue.put(message)

    if self.parent is not None:
      self.parent.publish(message)

    return True

  def subscribe(self, listener):
    """
    Subscribes the given listener to this channel.
    """
    # reserve a new listener queue for this listener.
    self.listeners[listener] = self.core.listener_queue(listener)
    return self.listeners[listener]

  def unsubscribe(self, listener):
    """
    Unsubscribes a given listener from the current channel.
    """
    del self.listeners[listener]

  def join(self):
    """
    Blocks until all jobs in this channel are done.
    """
    for listener,queue in self.listeners.iteritems():
      queue.join()

  def clear(self):
    """
    Sends all listeners on the current channel a quit signal.
    Blocks until processes complete.
    """
    for listener,queue in self.listeners.iteritems():
      queue.put("QUIT", False)
    self.join()
    self.listeners = {}
