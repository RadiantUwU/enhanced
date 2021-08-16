# enhanced - Adds new features to python
#
# Copyright (c) 2021-2021 Radiant <stefan.i.davidoiu@gmail.com>
#
# This program is dual licensed under GPLv3 and MIT.
#
# GPLv3
# -----
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

psutil = None
# noinspection PyUnresolvedReferences
import builtins
import copy
import json
import traceback
# noinspection PyUnresolvedReferences
from types import FunctionType, MethodType, ModuleType
from typing import Any, List, Tuple, Iterator, Union
import forbiddenfruit
import gc
import time
import inspect
import ctypes
import threading
import multiprocessing
import weakref
import sys
import socket
import pickle
import os
from time import sleep as wait_seconds


# noinspection PyUnusedLocal
def passkw(*args, **kwargs):
    pass


def alwaysreturn(var: Any):
    thevar = var

    # noinspection PyUnusedLocal
    def returner(*args, **kwargs):
        return thevar

    return returner


dict_keys = type(dict().keys())
dict_values = type(dict().values())
function = FunctionType
module = ModuleType
IpAddress = Tuple[str, int]


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        pass
    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


class CString:
    """Array of characters"""

    def __new__(cls, string: str, length: int = None):
        """Converts python string to C string."""
        if length is None:
            ch = (ctypes.c_char * len(string))()
            ch.value = string.encode()
            return ch
        else:
            ch = (ctypes.c_char * int(length))()
            ch.value = string.encode()
            return ch


class CacherMap:
    def __init__(self) -> None:
        self.map = {}

    def __setitem__(self, key, value) -> None:
        self.map[key] = value

    def __getitem__(self, key) -> None:
        return self.map[key]

    def clear(self) -> None:
        self.map.clear()

    def keys(self) -> dict_keys:
        return self.map.keys()


# noinspection PyNoneFunctionAssignment
class Cacher:
    def __init__(self, **kwargs):
        self.cached = CacherMap()
        self.funct = passkw
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def __getitem__(self, num, memcap=True):
        if memcap:
            try:
                checkMem(500, False, False)
            except MemoryError:
                self.flush()
                checkMem(500)
        if not num in self.cached.keys():
            self.cached[num] = self.funct(num)
        return self.cached[num]

    def __call__(self, num, memcap=True):
        return self.__getitem__(num, memcap)

    def flush(self):
        self.cached.clear()


class MathMisc:
    @staticmethod
    def isprime(n) -> bool:
        f = True
        for i in range(2, n - 1):
            if (n % i) == 0:
                f = False
                break
        return f

    @staticmethod
    def primen(a) -> int:
        n = 2
        b = a
        while b != 0:
            if MathMisc.isprime(n):
                b -= 1
            n += 1
        return n - 1

    @staticmethod
    def spliexpb(a) -> list:
        thelist = []
        b = a
        while b != 1:
            n = 1
            while True:
                if (b % primenum[n]) == 0:
                    break
                n += 1
            b = b // primenum[n]
            thelist.append(primenum[n])
        return thelist

    @staticmethod
    def gcd(x, y) -> int:
        while y:
            x, y = y, x % y
        return x

    @staticmethod
    def cmmdc(*args) -> int:
        x = args[0]
        for i in args:
            x = MathMisc.gcd(x, i)
            if x == 1:
                break
        return x

    @staticmethod
    def lcm(x, y):
        return x * y // MathMisc.gcd(x, y)

    @staticmethod
    def union(*args) -> list:
        c = set(args[0])
        for i in args:
            if i == args[0]:
                continue
            c |= set(i)
        return list(c)

    @staticmethod
    def comparebothhave(*args) -> list:
        a = args[0].copy()
        for arg in args:
            a = list(set(a).intersection(arg))
        return a

    @staticmethod
    def difference(*args) -> list:
        c = set(args[0])
        for i in args:
            if i == args[0]:
                continue
            c -= set(i)
        return list(c)

    @staticmethod
    def symdif(*args) -> list:
        c = set(args[0])
        for i in args:
            if i == args[0]:
                continue
            c ^= set(i)
        return list(c)

    @staticmethod
    def cmmmc(*args) -> int:
        x = args[0]
        for i in args:
            x = MathMisc.lcm(x, i)
        return x


primenum = Cacher(funct=MathMisc.primen)


# noinspection PyUnresolvedReferences
class Fraction:
    pass


# noinspection PyRedeclaration
class Fraction:
    def __init__(self, n, div) -> None:
        self.n = n
        self.div = div

    def tofloat(self) -> float:
        try:
            return float(self.n / self.div)
        except ZeroDivisionError:
            return float('inf')

    def __add__(self, other):
        if type(other) == int:
            return Fraction((self.n + other * self.div), self.div)
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div, other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return Fraction((self.n * mymult + other.n * urmult), mult)
        elif type(other) == float:
            f = other.as_integer_ratio()
            f = Fraction(f[0], f[1]).simplify()
            mult = MathMisc.cmmmc(self.div, f.div)
            mymult = mult // self.div
            urmult = mult // f.div
            return Fraction((self.n * mymult + f.n * urmult), mult)
        else:
            raise TypeError

    def __sub__(self, other):
        if type(other) == int:
            return Fraction((self.n - other * self.div), self.div)
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div, other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return Fraction((self.n * mymult - other.n * urmult), mult)
        elif type(other) == float:
            f = other.as_integer_ratio()
            f = Fraction(f[0], f[1]).simplify()
            mult = MathMisc.cmmmc(self.div, f.div)
            mymult = mult // self.div
            urmult = mult // f.div
            return Fraction((self.n * mymult - f.n * urmult), mult)
        else:
            raise TypeError

    def __mult__(self, other):
        if type(other) == int:
            return Fraction((self.n * other), self.div)
        elif type(other) == type(self):
            return Fraction((self.n * other.n), self.div * other.div).simplify()
        elif type(other) == float:
            f = other.as_integer_ratio()
            f = Fraction(f[0], f[1]).simplify()
            return Fraction((self.n * f.n), self.div * f.div).simplify()
        else:
            raise TypeError

    def __truediv__(self, other):
        if type(other) == int:
            return Fraction(self.n, (self.div * other))
        elif type(other) == type(self):
            return Fraction((self.n * other.div), (self.div * other.n)).simplify()
        elif type(other) == float:
            f = other.as_integer_ratio()
            f = Fraction(f[0], f[1]).simplify()
            return Fraction((self.n * f.div), self.div * f.n).simplify()
        else:
            raise TypeError

    def copy(self) -> Fraction:
        return Fraction(self.n, self.div)

    def simplify(self) -> Fraction:
        d = self.div
        n = self.n
        c = MathMisc.cmmdc(d, n)
        d = d // c
        n = n // c
        self.div = d
        self.n = n
        return self

    def __eq__(self, other):
        if type(other) == int or type(other) == float:
            return self.tofloat() == other
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div, other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return (self.n * mymult) == (other.n * urmult)
        else:
            raise TypeError

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if type(other) == int or type(other) == float:
            return self.tofloat() < other
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div, other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return (self.n * mymult) < (other.n * urmult)
        else:
            raise TypeError

    def __gt__(self, other):
        if type(other) == int or type(other) == float:
            return self.tofloat() > other
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div, other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return (self.n * mymult) > (other.n * urmult)
        else:
            raise TypeError

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)

    def __pow__(self, other):
        if type(other) == int or type(other) == float:
            a = Fraction(self.n ** other, self.div ** other).tofloat().as_integer_ratio()
            return Fraction(a[0], a[1]).simplify()
        elif type(other) == type(self):
            a = Fraction(((self.n ** other.n) ** (1 / other.div)),
                         ((self.div ** other.n) ** (1 / other.div))).tofloat().as_integer_ratio()
            return Fraction(a[0], a[1]).simplify()
        else:
            raise TypeError

    def __str__(self):
        return str(self.n) + '/' + str(self.div)

    def __repr__(self):
        return 'Fraction(' + str(self.n) + ',' + str(self.div) + ')'


def waituntil(cond: str, local_vars=None, interval: int = 0.01):
    if local_vars is None:
        local_vars = {}
    while not eval(cond, local_vars):
        time.sleep(interval)


@forbiddenfruit.curses(dict, 'index')
def index_dict(self, value) -> Any:
    if value in self.values():
        return list(self.keys())[list(self.values()).index(value)]
    else:
        raise IndexError("Key with value " + str(value) + " does not exist.")


@forbiddenfruit.curses(dict, 'hash')
def hash_dict(self) -> int:
    return hash(json.dumps(copy.deepcopy(self), sort_keys=True))


def forcedeallocate(obj: object) -> None:
    """Forces deallocation on object."""
    e = ctypes.py_object(obj)
    for _ in range(sys.getrefcount(obj) - 3): pythonapi.Py_DecRef(e)


def partial_delete(self, log=False) -> int:
    ref = gc.get_referrers(self)
    immuttables = (tuple, str, type(dict().keys()), type(dict().values()), set, frozenset)
    for i in ref:
        if not inspect.isframe(i):
            if type(i) in immuttables:
                ty = type(i)
                f = list(i)
                f.remove(self)
                f = ty(f)
                for j in gc.get_referrers(i):
                    try:
                        partial_update_obj(j, i, f)
                    except Exception:
                        if log:
                            printError()
            else:
                if type(i) == dict:
                    if '__holddestroyedobjects' in i.keys():
                        if i['__holddestroyedobjects']:
                            pass
                        else:
                            try:
                                del i[i.index(self)]
                            except Exception:
                                if log:
                                    printError()
                    else:
                        try:
                            del i[i.index(self)]
                        except Exception:
                            if log:
                                printError()
                elif type(i) == list:
                    try:
                        i.remove(self)
                    except:
                        if log:
                            printError()
        else:
            pass
    return sys.getrefcount(self) - 2


def update_obj(obj, old, new):
    immuttables = (tuple, str, type(dict().keys()), type(dict().values()), set, frozenset)
    if type(obj) in immuttables:
        ty = type(obj)
        f = list(obj)
        f[f.index(old)] = new
        f = ty(f)
        for j in gc.get_referrers(obj):
            update_obj(j, obj, f)
    else:
        if type(obj) == dict or type(obj) == list:
            obj[obj.index(old)] = new


def partial_update_obj(obj, old, new, log=False):
    immuttables = (tuple, str, type(dict().keys()), type(dict().values()), set, frozenset)
    if type(obj) in immuttables:
        try:
            ty = type(obj)
            f = list(obj)
            f[f.index(old)] = new
            f = ty(f)
            for j in gc.get_referrers(obj):
                partial_update_obj(j, obj, f)
        except Exception:
            if log:
                printError()
    else:
        if type(obj) == dict or type(obj) == list:
            try:
                obj[obj.index(old)] = new
            except Exception:
                if log:
                    printError()


def getError():
    return traceback.format_exc()


class enhancedobject:
    pass


class AlreadyInitializedWarning(RuntimeWarning):
    pass


class terminalcolors:
    magenta = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    reset = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    colors = ['\033[0m', '\033[94m', '\033[92m', '\033[96m', '\033[91m', '\033[95m', '\033[93m', '\033[0m\033[1m']
    types = ['\033[0m', '\033[1m', '\033[4m', '\033[1m\033[4m']
    colortest = ""
    typetest = ""
    for i in range(len(colors)):
        colortest += colors[i]
        colortest += str(i)
    colortest += types[0]
    for i in range(len(types)):
        typetest += types[i]
        typetest += str(i)
        typetest += types[0]

    @staticmethod
    def rgbcolor(r: int, g: int, b: int, isfg: bool = True):
        return f"\x1b[{('38' if isfg else '48')};2;{str(r)};{str(g)};{str(b)}m"


# noinspection PyRedeclaration,PyUnresolvedReferences,PyAttributeOutsideInit
class enhancedobject(object):
    def __new__(cls, *args, **kwargs) -> enhancedobject:
        self = object.__new__(cls)
        self.__initialized = False
        self.__preinitialized = False
        self.__deleted = False
        self.deleted = False
        cls.onpreinit(self, *args, **kwargs)
        self.__preinitialized = True
        return self

    def __init__(self, *args, **kwargs) -> None:
        self.oninit(*args, **kwargs)
        self.__initialized = True

    def __hash__(self) -> int:
        return hash(json.dumps(copy.deepcopy(self.__dict__), sort_keys=True))

    def __eq__(self, other: object) -> bool:
        if self.__class__.__mro__[-2] is other.__class__.__mro__[-2]:
            return hash(self) == hash(other)
        else:
            return False

    def __repr__(self) -> str:
        if self.__initialized:
            return "<" + str(self.__class__).replace("<class '", "").replace("'>", "") + ' enhancedobject at 0x' + (
                    "0" * (16 - len(hex(id(self)).replace("0x", "").upper())) + hex(id(self)).replace("0x",
                                                                                                      "").upper()) + ">"
        else:
            return "<" + str(self.__class__).replace("<class '", "").replace("'>",
                                                                             "") + ' enhancedobject(uninitialized) at 0x' + (
                           "0" * (16 - len(hex(id(self)).replace("0x", "").upper())) + hex(id(self)).replace("0x",
                                                                                                             "").upper()) + ">"

    def __str__(self) -> str:
        return self.__repr__()

    def shallowCopy(self) -> enhancedobject:
        """Shallowcopy the object"""
        return copy.copy(self)

    def deepCopy(self) -> enhancedobject:
        """Deepcopy the object"""
        return copy.deepcopy(self)

    def equals(self, other: object) -> bool:
        """Checks if an object is equal to the other."""
        if self.__class__.__mro__[-2] is other.__class__.__mro__[-2]:
            return hash(self) == hash(other)
        else:
            return False

    def toString(self) -> str:
        """Stringifies the object."""
        return self.__str__()

    @classmethod
    def getInheritances(cls) -> tuple:
        """Returns the inheritances of the object, the last, being builtins.object"""
        return cls.__mro__

    def __ne__(self, other: enhancedobject) -> bool:
        return not self.__eq__(other)

    @classmethod
    def headlessnew(cls, *args, **kwargs) -> enhancedobject:
        """Returns an uninitialized instance of this class."""
        return cls.__new__(cls, *args, **kwargs)

    def onpreinit(self, *args, **kwargs) -> None:
        pass

    def oninit(self, *args, **kwargs) -> None:
        pass

    @classmethod
    def new(cls, *args, **kwargs) -> enhancedobject:
        """Returns an initialized instance of this class."""
        obj = cls.__new__(*args, **kwargs)
        if isinstance(obj, cls):
            obj.init(*args, **kwargs)
        return obj

    def init(self, *args, **kwargs) -> None:
        """Initializes the object, if its already initialized, throws a Warning"""
        if not self.__initialized:
            self.__init__(*args, **kwargs)
        else:
            raise AlreadyInitializedWarning

    def ondelete(self, deletedalready=False) -> None:
        pass

    def ongcdelete(self) -> None:
        pass

    def delete(self, force=False) -> int:
        if not self.__deleted:
            self.ondelete()
        ref = gc.get_referrers(self)
        immuttables = (tuple, str, type(dict().keys()), type(dict().values()), set, frozenset)
        for i in ref:
            if not inspect.isframe(i):
                if type(i) in immuttables:
                    ty = type(i)
                    f = list(i)
                    f.remove(self)
                    f = ty(f)
                    for j in gc.get_referrers(i):
                        update_obj(j, i, f)
                else:
                    if type(i) == dict:
                        if '__holddestroyedobjects' in i.keys():
                            if i['__holddestroyedobjects']:
                                pass
                            else:
                                del i[i.index(self)]
                        else:
                            del i[i.index(self)]
                    elif type(i) == list:
                        i.remove(self)
            else:
                pass
        self.__deleted = True
        self.deleted = True
        if force:
            self.forcedel()
            return -1
        return sys.getrefcount(self) - 2

    def hash(self) -> int:
        """Returns object's hash."""
        return hash(self)

    def getReferences(self) -> list:
        """Gets the references of the object."""
        return gc.get_referrers(self)

    def __del__(self) -> None:
        if not self.__deleted:
            self.ondelete(True)
            self.__deleted = True
            self.deleted = True
        self.ongcdelete()

    def getActiveReferencesCount(self) -> int:
        """Returns active references"""
        e = self.getReferences()
        for i in e:
            if inspect.isframe(i):
                e.remove(i)
        return len(e)

    def getReferenceCount(self) -> Tuple[int, int]:
        """Returns reference count from the sys module.
        0th position in tuple is total references
        1st position in tuple is active references"""
        return sys.getrefcount(self) - 3, self.getActiveReferencesCount()

    def getWeakReferenceCount(self) -> int:
        """Returns weak reference count from the sys module."""
        return weakref.getweakrefcount(self)

    def getWeakReferences(self) -> list:
        """Gets the weak references of the object."""
        return weakref.getweakrefs(self)

    def getWeakRef(self) -> weakref.ReferenceType:
        """Returns a weak reference of the object."""
        return weakref.ref(self)

    def inc_ref(self) -> None:
        """Tells the system that another reference of this object has been made."""
        ctypes.pythonapi.Py_IncRef(ctypes.py_object(self))

    def dec_ref(self) -> None:
        """Tells the system that a reference of this object has been deleted.\n
        When there are no active references of this object, this object will be deallocated.\n
        After it has been deallocated, ANY interactions with this deleted object will CRASH python."""
        ctypes.pythonapi.Py_DecRef(ctypes.py_object(self))

    def forcedel(self) -> None:
        """This function is highly unstable and crashes python all the time. Its recommended to use the normal delete(True) instead."""
        e = ctypes.py_object(self)
        for _ in range(self.getReferenceCount()[0]): pythonapi.Py_DecRef(e)


class AttributableObject(enhancedobject):
    def __init__(self, thedict=None):
        """Makes a new attributable object from the dictionary"""
        super().__init__()
        if thedict is None:
            thedict = {}
        for i in thedict.keys():
            if not (i.startswith("__") and i.endswith("__")):
                setattr(self, i, thedict[i])


class unfrozentuple(enhancedobject):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if len(args) == 1:
            self.thetuple: Tuple[Any] = args[0]
        else:
            self.thetuple: Tuple[Any] = tuple(args)

    def __repr__(self) -> str:
        return "unfrozentuple" + str(self.thetuple)

    def __len__(self) -> int:
        return len(self.thetuple)

    def __getitem__(self, key: int) -> Any:
        return self.thetuple[key]

    def __setitem__(self, key: int, value: Any) -> None:
        f = list(self.thetuple)
        f[key] = value
        self.thetuple = tuple(f)

    def toTuple(self) -> tuple:
        return self.thetuple

    def __iter__(self) -> Iterator:
        return iter(self.thetuple)

    def __delitem__(self, key: int) -> None:
        f = list(self.thetuple)
        del f[key]
        self.thetuple = tuple(f)

    def freeze(self):
        replace_all(self, self.toTuple())

    def __getslice__(self, i: int, j: int) -> Tuple[Any]:
        return self.thetuple[i:j]

    def __setslice__(self, i: int, j: int, val: Tuple[Any]) -> None:
        f = list(self.thetuple)
        f[i:j] = list(tuple(val))
        self.thetuple = tuple(f)

    def __delslice__(self, i: int, j: int) -> None:
        f = list(self.thetuple)
        del f[i:j]
        self.thetuple = tuple(f)

    def __contains__(self, obj) -> bool:
        return obj in self.thetuple

    def __hash__(self) -> int:
        return hash(self.thetuple)

    def count(self, val: Any) -> int:
        return self.thetuple.count(val)

    def index(self, val: Any) -> int:
        return self.thetuple.index(val)


def printError():
    print(terminalcolors.red + traceback.format_exc() + terminalcolors.reset)
    return terminalcolors.red + traceback.format_exc() + terminalcolors.reset


class Shell:
    def __init__(self) -> None:
        self.running = False
        self.locals = {'self': self, 'exit': self.exit}
        self.isolglobals = {}
        self.globals = globals()
        self.__isolated = False
        self.__isolpass = "XcZq"
        self.canexitisol = True
        self.__isolexitstage = 0

    def run(self, globalss=None) -> None:
        if globalss is None:
            globalss = {}
        self.running = True
        self.globals = globalss
        while self.running:
            try:
                self.shellc(input('>>> '))
            except KeyboardInterrupt:
                print('')
                printError()

    def shellc(self, c) -> Union[None, ValueError, Exception]:
        """Runs command as if it was ran in a shell"""
        if c == ">EXITISOL<" and self.canexitisol and self.__isolated:
            try:
                self.exitisol(input('Password:'))
                return None
            except ValueError as e:
                print("Invalid password!")
                return e
        else:
            try:
                try:
                    if self.__isolated:
                        print(eval(c, {**self.isolglobals, "globals": alwaysreturn(self.isolglobals)}, self.locals))
                    else:
                        print(eval(c, self.globals, self.locals))
                except SyntaxError:
                    if self.__isolated:
                        exec(c, {**self.isolglobals, "globals": alwaysreturn(self.isolglobals)}, self.locals)
                    else:
                        exec(c, self.globals, self.locals)
                return None
            except Exception as e:
                printError()
                return e

    def runc(self, c) -> Union[None, Exception, ValueError]:
        """Runs command"""
        if self.__isolexitstage == 0:
            if c == ">EXITISOL<" and self.canexitisol and self.__isolated:
                self.__isolexitstage = 1
            else:
                try:
                    c = c.replace("locals()", str(self.locals))
                    if self.__isolated:
                        c = c.replace("globals()", str(self.isolglobals))
                        exec(c, self.isolglobals, self.locals)
                    else:
                        exec(c, self.globals, self.locals)
                    return None
                except Exception as e:
                    printError()
                    return e
        else:
            try:
                self.exitisol(c)
                return None
            except ValueError as e:
                print("Invalid password!")
                return e

    def enterisol(self, passwrd="XcZq", eraselocals=False) -> None:
        """Enters isolation, sets password to argument1.
        During isolated mode, you cannot access the self variable, and globals.
        Argument2 specifies if it will delete all local variables, default false."""
        self.__isolated = True
        self.__isolpass = passwrd
        try:
            if not eraselocals:
                while True:
                    del self.locals[self.locals.index(self)]
            else:
                self.locals.clear()
        except IndexError:
            pass
        try:
            if not eraselocals:
                while True:
                    del self.locals[self.locals.index(self.exit)]
            else:
                self.locals.clear()
        except IndexError:
            pass

    def exitisol(self, passwrd="") -> None:
        """Exits isolation, argument must be a correct password otherwise it will raise ValueError"""
        if passwrd == "":
            passwrd = "XcZq"
        if passwrd == self.__isolpass:
            self.__isolated = False
            self.locals['self'] = self
        else:
            raise ValueError("Password is incorrect!")

    def exit(self) -> None:
        self.running = False


def replace_all(old: object, new: object):
    e = gc.get_referrers(old)
    for i in e:
        update_obj(i, old, new)


def isolated_exec(code: str, global_vars=None, local_vars=None):
    if local_vars is None:
        local_vars = {}
    if global_vars is None:
        global_vars = {}
    shl = Shell()
    shl.enterisol("", True)
    shl.locals = local_vars
    shl.isolglobals = global_vars
    shl.canexitisol = False
    return shl.runc(code)


def print_color(string: str, color: int = 0, thetype: int = 0, end: str = "\n") -> None:
    """Prints colorful!
    String: string to be printed
    Color(default 0): Color, for more info, do terminalcolors.colortest
    Type(default 0): Type, for more info, do terminalcolors.typetest
    End(default \\n): End of print"""
    print(terminalcolors.reset + terminalcolors.types[thetype % terminalcolors.types.__len__()] + terminalcolors.colors[
        color % terminalcolors.colors.__len__()] + string + terminalcolors.reset, end=end)


def print_rainbow(string: str, thetype: int = 0, end: str = "\n") -> None:
    """Prints text in rainbow!
    String: string to be printed
    Type(default 0): Type, for more info, do terminalcolors.typetest
    End(default \\n): End of print"""
    print(rainbowify(string, thetype), end=end)


def colorify_high(string: str, fgcolor: Tuple[int, int, int], thetype: int = 0, bgcolor: Tuple[int, int, int] = None):
    assert len(fgcolor) == 3
    if bgcolor is None:
        return terminalcolors.types[thetype % 4] + terminalcolors.rgbcolor(*fgcolor) + string + terminalcolors.reset
    else:
        assert len(bgcolor) == 3
        return terminalcolors.types[thetype % 4] + terminalcolors.rgbcolor(*fgcolor) + terminalcolors.rgbcolor(*bgcolor,
                                                                                                               False) + string + terminalcolors.reset


def rainbowify(string: str, thetype: int = 0) -> str:
    """Rainbowifies string, makes it rainbow when printed."""
    newstr = copy.copy(terminalcolors.types[thetype % 4])
    i = 0
    rainbow = (
        terminalcolors.red, terminalcolors.yellow, terminalcolors.green, terminalcolors.cyan, terminalcolors.blue,
        terminalcolors.magenta)
    for c in string:
        newstr += rainbow[i] + c
        i += 1
        i %= 6
    return newstr + terminalcolors.reset


def colorify(string: str, color: int = 0, thetype: int = 0):
    """Makes a string colorful!"""
    return terminalcolors.reset + terminalcolors.types[thetype % terminalcolors.types.__len__()] + \
           terminalcolors.colors[color % terminalcolors.colors.__len__()] + string + terminalcolors.reset


def print_info(string: str, end: str = "\n"):
    print_color("[" + gettime() + " INFO]: " + string, 1, 0, end)


def print_warn(string: str, end: str = "\n"):
    print_color("[" + gettime() + " WARN]: " + string, 6, 0, end)


def print_err(string: str, end: str = "\n"):
    print_color("[" + gettime() + " ERROR]: " + string, 4, 0, end)


def print_fatalerr(string: str, end: str = "\n"):
    print_color("[" + gettime() + " FATAL ERROR]: " + string, 4, 1, end)


def print_debug(string: str, end: str = "\n"):
    print_color("[" + gettime() + " DEBUG]: " + string, 3, 0, end)


def print_extra(string: str, color: int = 1, typeofmessage: str = "INFO", thetype: int = 0, end: str = "\n"):
    print_color("[" + gettime() + " " + typeofmessage + "]: " + string, color % 8, thetype, end)


def make2digit(num: str):
    while len(num) < 2:
        num = "0" + num
    return num


def gettime():
    thetime = time.localtime(time.time())
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Dec")
    return make2digit(str(thetime.tm_mday)) + " " + months[thetime.tm_mon - 1] + " " + make2digit(
        str(thetime.tm_year)) + " " + make2digit(str(thetime.tm_hour)) + ":" + make2digit(
        str(thetime.tm_min)) + ":" + make2digit(str(thetime.tm_sec))


def getdir(obj: object, noreserved: bool = False) -> list:
    thedir = dir(obj)
    e = []
    for i in thedir:
        if noreserved and i.startswith("__") and i.endswith("__"): continue
        e.append((i, eval("obj." + str(i), {}, {'obj': obj})))
    return e


def objtodict(obj: object) -> dict:
    thedir = list(object.__dir__(obj))
    try:
        thedir.remove("__abstractmethods__")
    except:
        pass
    e = {}
    for i in thedir:
        e[i] = eval("obj." + str(i), {}, {'obj': obj})
    return e


def getdirstr(obj: object, noreserved: bool = False) -> str:
    thedir = dir(obj)
    e = ""
    for i in thedir:
        if i == "__dict__": continue
        if noreserved and i.startswith("__") and i.endswith("__"): continue
        e += str((i, eval("obj." + i, {}, {"obj": obj}))) + ")\n"
    return e[:-1]


def getdirstrwodf(obj: object, noreserved: bool = False) -> str:
    thedir = list(object.__dir__(obj))
    try:
        thedir.remove("__abstractmethods__")
    except:
        pass
    e = ""
    for i in thedir:
        if i == "__dict__": continue
        if noreserved and i.startswith("__") and i.endswith("__"): continue
        e += str((i, eval("obj." + i, {}, {"obj": obj}))) + ")\n"
    return e[:-1]


def getobjfromid(theid: int) -> object:
    """Recommended to use instead of this a weak-reference."""
    return ctypes.cast(theid, ctypes.py_object).value


class thread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=True):
        if name is None:
            name = "Thread-" + hex(id(self)).replace("0x", "__").upper().replace("__", "0x")
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.name = name
        self.out = None

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        # noinspection PyProtectedMember
        for t_id, thr in threading._active.items():
            if thr is self:
                return t_id

    def kill(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit(-1)))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print_err("Kill thread failure. Thread ID:" + thread_id + " Thread Name:" + self.name)


class run_with_multiprocessing(multiprocessing.Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        if kwargs is None:
            kwargs = {}
        multiprocessing.Process.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs,
                                         daemon=daemon)
        self.start()


def run_with_thread(group=None, target=None, name=None, args=(), kwargs=None, *, daemon=True):
    thr = threading.Thread(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
    thr.start()
    thr.join()


def run_as_thread(group=None, target=None, name=None, args=(), kwargs=None, *, daemon=True):
    thr = thread(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
    thr.start()
    return thr


try:
    import psutil
except:
    print_err("Psutil import error.")
if psutil is not None:
    def getAvailMem() -> float:
        """Available Memory in MB."""
        return psutil.virtual_memory().available / 1024 ** 2


    def checkMem(threshold: int = 250, freeze: bool = True, printwarn: bool = True) -> int:
        """Checks if enough memory is available. If not over threshold, will return 2.\n
        If its over the threshold it will try a collect command on the garbagecollector and will return a 1\n
        If its still over the threshold, 2 stuff can happen:\n
        If freeze is true(as default), the thread calling will freeze till its under the threshold and will return 0.\n
        If freeze is false, MemoryError will be raised."""
        isover = threshold >= getAvailMem()
        if isover:
            gc.collect()
        else:
            return 2
        isover = threshold >= getAvailMem()
        if freeze and isover:
            if printwarn:
                print_warn("Out of memory warning. Available memory is under the threshold of " + str(
                    threshold) + " megabytes.")
                print_warn(
                    "Program has frozen. Program will automatically unfreeze until available memory is over threshold.")
            waituntil("threshold < getAvailMem()", {"getAvailMem": getAvailMem, "threshold": threshold}, 1)
            if printwarn:
                print_warn("Program automatically unfrozen.")
            return 0
        elif isover:
            raise MemoryError
        else:
            return 1
else:
    getAvailMem = passkw
    checkMem = passkw
    print_warn("getAvailMem and checkMem will be unavailable due to psutil import error.")


def servcontosock(connection: Tuple[socket.socket, IpAddress]):
    sock = Socket(connection[1], connection[0])
    return sock


# noinspection PyAttributeOutsideInit
class Socket(enhancedobject):
    """A network socket. You can send anything through it."""

    def __init__(self, address: IpAddress, thesocket: socket.SocketType = None, **kwargs):
        """Create a new socket on address"""
        super().__init__(address, thesocket, **kwargs)

    # noinspection PyAttributeOutsideInit
    def oninit(self, address: IpAddress, thesocket: socket.SocketType = None, **kwargs):
        self.address = address
        if thesocket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(address)
        else:
            self._socket = thesocket
        self.issocketclosed = False

    # noinspection PyAttributeOutsideInit
    def send(self, data, internalinstruction=0) -> Union[None, ConnectionResetError]:
        """Sends data. It gets converted into a bytes object by pickle module and sent."""
        if not self.issocketclosed:
            try:
                self._socket.send(
                    pickle.dumps(
                        {
                            "internal": internalinstruction,
                            "message": data
                        }
                    )
                )
            except ConnectionResetError as e:
                self.issocketclosed = True
                return e

    def recv(self, buffer_size: int) -> Any:
        """Reads data.\n
        It gets returned as a bytes object if decode is False"""
        if not self.issocketclosed:
            try:
                data = pickle.loads(self._socket.recv(buffer_size))
                return data
            except ConnectionResetError:
                self.issocketclosed = True
            except pickle.PickleError as e:
                print_err("Connection error. Socket id {sockid} will be closed.".format(sockid=id(self)))
                self.send(self.internalinstr("disconnect", "pickle.UnpicklingError:" + str(str(" ").join(e.args))),
                          True)
                self.close()
                self.issocketclosed = True

    @staticmethod
    def internalinstr(inst, *args):
        args: list = list(args)
        for _ in range(5 - len(args)): args.append(None)
        instructions = {
            "disconnect": {
                "type": "disconnect",
                "message": str((args[0] if args[0] is not None else "Disconnected"))},
            "connectfail": {
                "type": "connectfail",
                "message": str((args[0] if args[0] is not None else "Disconnected"))},
            "connectok": {
                "type": "connectok",
                "message": args[0]},
            "isonlinecheck": {
                "type": "isonlinecheck"},
            "ch_buf_size": {
                "type": "ch_buf_size",
                "message": int((args[0] if args[0] is not None else 1024))},
        }
        return instructions[inst]

    def close(self):
        try:
            self._socket.close()
            self.issocketclosed = True
        except ConnectionResetError:
            self.issocketclosed = True


# noinspection PyAttributeOutsideInit
class ListeningServerSocket(enhancedobject):
    """A listening network socket."""

    def __init__(self, address: Tuple[str, int]):
        super().__init__(address)

    def oninit(self, address: Tuple[str, int]):
        """Make a listening network socket on the address."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._socket.listen(4)
        self.newconnections: List[Socket] = []
        self.connections: List[Socket] = []
        self.listening = False
        self.__listeningthread = None

    def listen(self, functonconnect: FunctionType = None):
        if not self.listening:
            self.listening = True
            self.__listeningthread = thread(target=self.__class__.__listen, args=(self, functonconnect))
            self.__listeningthread.start()

    def __listen(self, functonconnect):
        while True:
            c = servcontosock(self._socket.accept())
            self.connections.append(c)
            self.newconnections.append(c)
            if functonconnect is not None:
                functonconnect(c)
            self.checkforclosedcons()

    def checkforclosedcons(self):
        for index, i in enumerate(self.connections):
            if i.issocketclosed:
                self.connections[index].delete()


class carg:
    def __new__(cls, arg, normaltype=None):
        if normaltype is not None:
            return normaltype(arg)
        else:
            return carg.__find(arg)

    @staticmethod
    def __bytes(arg: bytes):
        if len(arg) == 1:
            return ctypes.c_char(arg)
        else:
            return ctypes.c_char_p(arg)

    @staticmethod
    def __str(arg: str):
        if len(arg) == 1:
            return ctypes.c_wchar(arg)
        else:
            return ctypes.c_wchar_p(arg)

    @staticmethod
    def __tuple(arg: tuple):
        arg = copy.copy(tuple(arg))
        if len(arg) == 0:
            raise ctypes.ArgumentError("If list/tuple is empty, you must follow it up with the type.")
        x = carg.__find(arg[0]).__class__
        for i in range(1, len(arg)):
            y = carg.__find(arg[i]).__class__
            if x != y:
                x = carg.__modtype(x, y)
        return (carg((arg[0], None)).__class__ * len(arg))(*arg)

    @staticmethod
    def __find(arg: Any):
        switch = {
            bool: ctypes.c_bool,
            bytes: carg.__bytes,
            str: carg.__str,
            int: ctypes.c_int,
            float: ctypes.c_float,
            type(None): ctypes.c_void_p,
            tuple: carg.__tuple,
            list: carg.__tuple
        }
        try:
            return switch[type(arg)](arg)
        except KeyError:
            if not type(arg).__module__.__name__ == "ctypes":
                return ctypes.py_object(arg)
            return arg

    @staticmethod
    def __modtype(old: type, new: type):
        if (old, new) in [(ctypes.c_wchar, ctypes.c_wchar_p), (ctypes.c_char_p, ctypes.c_char),
                          (ctypes.c_char, ctypes.c_char_p), (ctypes.c_char_p, ctypes.c_char)]:
            if (old, new) == (ctypes.c_wchar, ctypes.c_wchar_p):
                return new
            elif (old, new) == (ctypes.c_char, ctypes.c_char_p):
                return new
            else:
                return old
        else:
            raise ctypes.ArgumentError("more types of arguments, cannot make into array.")


def exec_CFUNC(func: ctypes.CFUNCTYPE, res_type: Any, *args: Any):
    """Executes c function with arguments"""
    func.restype = res_type
    newargs = (carg(i) for i in args)
    return func(*newargs)


def exec_nrCFUNC(func: ctypes.CFUNCTYPE, *args: Any):
    """Executes c function with arguments"""
    newargs = (carg(i) for i in args)
    return func(*newargs)


def getfromchoicewcond(prompt: str, cond: str, global_vars=None, local_vars=None) -> str:
    if local_vars is None:
        local_vars = {}
    if global_vars is None:
        global_vars = {}
    chose = False
    while not chose:
        inp = input(prompt)
        chose = bool(eval(cond, global_vars, {**local_vars, "inp": inp}))
    # noinspection PyUnboundLocalVariable
    return inp


pythonapi = ctypes.pythonapi


def rw_curse_modified(klass, attr, value):
    dikt = forbiddenfruit.patchable_builtin(klass)

    old_value = dikt.get(attr, None)
    old_name = '_c_%s' % attr  # do not use .format here, it breaks py2.{5,6}

    # Patch the thing
    dikt[attr] = value

    if old_value:
        hide_from_dir = False  # It was already in dir
        dikt[old_name] = old_value

        try:
            dikt[attr].__name__ = old_value.__name__
        except (AttributeError, TypeError):  # py2.5 will raise `TypeError`
            pass
        try:
            dikt[attr].__qualname__ = old_value.__qualname__
        except AttributeError:
            pass

    ctypes.pythonapi.PyType_Modified(ctypes.py_object(klass))

    # noinspection PyUnboundLocalVariable
    if hide_from_dir:
        forbiddenfruit.__hidden_elements__[klass.__name__].append(attr)


def rw_revert_modified(klass, attr):
    dikt = forbiddenfruit.patchable_builtin(klass)
    del dikt[attr]
    del dikt["_c_%s" % attr]
    ctypes.pythonapi.PyType_Modified(ctypes.py_object(klass))


def curse_mod(klass, attr, val):
    c = False
    while not c:
        try:
            rw_curse_modified(klass, attr, val)
            c = True
        except UnboundLocalError:
            pass


revert_mod = rw_revert_modified


def hash_obj(obj: object):
    if obj.__hash__ is not None:
        return obj.__hash__()
    else:
        raise TypeError("unhashable type: '" + obj.__class__.__name__ + "'")


def repr_obj(obj: object):
    return obj.__repr__()


def str_obj(self):
    if type(self) == type(""):
        return type("")(self)
    if type in self.__class__.__mro__:
        return self.__str__(self)
    return self.__str__()


def runfuncwthread(func, group=None, name=None, *, daemon=True):
    def wrapper(*args, **kwargs):
        return run_as_thread(group=group, target=func, name=name, args=args, kwargs=kwargs, daemon=daemon)

    return wrapper


@forbiddenfruit.curses(tuple, "unfreeze")
def unfreeze_tuple(self):
    replace_all(self, unfrozentuple(list(self)))


class Clock:
    def __init__(self):
        self.start = time.time()

    def tick(self, fps: int):
        p = (1 / fps) - (time.time() - self.start)
        if p > 0:
            wait_seconds(p)


def print_a_rainbow(splits: int = 1):
    string = ""
    i = 0.0
    try:
        while i != 360:
            x = tuple(int(i) for i in hsv_to_rgb((i, 1.0, 1.0)))
            string += colorify_high(" ", (0, 0, 0), 0, x)
            i += (90.0 / splits)
            if i > 360:
                break
    except KeyboardInterrupt:
        pass
    print(string)
    return string


def hsv_to_rgb(hsv: Tuple[Union[int, float], Union[int, float], Union[int, float]]) -> Tuple[int, int, int]:
    C = hsv[2] * hsv[1]
    X = C * (1 - abs((hsv[0] / 60) % 2 - 1))
    m = hsv[2] - C
    switch = {
        0 <= hsv[0] < 60: (C, X, 0),
        60 <= hsv[0] < 120: (X, C, 0),
        120 <= hsv[0] < 180: (0, C, X),
        180 <= hsv[0] < 240: (0, X, C),
        240 <= hsv[0] < 300: (X, 0, C),
        300 <= hsv[0] < 360: (C, 0, X)
    }
    x = switch[True]
    return ((x[0] + m) * 255, (x[1] + m) * 255, (x[2] + m) * 255)


if os.name == 'nt':
    e = os.system("color 07")
    if e == 0:
        print_extra("Successfully ran 'color 07', the terminal should now be able to run in custom colors!", 2,
                    "SUCCESS")
    else:
        print_err("An error has occurred while running 'color 07'")
        print_warn("Could not initialize high colors via 'color 07'")
else:
    print_warn("Could not initialize high colors via 'color 07'")
curse_mod(dict, "__hash__", hash_dict)
replace_all(hash, hash_obj)
replace_all(repr, repr_obj)
curse_mod(object, "toString", str_obj)
curse_mod(type(type), "toString", str_obj)

if __name__ == "__main__":
    Shell().run(globals())
