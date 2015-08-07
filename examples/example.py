#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import time

import async_pubsub
import async_pubsub.listeners

class NumMessagesPublisher(async_pubsub.listeners.QuittableListener):
  def __init__(self):
    super(NumMessagesPublisher, self).__init__()
    self.messages = 0
    self.last_time = time.time()

  def process_message(self, channel, message):
    self.messages += 1
    now = time.time()
    if now - self.last_time > 1:
      message = async_pubsub.Message(sender=self, message=self.messages)
      self.publish(message)
      self.last_time = now
      self.messages = 0

class NumMessagesSubscriber(async_pubsub.listeners.QuittableListener):
  def process_message(self, channel, message):
    print "Number of messages per second: " + str(message.message)

class Publisher(async_pubsub.listeners.Listener):
  def listen(self, channel, queue):
    while True:
      channel.publish('message')

core = async_pubsub.Core()
pub = Publisher()
num_messages_pub = NumMessagesPublisher()
num_messages_sub = NumMessagesSubscriber()


pub.subscribe(core.channel('foo'))
num_messages_pub.subscribe(core.channel('root'), publish=False)
num_mesages_sub.subscribe(core.channel('metrics'))

pub.publish('start')