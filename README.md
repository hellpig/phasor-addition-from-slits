# phasor-addition-from-slits

phasor.py contains 3 main functions. Each function studies the interference of light waves that emerge in phase from equal-width evenly-spaced slits assuming a screen is far away relative to slit spacing. The intended audience is students and instructors of introductory university (calc-based) physics.
 * phasors(N) animates, graphs, and provides an interactive mode for N > 1 slits
 * phasorsSingle(a) animates and graphs single-slit patterns
 * phasorsFull(N, d, a) animates and graphs N slits of width a, where d > a is the distance between the centers of adjacent slits

All distance units are the light's wavelength.

See the top of phasor.py for how to import the functions into Python 3! The matplotlib module is required. I thought it would be interesting to not import the numpy module, so I don't import it!

To complete an animation, close the figure window. Or, you may set *animate = False* in phasor.py.

According to Kirchhoff's diffraction formula, intensity of far-screen
(Fraunhofer) diffraction through a single slit acquires an obliquity factor of
(1+cos(theta))^2/4 that the Huygens-Fresnel principle cannot derive.
In any animation that takes into account slit width, the length of each arrow changes due to this factor.
Even with this factor, all results are approximate due to approximations
made in deriving Kirchhoff's diffraction formula. Results are especially
approximate when a << 1.

You are meant to play around with the code in phasor.py, so look at phasor.py to find more thorough documentation!
