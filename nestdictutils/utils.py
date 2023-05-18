#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    nestdictutils.py
#
#    Dictionary utility functions for nested dictionaries.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public
#    License along with this program. 
#    If not, see <http://www.gnu.org/licenses/>.


# Standard library
import collections
import copy
import itertools
import logging as log


# Get the module's logger
logger = log.getLogger(__name__)


def recursive_get_values_from_key(d,
                                  key):
    """Given a key, returns a list of all values in the dictionary
    associated with it. Since the dictionary may be nested, the
    same key could be found at different levels. In this case, the
    list will contains all values the key has been found associated
    with. 

    Parameters
    ----------
    d : ``dict``
        Input dictionary.

    key : any immutable object
        Key of interest.

    Returns
    -------
    ``list``
        List of values associated with the key of interest.

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}}}

        # Get all values associated with the key 3
        >>> nestdictutils.recursive_get_values_from_key(d, 3)
        [{4: 5}, {7: 8}]
    """

    # Initialize an empty list to store all the values
    # found associated with the given key
    values = []

    # Define the recursive step internally so that the 'values'
    # argument is not exposed to the user in the function
    def recursive_step(d,
                       key,
                       values):

        # If the key is found in the dictionary
        if key in d.keys():

            # Append the value to the list
            values.append(d[key])

        # For each key, value pair in the dictionary
        for k, val in d.items():
            
            # If the value is a dictionary
            if isinstance(val, dict):
                
                # Recursively try to find the value
                # in the dictionary
                recursive_step(d = val, 
                               key = key,
                               values = values)

    # Call the recursive function
    recursive_step(d = d,
                   key = key,
                   values = values)

    # Return the list modified in place
    return values


def recursive_get_values_from_keys(d,
                                   keys):
    """Given a set of keys, returns a list of all values in the
    dictionary associated with them (since it may be a nested
    dictionary, the same key could be found at different levels).

    Parameters
    ----------
    d : ``dict``
        Input dictionary.

    keys : an iterable of immutable objects
        Keys of interest.

    Returns
    -------
    ``dict``
        Dictionary of values associated with the corresponding
        keys of interest.

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}}}
        
        # Get all values associated with the keys 3 and 6
        >>> nestdictutils.recursive_get_values_from_keys(d, [3, 6])
        {3: [{4: 5}, {7: 8}], 6: [{3: {7: 8}}]}
    """

    # Call 'recursive_get_values_from_key' on each key
    return {key : recursive_get_values_from_key(d = d,
                                                key = key) \
            for key in keys}


def recursive_get_key_paths(d,
                            value):
    """Get a list of "key paths" (= sequences of keys) to access
    a specific value inside the dictionary. If the value is present
    only once inside the dictionary, the output list will contain
    only one element.

    Parameters
    ----------
    d : ``dict``
        Input dictionary.

    value : any object apart from ``dict``
        Value whose "key paths" will be reported.

    Returns
    -------
    ``list``
        List of "key paths".

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
        
        # Get the "key paths" to the value 7
        >>> nestdictutils.recursive_get_key_paths(d, 7)
        [([6, 3], 7), ([6], 7), ([], 7)]

        # Note that the last "key path" is empty because
        # 7 is a key of the outer dictionary  
    """
    
    # Recursive step to traverse the dictionary
    def recursive_step(d,
                       key_path,
                       value,
                       key_paths):

        # For each key, value pair in the current dictionary
        for key, val in d.items():

            # If the key is the value of interest
            if key == value:

                # Append the "key path" to the key to the list
                # of "key paths"
                key_paths.append((key_path, key))
            
            # If the value is itself a dictionary (we are
            # not at a "leaf" value of the dictionary)
            if isinstance(val, dict):
                
                # Add all "key paths" recursively found starting
                # from the value (since it is a dictionary).
                recursive_step(d = val, 
                               key_path = key_path + [key],
                               value = value,
                               key_paths = key_paths)
            
            # If the value is the one of interest
            if val == value:

                if (key_path + [key], val) not in key_paths:
                
                    # Append the "key path" found to the list
                    key_paths.append((key_path + [key], val))
        
        # Return all key paths found
        return key_paths

    # Call the recursive function starting from the original
    # dictionary and an empty list (since when starting
    # traversing the dictionary we have no "key paths"
    # found)
    return recursive_step(d = d,
                          key_path = [],
                          value = value,
                          key_paths = [])


def recursive_iter_key_paths(d):
    """Recursively iterate over a dictionary and return a list
    of tuples containing the "key path" (= sequence of keys)
    to reach each point in the dictionary and the value that
    each "key path" leads to.

    Parameters
    ----------
    d : ``dict``
        Input dictionary.

    Returns
    -------
    ``generator``
        Generator of "key paths".

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
        
        # Get the "key paths" for all items in the dictionary
        # and list them
        >>> list(nestdictutils.recursive_iter_key_paths(d))
        [([1], 2), ([3, 4], 5), ([3], {4: 5}), ([6, 3, 7], 8),
        ([6, 3], {7: 8}), ([6, 7], 10), ([6], {3: {7: 8}, 7: 10}),
        ([7], 11)]
    """
    
    # Recursive step to traverse the dictionary
    def recursive_step(d,
                       key_path):
        
        # For each key, value pair in the current dictionary
        for key, val in d.items():
            
            # If the value is itself a dictionary (we are
            # not at a "leaf" value of the dictionary)
            if isinstance(val, dict):
                
                # Add all "key paths" recursively found starting
                # from the value (since it is a dictionary).
                yield from \
                    recursive_step(d = val,
                                   key_path = key_path + [key])
            
            # Append the "key paths" found to the list (the
            # first element is the "key path" leading to
            # some value, the second element is the value
            # itself)
            yield (key_path + [key], val)
    
    # Call the recursive function starting from the original
    # dictionary and an empty list (since when starting
    # traversing the dictionary we have no "key paths"
    # found)
    yield from recursive_step(d = d,
                              key_path = [])


def recursive_add(d,
                  key_path,
                  in_place = False):
    """Recursively add to a dictionary from a "key path"
    (= sequence of keys) and the associated value.

    Parameters
    ----------
    d : ``dict``
        Input dictionary.

    key_path : ``tuple``
        The "key path" and the associated value.

    in_place : ``bool``, default: ``False``
        Whether to modify the input dictionary in place
        or return a new dictionary.

    Returns
    -------
    ``dict`` or ``None``
        Either a new dictionary (if ``in_place`` is ``False``)
        or ``None`` (if ``in_place`` is ``True``).

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
        
        # Add an element to the {7:8} inner dictionary and return
        # a new dictionary
        >>> new_d = nestdictutils.recursive_add(d, ((6, 3, 12), 13), False)
        >>> new_d
        {1: 2, 3: {4: 5}, 6: {3: {7: 8, 12: 13}, 7: 10}, 7: 11}

    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}

        # Try to add a new element associated with key 7 in the
        # {7:8} inner dictionary
        >>> new_d = nestdictutils.recursive_add(d, ((6, 3, 7, 12), 13), False)
        You cannot add element '13' at position (6, 3, 7, 12) because
        at least one key in the path is not associated with a
        dictionary.
        >>> new_d
        {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
    """
    
    # Recursive step to traverse the dictionary
    def recursive_step(d,
                       key_path,
                       value,
                       init_key_path):
        
        # If 'd' is a dictionary
        if isinstance(d, dict):
        
            # If the "key path" contains only one key (= we have
            # reached a "leaf" value)
            if len(key_path) == 1:

                # Add the value to the dictionary at the
                # corresponding key
                d[key_path[0]] = value
            
            # If the "key path" contains more than one key (we are
            # somewhere in the middle of the dictionary that we
            # are building)
            else:

                # If the first key of the "key path" is not
                # in the dictionary
                if key_path[0] not in d:

                    # Add the key associated with an empty
                    # dictionary (that will be populated in the
                    # recursive calls since we know we have not
                    # reached the end of this "key path" yet)
                    d[key_path[0]] = {}

                # Recursively traverse the current "key path"
                recursive_step(d = d[key_path[0]],
                               key_path = key_path[1:],
                               value = value,
                               init_key_path = init_key_path)

        # Otherwise
        else:

            # Warn the user that they cannot add an element
            # at that position because the key is not
            # associated with a dictionary (therefore,
            # no additional key can be added)
            warnstr = \
                f"It was not possible to add element '{value}' " \
                f"at position {repr(init_key_path)} " \
                f"because at least one key in the path is not " \
                f"associated with a dictionary."
            logger.warning(warnstr)

            # Return
            return

    # If the dictionary should not be modified in place
    if not in_place:

        # Create a copy of the input dictionary
        new_d = copy.deepcopy(d)

    # Otherwise
    else:

        # Reference the original dictionary
        new_d = d

    # Split the key path passed by the user into the path
    # itself and the value associated to it
    path, value = key_path

    # Add the "key path" and its value to either the
    # input dictionary or the new dictionary.
    # The 'init_key_path' will hold the initial key path
    # for all the recursion steps so that, in case the
    # user tries to insert an element into an invalid
    # position, the warning will be informative.
    recursive_step(d = new_d,
                   key_path = path,
                   value = value,
                   init_key_path = path)

    # If the original dictionary was not modified in place
    if not in_place:

        # Return the new dictionary
        return new_d


def recursive_replace(d,
                      key_path,
                      in_place = False):
    """Recursively replace a value in a dictionary from a
    "key path" (= sequence of keys) and the associated value.

    Parameters
    ----------
    d : ``dict``
        Input dictionary.

    key_path : ``tuple``
        The "key path" and the associated value.

    in_place : ``bool``, default: ``False``
        Whether to modify the input dictionary in place
        or return a new dictionary.

    Returns
    -------
    ``dict`` or ``None``
        Either a new dictionary (if ``in_place`` is ``False``)
        or ``None`` (if ``in_place`` is ``True``).

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
        
        # Replace element 5 in the {4: 5} inner dictionary
        # with 4
        >>> new_d = nestdictutils.recursive_replace(d, ((3, 4), 4), False)
        >>> new_d
        {1: 2, 3: {4: 4}, 6: {3: {7: 8}, 7: 10}, 7: 11}
    """
    
    # Recursive step to traverse the dictionary
    def recursive_step(d,
                       key_path,
                       key_path_list):

        # If the "key path" contains only one key (= we have
        # reached a "leaf" value)
        if len(key_path[0]) == 1:

            # Add the key that was not found to the
            # list representation of the key path
            key_path_list += [key_path[0][0]]

            # Try to access the key
            try:

                val = d[key_path[0][0]]

            # If the key was not found
            except KeyError:

                # Compose a more verbose error message and
                # re-raise the exception
                errstr = \
                    f"The key path {repr(key_path_list)} " \
                    f"does not exist."
                raise KeyError(errstr)

            d[key_path[0][0]] = key_path[1]
        
        # If the "key path" contains more than one key (we are
        # somewhere in the middle of the dictionary that we
        # are building)
        else:

            # If the first key of the "key path" is not
            # in the dictionary
            if key_path[0][0] in d:

                # Recursively traverse the current "key path"
                recursive_step(\
                    d = d[key_path[0][0]],
                    key_path = (key_path[0][1:], key_path[1]),
                    key_path_list = key_path_list + [key_path[0][0]])

    # If the dictionary should not be modified in place
    if not in_place:

        # Create a copy of the input dictionary
        new_d = copy.deepcopy(d)

    # Otherwise
    else:

        # Reference the original dictionary
        new_d = d

    # Add the "key path" and its value to either the
    # input dictionary or the new dictionary
    recursive_step(d = new_d,
                   key_path = key_path,
                   key_path_list = [])

    # If the original dictionary was not modified in place
    if not in_place:

        # Return the new dictionary
        return new_d


def recursive_remove(d,
                     key_path,
                     in_place = False):
    """Recursively remove a value in a dictionary given its
    "key path" (= sequence of keys) in the dictionary.
    
    Parameters
    ----------
    d : ``dict``
        Input dictionary.

    key_path : ``tuple``
        The "key path" and the associated value.

    in_place : ``bool``, default: ``False``
        Whether to modify the input dictionary in place
        or return a new dictionary.

    Returns
    -------
    ``dict`` or ``None``
        Either a new dictionary (if ``in_place`` is ``False``)
        or ``None`` (if ``in_place`` is ``True``).

    Raises
    ------
    ``KeyError``
        If the "key path" is not found in the input dictionary.

    ``ValueError``
        If the "key path" is found in the input dictionary, but
        it is associated to a value different from the one
        provided.

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
        
        # Remove element 11 in the outer dictionary
        >>> new_d = nestdictutils.recursive_remove(d, ((7,), 11), False)
        >>> new_d
        {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}}

        # Note how also the associated key has been removed from the
        # dictionary

    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}

        # Remove element 5 in the inner dictionary {4: 5}
        >>> new_d = nestdictutils.recursive_remove(d, ((3, 4), 5), False)
        >>> new_d
        {1: 2, 3: {}, 6: {3: {7: 8}, 7: 10}, 7: 11}

        # Note how also the associated key has been removed from the
        # dictionary

    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}

        # Try to remove element 5 given a nonexistent path (3, 6)
        >>> new_d = nestdictutils.recursive_remove(d, ((3, 6), 5), False)
        KeyError: 'The key path (3, 6) does not exist.'

    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}

        # Try to remove a nonexistent element 6 from the inner
        # dictionary {4: 5}
        >>> new_d = nestdictutils.recursive_remove(d, ((3, 4), 6), False)
        ValueError: The key path (3, 4) was found, but its associated value
        in the provided key path (6) does not correspond to the one found
        in the dictionary (5).
    """
    
    # Recursive step to traverse the dictionary
    def recursive_step(d,
                       key_path,
                       key_path_list):

        if isinstance(d, dict):

            # If the "key path" contains only one key (= we have
            # reached a "leaf" value)
            if len(key_path[0]) == 1:

                # Add the key that was not found to the
                # list representation of the key path
                key_path_list += [key_path[0][0]]

                # Try to access the key
                try:

                    val = d[key_path[0][0]]

                # If the key was not found
                except KeyError:

                    # Compose a more verbose error message and
                    # re-raise the exception
                    errstr = \
                        f"The key path {repr(key_path_list)} " \
                        f"does not exist."
                    raise KeyError(errstr)

                # If the associated value does not correspond to the one
                # we expect
                if val != key_path[1]:

                    # Raise an exception
                    errstr = \
                        f"The key path {repr(key_path_list)} " \
                        f"was found, but its associated value in the " \
                        f"provided key path ({repr(key_path[1])}) does not " \
                        f"correspond to the one found in the " \
                        f"dictionary ({repr(val)})."
                    raise ValueError(errstr)

                # Remove the key and associated value
                del d[key_path[0][0]]
            
            # If the "key path" contains more than one key (we are
            # somewhere in the middle of the dictionary that we
            # are building)
            else:

                # If the first key of the "key path" is
                # in the dictionary
                if key_path[0][0] in d:

                    # Recursively traverse the current "key path"
                    recursive_step(\
                        d = d[key_path[0][0]],
                        key_path = (key_path[0][1:], key_path[1]),
                        key_path_list = key_path_list + [key_path[0][0]])

    # If the dictionary should not be modified in place
    if not in_place:

        # Create a copy of the input dictionary
        new_d = copy.deepcopy(d)

    # Otherwise
    else:

        # Reference the original dictionary
        new_d = d

    # Add the "key path" and its value to either the
    # input dictionary or the new dictionary
    recursive_step(d = new_d,
                   key_path = key_path,
                   key_path_list = [])

    # If the original dictionary was not modified in place
    if not in_place:

        # Return the new dictionary
        return new_d


def recursive_pop(d,
                  keys,
                  in_place = False):
    """Recursively remove specific keys (and the
    associated values) from a dictionary.

    Parameters
    ----------
    d : ``dict``
        Input dictionary.

    keys : an iterable of immutable objects
        The keys to be removed.

    in_place : ``bool``, default: ``False``
        Whether to modify the input dictionary in place
        or return a new dictionary.

    Returns
    -------
    ``dict`` or ``None``
        Either a new dictionary (if ``in_place`` is ``False``)
        or ``None`` (if ``in_place`` is ``True``).

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
        
        # Remove keys 3 and 7 and associated values
        >>> new_d = nestdictutils.recursive_pop(d, (3, 7), False)
        >>> new_d
        {1: 2, 6: {}}

        # Note that all occurrences of the keys have been removed
        # from the dictionary, not just their outermost instances      
    """
    
    # If the current object is a dictionary
    if isinstance(d, dict):

        # Recursively return dictionaries where
        # the keys of interest are removed
        return \
            {key: recursive_pop(d = val, 
                                keys = keys) \
             for key, val in d.items() \
             if key not in keys}

    # Otherwise
    else:

        # Return the object
        return d


def recursive_build(key_paths):
    """Recursively build a dictionary from "key paths"
    (= sequence of keys) and their associated values.

    Parameters
    ----------
    key_paths : any iterable of "key paths"
        The "key paths".

    Returns
    -------
    ``dict``
        The dictionary built from the "key paths".

    Examples
    --------
    .. code-block:: python

        # Define the key paths
        >>> key_paths = (((1,2),3), ((4,),5))
        
        # Build the dictionary
        >>> d = nestdictutils.recursive_build(key_paths)
        >>> d
        {1: {2: 3}, 4: 5}

    .. code-block:: python

        # Define the key paths
        >>> key_paths = (((1,2),3), ((4,),5), ((4,),6))
        
        # Build the dictionary
        >>> d = nestdictutils.recursive_build(key_paths)
        >>> d
        {1: {2: 3}, 4: 6}
        You provided several instances of the key path ((4,)).
        Only ((4,), 5) will be used when building the dictionary.
    """

    # Create an empty dictionary to fill
    final_d = {}

    # Initialize an empty dictionary to store the unique key
    # paths provided
    unique_key_paths = {}
    
    # For each key path and associated value provided
    for key_path, value in key_paths:
        
        # If the key path has not been seen yet
        if key_path not in unique_key_paths:

            # Add it to the dictionary of unique key paths
            unique_key_paths[key_path] = value
        
        # Otherwise
        else:
            
            # Warn the user that the path has been seen already
            warnstr = \
                f"You provided several instances of the key path " \
                f"({repr(key_path)}). Only ({repr(key_path)}, " \
                f"{str(unique_key_paths[key_path])}) will be used " \
                f"when building the dictionary."
            logger.warning(warnstr)

    # For each key path provided
    for key_path in tuple(unique_key_paths.items()):

        # Update the dictionary
        recursive_add(d = final_d,
                      key_path = key_path,
                      in_place = True)

    # Return the final dictionary
    return final_d


def recursive_merge_dicts(dicts):
    """Merge two nested dictionaries.

    Parameters
    ----------
    dicts : iterable of `dict`
        Iterable of dictionaries to be merged.

    Returns
    -------
    ``merged_d`` : ``collections.defaultict``
        Merged dictionary.

    Notes
    -----
    If an identical key at an identical position is found in
    any two or more input dictionaries, the value in the dictionary
    that comes first in the iterable will be reported in the
    merged dictionary.

    If the value associated to the key in two or more input
    dictionaries is a dictionary, the key/value pairs from all these
    dictionaries will be reported in the merged dictionary.

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}

        # Create a second nested dictionary
        >>> d2 = {14: {15: 16}, 3: 6}
        
        # Merge the two dictionaries
        >>> new_d = nestdictutils.recursive_merge_dicts([d, d2])
        >>> new_d
        {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11, 14: {15: 16}}

    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}

        # Create a second nested dictionary
        >>> d2 = {14: {15: 16}, 3: {17: 18}}

        # Create a third nested dictionary
        >>> d3 = {6 : {3 : {9:10}}}
        
        # Merge the three dictionaries
        >>> new_d = nestdictutils.recursive_merge_dicts([d, d2, d3])
        >>> new_d
        {1: 2, 3: {4: 5, 17: 18}, 6: {3: {7: 8, 9: 10}, 7: 10},
        7: 11, 14: {15: 16}}
    """

    # Create a defaultdict to store the values of the final
    # dictionary
    merged_d = collections.defaultdict(collections.defaultdict)

    # Get the "key paths" to all points in all dictionaries
    # (use a generator to save memory in case the dictionaries
    # are big)
    key_paths_and_values = \
        itertools.chain.from_iterable(\
            recursive_iter_key_paths(d = d) for d in dicts)

    # Initialize a list of unique "key paths" and associated
    # values to keep track of the unique "key paths" found when
    # considering both dictionaries
    unique_key_paths = []
    
    # Initialize a list that will contain the "key paths"
    # and values that will be used to build the new
    # merged dictionary
    new_key_paths_and_values = []
    
    # For every "key path" and associated value in the
    # original combined list
    for key_path, val in key_paths_and_values:

        # If the "key path" has not been seet yet
        if not key_path in unique_key_paths:

            # Add it together with its associated value
            # to the new list
            new_key_paths_and_values.append((key_path, val))

            # Add the "key path" to the list of unique
            # "key paths"
            unique_key_paths.append(key_path)

    # For each "key path" and associated value in the
    # new list
    for key_path, value in new_key_paths_and_values:

        # Recursively build the merged dictionary
        recursive_add(d = merged_d,
                      key_path = (key_path, value),
                      in_place = True)

    # Return the merged dictionary
    return dict(merged_d)


def recursive_map_dict(d,
                       func,
                       keys = None,
                       in_place = False,
                       permissive = False):
    """Recursively traverse a dictionary mapping a function to the
    dictionary's leaf values (= substituting the values
    which the return value of the function applied to those
    values).

    Parameters
    ----------
    d : ``dict``
        The input dictionary.

    func : any callable
        Callable taking as inputs the leaf values of the dictionary
        and returning a value which will take the dictionary's
        place.

    keys : ``list``, ``set``, optional
        List of specific keys on whose items the mapping
        should be performed. This means that all values associated
        with keys different from those in the list will not be
        affected. If ``None``, all keys and associated values
        will be considered.

    in_place : ``bool``, default: ``False``
        Whether to modify the input dictionary in place
        or return a new dictionary.

    permissive : ``bool``, default: ``False``
        If ``True`` and ``func`` cannot be applied to some
        values, return the dictionary with those values untouched.

        If ``False``, raise an error if ``func`` cannot be
        applied to some values.
    
    Returns
    -------
    ``dict`` or ``None``
        Either a new dictionary (if ``in_place`` is ``False``)
        or ``None`` (if ``in_place`` is ``True``).

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
        
        # Define a function to raise all values to the power of two
        f = lambda x: x**2
        
        # Raise all values to the power of two
        >>> new_d = nestdictutils.map_dict(d, f, in_place = False)
        >>> new_d

    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: [2], 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 11}
        
        # Define a function to raise all values to the power of two
        f = lambda x: x**2
        
        # Raise all values to the power of two
        >>> new_d = nestdictutils.map_dict(d, f, in_place = False)
        >>> new_d
        Traceback (most recent call last):
            f = lambda x: x**2
                          ~^^~
        TypeError: unsupported operand type(s) for ** or pow():
        'list' and 'int'

        The above exception was the direct cause of the following
        exception:

        Traceback (most recent call last):

            new_d = nestdictutils.map_dict(d, f, in_place = False)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            raise Exception(errstr) from e
        Exception: Could not apply the function to [2].  
    """

    # Define the recursive step
    def recursive_step(d,
                       func,
                       keys,
                       permissive):

        # If the current object is a dictionary
        if isinstance(d, dict):
            
            # Get the keys of items on which the maping will be
            # performed. If no keys are passed, all keys
            # in the dictionary will be considered.
            sel_keys = keys if keys else d.keys()
            
            # For each key, value pair in the dictionary
            for k, v in list(d.items()):

                # If the value is a dictionary
                if isinstance(v, dict):
                    
                    # Recursively check the sub-dictionaries
                    # of the current dictionary
                    recursive_step(d = v,
                                   func = func,
                                   keys = keys,
                                   permissive = permissive)

                # Otherwise
                else:

                    # If the key is in the selected keys
                    if k in sel_keys:

                        # Try to apply the function to the value
                        try:

                            new_val = func(v)

                        # If something went wrong
                        except Exception as e:

                            # If not in permissive mode
                            if not permissive:
                                
                                # Raise an error
                                errstr = \
                                    f"Could not apply the function to " \
                                    f"{repr(v)}."
                                raise Exception(errstr) from e

                            # Otherwise, continue
                            continue

                        # Substitute the value with the return value
                        # of 'func' applied to it
                        d[k] = func(v)

    # If the dictionary should not be modified in place
    if not in_place:

        # Create a copy of the input dictionary
        new_d = copy.deepcopy(d)

    # Otherwise
    else:

        # Reference the original dictionary
        new_d = d

    # Add the "key path" and its value to either the
    # input dictionary or the new dictionary
    recursive_step(d = new_d,
                   func = func,
                   keys = keys,
                   permissive = permissive)

    # If the original dictionary was not modified in place
    if not in_place:

        # Return the new dictionary
        return new_d


def recursive_filter_dict(d,
                          func,
                          keys = None,
                          in_place = False,
                          permissive = False):
    """Recursively filter a dictionary's values. Only
    values for which the filter ``func`` returns ``True``
    will be kept, while the others (together with their
    associated keys) will be removed from the dictionary.

    Parameters
    ----------
    d : ``dict``
        The input dictionary.

    func : any callable
        Filtering callable taking as inputs the leaf values in
        the dictionary and returning ``True`` or ``False``.

    keys : ``list``, ``set``, optional
        List of specific keys on whose values the filtering
        should be performed. This means that all values associated
        with keys different from those in the list will not be
        affected. If ``None``, all keys and associated values
        will be considered.

    in_place : ``bool``, default: ``False``
        Whether to modify the input dictionary in place
        or return a new dictionary.

    permissive : ``bool``, default: ``False``
        If ``True`` and ``func`` cannot be applied to some
        values, return the dictionary with those values untouched.

        If ``False``, raise an error if ``func`` cannot be
        applied to some values.
    
    Returns
    -------
    ``dict`` or ``None``
        Either a new dictionary (if ``in_place`` is ``False``)
        or ``None`` (if ``in_place`` is ``True``).

    Examples
    --------
    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: 10}, 7: 2}
        
        # Define a function to filter out all values strictly
        # lower than 4
        f = lambda x: x > 4
        
        # Filter the dictionary
        >>> new_d = nestdictutils.map_dict(d, f, in_place = False)
        >>> new_d
        {3: {4: 5}, 6: {3: {7: 8}, 7: 10}}

        # Note that values lower than 4 are still kept as keys,
        # and only removed if they are values

    .. code-block:: python

        # Create a nested dictionary
        >>> d = {1: 2, 3: {4: 5}, 6: {3: {7: 8}, 7: [10]}, 7: 2}
        
        # Define a function to filter out all values strictly
        # lower than 4
        f = lambda x: x > 4
        
        # Filter the dictionary
        >>> new_d = nestdictutils.map_dict(d, f, in_place = False)
        >>> new_d
        Traceback (most recent call last):
            f = lambda x: x > 4
                          ^^^^^
        TypeError: '>' not supported between instances of 'list'
        and 'int'
        
        The above exception was the direct cause of the following
        exception:

        Traceback (most recent call last):

            new_d = nestdictutils.recursive_filter_dict(d, f, in_place = False)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            raise Exception(errstr) from e
        Exception: Could not apply the function to [10].  
    """
    
    # Define the recursive step
    def recursive_step(d,
                       func,
                       keys,
                       permissive):

        # If the current object is a dictionary
        if isinstance(d, dict):
            
            # Get the keys of items on which the filtering
            # will be performed. If no keys are passed, all keys
            # in the dictionary will be considered.
            sel_keys = keys if keys else d.keys()
            
            # For each key, value pair in the dictionary
            for k, v in list(d.items()):

                # If the value is a dictionary
                if isinstance(v, dict):
                    
                    # Recursively check the sub-dictionaries
                    # of the current dictionary
                    recursive_step(d = v,
                                   func = func,
                                   keys = keys,
                                   permissive = permissive)

                # Otherwise
                else:

                    # If the key is in the selected keys
                    if k in sel_keys:

                        # Try to apply the function to the value
                        try:

                            return_val = func(v)

                        # If something went wrong
                        except Exception as e:

                            # If not in permissive mode
                            if not permissive:
                                
                                # Raise an error
                                errstr = \
                                    f"Could not apply the function to " \
                                    f"{repr(v)}."
                                raise Exception(errstr) from e

                            # Otherwise, continue
                            continue

                        # If the function returned False
                        if return_val is False:

                            # Delete the value and associated key
                            del d[k]

                        # If the function returned True
                        elif return_val is True:

                            # Continue
                            continue

                        # If the function returned something else
                        else:

                            # Raise an error
                            errstr = \
                                f"'func' must return either True or " \
                                f"False, but it returned " \
                                f"{repr(return_val)} for {repr(v)}."
                            raise TypeError(errstr)

    # If the dictionary should not be modified in place
    if not in_place:

        # Create a copy of the input dictionary
        new_d = copy.deepcopy(d)

    # Otherwise
    else:

        # Reference the original dictionary
        new_d = d

    # Add the "key path" and its value to either the
    # input dictionary or the new dictionary
    recursive_step(d = new_d,
                   func = func,
                   keys = keys,
                   permissive = permissive)

    # If the original dictionary was not modified in place
    if not in_place:

        # Return the new dictionary
        return new_d