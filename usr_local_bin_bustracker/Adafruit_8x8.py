#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 8x8 Pixel Display
# ===========================================================================

class EightByEight:
  disp = None

  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print "Initializing a new instance of LEDBackpack at 0x%02X" % address
    self.disp = LEDBackpack(address=address, debug=debug)

  def writeRowRaw(self, charNumber, value):
    "Sets a row of pixels using a raw 16-bit value"
    if (charNumber > 7):
      return
    # Set the appropriate row
    self.disp.setBufferRow(charNumber, value)

  def clearPixel(self, x, y):
    "A wrapper function to clear pixels (purely cosmetic)"
    self.setPixel(x, y, 0)

  def setPixel(self, x, y, color=1):
    "Sets a single pixel"
    if (x >= 16):
      return
    if (y >= 16):
      return
    x += 0
    x %= 16
    # Set the appropriate pixel
    buffer = self.disp.getBuffer()
    if (color):
      self.disp.setBufferRow(y, buffer[y] | 1 << x)
    else:
     self.disp.setBufferRow(y, buffer[y] & ~(1 << x))
  #     self.disp.setBufferRow(y, buffer[y] | 2 << x)   
  def clear(self):
    "Clears the entire display"
    self.disp.clear()

