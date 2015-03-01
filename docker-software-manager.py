#!/usr/bin/python

import sys
import argparse
import os
import shutil
import subprocess
import pipes
from string import Template

# path of this script
basepath = os.path.dirname(os.path.realpath(__file__))

# define argument parser
parser = argparse.ArgumentParser(description="Docker software manager")
subparsers = parser.add_subparsers()

# subcommand install
def install(args):
    print "Installing tools"
    
    # install docker-gen
    print "[    ] Installing docker-gen",
    subprocess.call([os.path.join(basepath, 'docker-gen/update.sh')])
    subprocess.call([os.path.join(basepath, 'docker-gen/install.sh')])
    print "\r[done] Installing docker-gen"
    
    # install docker-compose
    print "[    ] Installing docker-compose",
    subprocess.call([os.path.join(basepath, 'docker-compose/update.sh')])
    subprocess.call([os.path.join(basepath, 'docker-compose/install.sh')])
    print "\r[done] Installing docker-compose"
    
    # install link to docker-software-manager
    print "[    ] Installing docker-software-manager",
    if not os.path.exists('/usr/local/bin/docker-software-manager'):
        command = ['ln', '-s', os.path.join(basepath, 'docker-software-manager.py'), '/usr/local/bin/docker-software-manager']
        subprocess.call(command)
    if not os.path.exists('/usr/local/bin/dsm'):
        command = ['ln', '-s', os.path.join(basepath, 'docker-software-manager.py'), '/usr/local/bin/dsm']
        subprocess.call(command)    
    print "\r[done] Installing docker-software-manager"    
    
parser_install = subparsers.add_parser('install')
parser_install.set_defaults(func=install)
    
# subcommand remove
def remove(args):
    print "Removing installed tools"
    
    # remove docker-gen
    print "[    ] Removing docker-gen",
    subprocess.call([os.path.join(basepath, 'docker-gen/remove.sh')])
    print "\r[done] Removing docker-gen"
    
    # remove docker-compose
    print "[    ] Removing docker-compose",
    subprocess.call([os.path.join(basepath, 'docker-compose/remove.sh')])
    print "\r[done] Removing docker-compose"
    
    # install link to docker-software-manager
    print "[    ] Removing docker-software-manager",
    if os.path.exists('/usr/local/bin/docker-software-manager'):
        subprocess.call(['rm', '/usr/local/bin/docker-software-manager'])
    if os.path.exists('/usr/local/bin/dsm'):
        subprocess.call(['rm', '/usr/local/bin/dsm'])
    print "\r[done] Removing docker-software-manager"

parser_remove = subparsers.add_parser('remove')
parser_remove.set_defaults(func=remove)

# subcommand list
def ls(args):
    software_list = [x for x in os.listdir(os.path.join(basepath, '../software/')) if os.path.isdir(os.path.join(basepath, '../software/', x))]
    
    if len(software_list):
        print "Existing software:"
        for x in software_list:
            print "- {0}".format(x)
    else:
        print "No software existing!"
    
parser_list = subparsers.add_parser('list')
parser_list.set_defaults(func=ls)

# helpers
def getTarget(name):
    return os.path.join(basepath, '../software/', name)

def isExisting(target):
    # check if software exists
    return os.path.exists(target)

# subcommand create
def create(args):
    target = getTarget(args.name)
    
    # check if software exists allready
    if isExisting(target):
        print "Software allready exists!"
        return
    
    # copy software template to software directory
    print "[    ] Copying software template",
    shutil.copytree(os.path.join(basepath, 'software-template/'), target)
    print "\r[done] Copying software template"
    
    # modify files with software name
    print "[    ] Modifying software template",
    with open(os.path.join(target, 'software.service'), "r+") as f:
        string = f.read() # read in file
        f.seek(0) # go back to start
        f.write(Template(string).substitute(name=args.name)) # write everything back
        f.close()
    
    with open(os.path.join(target, 'docker-compose.yml'), "r+") as f:
        string = f.read() # read in file
        f.seek(0) # go back to start
        f.write(Template(string).substitute(name=args.name)) # write everything back
        f.close()
        
    os.rename(os.path.join(target, 'software.service'), os.path.join(target, "{0}.service".format(args.name)))
    print "\r[done] Modifying software template"
    
    print "Software directory created"
    
parser_create = subparsers.add_parser('create')
parser_create.add_argument("name",
                    help="name of the software", metavar='name')
parser_create.set_defaults(func=create)
    
# subcommand activate
def activate(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        command = ['/bin/systemctl', 'enable', pipes.quote(os.path.join(target, "{0}.service".format(args.name)))]
        subprocess.call(command)
    else:
        print "Software does not exist!"
        
parser_activate = subparsers.add_parser('activate')
parser_activate.add_argument("name",
                    help="name of the software", metavar='name')
parser_activate.set_defaults(func=activate)

# subcommand deactivate        
def deactivate(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        command = ['/bin/systemctl', 'disable', pipes.quote(os.path.join(target, "{0}.service".format(args.name)))]
        subprocess.call(command)
    else:
        print "Software does not exist!"

parser_deactivate = subparsers.add_parser('deactivate')
parser_deactivate.add_argument("name",
                    help="name of the software", metavar='name')
parser_deactivate.set_defaults(func=deactivate)
   
# subcommand start
def start(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        command = ['/bin/systemctl', 'start', "{0}.service".format(args.name)]
        subprocess.call(command)
    else:
        print "Software does not exist!"

parser_start = subparsers.add_parser('start')
parser_start.add_argument("name",
                    help="name of the software", metavar='name')
parser_start.set_defaults(func=start)
        
# subcommand stop
def stop(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        command = ['/bin/systemctl', 'stop', "{0}.service".format(args.name)]
        subprocess.call(command)
    else:
        print "Software does not exist!"
        
parser_stop = subparsers.add_parser('stop')
parser_stop.add_argument("name",
                    help="name of the software", metavar='name')
parser_stop.set_defaults(func=stop)
        
# subcommand status
def status(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        command = ['/bin/systemctl', 'status', "{0}.service".format(args.name)]
        subprocess.call(command)
    else:
        print "Software does not exist!"
        
parser_status = subparsers.add_parser('status')
parser_status.add_argument("name",
                    help="name of the software", metavar='name')
parser_status.set_defaults(func=status)
        
# subcommand ps
def ps(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        command = ['docker-compose', '-f', pipes.quote(os.path.join(target, "docker-compose.yml")), '-p', args.name, 'ps']
        subprocess.call(command)
    else:
        print "Software does not exist!"
        
parser_ps = subparsers.add_parser('ps')
parser_ps.add_argument("name",
                    help="name of the software", metavar='name')
parser_ps.set_defaults(func=ps)

# subcommand kill
def kill(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        command = ['docker-compose', '-f', pipes.quote(os.path.join(target, "docker-compose.yml")), '-p', args.name, 'kill']
        subprocess.call(command)
    else:
        print "Software does not exist!"

parser_kill = subparsers.add_parser('kill')
parser_kill.add_argument("name",
                    help="name of the software", metavar='name')
parser_kill.set_defaults(func=kill)
        
# subcommand logs
def logs(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        command = ['docker-compose', '-f', pipes.quote(os.path.join(target, "docker-compose.yml")), '-p', args.name, 'logs']
        subprocess.call(command)
    else:
        print "Software does not exist!"

parser_logs = subparsers.add_parser('logs')
parser_logs.add_argument("name",
                    help="name of the software", metavar='name')
parser_logs.set_defaults(func=logs)

# subcommand edit
def edit(args):
    target = getTarget(args.name)
    
    # check if software exists
    if isExisting(target):
        editor = os.environ.get('EDITOR','vi')
        command = [editor, pipes.quote(os.path.join(target, "docker-compose.yml"))]
        subprocess.call(command)
    else:
        print "Software does not exist!"

parser_edit = subparsers.add_parser('edit')
parser_edit.add_argument("name",
                    help="name of the software", metavar='name')
parser_edit.set_defaults(func=edit)

# parse given arguments
args = parser.parse_args()
args.func(args)
