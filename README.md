# Worms
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Pylint](https://github.com/Rankuli-Ang/Worms/actions/workflows/pylint.yml/badge.svg)](https://github.com/Rankuli-Ang/Worms/actions/workflows/pylint.yml)
[![Pytest](https://github.com/Rankuli-Ang/Worms/actions/workflows/python-app.yml/badge.svg)](https://github.com/Rankuli-Ang/Worms/actions/workflows/python-app.yml)


This repository includes the implementation of a simulation model of existence, development, generational change by units called worms. 
Worms are objects located on the map and occupying one cell. They are able to move around the map, attack other worms, and eat food located on the map. 
A simple genome model has been implemented, genes give a bonus to the characteristics of worms and are passed on to descendants. 
Also, with the direct contact of two worms and the creation of a descendant, the genes of the parents are mixed.

![Alt text](images/worms.gif?raw=True "Worms")

the visualization of the GIF shows an example of the simulation. White, blue, green, yellow elements are worms of different generations. Reds are food. light blue elements are rains that have a stat-degrading effect on worms and food. The gray ones are tornadoes, scattering worms and food around them.

- Build: copy all repository files, run worms.py

In realization of program used third party libraries: 
- cv2
- numpy
- configparser
- logging
- unittest
