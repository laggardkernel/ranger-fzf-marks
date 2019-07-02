# Copyright 2019, laggardkernel and the ranger-fzf-marks contributors
# SPDX-License-Identifier: MIT

from __future__ import absolute_import, division, print_function
import os
from ranger.api.commands import Command


class fmark(Command):
    """
    :fmark
    Mark the current directory into fzf-marks file
    """

    def execute(self):
        if not self.arg(1):
            self.fm.notify(
                "A keyword must be given for the current bookmark!", bad=True
            )
            return

        mark_file = os.path.join(
            os.environ.get("HOME", os.path.expanduser("~")), ".fzf-marks"
        )
        mark_file = os.environ.get("FZF_MARKS_FILE", mark_file)
        item = "{} : {}".format(self.arg(1), self.fm.thisdir.path)

        if not os.path.exists(mark_file):
            with open(mark_file, "a") as f:
                pass

        with open(mark_file, "r") as f:
            for line in f.readlines():
                if line.split(":")[1].strip() == self.fm.thisdir.path:
                    self.fm.notify(
                        "Fzf bookmark already exists: {}".format(line.strip()), bad=True
                    )
                    return

        with open(mark_file, "a") as f:
            f.write("{}{}".format(item, os.linesep))
            self.fm.notify("Fzf bookmark has been added: {}".format(item))


class dmark(Command):
    """
    dmark: delete current directory from fzf-marks file
    """

    def execute(self):
        import subprocess

        mark_file = os.path.join(
            os.environ.get("HOME", os.path.expanduser("~")), ".fzf-marks"
        )
        mark_file = os.environ.get("FZF_MARKS_FILE", mark_file)
        items = None
        query = ""

        if self.arg(1):
            query = self.arg(1)

        if not os.path.exists(mark_file):
            self.fm.notify("No fzf bookmark is created yet!", bad=True)
            return

        # TODO: batch deletion
        command = '< "{}" sort -f | fzf --height 62% \
            -m --ansi --bind=ctrl-o:accept,ctrl-t:toggle --query="{}"'.format(
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

        self.fm.notify("Fzf bookmark is deleted: {}".format(", ".join(items)))


class fzm(Command):
    """
    fzm: select and jump to bookmark stored in fzf-marks
    """

    def execute(self):
        import subprocess

        mark_file = os.path.join(
            os.environ.get("HOME", os.path.expanduser("~")), ".fzf-marks"
        )
        mark_file = os.environ.get("FZF_MARKS_FILE", mark_file)
        target = None
        query = ""

        if self.arg(1):
            query = self.arg(1)

        if not os.path.exists(mark_file):
            self.fm.notify("No fzf bookmark is created yet!", bad=True)
            return

        command = '< "{}" sort -f | fzf --height 62% \
            +m --ansi --bind=ctrl-o:accept,ctrl-t:toggle --query="{}" --select-1'.format(
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
        elif os.path.isfile(target):
            self.fm.select_file(target)
        else:
            self.fm.notify(
                "Unavailable fzf bookmark location: {} : {}".format(key, target), True
            )
