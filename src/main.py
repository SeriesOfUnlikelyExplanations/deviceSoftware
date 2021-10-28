# this program is meant to be run periodically by the device and performs a series of functions that sync it with the server
from components.cron import cron
from components.updateip import updateip
from components.movies import movies

# Update cron
cron()

# Update IP address
updateip()

# get Movies
movies()

