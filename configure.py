#!/usr/bin/env python 

import os
import time
import argparse
from includes import utils
from includes import kubernetes

# Command line options 
parser = argparse.ArgumentParser(description='Proxy Configurator for Kubernetes')
parser.add_argument('-i', '--interval', default=5, help='Sampling interval')
parser.add_argument('-d', '--dryrun', default=False, help='Just show the output', action="store_true")
parser.add_argument('-v', '--verbose', default=False, help='Verbose mode', action="store_true")
parser.add_argument('-a', '--api-server', default="http://Kubernetes.api:8080", help='Kubernetes API server')
parser.add_argument('-c', '--command', default="./dosomething.sh", help='shell command to run in case of a change')
parser.add_argument('-p', '--proxy-type', default="haproxy", help="type of proxy to configure", choices=['haproxy', 'nginx'])
cliarguments = parser.parse_args()

if __name__ == '__main__':

    # First time running... run the script and sample
    currentMD5SUM, currentSERVICESMD5SUM = utils.utilities().checkMD5s(cliarguments)
    print("%s : Script started!" % time.strftime("%c"))

    utils.utilities().andAction(cliarguments)

    while True:
        currentTime = time.strftime("%c")
        
        newMD5SUM, newSERVICESMD5SUM = utils.utilities().checkMD5s(cliarguments)

        if (newMD5SUM not in currentMD5SUM) or (newSERVICESMD5SUM not in currentSERVICESMD5SUM):
            print("%s : Something Changed! Lets run the command: %s" % (currentTime, cliarguments.command))
            utils.utilities().andAction(cliarguments)

        newMD5SUM = currentMD5SUM
        newSERVICESMD5SUM = currentSERVICESMD5SUM

        time.sleep(cliarguments.interval)

        if cliarguments.verbose:
            print(currentTime, newMD5SUM, currentMD5SUM)
            print(currentTime, currentSERVICESMD5SUM, newSERVICESMD5SUM)
