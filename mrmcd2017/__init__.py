#!/usr/bin/python3

import subprocess
from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://cfp.mrmcd.net/2017/schedule.xml'

# For (really) too long titles
titlemap = {
}

def introFrames(params):
	move=40

	# 1 Sekunden stillstand
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', "%.4f" % 0),
			('subtitle', 'style', 'opacity', "%.4f" % 0),
			('persons', 'style',   'opacity', "%.4f" % 0),
			('rect', 'style', 'opacity', "%.4f" % easeInSine(i, 0, 0.7, frames))
		)

	# 4 Sekunde Text Fadein
	frames = 4*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, i, 0, 1, 2*fps)),
			('title', 'attr',     'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 0*fps, i, -move, move, 2*fps)),

			('subtitle', 'style', 'opacity', "%.4f" % easeDelay(easeLinear, 1*fps, i, 0, 1, 2*fps)),
			('subtitle', 'attr',  'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 1*fps, i, -move, move, 2*fps)),

			('persons', 'style',   'opacity', "%.4f" % easeDelay(easeLinear, 2*fps, i, 0, 1, 2*fps)),
			('persons', 'attr',    'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 2*fps, i, -move, move, 2*fps)),
		)

	# 2 Sekunden stillstand
	frames = 2*fps
	for i in range(0, frames):
		yield tuple()

	# 1 Sekunde fadeout
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
			('subtitle', 'style', 'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
			('persons', 'style',  'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
			('rect', 'style',     'opacity', "%.4f" % easeLinear(i, 0.6, -1, frames)),
		)

# def outroFrames(params):
# 	move=50
#
# 	# 1 Sekunden stillstand
# 	frames = 1*fps
# 	for i in range(0, frames):
# 		yield (
# 			('license', 'style',   'opacity', "%.4f" % 0),
# 		)
#
# 	# 2 Sekunde Text Fadein
# 	frames = 2*fps
# 	for i in range(0, frames):
# 		yield (
# 			('license', 'style',  'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, i, 0, 1, 2*fps)),
# 			('license', 'attr',   'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 0*fps, i, -move, move, 2*fps)),
# 		)
#
# 	# 2 Sekunden stillstand
# 	frames = 2*fps
# 	for i in range(0, frames):
# 		yield tuple()


def debug():
	# render(
	# 	'outro.svg',
	# 	'../outro.ts',
	# 	outroFrames
	# )

	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$id': 904,
			'$title': 'Was ist Open Source, wie funktioniert das?',
			'$subtitle': 'Die Organisation der Open Geo- und GIS-Welt. Worauf man achten sollte.',
			'$personnames': 'Arnulf Christl, Astrid Emde, Dominik Helle, Till Adams'
		}
	)

def tasks(queue, args, idlist, skiplist):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if event['room'] not in ('Prachtgarten', 'Ziergarten'):
			print("skipping room %s (%s)" % (event['room'], event['title']))
			continue

		# generate a task description and put them into the queue
		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".ts",
			sequence = introFrames,
			parameters = {
				'$id': event['id'],
				'$title': event['title'],
				'$subtitle': event['subtitle'],
				'$personnames': event['personnames']
			}
		))

	# # place a task for the outro into the queue
	# queue.put(Rendertask(
	# 	infile = 'outro.svg',
	# 	outfile = 'outro.ts',
	# 	sequence = outroFrames
	# ))
	#
	# # place the pause-sequence into the queue
	# queue.put(Rendertask(
	# 	infile = 'pause.svg',
	# 	outfile = 'pause.ts',
	# 	sequence = pauseFrames
	# ))
