'''tools.py - Contains various helper functions.'''

import os
import sys
import re
import gc
import bisect
import operator
import math
import io
from functools import reduce

if sys.version_info < (3, 7):
    from importlib_resources import files
else:
    from importlib.resources import files

ROOTPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_PORTABLE_MODE = []
_NOGUI = []
NUMERIC_REGEXP = re.compile(r'\d+[.]{1}\d+|\d+|\D+')  # Split into float, int, and characters
PREFIXED_BYTE_UNITS = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')


def cmp(x, y):
    if x > y:
        return 1
    if x < y:
        return -1
    return 0


def alphanumeric_sort(filenames):
    '''Do an in-place alphanumeric sort of the strings in <filenames>,
    such that for an example "1.jpg", "2.jpg", "10.jpg" is a sorted
    ordering.
    '''

    def _isfloat(p):
        try:
            return 0, float(p)
        except ValueError:
            return 1, p.lower()

    def keyfunc(s):
        s, e = os.path.splitext(s)
        if e[1:].isdigit():  # extension with only digital is not extension
            s += e
            e = ''
        return [_isfloat(p) for p in (*NUMERIC_REGEXP.findall(s), e)]

    filenames.sort(key=keyfunc)


def alphanumeric_compare(s1, s2):
    ''' Compares two strings by their natural order (i.e. 1 before 10)
    and returns a result comparable to the cmp function.
    @return: 0 if identical, -1 if s1 < s2, +1 if s1 > s2. '''
    if s1 is None:
        return 1
    elif s2 is None:
        return -1

    stringparts1 = NUMERIC_REGEXP.findall(s1.lower())
    stringparts2 = NUMERIC_REGEXP.findall(s2.lower())
    for i, part in enumerate(stringparts1):
        if part.isdigit():
            stringparts1[i] = 0, int(part)
        else:
            stringparts1[i] = 1, part
    for i, part in enumerate(stringparts2):
        if part.isdigit():
            stringparts2[i] = 0, int(part)
        else:
            stringparts2[i] = 1, part

    return cmp(stringparts1, stringparts2)


def bin_search(lst, value):
    ''' Binary search for sorted list C{lst}, looking for C{value}.
    @return: List index on success. On failure, it returns the 1's
    complement of the index where C{value} would be inserted.
    This implies that the return value is non-negative if and only if
    C{value} is contained in C{lst}. '''

    index = bisect.bisect_left(lst, value)
    if index != len(lst) and lst[index] == value:
        return index
    else:
        return ~index


def get_home_directory():
    '''Return the path to the MComix home directory.
    In portable mode, it is 'profile' in the same directory with mcomixstarter.py.
    In Windows, it is %APPDATA%/MComix if not in portable mode.
    In UNIX, it is $HOME if not in portable mode.
    '''
    if is_portable_mode():
        # multiple profiles, maybe :)
        return os.path.join(rootdir(), 'profile')
    if sys.platform == 'win32':
        return os.path.join(os.environ.get('APPDATA'), 'MComix')
    else:
        return os.environ.get('HOME')


def get_config_directory():
    '''Return the path to the MComix config directory.
    It is get_home_directory()/.config/mcomix if in portable mode.
    If not in portable mode, it will be $XDG_CONFIG_HOME/mcomix,
    or get_home_directory()/.config/mcomix if $XDG_CONFIG_HOME is empty.

    See http://standards.freedesktop.org/basedir-spec/latest/ for more
    information on the $XDG_CONFIG_HOME environmental variable.
    '''
    prefix = os.path.join(get_home_directory(), '.config')
    # always using get_home_directory() even if in unix
    if not is_portable_mode():
        prefix = os.environ.get('XDG_CONFIG_HOME', prefix)
    return os.path.join(prefix, 'mcomix')


def get_data_directory():
    '''Return the path to the MComix data directory.
    It is get_home_directory()/.local/share/mcomix if in portable mode.
    If not in portable mode, it will be $XDG_DATA_HOME/mcomix,
    or get_home_directory()/.local/share/mcomix if $XDG_DATA_HOME is empty.

    See http://standards.freedesktop.org/basedir-spec/latest/ for more
    information on the $XDG_DATA_HOME environmental variable.
    '''
    prefix = os.path.join(get_home_directory(), '.local/share')
    if not is_portable_mode():
        prefix = os.environ.get('XDG_DATA_HOME', prefix)
    return os.path.join(prefix, 'mcomix')


def get_thumbnails_directory():
    '''Return the path to the thumbnail cache directory.
    It is get_home_directory()/.cache/.thumbnails/normal if in portable mode.
    If not in portable mode, it will be $XDG_CACHE_HOME/thumbnails/normal,
    or get_home_directory()/.cache/.thumbnails/normal if $XDG_CACHE_HOME is empty.

    See http://standards.freedesktop.org/basedir-spec/latest/ for more
    information about the $XDG_CACHE_HOME environmental variable.
    '''
    prefix = os.path.join(get_home_directory(), '.cache')
    if not is_portable_mode():
        prefix = os.environ.get('XDG_CACHE_HOME', prefix)
    return os.path.join(prefix, 'thumbnails/normal')


def number_of_digits(n):
    if 0 == n:
        return 1
    return int(math.log10(abs(n))) + 1


def format_byte_size(n):
    s = 0
    while n >= 1024:
        s += 1
        n /= 1024.0
    try:
        e = PREFIXED_BYTE_UNITS[s]
    except IndexError:
        e = 'C{}i'.format(s)
    return '{:.3f} {}'.format(n, e)


def garbage_collect():
    ''' Runs the garbage collector. '''
    gc.collect(0)


def rootdir():
    # return path contains mcomixstarter.py
    return ROOTPATH


def is_portable_mode():
    # check if running in portable mode
    if not _PORTABLE_MODE:
        portable_file = os.path.join(rootdir(), 'portable.txt')
        _PORTABLE_MODE.append(os.path.exists(portable_file))
        if _PORTABLE_MODE[0]:
            # chdir to rootdir early
            os.chdir(rootdir())
    return _PORTABLE_MODE[0]


def nogui():
    _NOGUI.append(0)


def use_gui():
    return not bool(_NOGUI)


def splitpath(path):
    # split path to a list of every level
    # use os.path.join(*pathlist) to convert such list into path
    pathname = os.path.normpath(path)
    pathlist = [pathname]
    while True:
        dirname, basename = os.path.split(pathlist[0])
        if not (dirname and basename):
            break
        pathlist[0:1] = dirname, basename
    return pathlist


def walkpath(root=None):
    # yield tuple of splited relative path of files in root
    # or current directory if root is None
    for name in os.listdir(root):
        path = os.path.join(root or '', name)
        if os.path.isdir(path):
            yield from map(lambda s: (name, *s), walkpath(path))
        else:
            yield name,


def relpath2root(path, abs_fallback=False):
    # return relative path to rootdir in portable mode
    # if path is not under the same mount point where rootdir placed
    # return abspath of path if abs_fallback is True, else None
    # but, always return absolue path if not in portable mode

    # ATTENTION:
    # avoid using os.path.relpath without checking mount point in win32
    # it will raise ValueError if path has a different driver letter
    # (see source code of ntpath.relpath)

    path = os.path.abspath(path)
    if not is_portable_mode():
        return path

    pathmp = os.path.dirname(path)
    while not os.path.ismount(pathmp):
        pathmp = os.path.dirname(pathmp)

    rootmp = rootdir()
    while not os.path.ismount(rootmp):
        rootmp = os.path.dirname(rootmp)

    if pathmp == rootmp:
        return os.path.relpath(path)
    return path if abs_fallback else None


def open_binary(*args):
    return files(__package__).joinpath(os.path.join(*args)).open(mode='rb')


def read_binary(*args):
    return files(__package__).joinpath(os.path.join(*args)).read_bytes()


def div(a, b):
    return float(a) / float(b)


def volume(t):
    return reduce(operator.mul, t, 1)


def relerr(approx, ideal):
    return abs(div(approx - ideal, ideal))


def smaller(a, b):
    ''' Returns a list with the i-th element set to True if and only the i-th
    element in a is less than the i-th element in b. '''
    return map(operator.lt, a, b)


def smaller_or_equal(a, b):
    ''' Returns a list with the i-th element set to True if and only the i-th
    element in a is less than or equal to the i-th element in b. '''
    return list(map(operator.le, a, b))


def scale(t, factor):
    return [x * factor for x in t]


def vector_sub(a, b):
    ''' Subtracts vector b from vector a. '''
    return tuple(map(operator.sub, a, b))


def vector_add(a, b):
    ''' Adds vector a to vector b. '''
    return tuple(map(operator.add, a, b))


def vector_opposite(a):
    ''' Returns the opposite vector -a. '''
    return tuple(map(operator.neg, a))

# vim: expandtab:sw=4:ts=4
