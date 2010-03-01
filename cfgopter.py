# coding=utf-8
""" 
* Copyright © 2010 by Thomas Roth <code@leveldown.de>
*
* Permission to use, copy, modify, and/or distribute this software for any
* purpose with or without fee is hereby granted, provided that the above
* copyright notice and this permission notice appear in all copies.
*
* THIS SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
* WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
* MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
* ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
* WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
* ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
* OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
from optparse import OptionParser
import ConfigParser
from new import classobj

class cfgopter:
	optparser = None
	cfgparser = None
	cfg = None
	def __init__(self, defaults=None):
		self.optparser = OptionParser()
		self.cfgparser = ConfigParser.SafeConfigParser()
		self.cfg = classobj('cfgopter_config', (object,),{})
		if defaults:
			for section in defaults:
				setattr(self.cfg, section, classobj('section', (object,),{}))
				for option in defaults[section]:
					setattr(getattr(self.cfg, section), option, defaults[section][option])

	def load(self, file):
		self.cfgparser.read(file)

	def get_config(self):
		#Iterate through all sections
		for section in self.cfgparser.sections():
			if not getattr(self.cfg, section, None):
				#Create object for the section.
				setattr(self.cfg, section, classobj('section', (object,),{}))

			#Iterate through all options
			for option in self.cfgparser.options(section):
				#Set attribute for option.
				setattr(getattr(self.cfg, section), option, self.cfgparser.get(section, option))

		return self.cfg

	def optparse_callback(opt, opt_str, value, parser, *args, **kwargs):
		setattr(kwargs['section'], kwargs['option'], parser)

	def optparse_toggle_callback(opt, opt_str, value, parser, *args, **kwargs):
		setattr(kwargs['section'], kwargs['option'], kwargs['to'])

	def add_opt(self,
		short_opt="",
		long_opt="",
		label="",
		section=None,
		option="",
		help=""):
		self.optparser.add_option(
			short_opt,
			long_opt,
			metavar=label,
			action="callback",
			type="string", 
			help=help,
			callback=self.optparse_callback,
			callback_kwargs={
				'section':section, 'option':option})

	def add_toggle_opt(self,
		short_opt="",
		long_opt="",
		label="",
		section=None,
		option="",
		help="",
		to=True):
		self.optparser.add_option(
			short_opt, 
			long_opt, 
			metavar=label, 
			action="callback", 
			help=help,
			callback=self.optparse_toggle_callback, 
			callback_kwargs={'section':section, 'option':option, 'to': to})
	def parse_args(self):
		options, args = self.optparser.parse_args()
