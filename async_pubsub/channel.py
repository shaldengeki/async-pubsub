#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import multiprocessing

class Channel(collections.defaultdict):
  """
  Channel class.
  """
  def __init__(self, name=None, parent=None):
    self.name = name
    self.parent = parent
    self.listeners = []
    self.listen_queues = []

  def __missing__(self, key):
    ret = self[key] = Channel(name=key, parent=self)
    return ret

  def fully_qualified_name(self):
    hierarchy = []
    curr_chan = self
    while True:
      hierarchy.append(curr_chan.name)
      if curr_chan.parent is None:
        break
      curr_chan = curr_chan.parent
    return ".".join(reversed(hierarchy))

  def publish(self, message):
    """
    Publishes the given arguments under the current channel.
    Also publishes under the parent channel, if one exists.
    """
    for q in self.listen_queues:
      print "PUTTING MESSAGE"
      print message
      q.put(message)

    if self.parent is not None:
      self.parent.publish(message)

    return True

  def subscribe(self, listener):
    """
    Subscribes to the current channel with the given listener.
    Returns the created process.
    """
    # reserve a new queue for this listener.
    self.listen_queues.append(multiprocessing.JoinableQueue())
    p = multiprocessing.Process(target=listener, args=(self.listen_queues[-1],))
    self.listeners.append(p)
    return p

  def join(self):
    """
    Blocks until all jobs in this channel are done.
    """
    for q in self.listen_queues:
      q.join()

  def clear(self, force=False):
    """
    Sends all listeners on the current channel a quit signal.
    If force is True, forcibly-terminates processes.
    Otherwise, blocks until processes complete.
    """
    if force:
      for p in self.listeners:
        if p.is_alive():
          p.terminate()
    else:
      for q in self.listen_queues:
        q.put("QUIT", False)
      self.join()
    self.listeners = []
    self.listen_queues = []
