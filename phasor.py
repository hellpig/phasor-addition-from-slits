# -*- coding: utf-8 -*-
#
# import this Python-3 file via:
#   from phasor import *
#
# After making changes to this file, reload via:
"""
from importlib import reload
import phasor
reload(phasor)
from phasor import *
"""
# Only the last two lines need to be run if reloading the next time
#
# (c) 2021 Bradley Knockel


import math

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider, TextBox





### global parameters


figSize = 5.6   # size of figures in both dimensions (in inches)

pi = 3.141592653589793

R = .025     #radius of circles (in units where 1 is figSize)


# For the code to complete after the animation, close the figure window.
# You may also set  animate = False  to prevent having to do this

animate = True

t = 10        #pause interval for animation (in milliseconds)





### helper functions


# just like MATLAB's linspace()
# except I assume that n > 1
def linspace(a, b, n):
    stepSize = (b - a)/(n - 1)
    return [stepSize*i + a  for i in range(n)]


# MATLAB's  a:stepSize:b
def sequence(a, stepSize, b):
    # because of roundoff error, err on the side of too many values, hence 1.00000000000001
    values = int(1.00000000000001 * (b-a) / stepSize) + 1
    return [a + i*stepSize for i in range(values)]


# Used by phasors(), phasorsSingle(), and phasorsFull()
#    to do calculations and, if animate, make animations
# Give theta[] if you want to display theta information on figure
# y[] is the output
def makeAnimation(N, phaseList, Llist, y, thetaList = []):

  # all input and output lists should be this length
  length = len(phaseList)

  # setup the figure
  if animate:

      fig, ax = plt.subplots()
      ax.axis('off')
      fig.set_size_inches( figSize, figSize )

      ann = ax.annotate('', (0.1, 0.1), xycoords = 'figure fraction')

      # I put circles on fig (not ax) to get them to line up with arrows
      circle1 = plt.Circle(( 0.5 , 0.5 ), R, fill=False )
      fig.add_artist(circle1)
      circle2 = plt.Circle(( 0.5 , 0.5 ), R, fill=False )
      fig.add_artist(circle2)

#      # create the N arrows
#      arrows = [0]*N
#      for i in range(N):
#          arrows[i] = ax.annotate("", (0.6, 0.5), xytext = (0.5, 0.5),
#              arrowprops=dict(arrowstyle="->"), xycoords='figure fraction')

  def animateFunc(frame):
      phase = phaseList[frame]
      L = Llist[frame]

      # Clear entire axis,
      # This is an extreme approach that slows the animation
      #   and requires that annotations (such as arrows) be created from scratch each time,
      #   but my macOS (not Windows or Linux) requires this for animation to update correctly.
      # I have commented-out code that can be used instead of this extreme approach.
      if animate:
          ax.clear()
          ax.axis('off')

      # here are the actual important calculations
      tip = (.5, .5)  #begin in center of figure
      for i in range(N):
          angle = i*phase
          tipnew = (tip[0] + L*math.cos(angle), tip[1] + L*math.sin(angle))
          if animate:
#              arrows[i]._x = tip[0]
#              arrows[i]._y = tip[1]
#              arrows[i].xy = tipnew
              ax.annotate("", tipnew, xytext=tip,
                arrowprops=dict(arrowstyle="->"), xycoords='figure fraction')   # draw arrow
          tip = tipnew
      y[frame] = ((tip[0]-.5)**2 + (tip[1]-.5)**2 )**0.5

      if animate:

          if len(thetaList):
#              ann.set_text('θ = ' + str(round(thetaList[frame]*180/pi,4)) + '°')
              ann = ax.annotate('θ = ' + str(round(thetaList[frame]*180/pi,4)) + '°',
                (0.1, 0.1), xycoords = 'figure fraction')

          circle2.center = tip

          plt.draw()

#          # On macOS, the following still required me to wiggle my mouse after window closes!
#          # Regardless of OS, I don't know if I want the window to automatically close.
#          if frame == length-1:
#             plt.close()

      return


  if animate:

      # make the animation! And calculate y[]
      _ = animation.FuncAnimation(fig, animateFunc, frames=length, interval=t, repeat=False)
      plt.show()

  else:

      # hijack animateFunc() to calculate y[]
      for i in range(length):
          animateFunc(i)





def phasors(N):
# This function studies the interference of light waves that emerge in
# phase from equal-width evenly-spaced slits assuming a screen is far away
# relative to slit spacing and ignoring the single-slit pattern.
#
# N>1 is an integer that is the number of slits
#
# In the animation or in the interactive mode, amplitude of total electric
# field at screen is given by distance between the two circles.
#
# phase = the phase difference at screen between waves that came from
#         adjacent slits
#
# To calculate the diffraction angle (theta) from a given phase, use
#     sin(theta) = lambda * phase / (2 * pi * d)
# where...
#     d is the distance between adjacent slits
#     lambda is the wavelength of light

  if N < 2 or round(N) != float(N):
    print('Error: N must be an integer larger than 1')
    return

  L0 = 0.99/(2*N)  #length of arrow (in units where 1 is figSize)

  # the following should be positive and ideally integers
  M = 1          #phase cycles (M>0)
  nPerCyclePerSlit = 10  #number of data points per cycle per slit


  ## do some initial calculations

  n = round(M*N*nPerCyclePerSlit + 1)  #number of data points
  dx = 2*pi*M     #x range (phases in radians)

  x = linspace(0.0, dx, n)  #phases (in radians)
  y = [0.0]*n     #initialize total amplitudes (in units of L0)


  ## do calculations and, if animate, make 1st figure

  # y[] is the output
  makeAnimation(N, x, [L0]*n, y)

  # scale y[]
  y = [yi/L0 for yi in y]


  ## make 2nd figure

  # convert to degrees
  x = [i*180/pi for i in x]
  dx = dx*180/pi

  fig, ax = plt.subplots()
  fig.set_size_inches( figSize, figSize )
  fig.suptitle(str(N) + ' slits')

  ax = plt.subplot(2,1,1)
  ax.plot(x,y,'b.-')
  ax.set_xlabel('phase (°)')
  ax.set_ylabel('electric field amplitude')
  plt.axis([0.0, dx, 0.0, N])

  ax = plt.subplot(2,1,2)
  ax.plot(x, [i**2 for i in y], 'b.-')
  ax.set_xlabel('phase (°)')
  ax.set_ylabel('intensity')
  plt.axis([0.0, dx, 0.0, N**2])


  ## make 3rd figure; it's interactive!

  fig, ax = plt.subplots()
  ax.axis('off')
  fig.set_size_inches( figSize, figSize )

  # I put circles on fig (not ax) to get them to line up with arrows
  circle1 = plt.Circle(( 0.5 , 0.5 ), R, fill=False )
  fig.add_artist(circle1)
  circle2 = plt.Circle(( 0.5 , 0.5 ), R, fill=False )
  fig.add_artist(circle2)

  ax.annotate('set phase (from 0 to 2*pi)', (.51, .03), xycoords = 'figure fraction')

  # interactive widgets
  slider = Slider(plt.axes([.2, .1, .6, .05]), '',
    valmin=0.0, valmax=2.0*pi, valinit=0.0, orientation="horizontal")
  textbox = TextBox(plt.axes([.2, .02, .3, .07]), '', initial = '')

  # create the N arrows
  arrows = [0]*N
  for i in range(N):
      arrows[i] = ax.annotate("", (0.6, 0.5), xytext = (0.5, 0.5),
          arrowprops=dict(arrowstyle="->"), xycoords='figure fraction')

  def update(phase):
    tip = (.5, .5)   #begin in center of figure
    for i in range(N):
        theta = i*phase
        tipnew = (tip[0] + L0*math.cos(theta), tip[1] + L0*math.sin(theta))
        arrows[i]._x = tip[0]
        arrows[i]._y = tip[1]
        arrows[i].xy = tipnew
        tip = tipnew
    circle2.center = tip
    plt.draw()

  def update2(phase):
    phase = float(eval(phase)) % (2*pi)
    slider.set_val(phase)   # calls update(phase)

  slider.on_changed(update)
  textbox.on_submit(update2)

  update(0.0)


  ## show figures 2 and 3
  plt.show()







def phasorsSingle(a):
# a>0 is the slit width in units of the light's wavelength, and floor(a) is
# the number of minima that will be in the diffraction pattern between
# diffraction angles 0 and pi/2. That is, as a gets larger, the central
# peak gets narrower. Keep a<10 if you are in a hurry.
#
# This function studies the interference of light waves that emerge in
# phase from different parts of a single slit assuming a screen is far away
# relative to slit width. The method used is to divide the slit into N
# equally-spaced sample points and see how the phasors from those points
# interfere, which gives approximate results. This code chooses N based on
# the value of a. The distance between adjacent sample points is a/N.
#
# Amplitude of total electric field at screen is proportional to distance
# between the two circles in the animation.
#
# theta = the angle of diffraction where we will consider theta's range to
#         be between 0 and pi/2
#
# According to Kirchhoff's diffraction formula, intensity of far screen
# (Fraunhofer) diffraction through a slit acquires an obliquity factor of
# (1+cos(theta))^2/4 that the Huygens-Fresnel principle cannot account for.
# In the animation, the length of each arrow changes due to this factor.
# Even with this factor, all results are approximate due to approximations
# made in deriving Kirchhoff's diffraction formula. Results are especially
# approximate when a << 1.
#
# The green curve on the bottom graph is the intensity curve prediction
# using the equation that you get when taking the limit as N goes to
# infinity.


  # N>1 is an integer that is the number of sample points.
  # a/N is the distance between adjacent sample points.
  # If a/N << 1, the approximation to a single slit is better.
  # N should at least be 2*a to prevent intensities from increasing again
  #    past a certain theta.
  # As long as N>a, the minima will be calculated at the correct spots.

  N = math.ceil(3*a)
  if N<5:
    N=5

  if a <= 0.0:
    print('Error: a is not positive')
    return


  L0 = .99/(2*N)  #max length of arrow (in units where 1 is figSize)

  n = 10  #number of data points per intensity maximum
  if n*a<90:
    n = round(90/a)


  dx = pi/2           #x range (in radians), not larger than pi/2
  sinTheta = sequence(0.0, 1.0/(n*a), math.sin(dx))
  x = [math.asin(x) for x in sinTheta]    #theta (in radians)
  y = [0]*len(x)      #initialize total amplitudes

  # take into account the inclination factor
  Llist = [L0*(1.0 + math.cos(xi))/2.0 for xi in x]


  ## do calculations and, if animate, make 1st figure

  # y[] is the output
  phaseList = [2.0*pi*a/N * si for si in sinTheta]
  makeAnimation(N, phaseList, Llist, y, x)

  # scale y[]
  y = [yi*a/(N*L0) for yi in y]


  ## make 2nd figure

  # the actual intensity curve (x=0 causes division by 0!)
  def curve(x):
    return a**2 * (math.sin(pi*a*math.sin(x))/(pi*a*math.sin(x)))**2 * (1.0 + math.cos(x))**2 / 4.0

  # make data points on the actual intensity curve
  x2 = [math.asin(i) for i in sequence(0.0, 1.0/(10.0*n*a), math.sin(dx))]
  y2 = [a**2] + [curve(x) for x in x2 if x!=0.0]

  # convert theta to degrees
  x = [i*180/pi for i in x]
  x2 = [i*180/pi for i in x2]
  dx = dx*180/pi

  fig, ax = plt.subplots()
  fig.set_size_inches( figSize, figSize )
  fig.suptitle('a = ' + str(round(a,4)))

  ax = plt.subplot(2,1,1)
  ax.plot(x,y,'b.')
  ax.set_xlabel('θ (°)')
  ax.set_ylabel('electric field amplitude')
  plt.axis([0.0, dx, 0.0, a])

  ax = plt.subplot(2,1,2)
  ax.plot(x,[i**2 for i in y],'b.',x2,y2,'g-')
  ax.set_xlabel('θ (°)')
  ax.set_ylabel('intensity')
  plt.axis([0.0, dx, 0.0, a**2])

  plt.show()






def phasorsFull(N,d,a):
# N>1 is an integer that is the number of slits
# d>0 is the distance between the centers of adjacent slits
#      in units of the light's wavelength
# 0<a<d is the slit width in units of the light's wavelength
#
# This function studies the interference of light waves that emerge in
# phase from equal-width evenly-spaced slits assuming a screen is far away
# relative to slit spacing.
#
# theta = the angle of diffraction where we will consider theta's range to
#         be between 0 and pi/2
#
# Amplitude of total electric field at screen is proportional to distance
# between the two circles in the animation. The length of each slit's arrow
# changes as a function of theta due to single-slit effects (see
# phasorsSingle() for a discussion of these effects).
#
# The green curve on the bottom graph is the single-slit envelope.

  if a<=0 or a>=d or N<2 or round(N)!=float(N) or d<=0:
    print('Error: invalid input')
    return


  L0 = .99/(2*N)  #max length of arrow (in units where 1 is figSize)

  n = 10  #number of data points per intensity maximum
  if n*N*d<90:
    n = round(90/(N*d))


  dx = pi/2           #x range (in radians), not larger than pi/2
  sinTheta = sequence(0.0, 1.0/(n*N*d), math.sin(dx))
  x = [math.asin(x) for x in sinTheta]    #theta (in radians)
  y = [0]*len(x)      #initialize total amplitudes

  # take into account the single-slit intensity curve
  Llist = [L0] + [L0*math.sin(pi*a*si)/(pi*a*si)*(1.0+math.cos(xi))/2.0 for (xi,si) in zip(x,sinTheta) if xi!=0.0]


  ## do calculations and, if animate, make 1st figure

  # y[] is the output
  phaseList = [2.0*pi*d * si for si in sinTheta]
  makeAnimation(N, phaseList, Llist, y, x)

  # scale y[]
  y = [yi*a/L0 for yi in y]


  ## make 2nd figure

  # the actual intensity curve (x=0 causes division by 0!)
  def curve(x):
    return (a*N)**2 * (math.sin(pi*a*math.sin(x))/(pi*a*math.sin(x)))**2 * (1.0 + math.cos(x))**2 / 4.0

  # make the single-slit envelope
  x2 = [math.asin(i) for i in sequence(0.0, 1.0/(10.0*n*N*d), math.sin(dx))]
  y2 = [(a*N)**2] + [curve(x) for x in x2 if x!=0.0]

  # convert theta to degrees
  x = [i*180/pi for i in x]
  x2 = [i*180/pi for i in x2]
  dx = dx*180/pi

  fig, ax = plt.subplots()
  fig.set_size_inches( figSize, figSize )
  fig.suptitle(str(N) + ' slits; d = ' + str(round(d,4)) + '; a = ' + str(round(a,4)))

  ax = plt.subplot(2,1,1)
  ax.plot(x,y,'b.-')
  ax.set_xlabel('θ (°)')
  ax.set_ylabel('electric field amplitude')
  plt.axis([0.0, dx, 0.0, N*a])

  ax = plt.subplot(2,1,2)
  ax.plot(x,[i**2 for i in y],'b.-',x2,y2,'g-')
  ax.set_xlabel('θ (°)')
  ax.set_ylabel('intensity')
  plt.axis([0.0, dx, 0.0, (N*a)**2])

  plt.show()

