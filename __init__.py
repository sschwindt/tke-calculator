import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    logging.getLogger()
except NameError:
    pass
