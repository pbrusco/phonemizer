# coding: utf-8

# Copyright 2016 Thomas Schatz, Xuan Nga Cao, Mathieu Bernard
#
# This file is part of phonemizer: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Phonemizer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with phonemizer. If not, see <http://www.gnu.org/licenses/>.
"""Test of the phonemizer.Phonemizer class"""

import pytest
import tempfile
import shlex

from phonemizer.main import main


def _test(input, output, args=''):
    with tempfile.NamedTemporaryFile('w', delete=False) as finput:
        finput.write(input)
        finput.seek(0)

        with tempfile.NamedTemporaryFile('w+', delete=False) as foutput:
            opts = '{} -o {} {}'.format(finput.name, foutput.name, args)
            main(shlex.split(opts))
            assert foutput.read() == output + '\n'

def test_help():
    with pytest.raises(SystemExit):
        main('-h'.split())

def test_readme():
    _test(u'hello world', u'hhaxlow werld ')
    _test(u'hello world', u'hhaxlow werld', '--strip')
    _test(u'hello world',
          u'hh ax l ;esyll ow ;esyll ;eword w er l d ;esyll ;eword ',
          u"-p ' ' -s ';esyll ' -w ';eword '")

def test_njobs():
    for njobs in range(1, 4):
        _test(
            u'hello world\ngoodbye\nthird line\nyet another',
            u'hh-ax-l|ow w-er-l-d\ng-uh-d|b-ay\nth-er-d l-ay-n\n'
            u'y-eh-t ax-n|ah-dh|er',
            u'--strip -j {} -p "-" -s "|" -w " "'.format(njobs))
