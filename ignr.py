#! /usr/bin/env python

import argparse, os, sys
import gitignoreio_api as api

def user_choice(query):
    while (True):
        choice = raw_input(query + " (y/n) ").lower()
        if choice in ['yes', 'y', 'yep', 'yup']:
           return True
        elif choice in ['no', 'n', 'nope', 'nah']:
           return False
        else:
           print "Please respond with 'y' or 'n'."

parser = argparse.ArgumentParser()

# Accept list instruction, search instruction, OR create instruction
task = parser.add_mutually_exclusive_group(required=True)
task.add_argument('--list', '-l', action='store_true', help='list all available .gitignore templates')
task.add_argument('--new', '-n', dest='n_stack', metavar='TECH', nargs='+', help='space-separated technologies - "macOS Node Sass"')
task.add_argument('--preview', '-p', dest='p_stack', metavar='TECH', nargs='+', help='preview for space-separated technologies')

args = parser.parse_args()

if args.list:
    template_list = api.get_template_list()
    print '\n'.join(template_list)

else:
    preview_needed = args.p_stack is not None
    gi_stack = args.p_stack or args.n_stack

    # Catch error raised by api and report
    try:
        ignr_file = api.get_gitignore(gi_stack)
    except ValueError as ve:
        print "ERROR: " + ve.args[0] + " is invalid or is not supported on gitignore.io."
        sys.exit(1)

    if preview_needed:
        print ignr_file

    else:
        if os.path.isfile('.gitignore'):
            overwrite = user_choice(".gitignore exists in current directory. Overwrite?")

            if overwrite is False:
                print "Ok. Exiting..."
                sys.exit(0)

            elif overwrite is True:
                if user_choice("Back up current .gitignore?") is True:
                    print "Backing up .gitignore as 'OLD_gitignore'..."
                    os.rename('.gitignore', 'OLD_gitignore')

        with open('.gitignore', 'w') as f:
            f.write("# File generated by ignr.py (github.com/Antrikshy/ignr)\n{0}".format(ignr_file))

        print "New .gitignore file generated for " + ", ".join(gi_stack) + "."

sys.exit(0)
