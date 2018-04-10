#!/usr/bin/python3
# Copyright (C) 2018 Evgeny Golyshev <eugulixes@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# The main motivation to create a substitution for du is that it can sometimes
# provide inaccurate result. For example, directory size may vary depending on
# when du is called -- before or after transferring the directory to an image.

import os
import sys
from optparse import OptionParser


def walk(path):
    """Recursively yields DirEntry objects for given directory. """
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from walk(entry.path)
        else:
            yield entry


def main():
    parser = OptionParser(usage='usage: %prog [options] <directory>')
    parser.add_option("-b", "--block-size", default=4096, type="int",
                      help="block size", metavar="SIZE")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    directory = args[0]

    total_size = items_number = 0

    # os.walk skips the symbolic links that resolve to directories, not
    # counting them at all. It has a great impact on the end result, so we need
    # a different way to solve the task.
    for dir_entry in walk(directory):
        items_number += 1

        if os.path.islink(dir_entry.path):
            total_size += options.block_size
        elif os.path.isfile(dir_entry.path):
            file_size = os.path.getsize(dir_entry.path)
            if file_size > options.block_size:
                total_size += file_size
            else:
                total_size += options.block_size

    print('Items number: {}'.format(items_number))
    print('Total size: {}'.format(total_size))


if __name__ == '__main__':
    main()
