#!/usr/bin/env python
# -*- coding: utf-8 -*-

import listener

class ForeverListener(listener.Listener):
  """
    A listener that listens forever, passing new messages to process_message.
  """
  def process_message(self, message):
    """
      Override this with custom behaviour.
    """
    raise NotImplementedError

  def listen(self):
    """
      Runs forever, passing new messages to process_message.
    """
    while True:
      message = self.queue.get()
      if message.sender != self:
        self.process_message(message)