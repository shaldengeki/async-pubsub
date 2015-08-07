#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .. import message

class Listener(object):
  """
  A basic listener class.
  """
  def __call__(self):
    return self.listen()

  def __key(self):
    return self.name

  def __eq__(x, y):
    return type(x) == type(y) and x.__key() == y.__key()

  def __hash__(self):
    return hash(self.__key())

  def __str__(self):
    return "<Listener(" + self.name + ")>"

  def __repr__(self):
    return str(self)

  def __init__(self, name):
    self.name = name
    self.queue = None
    self.subscribe_channels = set()
    self.publish_channels = set()
    self.process = None

  def publish(self, text, channels=None):
    """
    Publishes a text message from the current listener under channels, if provided.
    If channels is not provided, publishes under everything in self.publish_channels.
    """
    if channels is None:
      channels = self.publish_channels
    for channel in channels:
      message = message.Message(sender=self, message=text, channel=channel)
      channel.publish(message)

  def subscribe(self, channel, publish=True):
    """
    Subscribes this listener to a channel.
    If publish is true, also add this channel to publish channels.
    """
    self.queue = channel.subscribe(self)
    self.subscribe_channels.add(channel)
    if publish:
      self.add_publish_channel(channel)

  def add_publish_channel(self, channel):
    self.publish_channels.add(channel)

  def listen(self):
    """
    Listens on all subscribed channels.
    """
    raise NotImplementedError

  def start(self):
    """
    Starts the current listener on all channels.
    Returns the created process.
    """
    self.process = multiprocessing.Process(target=self, args=(self.queue,))
    self.process.daemon = True
    self.process.start()
    return self.process
