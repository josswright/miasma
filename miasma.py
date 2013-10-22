#!/usr/bin/python

# file:	miasma.py
# desc:	Randomised soundscape player

import cmd 
import pygame
import os
import time

import track
#import array
#import readline
import sys

class miasma( cmd.Cmd ):

	"""A tool for creating and playing randomised ambient soundscapes."""

	prompt = "miasma> "

	def __init__( self ):
		"""Initialise settings"""

		# A command object for the readline interface
		cmd.Cmd.__init__(self)

		# Set up the PyGame mixer device
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.mixer.init()
		pygame.mixer.set_num_channels( 18 )

		# A hashmap of tracks to be initialised.
		self._tracks = {}

		# Channel counter
		self._num_channels = 0	

		# Initialisation can only happen once.
		# This keeps track of that.
		self._begun = 0

	def load_track( self, path, name="", loop=True, randomise=1, volume=1.0, fadein_percent=10 ):
		"""Load the specified sound into a track."""

		# If name is unspecified, just use the path
		if( name == "" ):
			name = path

		# Increment the channel counter and assign that ID to this track
		self._num_channels += 1
		self._tracks[name] = track.track( pygame.mixer.Channel( self._num_channels ), path, name, loop, randomise, volume, fadein_percent )
		print("Track " + name + " loaded.")


	def begin( self ):
		"""Set all initialised tracks playing."""

		if self._begun == 0:
			for track in self._tracks.keys():
				self._tracks[track].start()
			self._begun = 1
		else:
			self.start()


	def start( self ):
		"""Start all tracks playing."""

		for track in self._tracks.keys():
			self._tracks[track].play_start()

	def stop( self ):
		"""Stop all initialised tracks."""

		for track in self._tracks.keys():
			self._tracks[track].play_stop()

	def quit( self ):
		"""Stop all tracks playing and quit."""

		# Stop all tracks gently
		print("Shutting down.")	
		for track in self._tracks.keys():
			if self._tracks[track].is_playing():
				self._tracks[track].fadeout( 2000 ) 

		time.sleep( 2.5 )

		# Allow all threads to end
		for track in self._tracks.keys():
			self._tracks[track].end()

		# Shut down the PyGame mixer
		pygame.mixer.quit()

		# Shut down the program
		sys.exit(0)

	def do_list_tracks( self, s ):

		print("Enabled tracks:")	
		for track in self._tracks.keys():
			print( " " + self._tracks[track].get_name() )

	def do_list_playing( self, s ):
	
		print("Playing tracks:")	
		for track in self._tracks.keys():
			if self._tracks[track].is_playing():
				print( " " + self._tracks[track].get_name() )

	def do_load_track( self, s ):

		# TODO: Need to rationalise loading/enabling/playing tracks
		# and overall soundscape
	
		args = s.split()

		if len(args) != 2:
			print("Please supply a path to an .ogg file and a track name.")
		else:
			self.load_track( os.path.join(args[0]), args[1] )

	def do_fadeout( self, s ) :
		
		args = s.split()

		if len(args) != 2:
			print("Please supply a track name and duration.")
		else:
			self._tracks[args[0]].fadeout( int( args[1] ) )

	def do_disable( self, s ):
		args = s.split()

		if len(args) != 1:
			print("Please supply only a track name.")
		else:
			self._tracks[args[0]].play_stop()

	def do_enable( self, s ):
		args = s.split()

		if len(args) != 1:
			print("Please supply only a track name.")
		else:
			self._tracks[args[0]].play_start()

	def do_set_volume( self, s ):
		args = s.split()

		if len(args) != 2:
			print("Please supply a track name and volume scale from 0.0 to 1.0.")
		else:
			self._tracks[args[0]].set_volume( float( args[1] ) )

	def do_EOF( self, s ):
		self.quit()

	def do_quit( self, s ):
		
		self.quit()

	def do_begin( self, s ):
		self.begin()

	def do_start( self, s ):
		self.start()

	def do_stop( self, s ):
		self.stop()

if __name__ == '__main__':

	# Create the main Miasma object	
	m = miasma()

	# Create a thread for each track
#	m.load_track( os.path.join('data','133832__felix-blume__the-muezzin-is-calling-the-people-for-the-praying-in-this-small-village-on-the-niger-river-the-muezzin-still-call-without-sound-reinforcement-sound-recorder-close-to-the-muezzin.wav.ogg'), "mali", False, 200, volume=0.4 )
	#m.load_track( os.path.join('data','150990__antigonia__muecin-srebrenica.mp3.ogg'), "srebenica", False, 200 )
	#m.load_track( os.path.join('data','174242__klankbeeld__traffic-along-flat-long-130104-00.flac.ogg'), "traffic", fadein_percent=0 )
	#m.load_track( os.path.join('data','175000__altfuture__helicopter-fly-by.wav.ogg'), "helicopter", False, 500 )
	#m.load_track( os.path.join('data','18497__jmfh__hallo-market.wav.ogg'), "hallo", False, 200, volume=0.5 )
	#m.load_track( os.path.join('data','34380__ejaz215__qur-an-recitation-from-chapter-mary.mp3.ogg'), "quran", False, 300, 0.2 )
	#m.load_track( os.path.join('data','41001__andriala__beer-vendor-at-the-beach.mp3.ogg'), "cerveza", False, 400 )
	#m.load_track( os.path.join('data','104026__rutgermuller__tires-squeaking.wav.ogg'), "tires", False, 800 )
#	m.load_track( os.path.join('data','191350__malupeeters__traffic-mel-1.wav.ogg'), "traffic2", fadein_percent=0 )
	#m.load_track( os.path.join('data','98538__recordinghopkins__motorcycle-1.wav.ogg'), "motorcycle", False, 400 )
#	m.load_track( os.path.join('data','180156__klankbeeld__traffic-horns-city-nervous-busy.wav.ogg'), "horns", False, 600 )
	#m.load_track( os.path.join('data','139951__nikitralala__china-market.aiff.ogg'), "china_market", False, 600, fadein_percent=2, volume=0.2 )
	#m.load_track( os.path.join('data','114396__thatjeffcarter__chicago-police-scanner-2.ogg'), "scanner", False, 500, 0.2 )
	#m.load_track( os.path.join('data','159747__conleec__amb-siren-police-pass-003.ogg'), "police_siren", False, 500 )
	#m.load_track( os.path.join('data','188004__motion-s__police-car-siren.ogg'), "police_siren2", False, 500 )
	#m.load_track( os.path.join('data','thunderstorm.ogg'), "thunder", fadein_percent=0 )

	intro_text = "miasma: Digital soundscape engine\n"
	m.cmdloop( intro_text )
