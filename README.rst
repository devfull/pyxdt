###########################
Python bindings for xdotool
###########################

**DESCRIPTION**

   `xdotool <https://github.com/jordansissel/xdotool>`_ lets you
   programmatically (or manually) simulate keyboard input and mouse activity,
   move and resize windows, etc.

Every xdotool commands can be chained together and are executed once with
``.run()``. The subprocess results are found under the instance variables
``stdout``, ``stderr`` and ``status``. An additional variable named ``outputs``
lists a structured version of stdout for each separate commands.
