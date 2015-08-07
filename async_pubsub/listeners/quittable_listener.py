#!/usr/bin/env python
# -*- coding: utf-8 -*-

import forever_listener

class QuittableListener(forever_listener.ForeverListener):
  """
    A listener that listens for messages, quitting when it receives a 'QUIT' message.
  """
  def listen(self):
    """
      Passes new messages to process_message until the message is 'QUIT'.
    """
    while True:
      message = self.queue.get()
      if message.message == 'QUIT':
        message.channel.unsubscribe(self)
        break
      if message.sender != self:
        self.process_message(message)