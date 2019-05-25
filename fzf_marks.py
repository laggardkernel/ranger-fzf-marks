from __future__ import absolute_import, division, print_function
import os
from ranger.api.commands import Command


class fmark(Command):
    """
    :fmark
    Mark the current directory into fzf-marks file
    """

    def execute(self):
        from os.path import join, expanduser, exists
        from os import makedirs, linesep

        if not self.arg(1):
            self.fm.notify(
                "A keyword must be given for the current bookmark!", bad=True
            )
            return

        mark_file = expanduser("~/.config/ranger/fzf-marks")
        item = "{} : {}".format(self.arg(1), self.fm.thisdir.path)

        if not exists(mark_file):
            with open(mark_file, "a") as f:
                pass

        with open(mark_file, "r") as f:
            for line in f.readlines():
                if line.strip() == item:
                    self.fm.notify(
                        "** The following mark already exists **: {}".format(item),
                        bad=True,
                    )
                    return

        with open(mark_file, "a") as f:
            f.write("{}{}".format(item, linesep))
            self.fm.notify("** The following mark has been added **: {}".format(item))


class dmark(Command):
    """
    dmark: delete current directory from fzf-marks file
    """

    def execute(self):
        import subprocess
        from os.path import join, expanduser, exists
        from os import linesep
        from time import sleep

        mark_file = expanduser("~/.config/ranger/fzf-marks")
        items = None
        query = ""

        if self.arg(1):
            query = self.arg(1)

        if not exists(mark_file):
            self.fm.notify("No fzf-marks is created yet!", bad=True)
            return

        command = '< "{}" sort -f | fzf --height 60% \
            -m --ansi --bind=ctrl-y:accept,ctrl-t:toggle --query="{}"'.format(
            mark_file, query
        )

        process = self.fm.execute_command(
            command, universal_newlines=True, stdout=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            items = stdout.rstrip().split("\n")

        if not items:
            return

        with open(mark_file, "r") as f:
            lines = f.readlines()

        with open(mark_file, "w") as f:
            for line in lines:
                if line.strip() not in items:
                    f.write(line)

        self.fm.notify("fmarks deleted: {}".format(", ".join(items)))


class fzm(Command):
    """
    fzm: select and jump to bookmark stored in fzf-marks
    """

    def execute(self):
        import subprocess
        import os

        mark_file = os.path.expanduser("~/.config/ranger/fzf-marks")
        target = None
        query = ""

        if self.arg(1):
            query = self.arg(1)

        if not os.path.exists(mark_file):
            self.fm.notify("No fzf-marks is created yet!", bad=True)
            return

        command = '< "{}" sort -f | fzf --height 60% \
            +m --ansi --bind=ctrl-y:accept,ctrl-t:toggle --query="{}" --select-1'.format(
            mark_file, query
        )

        process = self.fm.execute_command(
            command, universal_newlines=True, stdout=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            key, target = stdout.rstrip().split(" : ", 1)
            target = os.path.expanduser(target)

        if not target:
            return
        elif os.path.isdir(target):
            self.fm.cd(target)
        else:
            self.fm.select_file(target)
