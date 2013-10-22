import pygame
import random
import time

import threading

class track( threading.Thread ):

	"""A single track, and accompanying settings, for use in a Miasma setting."""

	def __init__(self, channel, path, name="", loop=True, randomise=1, volume=1.0, fadein_percent=10 ):
		"""Initialise settings"""

		# We will dedicate a channel for sounds -- it makes things much easier
		# with respect to looping and randomized sounds to stop them from playing
		# over themselves. (We can always check if this channel is busy.)
		self.__channel = channel
		self.__path = path
		self.__loop = loop
		self.__randomise = randomise
		self.__volume = volume
		self.__fadein_percent = fadein_percent

		if name == "":
			self.__name = path
		else:
			self.__name = name

		# To keep the thread alive by looping
		self._alive = 1
		
		# To handle if the sound should be playing right now
		self.enabled = 1


		# Initialise thread		
		threading.Thread.__init__( self )

		try:
			# Load the given sound
			self.__sound = pygame.mixer.Sound( path )

		except:
			raise UserWarning( "Could not load or play sound file: " + path )

		# Set the sound's default volume
		self.__sound.set_volume( self.__volume )

		# Calculate the exact fadein time, based on the percentage
		# (Get_length returns seconds, fadein wants milliseconds)
		self.__fadein = int( ( self.__sound.get_length() * 10 ) * self.__fadein_percent )

	def run( self ):

		# If we're to loop, we should start straight away
		if self.__loop:
			self.__channel.play( self.__sound, -1, fade_ms=self.__fadein )		
	
		while( self._alive == 1 ):

			#  This handles looping sounds.  Note that this is a straight 'if' on
			#  the loop variable. If a track is set to loop, then the value of the
			#  randomise variable is ignored and no randomisation can occur.
			if self.__loop:
				if self.enabled == 0:
					self.__channel.stop()
				elif self.enabled == 1 and not self.__channel.get_busy():
						self.__channel.play( self.__sound, -1, fade_ms=self.__fadein )
			
			elif self.__randomise:
				if self.enabled and not self.__channel.get_busy():
					chance = random.randint(0,self.__randomise)
					if chance == self.__randomise:
						self.__channel.play(self.__sound, fade_ms=self.__fadein)
				elif not self.enabled:
					self.__channel.stop()

			# If we're here then the sound is neither looping nor randomised.
			# As an arbitrary interpretation, this can play once every loop.
			# (This is unlikely to be desirable.)
			else:
				if not self.__channel.get_busy():
					self.__channel.play(self.__sound, fade_ms=self.__fadein)

			# Sleep for a short time. This is the 'resolution of randomness' in our discrete time events.
			time.sleep( 0.2 )

	def play_start( self ):
		self.enabled = 1

	def play_stop( self ):
		self.enabled = 0

	def end( self ):
		self._alive = 0

	def fadeout( self, duration ):
		self.__channel.fadeout( duration )

	def is_playing( self ):
		return self.__channel.get_busy()

	def get_name( self ):
		return self.__name

	def set_volume( self, volume ):
		# Set the volume of the sound, not the channel.
		# This is absolute, rather than relative to current volume.
		self.__volume = volume	
		self.__sound.set_volume( self.__volume )
