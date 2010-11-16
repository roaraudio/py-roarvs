#!/usr/bin/env python

"""
 *      Copyright (C) Philipp 'ph3-der-loewe' Schafft - 2008, 2009, 2010
 *      Copyright (C) Hans-Kristian Arntzen           - 2010
 *
 *  This file is part of pyroarvs a Python wrapper for libroar VS API.
 *
 *  This file is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License version 3
 *  as published by the Free Software Foundation.
 *
 *  libroar is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this software; see the file COPYING.  If not, write to
 *  the Free Software Foundation, 51 Franklin Street, Fifth Floor,
 *  Boston, MA 02110-1301, USA.
"""

from ctypes import *
import sys

libroar = cdll.LoadLibrary('libroar.so')

roar_vs_new_simple = libroar.roar_vs_new_simple
roar_vs_new_simple.argtypes = [c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_void_p]
roar_vs_new_simple.restypes = [c_void_p]

roar_vs_write = libroar.roar_vs_write
roar_vs_write.argtypes = [c_void_p, c_void_p, c_long, c_void_p]
roar_vs_write.restypes = [c_long]

roar_vs_close = libroar.roar_vs_close
roar_vs_close.argtypes = [c_void_p, c_int, c_void_p]
roar_vs_close.restypes = None

ROAR_VS_TRUE = 1
ROAR_CODEC_PCM_S_LE = 1
ROAR_DIR_PLAY = 1

class roar_vs:
   def __init__(self, rate, chans):
      self.handle = roar_vs_new_simple(None, None, rate, chans, ROAR_CODEC_PCM_S_LE, 16, ROAR_DIR_PLAY, None)
      if self.handle == None:
         raise IOError

   def write(self, buf):
      return roar_vs_write(self.handle, buf, len(buf), None)

   def close(self):
      roar_vs_close(self.handle, ROAR_VS_TRUE, None)
      self.handle = None

if __name__ == '__main__':

   sys.stdin = sys.stdin.detach()

   rd = roar_vs(44100, 2)
   buf = sys.stdin.read(44)
   buf = sys.stdin.read(128)
   while rd.write(buf):
      buf = sys.stdin.read(128)
   rd.close()

