#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing

import channel

class Core(object):
  """
  Middleware singleton class between publishers and subscribers.
  You'll want to register all publishers and subscribers through this.
  """
  def __init__(self):
    self.channels = channel.Channel(core=self, name='root')
    self.manager = multiprocessing.Manager()
    self.listener_queues = self.manager.dict()

  def parse_channel_hierarchy(self, channel):
    """
    Given a fully-qualified channel name like "root-topic.sub-topic.sub-topic"
    Return a list representing the channel hierarchy, like ['root-topic', 'sub-topic', 'sub-topic']
    """
    return channel.split('.')

  def get_channel(self, channel):
    """
    Given a fully-qualified channel name like "root-topic.sub-topic.sub-topic"
    Create the channel if it doesn't exist, and return the channel.
    """
    channel_hierarchy = self.parse_channel_hierarchy(channel)
    curr_parent_channel = self.channels
    for c in channel_hierarchy[:-1]:
      curr_parent_channel = curr_parent_channel[c]
    return curr_parent_channel[channel_hierarchy[-1]]

  def channel(self, channel):
    """
    Convenience method for get_channel.
    """
    return self.get_channel(channel)

  def listener_queue(self, listener):
    # reserves a new queue for a given listener, if it doesn't exist already.
    # returns the listener's queue.
    if listener not in self.listener_queues:
      self.listener_queues[listener] = self.manager.Queue()
    return self.listener_queues[listener]

  def subscribe(self, listener, channel):
    """
    Registers listener under channel.
    """
    return self.get_channel(channel).subscribe(listener)

  def publish(self, channel, message):
    """
    Publishes *args and **kwargs under the given channel.
    """
    return self.get_channel(channel).publish(message)

  def join(self):
    """
    Blocks until all channels are completed.
    """
    for c in self.channels:
      self.channels[c].join()