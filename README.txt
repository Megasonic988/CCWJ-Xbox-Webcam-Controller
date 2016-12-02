CCWJ Helmet Camera Controller
By Kevin Wang and Goetz Dapp

Description
This Python script allows you to control the parameters of a connected webcam
(e.g. pan, exposure, zoom) using an XBOX controller. Written for running
on OpenSuse Leap 42.2 with a Logitech webcam.

Dependencies:
- Python 3
- xboxdrv (driver for XBOX controller)
- v4l2-utils (driver for webcam)
- guvcview (for viewing the webcam output)
- ffmpeg (for adding the logo watermark)
- pygame (for interfacing XBOX controller and Python. Install with pip)

Running:
1. Run 'sudo xboxdrv'. For ease, run xboxdrv on system startup.
2. Run script with 'python3 init.py'

To do:
- run guvcview automatically
- use guvcview to record
- CCWJ watermark on file
