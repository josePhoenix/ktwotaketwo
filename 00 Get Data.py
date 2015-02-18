from astropy.io import ascii
import requests
import os.path
import os
import sys
import errno
import subprocess

def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

targets = ascii.read('./targets.csv')

DOWNLOAD_CHUNK_BYTES = 1024

for target in targets:
    ensure_dir("./{}".format(target['Shortname']))
    filename = "./{}/{}_original.fits".format(target['Shortname'],
                                            target['Shortname'])
    if os.path.exists(filename):
        print "Already downloaded", target['URL']
        continue
    print "Downloading", target['URL']
    r = requests.get(target['URL'])
    with open(filename + '.gz', 'wb') as fd:
        for chunk in r.iter_content(DOWNLOAD_CHUNK_BYTES):
            fd.write(chunk)
    print "Un-gzipping..."
    subprocess.check_call(['gzip', '-d', filename])
    print "Done!"
