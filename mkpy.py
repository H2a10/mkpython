#!/Users/tali/v3.9.0.a5/bin/python3 
import sys,os
sys.path.append(os.path.expanduser("~/projects/mkpython"))
import argparse,ini,sets
parser=argparse.ArgumentParser()
parser.add_argument("-n","--proj-name",help="the projects name",required=True)
parser.add_argument("-c","--conf",help="configuration file",required=True)
parser.add_argument("-l","--location",help="project location",default=os.path.expanduser("~/projects"))
r=parser.parse_args()
ini.mkmkf(r.conf,r.location,r.proj_name)
