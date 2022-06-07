Python extension to AstroDienst Swiss Ephemeris library.

Swiss Ephemeris homepage: http://www.astro.com/swisseph/

Compatible with Python 2.x and 3.x.

Usage example:

>>> import swisseph as swe
>>> swe.set_ephe_path('/usr/share/ephe') # set path to ephemeris files
>>> now = swe.julday(2007,3,3) # get Julian day number
>>> res = swe.lun_eclipse_when(now) # find next lunar eclipse (from now on)
>>> ecltime = swe.revjul(res[1][0]) # get date UTC
>>> ecltime
(2007, 3, 3, 23.347975596785545)
>>> jd = swe.julday(2008,3,21)
>>> swe.calc_ut(jd, swe.AST_OFFSET+13681)[0] # asteroid Monty Python
0.098474291148756998
>>> help(swe)

Standard installation (unixes): ``# python setup.py install``



