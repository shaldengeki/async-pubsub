#!/usr/bin/env python

from nose.tools import *
import multiprocessing
import async_pubsub

class BasicListener(object):
  def __init__(self):
    self.x = multiprocessing.Queue()
  def __call__(self, channel, queue):
    return self.listen(channel, queue)
  def listen(self, channel, queue):
    self.x.put(queue.get())

class testChannelClass(object):
  @classmethod
  def setUpClass(self):
    self.root_channel = async_pubsub.Channel()
    self.listener = BasicListener()

  def test_access_nonexistent_key_creates_channel(self):
    assert not 'does-not-exist' in self.root_channel
    assert isinstance(self.root_channel['does-not-exist'], async_pubsub.Channel)

  def test_clear_channel_forcibly(self):
    self.root_channel.subscribe(self.listener)
    self.root_channel.clear(force=True)
    assert len(self.root_channel.listeners) == 0
    assert len(self.root_channel.listen_queues) == 0

  def test_subscribe_with_valid_channel(self):
    self.root_channel.clear(force=True)
    p = self.root_channel.subscribe(self.listener)
    p.start()
    assert len(self.root_channel.listeners) == 1
    assert len(self.root_channel.listen_queues) == 1
    self.root_channel.join()
    p.terminate()

  def test_publish_message(self):
    self.root_channel.clear(force=True)
    p = self.root_channel.subscribe(self.listener)
    p.start()
    self.root_channel.publish(self.listener, "test message")
    assert self.listener.x.get() == "test message"
    p.terminate()
