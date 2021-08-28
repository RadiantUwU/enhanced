# enhanced
Python module that adds lots of common stuff

Features:

> Hashing of dictionaries

> Colored text (colorify_high for 24 bit colors, colorify supplies only 8 colors, rainbowify for making text rainbow, print_color, print_rainbow)

> Colored Logging (print_debug,print_info,print_warn,print_err,print_fatalerr,print_extra is for logging in a custom way)

> .toString() to **all** objects, calls \_\_str\_\_()

> .hash() also to all objects, calls \_\_hash\_\_()

> Getting objects from ID (get_obj_from_id, not recommended, use weak references)

> Easy networking (ListeningServerSocket,Socket)

> Threading support (run_as_thread,run_with_thread(returns thread),run_func_with_thread(wrapper which returns thread on function executed))

> Easy function for getting input with a specific condition(get_from_choice_with_cond, where inp inside the eval function is input)

> Unfrozen tuples (unfrozentuple, adds .unfreeze() to basic tuple)

> Function to check if an object is iterable (isiterable)

> New method try_delete() to dict, attempts deletion of key, if non existent does not throw error

> New method index() to dict, works like on lists

> Function to get only a character getch

> Functions to do memory related stuff (getAvailMem returns megabytes of free memory, checkMem to check if memory is under a threshold)

> Cacher class

> Unoptimized prime number generator `prime_num`, Cacher object

> always_return function which returns another function that always returns the value given, not caring about the arguments given to it.

> pass_func which returns `None` always, not caring about the arguments
