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
import copy
import json
import traceback
from types import FunctionType, ModuleType
from typing import Any, List, Tuple
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


def passkw(*args,**kwargs):
    pass
dict_keys = type(dict().keys())
dict_values = type(dict().values())
function = FunctionType
module = ModuleType
class CString:
    """Array of characters"""
    def __new__(self,string : str,length : int=None):
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
    def __setitem__(self,key,value) -> None:
        self.map[key] = value
    def __getitem__(self,key) -> None:
        return self.map[key]
    def clear(self) -> None:
        self.map.clear()
    def keys(self) -> dict_keys:
        return self.map.keys()
class Cacher:
    def __init__(self,**kwargs):
        self.cached = CacherMap()
        self.funct = ""
        for i in kwargs:
            setattr(self,i,kwargs[i])
    def __getitem__(self,num,memcap=True):
        if memcap:
            try:
                checkMem(500,False,False)
            except MemoryError:
                self.flush()
                checkMem(500)
        if not num in self.cached.keys():
            self.cached[num] = self.funct(num)
        return self.cached[num]
    def __call__(self,num,memcap=True):
        return self.__getitem__(num,memcap)
    def flush(self):
        self.cached.clear()
class MathMisc:
    def isprime(n) -> bool:
        f = True
        for i in range(2,n - 1):
            if ((n % i) == 0):
                f = False
                break
        return f
    def primen(a) -> int:
        n = 2
        b = a
        while b != 0:
            if MathMisc.isprime(n):
                b -= 1
            n += 1
        return n - 1
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
    def gcd(x,y) -> int:
        while(y):
            x, y = y, x % y
        return x
    def cmmdc(*args) -> int:
        x = args[0]
        for i in args:
            x = MathMisc.gcd(x,i)
            if x == 1:
                break
        return x
    def lcm(x,y):
        return x*y//MathMisc.gcd(x,y)
    def union(*args) -> list:
        c = set(args[0])
        for i in args:
            if i == args[0]:
                continue
            c |= set(i)
        return list(c)
    def comparebothhave(*args) -> list:
        a = args[0].copy()
        for arg in args:
            a = list(set(a).intersection(arg))
        return a
    def difference(*args) -> list:
        c = set(args[0])
        for i in args:
            if i == args[0]:
                continue
            c -= set(i)
        return list(c)
    def symdif(*args) -> list:
        c = set(args[0])
        for i in args:
            if i == args[0]:
                continue
            c ^= set(i)
        return list(c)
    def cmmmc(*args) -> int:
        x = args[0]
        for i in args:
            x = MathMisc.lcm(x,i)
        return x
primenum = Cacher(funct=MathMisc.primen)
class Fraction:
    def __init__(self,n,div):
        self.n = n
        self.div = div
    def tofloat(self) -> float:
        try:
            return(float(self.n / self.div))
        except ZeroDivisionError:
            return(float('inf'))
    def __add__(self,other):
        if type(other) == int:
            return Fraction((self.n + other * self.div),self.div)
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div,other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return Fraction((self.n * mymult + other.n * urmult),mult)
        elif type(other) == float:
            f = other.as_integer_ratio()
            f = Fraction(f[0],f[1]).simplify()
            mult = MathMisc.cmmmc(self.div,f.div)
            mymult = mult // self.div
            urmult = mult // f.div
            return Fraction((self.n * mymult + f.n * urmult),mult)
        else:
            raise TypeError
    def __sub__(self,other):
        if type(other) == int:
            return Fraction((self.n - other * self.div),self.div)
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div,other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return Fraction((self.n * mymult - other.n * urmult),mult)
        elif type(other) == float:
            f = other.as_integer_ratio()
            f = Fraction(f[0],f[1]).simplify()
            mult = MathMisc.cmmmc(self.div,f.div)
            mymult = mult // self.div
            urmult = mult // f.div
            return Fraction((self.n * mymult - f.n * urmult),mult)
        else:
            raise TypeError
    def __mult__(self,other):
        if type(other) == int:
            return Fraction((self.n * other),self.div)
        elif type(other) == type(self):
            return Fraction((self.n * other.n),self.div * other.div).simplify()
        elif type(other) == float:
            f = other.as_integer_ratio()
            f = Fraction(f[0],f[1]).simplify()
            return Fraction((self.n * f.n),self.div * f.div).simplify()
        else:
            raise TypeError
    def __truediv__(self,other):
        if type(other) == int:
            return Fraction(self.n,(self.div * other))
        elif type(other) == type(self):
            return Fraction((self.n * other.div),(self.div * other.n)).simplify()
        elif type(other) == float:
            f = other.as_integer_ratio()
            f = Fraction(f[0],f[1]).simplify()
            return Fraction((self.n * f.div),self.div * f.n).simplify()
        else:
            raise TypeError
    def copy(self):
        return Fraction(self.n,self.div)
    def simplify(self):
        d = self.div
        n = self.n
        c = MathMisc.cmmdc(d,n)
        d = d // c
        n = n // c
        self.div = d
        self.n = n
    def __eq__(self,other):
        if type(other) == int or type(other) == float:
            return (self.tofloat() == other)
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div,other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return ((self.n * mymult) == (other.n * urmult))
        else:
            raise TypeError
    def __ne__(self,other):
        return not (self == other)
    def __lt__(self,other):
        if type(other) == int or type(other) == float:
            return (self.tofloat() < other)
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div,other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return ((self.n * mymult) < (other.n * urmult))
        else:
            raise TypeError
    def __gt__(self,other):
        if type(other) == int or type(other) == float:
            return (self.tofloat() > other)
        elif type(other) == type(self):
            mult = MathMisc.cmmmc(self.div,other.div)
            mymult = mult // self.div
            urmult = mult // other.div
            return ((self.n * mymult) > (other.n * urmult))
        else:
            raise TypeError
    def __le__(self,other):
        return (self < other) or (self == other)
    def __ge__(self,other):
        return (self > other) or (self == other)
    def __pow__(self,other):
        if type(other) == int or type(other) == float:
            a = Fraction(self.n ** other,self.div ** other).tofloat().as_integer_ratio()
            return Fraction(a[0],a[1]).simplify()
        elif type(other) == type(self):
            a = Fraction(((self.n ** other.n) ** (1 / other.div)),((self.div ** other.n) ** (1 / other.div))).tofloat().as_integer_ratio()
            return Fraction(a[0],a[1]).simplify()
        else:
            raise TypeError
    def __str__(self):
        return str(self.n) + '/' + str(self.div)
    def __repr__(self):
        return 'Fraction(' + str(self.n) + ',' + str(self.div) + ')'
def waituntil(cond : str,vars : dict={},interval : int=0.01):
    while not eval(cond,vars):
        time.sleep(interval)
@forbiddenfruit.curses(dict,'index')
def index_dict(self,value) -> Any:
    if value in self.values():
        return list(self.keys())[list(self.values()).index(value)]
    else:
        raise IndexError("Key with value " + str(value) + " does not exist.")
@forbiddenfruit.curses(dict,'hash')
def hash_dict(self) -> int:
    return hash(json.dumps(copy.deepcopy(self), sort_keys=True))
def update_obj(obj,old,new):
    immuttables = (tuple,str,type(dict().keys()),type(dict().values()),set,frozenset)
    if type(obj) in immuttables:
        ty = type(obj)
        f = list(obj)
        f[f.index(old)] = new
        f = ty(f)
        for j in gc.get_referrers(obj):
            update_obj(j,obj,f)
    else:
        if type(obj) == dict or type(obj) == list:
            obj[obj.index(old)] = new
def getError():
    return traceback.format_exc()
class AttributableObject:
    def __init__(self) -> None:
        pass
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
    colors = ['\033[0m','\033[94m','\033[92m','\033[96m','\033[91m','\033[95m','\033[93m','\033[0m\033[1m']
    types = ['\033[0m','\033[1m','\033[4m','\033[1m\033[4m']
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
class enhancedobject(object):
    @classmethod
    def __new__(cls,*args,**kwargs) -> enhancedobject:
        self = object.__new__(cls)
        self.__initialized = False
        self.__preinitialized = False
        self.__deleted = False
        self.deleted = False
        cls.onpreinit(self,*args,**kwargs)
        self.__preinitialized = True
        return self
    def __init__(self,*args,**kwargs) -> None:
        self.oninit(*args,**kwargs)
        self.__initialized = True
    def __hash__(self) -> int:
        return hash(json.dumps(copy.deepcopy(self.__dict__), sort_keys=True))
    def __eq__(self,other : object) -> bool:
        if (self.__class__.__mro__[-2] is other.__class__.__mro__[-2]):
            return hash(self) == hash(other)
        else:
            return False
    def __repr__(self) -> str:
        if self.__initialized:
            return str(self.__class__).replace("<class '","").replace("'>","") + '@' + hex(id(self)).replace("0x","__").upper().replace("__","0x")
        else:
            return str(self.__class__).replace("<class '","").replace("'>","") + '(uninitialized)@' + hex(id(self)).replace("0x","__").upper().replace("__","0x")
    def __str__(self) -> str:
        return self.__repr__()
    def shallowCopy(self) -> enhancedobject:
        """Shallowcopy the object"""
        return copy.copy(self)
    def deepCopy(self) -> enhancedobject:
        """Deepcopy the object"""
        return copy.deepcopy(self)
    def equals(self,other : object) -> bool:
        """Checks if an object is equal to the other."""
        if (self.__class__.__mro__[-2] is other.__class__.__mro__[-2]):
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
    def __ne__(self,other : enhancedobject) -> bool:
        return not self.__eq__(other)
    @classmethod
    def headlessnew(cls,*args,**kwargs) -> None:
        """Returns an uninitialized instance of this class."""
        return cls.__new__(cls,*args,**kwargs)
    def onpreinit(self,*args,**kwargs) -> None:
        pass
    def oninit(self,*args,**kwargs) -> None:
        pass
    @classmethod
    def new(cls,*args,**kwargs) -> None:
        """Returns an initialized instance of this class."""
        obj = cls.__new__(*args,**kwargs)
        if isinstance(obj,cls):
            obj.init(*args,**kwargs)
        return obj
    def init(self,*args,**kwargs) -> None:
        """Initializes the object, if its already initialized, throws a Warning"""
        if not self.__initialized:
            self.__init__(*args,**kwargs)
        else:
            raise AlreadyInitializedWarning
    def ondelete(self,deletedalready=False) -> None:
        pass
    def ongcdelete(self) -> None:
        print_debug("EnhancedObject Object has been deleted by GC.")
    def delete(self,force=False) -> None:
        self.ondelete()
        ref = gc.get_referrers(self)
        immuttables = (tuple,str,type(dict().keys()),type(dict().values()),set,frozenset)
        for i in ref:
            if not inspect.isframe(i):
                if type(i) in immuttables:
                    ty = type(i)
                    f = list(i)
                    f.remove(self)
                    f = ty(f)
                    for j in gc.get_referrers(i):
                        update_obj(j,i,f)
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
    def getReferenceCount(self) -> Tuple[int,int]:
        """Returns reference count from the sys module.
        0th position in tuple is total references
        1st position in tuple is active references"""
        return (sys.getrefcount(self) - 3,self.getActiveReferencesCount())
    def getWeakReferenceCount(self) -> int:
        """Returns weak reference count from the sys module."""
        return weakref.getweakrefcount(self)
    def getWeakReferences(self) -> list:
        """Gets the weak references of the object."""
        return weakref.getweakrefs(self)
    def getWeakRef(self) -> weakref.ReferenceType:
        """Returns a weak reference of the object."""
        return weakref.ref(self)
    def hash(self) -> int:
        """Returns the object's hash."""
        return hash(self)
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
        for _ in range(self.getReferenceCount()[0]):pythonapi.Py_DecRef(e)
def printError():
    print(terminalcolors.red + traceback.format_exc() + terminalcolors.reset)
    return terminalcolors.red + traceback.format_exc() + terminalcolors.reset
class Shell:
    def __init__(self) -> None:
        self.running = False
        self.locals = {'self':self,'exit':self.exit}
        self.isolglobals = {}
        self.globals = globals()
        self.__isolated = False
        self.__isolpass = "XcZq"
        self.canexitisol = True
        self.__isolexitstage = 0
    def run(self,globalss={}) -> None:
        self.running = True
        self.globals = globalss
        while self.running:
            try:
                self.shellc(input('>>> '))
            except KeyboardInterrupt:
                print('')
                printError()
    def shellc(self,c) -> Exception:
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
                c = c.replace("locals()",str(self.locals))
                try:
                    if self.__isolated:
                        c = c.replace("globals()",str(self.isolglobals))
                        print(eval(c,self.isolglobals,self.locals))
                    else:
                        print(eval(c,self.globals,self.locals))
                except SyntaxError:
                    if self.__isolated:
                        exec(c,self.isolglobals,self.locals)
                    else:
                        exec(c,self.globals,self.locals)
                return None
            except Exception as e:
                printError()
                return e
    def runc(self,c) -> Exception:
        """Runs command"""
        if self.__isolexitstage == 0:
            if c == ">EXITISOL<" and self.canexitisol and self.__isolated:
                self.__isolexitstage = 1
            else:
                try:
                    c = c.replace("locals()",str(self.locals))
                    if self.__isolated:
                        c = c.replace("globals()",str(self.isolglobals))
                        exec(c,self.isolglobals,self.locals)
                    else:
                        exec(c,self.globals,self.locals)
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
    def enterisol(self,passwrd="XcZq",eraselocals=False) -> None:
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
    def exitisol(self,passwrd="") -> None:
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
def isolated_exec(code : str,globals : dict={},locals : dict={}):
    shl = Shell()
    shl.enterisol("",True)
    shl.locals = locals
    shl.isolglobals = globals
    shl.canexitisol = False
    return shl.runc(code)
def print_color(string : str,color : int=0,thetype : int=0,end : str="\n") -> None:
    """Prints colorful!
    String: string to be printed
    Color(default 0): Color, for more info, do terminalcolors.colortest
    Type(default 0): Type, for more info, do terminalcolors.typetest
    End(default \\n): End of print"""
    print(terminalcolors.reset + terminalcolors.types[thetype % terminalcolors.types.__len__()] + terminalcolors.colors[color % terminalcolors.colors.__len__()] + string + terminalcolors.reset,end=end)
def print_rainbow(string : str,thetype : int=0,end : str="\n") -> None:
    """Prints text in rainbow!
    String: string to be printed
    Type(default 0): Type, for more info, do terminalcolors.typetest
    End(default \\n): End of print"""
    print(rainbowify(string,thetype),end=end)
def rainbowify(string : str,thetype : int=0) -> str:
    """Rainbowifies string, makes it rainbow when printed."""
    newstr = copy.copy(terminalcolors.types[thetype % 4])
    i = 0
    rainbow = (terminalcolors.red,terminalcolors.yellow,terminalcolors.green,terminalcolors.cyan,terminalcolors.blue,terminalcolors.magenta)
    for c in string:
        newstr += rainbow[i] + c
        i += 1
        i %= 6
    return newstr + terminalcolors.reset
class PropertyFunc:
    def __init__(self,funcget,funcset):
        self.fget = funcget
        self.fset = funcset
    def __get__(self,instance,cls):
        return self.fget(instance)
    def __set__(self,instance,value):
        return self.fset(instance,value)
def print_info(string : str,end : str="\n"):
    print_color("[" + gettime() + " INFO]: " + string,1,0,end)
def print_warn(string : str,end : str="\n"):
    print_color("[" + gettime() + " WARN]: " + string,6,0,end)
def print_err(string : str,end : str="\n"):
    print_color("[" + gettime() + " ERROR]: " + string,4,0,end)
def print_fatalerr(string : str,end : str="\n"):
    print_color("[" + gettime() + " FATAL ERROR]: " + string,4,1,end)
def print_debug(string : str,end : str="\n"):
    print_color("[" + gettime() + " DEBUG]: " + string,3,0,end)
def print_extra(string : str,color : int=1,typeofmessage : str="INFO",thetype : int=0,end : str="\n"):
    print_color("[" + gettime() + " " + typeofmessage + "]: " + string,color % 8,thetype,end)
def make2digit(num : str):
    while len(num) < 2:
        num = "0" + num
    return num
def gettime():
    thetime = time.localtime(time.time())
    months = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Dec")
    return make2digit(str(thetime.tm_mday)) + " " + months[thetime.tm_mon - 1] + " " + make2digit(str(thetime.tm_year)) + " " + make2digit(str(thetime.tm_hour)) + ":" + make2digit(str(thetime.tm_min)) + ":" + make2digit(str(thetime.tm_sec))
def getdir(obj : object,noreserved : bool=False) -> list:
    thedir = dir(obj)
    e = []
    for i in thedir:
        if noreserved and i.startswith("__") and i.endswith("__"):continue
        e.append((i,eval("obj." + str(i),{},{'obj' : obj})))
    return e
def objtodict(obj : object) -> dict:
    thedir = dir(obj)
    e = {}
    for i in thedir:
        e[i] = eval("obj." + str(i),{},{'obj' : obj})
    return e
def getdirstr(obj : object,noreserved : bool=False) -> str:
    thedir = dir(obj)
    e = ""
    for i in thedir:
        if i == "__dict__":continue
        if noreserved and i.startswith("__") and i.endswith("__"):continue
        e += "(\"" + str(i) + "\", " + str(eval("obj." + str(i),{},{'obj' : obj})) + ")\n"
    return e[:-1]
class thread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=True):
        if name is None:
            name = "Thread-" + hex(id(self)).replace("0x","__").upper().replace("__","0x")
        threading.Thread.__init__(self,group=group,target=target,name=name,args=args,kwargs=kwargs,daemon=daemon)
        self.name = name
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def kill(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit(-1)))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print_err("Kill thread failure. Thread ID:" + thread_id + " Thread Name:" + self.name)
class run_with_multiprocessing(multiprocessing.Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        multiprocessing.Process.__init__(self,group,target,name,args,kwargs,daemon)
        self.start()
def run_with_disabled_keyboardinterrupt(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=True):
    thr = threading.Thread.__init__(self,group,target,name,args,kwargs,daemon)
    thr.start()
    thr.join()
try:
    import psutil
except:
    print_warn("Psutil import error.")
if psutil is not None:
    def getAvailMem() -> float:
        """Available Memory in MB."""
        return psutil.virtual_memory().available / 1024 ** 2
    def checkMem(threshold : int=250,freeze : bool=True,printwarn : bool = True) -> int:
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
                print_warn("Out of memory warning. Available memory is under the threshold of " + str(threshold) + " megabytes.")
                print_warn("Program has frozen. Program will automatically unfreeze until available memory is over threshold.")
            waituntil("threshold < getAvailMem()",{"getAvailMem":getAvailMem,"threshold":threshold},1)
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
def servcontosock(connection : Tuple[socket.socket,Tuple[str,int]]):
    sock = Socket(connection[1],connection[0])
    return sock
class Socket(enhancedobject):
    """A network socket. You can send anything through it."""
    def oninit(self,address : Tuple[str,int],thesocket : socket.SocketType=None,**kwargs):
        """Create a new socket on address"""
        self.address = address
        if thesocket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(address)
        else:
            self._socket = thesocket
        self.issocketclosed = False
    def send(self,data,internalinstruction=False) -> None:
        """Sends data. It gets converted into a bytes object by pickle module and sent."""
        if not self.issocketclosed:
            try:
                self._socket.send(
                    pickle.dumps(
                        {
                            "internal":internalinstruction,
                            "message":data
                        }
                    )
                )
            except ConnectionResetError:
                self.issocketclosed = True
                raise
    def read(self,buffer_size : int) -> Any:
        """Reads data.\n
        It gets returned as a bytes object if decode is False"""
        if not self.issocketclosed:
            try:
                data = pickle.loads(self._socket.recv(buffer_size))
                return data
            except ConnectionResetError:
                self.issocketclosed = True
                raise
            except pickle.PickleError:
                print_err("Connection error. Socket id {sockid} will be closed.".format(sockid=id(self)))
                self.send(self.internalinstr("disconnect","PickleError"),True)
                self.close()
                self.issocketclosed = True
    @staticmethod
    def internalinstr(inst,arg1=None,arg2=None):
        instructions = {
            "disconnect":{
                "type":"disconnect",
                "message":str(arg1)
            }
        }
        return instructions[inst]
    def close(self):
        try:
            self._socket.close()
            self.issocketclosed = True
        except ConnectionResetError:
            pass
class ListeningServerSocket(enhancedobject):
    """A listening network socket."""
    def oninit(self, address: Tuple[str, int]):
        """Make a listening network socket on the address."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._socket.listen(4)
        self.newconnections : List[Socket] = []
        self.connections : List[Socket]= []
        self.listening = False
        self.__listeningthread = None
    def listen(self,functonconnect : FunctionType=None):
        if not self.listening:
            self.listening = True
            self.__listeningthread = thread(target=self.__class__.__listen,args=(self,functonconnect))
            self.__listeningthread.start()
    def __listen(self,functonconnect):
        while True:
            c = servcontosock(self._socket.accept())
            self.connections.append(c)
            self.newconnections.append(c)
            if functonconnect is not None:
                functonconnect(c)
            self.checkforclosedcons()
    def checkforclosedcons(self):
        for index,i in enumerate(self.connections):
            if i.issocketclosed:
                del self.connections[index]
        for index,i in enumerate(self.newconnections):
            if i.issocketclosed:
                del self.newconnections[index]
def __dir__():
    l = [
        "passkw",
        "dict_keys","dict_values","function","module",
        "CacherMap","Cacher",
        "MathMisc","primenum","Fraction",
        "waituntil",
        "update_obj",
        "getError","printError",
        "AttributableObject","enhancedobject",
        "AlreadyInitializedWarning",
        "terminalcolors","print_color","print_rainbow","rainbowify"
        "PropertyFunc",
        "Shell","isolated_exec",
        "print_info","print_warn","print_err","print_fatalerr","print_extra","print_debug",
        "make2digit","gettime",
        "getdir","getdirstr","objtodict",
        "thread","run_with_multiprocessing","run_with_disabled_keyboardinterrupt",
        "getAvailMem","checkMem",
        #"Socket","ListeningServerSocket","servcontosock",
        "__dir__","pythonapi",
        "CString","ctypes"
        ]
    l.sort()
    return l
pythonapi = ctypes.pythonapi
if __name__ == "__main__":
    Shell().run(globals())
