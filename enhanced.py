# enhanced - Adds new features to python
# new_terminalcolors made by GamingBox#8187


import builtins as __builtins__
import copy
import json
import traceback
import typing
from decimal import Decimal
from functools import wraps
from types import FunctionType, ModuleType
from typing import Any, List, Tuple, Iterator, Union, Iterable, Sized, Dict, Callable, Type
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


@forbiddenfruit.curses(dict, 'index')
def index_dict(self, value) -> Any:
    if value in self.values():
        return list(self.keys())[list(self.values()).index(value)]
    else:

        raise IndexError("Key with value " + str(value) + " does not exist.")


def replace_all(old: object, new: object):
    """Replace all references of old with new"""
    e = gc.get_referrers(old)
    for i in e:
        update_obj(i, old, new)


def update_obj(obj, old, new):
    """Update old with new in obj"""
    immutables = (tuple, str, type(dict().keys()), type(dict().values()), set, frozenset)
    if type(obj) in immutables:
        ty = type(obj)
        f = list(obj)
        f[f.index(old)] = new
        f = ty(f)
        for j in gc.get_referrers(obj):
            update_obj(j, obj, f)
    else:
        if type(obj) == dict or type(obj) == list:
            obj[obj.index(old)] = new


# noinspection PyUnusedLocal
def pass_func(*args, **kwargs):
    """Doesnt care about arguments, always returns None"""
    pass


def always_return(var: Any):
    """Always returns variable. Returns function which always returns that variable and does not care about arguments."""
    the_var = var

    # noinspection PyUnusedLocal
    def returner(*args, **kwargs):
        return the_var

    return returner


# noinspection PyPep8Naming,PyMissingConstructor
class enhanced_type(type):
    """Enhanced type.
    With this, you could add types together and make a hybrid from them.
    If doesnt import enhanced_object, it does it automatically"""

    @classmethod
    def enhance(mcs, klass: type) -> type:
        assert isinstance(klass, type)
        if type(klass) is not mcs:
            klass_dict: dict = forbiddenfruit.patchable_builtin(klass)
            type_enhanced = enhanced_type(klass.__qualname__, klass.__bases__, copy.copy(klass_dict))
            klass_dict.clear()
            tuple(klass_dict.setdefault(key, value) for key, value in dict(type_enhanced.__dict__).items())
            replace_all(klass, type_enhanced)
            return type_enhanced
        return klass

    @staticmethod
    def splittype(klass: type) -> Tuple[str, Tuple[type, ...], Dict[str, Any]]:
        return klass.__qualname__, klass.__bases__, forbiddenfruit.patchable_builtin(klass)

    def __new__(mcs, what: Union[Any, str], cls_bases: Tuple[type] = None, cls_dict: Dict[str, Any] = None):
        """
        enhanced_type(object_or_name, bases, dict)
        enhanced_type(object) -> the object's enhanced_type
        enhanced_type(name, bas es, dict) -> a new enhanced_type
        """
        if cls_bases == cls_dict is None:
            return type(what)
        elif cls_dict is not None:
            tp: List[type] = list(copy.copy(cls_bases))
            if enhanced_object not in tp:
                tp.append(enhanced_object)
            if object in tp:
                tp.remove(object)
            tp: tuple[type, ...] = tuple(tp)
            x = type.__new__(mcs, what, tp, cls_dict)
            return x
        else:
            raise TypeError('enhanced_type() takes 1 or 3 arguments')

    def __init__(cls, *args, **kwargs):
        pass

    def __add__(self, other):
        assert isinstance(other, type)
        assert type(self) == type(other)
        new_dict = {**dict(self.__dict__), **dict(other.__dict__)}
        new_bases = list(self.__bases__)
        new_bases.extend(other.__bases__)
        new_bases = tuple(set(new_bases))
        new_name = self.__qualname__ + "___" + other.__qualname__
        return type(self).__new__(type(self), new_name, new_bases, new_dict)


# noinspection PyRedeclaration,PyUnresolvedReferences,PyAttributeOutsideInit,PyPep8Naming,SpellCheckingInspection
class enhanced_object(object):
    """Enhanced object."""

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        self._private_initialized = False
        self._private_preInitialized = False
        self._private_deleted = False
        cls.onPreInit(self, *args, **kwargs)
        self._private_preInitialized = True
        return self

    def __init__(self, *args, **kwargs) -> None:
        self.onInit(*args, **kwargs)
        self._private_initialized = True

    def __hash__(self) -> int:
        return hash(json.dumps(copy.deepcopy(self.__dict__), sort_keys=True))

    def __eq__(self, other: object) -> bool:
        if enhanced_object in type(other).__mro__:
            return hash(self) == hash(other)
        else:
            return False

    def __repr__(self) -> str:
        if self._private_initialized:
            return "<" + str(self.__class__).replace("<class '", "").replace("'>", "") + ' enhanced_object at 0x' + (
                    "0" * (16 - len(hex(id(self)).replace("0x", "").upper())) + hex(id(self)).replace("0x",
                                                                                                      "").upper()) + ">"
        else:
            return "<" + str(self.__class__).replace("<class '", "").replace("'>",
                                                                             "") + ' enhanced_object(uninitialized) at 0x' + (
                           "0" * (16 - len(hex(id(self)).replace("0x", "").upper())) + hex(id(self)).replace("0x",
                                                                                                             "").upper()) + ">"

    def __str__(self) -> str:
        return self.__repr__()

    def shallowCopy(self):
        """Shallow copy the object"""
        return copy.copy(self)

    def deepCopy(self):
        """Deep copy the object"""
        return copy.deepcopy(self)

    def equals(self, other: object) -> bool:
        """Checks if an object is equal to the other."""
        if enhanced_object in type(other).__mro__:
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

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @classmethod
    def headlessNew(cls, *args, **kwargs):
        """Returns an uninitialized instance of this class."""
        return cls.__new__(cls, *args, **kwargs)

    def onPreInit(self, *args, **kwargs) -> None:
        pass

    def onInit(self, *args, **kwargs) -> None:
        pass

    @classmethod
    def new(cls, *args, **kwargs):
        """Returns an initialized instance of this class."""
        obj = cls.__new__(*args, **kwargs)
        if isinstance(obj, cls):
            obj.init(*args, **kwargs)
        return obj

    def init(self, *args, **kwargs) -> None:
        """Initializes the object, if its already initialized, throws a Warning"""
        if not self._private_initialized:
            self.__init__(*args, **kwargs)
        else:
            raise AlreadyInitializedWarning

    def ondelete(self, deletedAlready=False) -> None:
        pass

    def ongcdelete(self) -> None:
        pass

    def delete(self, force=False) -> int:
        if not self._private_deleted:
            self.ondelete()
        ref = gc.get_referrers(self)
        immutables = (tuple, str, type(dict().keys()), type(dict().values()), set, frozenset)
        for i in ref:
            if not inspect.isframe(i):
                if type(i) in immutables:
                    ty = type(i)
                    f = list(i)
                    f.remove(self)
                    f = ty(f)
                    for j in gc.get_referrers(i):
                        update_obj(j, i, f)
                else:
                    if type(i) == dict:
                        if '__holdDestroyedObjects__' in i.keys():
                            if i['__holdDestroyedObjects__']:
                                pass
                            else:
                                del i[i.index(self)]
                        else:
                            del i[i.index(self)]
                    elif type(i) == list:
                        i.remove(self)
            else:
                pass
        self._private_deleted = True
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
        if not self._private_deleted:
            self.ondelete(True)
            self._private_deleted = True
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
        for _ in range(self.getReferenceCount()[0]):
            pythonapi.Py_DecRef(e)

    # noinspection PyUnusedLocal
    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        return self.__biggerdeepcopy__(self)

    @classmethod
    def __biggerdeepcopy__(cls, self):
        x = super().__new__(cls)
        x.__dict__ = dict(((key, copy.deepcopy(value)) for key, value in self.__dict__))
        return x


enhanced_type.enhance(enhanced_object)
dict_keys = type(dict().keys())
dict_values = type(dict().values())
function = FunctionType
module = ModuleType
IpAddress = Tuple[str, int]
dict_items = type(dict().items())
NoneType = type(None)


# noinspection SpellCheckingInspection
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


# noinspection SpellCheckingInspection
class _GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# noinspection SpellCheckingInspection
class _GetchWindows:
    def __init__(self):
        pass

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


# noinspection SpellCheckingInspection
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


@enhanced_type.enhance
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
@enhanced_type.enhance
class Cacher:
    """Cacher object
    .flush() to clear the cache."""

    def __init__(self, **kwargs):
        self.cached = CacherMap()
        self.function = pass_func
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def __getitem__(self, num, memcap=True):
        if memcap:
            try:
                checkMem(500, False, False)
            except MemoryError:
                self.flush()
                checkMem(500)
        if num not in self.cached.keys():
            self.cached[num] = self.function(num)
        return self.cached[num]

    def __call__(self, num, memcap=True):
        return self.__getitem__(num, memcap)

    def flush(self):
        self.cached.clear()


# noinspection SpellCheckingInspection
class MathMisc:
    @staticmethod
    def isPrime(n) -> bool:
        f = True
        for i in range(2, n - 1):
            if (n % i) == 0:
                f = False
                break
        return f

    @staticmethod
    def prime(a) -> int:
        n = 2
        b = a
        while b != 0:
            if MathMisc.isPrime(n):
                b -= 1
            n += 1
        return n - 1

    # noinspection SpellCheckingInspection
    @staticmethod
    def split_exp_bases(a) -> list:
        thelist = []
        b = a
        while b != 1:
            n = 1
            while True:
                if (b % prime_num[n]) == 0:
                    break
                n += 1
            b = b // prime_num[n]
            thelist.append(prime_num[n])
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


prime_num = Cacher(funct=MathMisc.prime)


# noinspection PyUnresolvedReferences
class Fraction:
    pass


# noinspection PyRedeclaration,SpellCheckingInspection
@enhanced_type.enhance
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


# noinspection SpellCheckingInspection
def waituntil(cond: str, local_vars=None, interval: Union[float, int] = 0.01):
    """Waits until condition is true."""
    if local_vars is None:
        local_vars = {}
    while not eval(cond, local_vars):
        time.sleep(interval)


@forbiddenfruit.curses(dict, 'hash')
def hash_dict(self) -> int:
    return hash(json.dumps(copy.deepcopy(self), sort_keys=True))


def force_deallocate(obj: object) -> None:
    """Forces deletion on object."""
    e = ctypes.py_object(obj)
    for _ in range(sys.getrefcount(obj) - 3):
        pythonapi.Py_DecRef(e)


# noinspection PyBroadException
def partial_delete(self, log=False) -> int:
    """Attempts to delete all references of object."""
    ref = gc.get_referrers(self)
    immutables = (tuple, str, type(dict().keys()), type(dict().values()), set, frozenset)
    for i in ref:
        if not inspect.isframe(i):
            if type(i) in immutables:
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
                    if '__holdDestroyedObjects__' in i.keys():
                        if i['__holdDestroyedObjects__']:
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
                    except Exception:
                        if log:
                            printError()
        else:
            pass
    return sys.getrefcount(self) - 2


# noinspection PyBroadException
def partial_update_obj(obj, old, new, log=False):
    """Attempts to update old object to new"""
    immutables = (tuple, str, type(dict().keys()), type(dict().values()), set, frozenset)
    if type(obj) in immutables:
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
    """Gets traceback via traceback module."""
    return traceback.format_exc()


@enhanced_type.enhance
class AlreadyInitializedWarning(RuntimeWarning):
    ...


# noinspection PyPep8Naming,SpellCheckingInspection
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


class BaseAttributableObject:
    pass


# noinspection SpellCheckingInspection
@enhanced_type.enhance
class AttributableObject(enhanced_object, BaseAttributableObject):
    def __init__(self, thedict=None):
        """Makes a new attributable object from the dictionary"""
        super().__init__()
        if thedict is None:
            thedict = {}
        for i in thedict.keys():
            if not (i.startswith("__") and i.endswith("__")):
                setattr(self, i, thedict[i])


# noinspection PyPep8Naming,SpellCheckingInspection
@enhanced_type.enhance
class unfrozentuple(enhanced_object):
    """Unfrozen tuple
    A tuple which allows item assignment
    > tuple.unfreeze()
    Makes all references of tuple object unfrozentuple

    > unfrozentuple.freeze()
    Makes all references of unfrozentuple object tuple"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if len(args) == 0:
            self.thetuple: Tuple[Any, ...] = ()
        elif len(args) == 1:
            self.thetuple: Tuple[Any, ...] = tuple(copy.copy(args[0]))
        else:
            self.thetuple: Tuple[Any, ...] = tuple(args)

    def __repr__(self) -> str:
        if len(self.thetuple) > 1 or len(self.thetuple) == 0:
            return "unfrozentuple" + repr(self.thetuple)
        else:
            return "unfrozentuple(" + repr(self.thetuple) + ")"

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

    def resize(self, size: int):
        assert size >= len(self.thetuple)
        f = list(self.thetuple)
        f.extend([null] * (size - len(f)))
        self.thetuple = tuple(f)


def printError():
    print(terminalcolors.red + traceback.format_exc() + terminalcolors.reset)
    return terminalcolors.red + traceback.format_exc() + terminalcolors.reset


# noinspection SpellCheckingInspection
@enhanced_type.enhance
class Shell:
    """EXPERIMENTAL"""

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
                if self.__isolated:
                    print(repr(eval(c, {**self.isolglobals, "globals": always_return(self.isolglobals), "locals": always_return(self.locals)}, self.locals)))
                else:
                    print(repr(eval(c, self.globals, self.locals)))
            except SyntaxError:
                try:
                    if self.__isolated:
                        exec(c, {**self.isolglobals, "globals": always_return(self.isolglobals)}, self.locals)
                    else:
                        exec(c, self.globals, self.locals)
                except Exception as e:
                    printError()
                    return e
            except Exception as e:
                printError()
                return e
            return None

    def runc(self, c) -> Union[None, Exception, ValueError]:
        """Runs command"""
        if self.__isolexitstage == 0:
            if c == ">EXITISOL<" and self.canexitisol and self.__isolated:
                self.__isolexitstage = 1
            else:
                try:
                    if self.__isolated:
                        exec(c, {**self.isolglobals, "globals": always_return(self.isolglobals), "locals": always_return(self.locals)}, self.locals)
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


# noinspection SpellCheckingInspection
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


# noinspection SpellCheckingInspection
def print_color(string: str, color: int = 0, the_type: int = 0, end: str = "\n") -> None:
    """Prints colorful!
    String: string to be printed
    Color(default 0): Color, for more info, do terminalcolors.colortest
    Type(default 0): Type, for more info, do terminalcolors.typetest
    End(default \\n): End of print"""
    print(
        terminalcolors.reset + terminalcolors.types[the_type % terminalcolors.types.__len__()] + terminalcolors.colors[
            color % terminalcolors.colors.__len__()] + string + terminalcolors.reset, end=end)


# noinspection SpellCheckingInspection
def print_rainbow(string: str, the_type: int = 0, end: str = "\n") -> None:
    """Prints text in rainbow!
    String: string to be printed
    Type(default 0): Type, for more info, do terminalcolors.typetest
    End(default \\n): End of print"""
    print(rainbowify(string, the_type), end=end)


def colorify_high(string: str, fg_color: Tuple[int, int, int], the_type: int = 0,
                  bg_color: Tuple[int, int, int] = None):
    """Colors string with 24-bit RGB values,
    > colorify_high(string,(fg_r,fg_g,fg_b)[,type,(bg_r,bg_g,bg_r)])

    where type is a number
    0b00
    0th bit is bold
    1st bit is underline"""
    assert len(fg_color) == 3
    if bg_color is None:
        return terminalcolors.types[the_type % 4] + terminalcolors.rgbcolor(*fg_color) + string + terminalcolors.reset
    else:
        assert len(bg_color) == 3
        return terminalcolors.types[the_type % 4] + terminalcolors.rgbcolor(*fg_color) + terminalcolors.rgbcolor(
            *bg_color,
            False) + string + terminalcolors.reset


def rainbowify(string: str, the_type: int = 0) -> str:
    """Makes a string rainbow, makes it rainbow when printed."""
    new_str = copy.copy(terminalcolors.types[the_type % 4])
    i = 0
    rainbow = (
        terminalcolors.red, terminalcolors.yellow, terminalcolors.green, terminalcolors.cyan, terminalcolors.blue,
        terminalcolors.magenta)
    for c in string:
        new_str += rainbow[i] + c
        i += 1
        i %= 6
    return new_str + terminalcolors.reset


def colorify(string: str, color: int = 0, the_type: int = 0):
    """Makes a string colorful!"""
    return terminalcolors.reset + terminalcolors.types[the_type % terminalcolors.types.__len__()] + \
           terminalcolors.colors[color % terminalcolors.colors.__len__()] + string + terminalcolors.reset


def print_info(string: str, end: str = "\n"):
    print_color("[" + get_time() + " INFO]: " + string, 1, 0, end)


def print_warn(string: str, end: str = "\n"):
    print_color("[" + get_time() + " WARN]: " + string, 6, 0, end)


def print_err(string: str, end: str = "\n"):
    print_color("[" + get_time() + " ERROR]: " + string, 4, 0, end)


def print_fatalerr(string: str, end: str = "\n"):
    print_color("[" + get_time() + " FATAL ERROR]: " + string, 4, 1, end)


def print_debug(string: str, end: str = "\n"):
    print_color("[" + get_time() + " DEBUG]: " + string, 3, 0, end)


def print_extra(string: str, color: int = 1, type_of_message: str = "INFO", the_type: int = 0, end: str = "\n"):
    print_color("[" + get_time() + " " + type_of_message + "]: " + string, color % 8, the_type, end)


def make2digit(num: str):
    while len(num) < 2:
        num = "0" + num
    return num


def get_time():
    the_time = time.localtime(time.time())
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Dec")
    return make2digit(str(the_time.tm_mday)) + " " + months[the_time.tm_mon - 1] + " " + make2digit(
        str(the_time.tm_year)) + " " + make2digit(str(the_time.tm_hour)) + ":" + make2digit(
        str(the_time.tm_min)) + ":" + make2digit(str(the_time.tm_sec))


def get_dir(obj: object, no_reserved: bool = False) -> list:
    """Returns directory of object as List[Tuple[key: str, val: Any]]"""
    the_dir = dir(obj)
    e = []
    for i in the_dir:
        if no_reserved and i.startswith("__") and i.endswith("__"):
            continue
        e.append((i, eval("obj." + str(i), {}, {'obj': obj})))
    return e


def get_dir_wodf(obj: object, no_reserved: bool = False) -> list:
    """Returns directory of object with the object's dir function as List[Tuple[key: str, val: Any]]"""
    the_dir = dir(obj)
    e = []
    for i in the_dir:
        if no_reserved and i.startswith("__") and i.endswith("__"):
            continue
        e.append((i, eval("obj." + str(i), {}, {'obj': obj})))
    return e


def obj_to_dict(obj: object) -> dict:
    the_dir = list(object.__dir__(obj))
    try:
        the_dir.remove("__abstractmethods__")
    except ValueError:
        pass
    e = {}
    for i in the_dir:
        e[i] = eval("obj." + str(i), {}, {'obj': obj})
    return e


def get_dir_str(obj: object, no_reserved: bool = False) -> str:
    the_dir = dir(obj)
    e = ""
    for i in the_dir:
        if i == "__dict__":
            continue
        if no_reserved and i.startswith("__") and i.endswith("__"):
            continue
        e += str((i, eval("obj." + i, {}, {"obj": obj}))) + ")\n"
    return e[:-1]


def get_dir_str_wodf(obj: object, no_reserved: bool = False) -> str:
    the_dir = list(object.__dir__(obj))
    try:
        the_dir.remove("__abstractmethods__")
    except ValueError:
        pass
    e = ""
    for i in the_dir:
        if i == "__dict__":
            continue
        if no_reserved and i.startswith("__") and i.endswith("__"):
            continue
        e += str((i, eval("obj." + i, {}, {"obj": obj}))) + ")\n"
    return e[:-1]


def get_obj_from_id(the_id: int) -> object:
    """Recommended to use a weak-reference instead of this."""
    return ctypes.cast(the_id, ctypes.py_object).value


# noinspection PyPep8Naming
@enhanced_type.enhance
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


# noinspection PyPep8Naming
@enhanced_type.enhance
class run_with_multiprocessing(multiprocessing.Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        if kwargs is None:
            kwargs = {}
        multiprocessing.Process.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs,
                                         daemon=daemon)
        self.start()


def run_as_thread(group=None, target=None, name=None, args=(), kwargs=None, *, daemon=True):
    thr = threading.Thread(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
    thr.start()
    thr.join()


def run_with_thread(group=None, target=None, name=None, args=(), kwargs=None, *, daemon=True):
    thr = thread(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
    thr.start()
    return thr


try:
    import psutil
except ImportError:
    print_err("Psutil import error.")
    psutil = None
if psutil is not None:
    def getAvailMem() -> float:
        """Available Memory in MB."""
        return psutil.virtual_memory().available / 1024 ** 2


    def checkMem(threshold: int = 250, freeze: bool = True, print_warning: bool = True) -> int:
        """Checks if enough memory is available. If not over threshold, will return 2.\n
        If its over the threshold it will try a collect command on the garbage collector and will return a 1\n
        If its still over the threshold, 2 stuff can happen:\n
        If freeze is true(as default), the thread calling will freeze till its under the threshold and will return 0.\n
        If freeze is false, MemoryError will be raised."""
        is_over = threshold >= getAvailMem()
        if is_over:
            gc.collect()
        else:
            return 2
        is_over = threshold >= getAvailMem()
        if freeze and is_over:
            if print_warning:
                print_warn("Out of memory warning. Available memory is under the threshold of " + str(
                    threshold) + " megabytes.")
                print_warn(
                    "Program has frozen. Program will automatically unfreeze until available memory is over threshold.")
            waituntil("threshold < getAvailMem()", {"getAvailMem": getAvailMem, "threshold": threshold}, 1)
            if print_warning:
                print_warn("Program automatically unfrozen.")
            return 0
        elif is_over:
            raise MemoryError
        else:
            return 1
else:
    getAvailMem = pass_func
    checkMem = pass_func
    print_warn("getAvailMem and checkMem will be unavailable due to psutil import error.")


def serv_con_to_sock(connection: Tuple[socket.socket, IpAddress]):
    sock = Socket(connection[1], connection[0])
    return sock


# noinspection PyAttributeOutsideInit
@enhanced_type.enhance
class Socket(enhanced_object):
    """A network socket. You can send anything through it."""

    def __init__(self, address: IpAddress, the_socket: socket.SocketType = None):
        """Create a new socket on address"""
        super().__init__(address, the_socket)

    # noinspection PyAttributeOutsideInit
    def onInit(self, address: IpAddress, the_socket: socket.SocketType = None):
        self.address = address
        if the_socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(address)
        else:
            self._socket = the_socket
        self.is_socket_closed = False

    # noinspection PyAttributeOutsideInit
    def send(self, data, internal_instruction=0) -> Union[None, ConnectionResetError]:
        """Sends data. It gets converted into a bytes object by pickle module and sent."""
        if not self.is_socket_closed:
            try:
                self._socket.send(
                    pickle.dumps(
                        {
                            "internal": internal_instruction,
                            "message": data
                        }
                    )
                )
            except ConnectionResetError as e:
                self.is_socket_closed = True
                return e

    def recv(self, buffer_size: int) -> Any:
        """Reads data.\n
        It gets returned as a bytes object if decode is False"""
        if not self.is_socket_closed:
            try:
                data = pickle.loads(self._socket.recv(buffer_size))
                return data
            except ConnectionResetError:
                self.is_socket_closed = True
            except pickle.PickleError as e:
                print_err("Connection error. Socket id {sock_id} will be closed.".format(sock_id=id(self)))
                self.send(
                    self.internal_instruction("disconnect", "pickle.UnpicklingError:" + str(str(" ").join(e.args))),
                    True)
                self.close()
                self.is_socket_closed = True

    @staticmethod
    def internal_instruction(inst, *args):
        args: list = list(args)
        for _ in range(5 - len(args)):
            args.append(None)
        instructions = {
            "disconnect": {
                "type": "disconnect",
                "message": str((args[0] if args[0] is not None else "Disconnected"))},
            "connectFail": {
                "type": "connectFail",
                "message": str((args[0] if args[0] is not None else "Disconnected"))},
            "connectOk": {
                "type": "connectOk",
                "message": args[0]},
            "ping": {
                "type": "ping"},
            "ch_buf_size": {
                "type": "ch_buf_size",
                "message": int((args[0] if args[0] is not None else 1024))},
        }
        return instructions[inst]

    def close(self):
        try:
            self._socket.close()
            self.is_socket_closed = True
        except ConnectionResetError:
            self.is_socket_closed = True


# noinspection PyAttributeOutsideInit
@enhanced_type.enhance
class ListeningServerSocket(enhanced_object):
    """A listening network socket."""

    def __init__(self, address: Tuple[str, int]):
        super().__init__(address)

    def onInit(self, address: Tuple[str, int]):
        """Make a listening network socket on the address."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._socket.listen(4)
        self.newConnections: List[Socket] = []
        self.connections: List[Socket] = []
        self.listening = False
        self._private_listening_thread = None

    def listen(self, function_on_connect: FunctionType = None):
        if not self.listening:
            self.listening = True
            self._private_listening_thread = thread(target=type(self)._private_listen, args=(self, function_on_connect))
            self._private_listening_thread.start()

    def _private_listen(self, function_on_connect):
        while True:
            c = serv_con_to_sock(self._socket.accept())
            self.connections.append(c)
            self.newConnections.append(c)
            if function_on_connect is not None:
                run_with_thread(target=function_on_connect, args=(c,))
            self.checkForClosedCons()

    def checkForClosedCons(self):
        for index, i in enumerate(self.connections):
            if i.is_socket_closed:
                self.connections[index].delete()


class UndefinedType:
    """Type of undefined."""
    undefined_id = 0

    def __new__(cls):
        return get_obj_from_id(UndefinedType.undefined_id)

    def __repr__(self):
        return 'undefined'

    def __bool__(self):
        return False

    def __int__(self):
        return 0

    def __index__(self):
        return 0


class NullType:
    """Type of null."""
    null_id = 0

    def __new__(cls):
        return get_obj_from_id(NullType.null_id)

    def __repr__(self):
        return 'null'

    def __bool__(self):
        return False

    def __int__(self):
        return 0

    def __index__(self):
        return 0


undefined = object.__new__(UndefinedType)
UndefinedType.undefined_id = id(undefined)
# noinspection PyTypeChecker
enhanced_object.inc_ref(undefined)
__builtins__.__dict__['undefined'] = undefined
null = object.__new__(NullType)
NullType.null_id = id(null)
# noinspection PyTypeChecker
enhanced_object.inc_ref(null)
__builtins__.__dict__['null'] = null


class CArgument:
    def __new__(cls, arg, normal_type=None):
        if normal_type is not None:
            return normal_type(arg)
        else:
            return cls._private_find(arg)

    @staticmethod
    def _private_bytes(arg: bytes):
        if len(arg) == 1:
            return ctypes.c_char(arg)
        else:
            return ctypes.c_char_p(arg)

    @staticmethod
    def _private_str(arg: str):
        if len(arg) == 1:
            return ctypes.c_wchar(arg)
        else:
            return ctypes.c_wchar_p(arg)

    @classmethod
    def _private_tuple(cls, arg: tuple):
        arg = copy.copy(tuple(arg))
        if len(arg) == 0:
            raise ctypes.ArgumentError("If list/tuple is empty, you must follow it up with the type.")
        x = cls._private_find(arg[0]).__class__
        for i in range(1, len(arg)):
            y = cls._private_find(arg[i]).__class__
            if x != y:
                x = cls._private_mod_type(x, y)
        return (cls((arg[0], None)).__class__ * len(arg))(*arg)

    @classmethod
    def _private_find(cls, arg: Any):
        switch = {
            bool: ctypes.c_bool,
            bytes: cls._private_bytes,
            str: cls._private_str,
            int: ctypes.c_int,
            float: ctypes.c_float,
            type(None): ctypes.c_void_p,
            tuple: cls._private_tuple,
            list: cls._private_tuple
        }
        try:
            return switch[type(arg)](arg)
        except KeyError:
            try:
                if not type(arg).__module__.__name__ == "ctypes":
                    return ctypes.py_object(arg)
            except AttributeError:
                return ctypes.py_object(arg)
            return arg

    @staticmethod
    def _private_mod_type(old: type, new: type):
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
    new_args = (CArgument(i) for i in args)
    return func(*new_args)


def exec_nrCFUNC(func: ctypes.CFUNCTYPE, *args: Any):
    """Executes c function with arguments"""
    new_args = (CArgument(i) for i in args)
    return func(*new_args)


def get_from_choice_with_cond(prompt: str, cond: str, invalid_choice_message: str = "Invalid choice!",
                              global_vars: dict = None, local_vars: dict = None) -> str:
    if local_vars is None:
        local_vars = {}
    if global_vars is None:
        global_vars = {}
    chose = False
    while not chose:
        inp = input(prompt)
        chose = bool(eval(cond, global_vars, {**local_vars, "inp": inp}))
        if not chose:
            print(invalid_choice_message)
    # noinspection PyUnboundLocalVariable
    return inp


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


pythonapi = ctypes.pythonapi
revert_mod = rw_revert_modified


def hash_obj(obj: Union[type, object]):
    if obj.__hash__ is not None:
        if isinstance(obj, type):
            return type(obj).__hash__(obj)
        return obj.__hash__()
    else:
        raise TypeError("unhashable type: '" + type(obj).__name__ + "'")


def repr_obj(obj: Union[object, type]):
    if isinstance(obj, type):
        # noinspection PyArgumentList
        return type(obj).__repr__(obj)
    return obj.__repr__()


def str_obj(self):
    if isinstance(self, str):
        return type("")(self)
    if isinstance(self, type):
        return type(self).__str__(self)
    return self.__str__()


def len_obj(self: Union[Type[Sized], Sized]):
    if isinstance(self, type):
        return type(self).__len__(self)
    return self.__len__()


def run_func_with_thread(func, group=None, name=None, *, daemon=True):
    """Wrapper for functions. Runs function with a thread and returns thread"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return run_with_thread(group=group, target=func, name=name, args=args, kwargs=kwargs, daemon=daemon)

    return wrapper


@forbiddenfruit.curses(tuple, "unfreeze")
def unfreeze_tuple(self):
    replace_all(self, unfrozentuple(list(self)))


@enhanced_type.enhance
class Clock:
    def __init__(self):
        self._private_start = time.time()
        self.thr = run_with_thread(target=type(self)._private_fps_count, args=(self,))
        self._private_f = 0
        self._private_new_f = 0
        self._private_t = [self._private_start, self._private_start]

    def tick(self, fps: int) -> float:
        """Tick clock and return ms waited float"""
        x = time.time()
        self._private_t.pop(0)
        self._private_t.append(x)
        p = (1 / fps) - (x - self._private_start)
        if p > 0:
            wait_seconds(p)
        self._private_f += 1
        self._private_start = time.time()
        return p * 1000.0

    def _private_fps_count(self):
        while True:
            wait_seconds(1)
            self._private_new_f = self._private_f
            self._private_f = 0

    def get_fps(self) -> int:
        """Gets FPS."""
        return self._private_new_f

    def get_time(self) -> float:
        """Return float of ms between the last 2 calls of tick()"""
        return (self._private_t[1] - self._private_t[0]) * 1000.0


def print_a_rainbow(splits: int = 1):
    string = ""
    i = 0.0
    try:
        while i != 360:
            # noinspection PyTypeChecker
            x: Tuple[int, int, int] = tuple(int(i) for i in hsv_to_rgb((i, 1.0, 1.0)))
            assert len(x) == 3
            string += colorify_high(" ", (0, 0, 0), 0, x)
            i += (90.0 / splits)
            if i > 360:
                break
    except KeyboardInterrupt:
        pass
    return string


def hsv_to_rgb(hsv: Tuple[Union[int, float], Union[int, float], Union[int, float]]) -> Tuple[int, int, int]:
    c = hsv[2] * hsv[1]
    x = c * (1 - abs((hsv[0] / 60) % 2 - 1))
    m = hsv[2] - c
    switch = {
        0 <= hsv[0] < 60: (c, x, 0),
        60 <= hsv[0] < 120: (x, c, 0),
        120 <= hsv[0] < 180: (0, c, x),
        180 <= hsv[0] < 240: (0, x, c),
        240 <= hsv[0] < 300: (x, 0, c),
        300 <= hsv[0] < 360: (c, 0, x)
    }
    x = switch[True]
    return (x[0] + m) * 255, (x[1] + m) * 255, (x[2] + m) * 255


def isiterable(obj: Union[Iterable, Any]):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


@forbiddenfruit.curses(dict, "try_delete")
def try_delete_dict(self, key: Union[Any, Iterable]):
    if isiterable(key):
        keys = key
        for key in keys:
            try:
                del self[key]
            except KeyError:
                pass
    else:
        try:
            del self[key]
        except KeyError:
            pass


def hash_self(self):
    return type(self).__hash__(self)


def str_self(self):
    return type(self).__str__(self)


def getattr_obj(o: Union[type, object], key: str, default: Any = null):
    if isinstance(o, type):
        try:
            # noinspection PyArgumentList
            return type(o).__getattribute__(o, key)
        except AttributeError:
            if default is not null:
                return default
            raise
    else:
        try:
            return o.__getattribute__(key)
        except AttributeError:
            if default is not null:
                return default
            raise


def setattr_obj(o: Union[type, object], key: str, val: Any):
    if isinstance(o, type):
        # noinspection PyArgumentList
        o.__setattr__(o, key, val)
    else:
        o.__setattr__(key, val)


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
replace_all(len, len_obj)
# replace_all(getattr, getattr_obj)
# replace_all(setattr, setattr_obj)
curse_mod(object, "toString", str_self)
curse_mod(type, "toString", str_self)
curse_mod(object, "hash", hash_self)
curse_mod(type, "hash", hash_self)


def get_obj_mem(obj):
    return (ctypes.c_char * sys.getsizeof(obj)).from_address(id(obj))


def memory_object(adr, len):
    return (ctypes.c_char * len).from_address(adr)


def change_mem_size(obj: object, len: int):
    obj_mem = get_obj_mem(obj)
    assert __builtins__.len(obj_mem[:]) <= len
    pythonapi.PyObject_Realloc.restype = ctypes.POINTER(ctypes.c_void_p)
    pointer_to_new_obj: ctypes.POINTER(ctypes.c_void_p) = pythonapi.PyObject_Realloc(
        ctypes.pointer(ctypes.py_object(obj)))
    new_mem = memory_object(ctypes.addressof(pointer_to_new_obj), len)
    new_mem[:] = obj_mem[:] + (b'\x00' * (len - __builtins__.len(obj_mem[:])))
    return ctypes.py_object.from_address(ctypes.addressof(pointer_to_new_obj)).value


# noinspection PyPep8Naming,SpellCheckingInspection
class new_terminalcolors:
    reset = "\033[0m"
    bold = "\033[1m"
    underline = "\033[4m"
    inverse = "\033[7m"

    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    lightblue = "\033[36m"
    white = "\033[37m"

    bblack = "\033[40m"
    bred = "\033[41m"
    bgreen = "\033[42m"
    byellow = "\033[43m"
    bblue = "\033[44m"
    bpurple = "\033[45m"
    blightblue = "\033[46m"
    bwhite = "\033[47m"

    sblack = "\033[90m"
    sred = "\033[91m"
    sgreen = "\033[92m"
    syellow = "\033[93m"
    sblue = "\033[94m"
    spurple = "\033[95m"
    slightblue = "\033[96m"
    swhite = "\033[97m"

    sbblack = "\033[100m"
    sbred = "\033[101m"
    sbgreen = "\033[102m"
    sbyellow = "\033[103m"
    sbblue = "\033[104m"
    sbpurple = "\033[105m"
    sblightblue = "\033[106m"
    sbwhite = "\033[107m"

    @classmethod
    def colorcmd(cls, bg: int, fg: int, text_type: int = 0):
        x = [
            "black", "blue", "green", "lightblue", "red", "purple", "yellow", "white", "bblack", "bblue", "bgreen",
            "blightblue", "bred", "bpurple", "byellow", "bwhite", "sblack", "sblue", "sgreen", "slightblue", "sred",
            "spurple", "syellow", "swhite", "sbblack", "sbblue", "sbgreen", "sblightblue", "sbred", "sbpurple",
            "sbyellow", "sbwhite"]
        assert 0 <= bg <= 15 and 0 <= fg <= 15 and 0 <= text_type <= 7
        if fg < 8:
            fg_col = fg
        else:
            fg_col = fg + 8
        if bg < 8:
            bg_col = bg + 8
        else:
            bg_col = bg + 16
        return cls.reset + (cls.bold * (text_type % 2) + cls.underline * ((text_type >> 1) % 2) + cls.inverse * (
                    (text_type >> 2) % 2)) + getattr(cls, x[bg_col]) + getattr(cls, x[fg_col])


def wrapper_maker(func: Callable, func_arg: Callable = None):
    """Wrapper maker.
    func -> Function to be ran with/without local variables
    If it does have local variables, gives 2 arguments, first being the local variables, 2nd being the object to be wrapped.
    If it does not however, it just gives 1 argument of the object to be wrapped

    func_arg -> Function to be ran to make the local_vars
    Returns local_vars to be used with func"""

    def wrapper(*args, **kwargs):
        local_vars = {}

        def inner(to_be_wrapped):
            return func(local_vars, to_be_wrapped)

        if len(kwargs) > 0 or len(args) > 1:
            local_vars = {'args': args, 'kwargs': kwargs}
            return inner
        elif func_arg is None:
            return func(args[0])
        else:
            local_vars = func_arg(*args, **kwargs)
            return inner

    return wrapper


class StructureType(enhanced_type):
    def __repr__(self):
        return "<structure '" + type.__repr__(self).replace("<class '", "").replace("'>", "") + "'>"

    def __new__(mcs, what: Union[Any, str], cls_bases: Tuple[type] = None, cls_dict: Dict[str, Any] = None):
        """
        StructureType(object_or_name, bases, dict)
        StructureType(object) -> the object's StructureType
        StructureType(name, bas es, dict) -> a new StructureType
        """
        if cls_bases == cls_dict is None:
            return type(what)
        elif cls_dict is not None:
            tp: List[type] = list(copy.copy(cls_bases))
            if object in tp:
                tp.remove(object)
            tp: tuple[type, ...] = tuple(tp)
            x = type.__new__(mcs, what, tp, cls_dict)
            return x
        else:
            raise TypeError('StructureType() takes 1 or 3 arguments')


def structure(klass):
    """Makes class a structure
    Note: Please make sure you are inheriting from any class except of 'object'
    If you do not intend to inherit on any, inherit from an empty class like 'BaseAttributableObject'"""
    klass_name, klass_bases, klass_dict = StructureType.splittype(klass)
    klass_dict = klass_dict.copy()
    klass_bases = list(klass_bases)
    if object in klass_bases:
        klass_bases.remove(object)
    if BaseAttributableObject not in klass_bases:
        klass_bases.append(BaseAttributableObject)
    klass = type.__new__(type, klass_name, tuple(klass_bases), klass_dict)
    klass_name, klass_bases, klass_dict = StructureType.splittype(klass)
    klass_dict = klass_dict.copy()
    klass_dict.setdefault('_struct_', [])
    klass_dict.setdefault('__init__', object.__init__)
    klass_dict.setdefault('__getattribute__', object.__getattribute__)
    klass_dict.setdefault('__setattr__', object.__setattr__)

    def new_dir(self):
        z = []
        is_special = (lambda x: x.startswith('__') and x.endswith('__'))
        # noinspection PyArgumentList
        z.extend(filter(is_special, super(type(self), self).__dir__()))
        # noinspection PyProtectedMember
        z.extend(type(self)._struct_)
        return z

    is_not_special = (lambda x: not (x.startswith('__') and x.endswith('__')))
    klass_dict['__dir__'] = new_dir
    klass_dict['_def_struct_'] = list(filter(is_not_special, klass_dict))
    klass_dict['_def_struct_'].remove("_struct_")
    klass_dict['_def_struct_'] = frozenset(klass_dict['_def_struct_'])
    klass_dict['_struct_'] = frozenset(klass_dict['_struct_']).union(klass_dict['_def_struct_'])
    klass_dict['_not_def_struct_'] = klass_dict['_struct_'] - klass_dict['_def_struct_']
    klass_dict['__former_init__'] = klass_dict['__init__']
    klass_dict['__former_getattribute__'] = klass_dict['__getattribute__']
    klass_dict['__former_setattr__'] = klass_dict['__setattr__']

    def new_init(self):
        tuple((type(self).__setattr__(self, x, undefined) for x in self._not_def_struct_))
        type(self).__former_init__(self)

    def new_getattr(self, key: str):
        # noinspection PyProtectedMember
        if key.startswith('_private_') or (key.startswith('__') and key.endswith('__')) or key in ('_struct_', '_def_struct_', '_not_def_struct_') or key in type(self)._struct_:
            return object.__getattribute__(self, key)
        raise AttributeError(f"'{type(self).__qualname__}' object has no attribute '{key}'")

    def new_setattr(self, key: str, val: Any):
        if key == "_struct_":
            raise TypeError("_struct_ assignment not supported to structure type classes")
        object.__setattr__(self, key, val)

    def new_repr(self):
        return "<" + repr(type(self)).replace("<structure '", "").replace("'>", "") + " structure object at 0x" + (
                "0" * (16 - len(hex(id(self)).replace("0x", "").upper())) + hex(id(self)).replace("0x",
                                                                                                  "").upper()) + ">"

    klass_dict['__init__'] = new_init
    klass_dict['__getattribute__'] = new_getattr
    klass_dict['__setattr__'] = new_setattr
    klass_dict['__repr__'] = new_repr
    new_klass = StructureType.__new__(StructureType, klass_name, klass_bases, klass_dict)
    return new_klass


def Tuple_SetItem(tuple_object: tuple, pos: int, item: Any):
    if len(tuple_object) <= pos:
        raise IndexError('index out of range.')
    t_mem = get_obj_mem(tuple_object)
    pythonapi.Py_IncRef(item)
    z = tuple_object[pos]
    t_mem[24 + (8 * pos):32 + (8 * pos)] = id(item).to_bytes(8, 'little')
    pythonapi.Py_DecRef(z)
    return tuple_object


structure = wrapper_maker(structure)


def reloadModule(module_name: str, loadAllFromModule: bool = False):
    globals()['partial_delete'](__import__(module_name))
    globals()[module_name] = __import__(module_name)
    if loadAllFromModule:
        for k, v in globals()[module_name].__dict__.items():
            globals()[k] = v


def loadFromModuleAll(module: ModuleType):
    for k, v in module.__dict__.items():
        globals()[k] = v


def file_size_comp(amount: Union[int, float, Decimal], asSmallAsPossible: bool = False):
    f = ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    i = 0
    n = Decimal(copy.copy(amount))
    while Decimal(1000) <= n:
        n /= Decimal(1000)
        i += 1
        if i == len(f) - 1:
            break
    z = f[i]
    if not asSmallAsPossible:
        if n >= 100:
            return str(round(n, 1)) + z
        elif n >= 10:
            return str(round(n, 2)) + z
        return str(round(n, 3)) + z
    else:
        return str(round(n)) + z


def size_comp(amount: Union[int, float, Decimal], asSmallAsPossible: bool = False):
    f = ('', 'K', 'M', 'B', 't', 'q', 'Q', 's', 'S', 'o', 'n', 'd', 'U', 'D', 'T', 'qu', 'Qu', 'se', 'Se', 'O', 'N', 'V')
    i = 0
    n = Decimal(copy.copy(amount))
    while Decimal(1000) <= n:
        n /= Decimal(1000)
        i += 1
        if i == len(f) - 1:
            break
    z = f[i]
    if not asSmallAsPossible:
        if n >= 100:
            return str(round(n, 1)) + z
        elif n >= 10:
            return str(round(n, 2)) + z
        return str(round(n, 3)) + z
    else:
        return str(round(n)) + z
