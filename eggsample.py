#!/usr/bin/python

import argparse
import contextlib
import difflib
import json
import logging
import os
import platform
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib2
import wintermute

def get_mirror(self):
    """ Status: Work in progress.
        Room for improvement: time download speed of /bandwidth file 
rather than socket time
        Search user ~/ for .s3itget-mirror file to use previously 
determined mirror.
        If it isn't found then do the following:
        Method will test against provided mirrors in class to find 
fastest mirror.
        Will leave token in active directory in home directory if temp 
not selected.
        If fails, defaults to Seattle.
        """
    home = os.path.expanduser('~')  # platform independent
    logger.debug('User home directory is: %s' % home)
    if os.path.exists(os.path.join(home, '.s3itget-mirror')) and 
self.mirror == 'False':
        with open(os.path.join(home, '.s3itget-mirror'), 'r') as 
mirror_file:
            mirror = mirror_file.readline().rstrip()
            logger.debug('Selected cached mirror: %s' % mirror)
            print 'Selected cached mirror: %s' % mirror
            return mirror

    elif self.mirror != 'False' and self.mirror is not None:
        logger.debug('Selected manual mirror: %s' % self.mirror)
        print 'Selected manual mirror: %s' % self.mirror
    else:
        # Splits urls into hostnames and "ping" test by timing port 
connect
        # Returns winner
        for x, mirror_con in enumerate(self.mirrors):
            try:
                time_before = time.time()
                benchmark = urllib2.urlopen(self.mirrors[x] + 
'benchmark')
                self.ping_times.append(time.time() - time_before)
            except urllib2.HTTPError, urllib2.URLError:
                self.ping_times.append(99)
                pass
            finally:
                logger.debug('Host: %s Performance: %s' % 
(self.mirrors[x], self.ping_times[x]))
                benchmark.close()
        # Return results
        # gets minimum index number from ping_times to ID the proper 
mirror from main list
        self.mirror = 
self.mirrors[self.ping_times.index(min(self.ping_times))]
        print 'Selected fastest mirror: %s' % self.mirror

    # Write to file
    logger.debug('Write mirror file to %s' % os.path.join(home, 
'.s3itget-mirror'))
    with open(os.path.join(home, '.s3itget-mirror'), 'w') as 
mirror_file:
        mirror_file.write(self.mirror + '\n')
    return self.mirror
