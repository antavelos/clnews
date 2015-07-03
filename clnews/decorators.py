"""
.. module:: decorators
   :platform: Unix
      :synopsis: This module contains general use decorators.

      .. moduleauthor:: Alexandros Ntavelos <a.ntavelos@gmail.com>

      """

from subprocess import Popen, PIPE
import errno

def less(func):
    """Less decorator.

    Pipes the output of the decorated function into the less commans

    """
    def inner(self):
        pipe = Popen(['less', '-R'], stdin=PIPE)
        line = func(self)
        try:
            pipe.stdin.write(line)
        except IOError as err:
            if err.errno == errno.EPIPE or err.errno == errno.EINVAL:
                # Stop loop on "Invalid pipe" or "Invalid argument".
                # No sense in continuing with broken pipe.
                return
            else:
                # Raise any other error.
                raise

        pipe.stdin.close()
        pipe.wait()
    return inner
