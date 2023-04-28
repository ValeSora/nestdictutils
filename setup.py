#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    nestdictutils.py
#
#    nestdictutils setup.
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
from setuptools import setup


# Name of the package 
name = "nestdictutils"

# URL where to find the package
url = f"https://github.com/ValeSora/{name}"

# Package author(s)
author = "Valentina Sora"

# Package version
version = "2023.0.0"

# A brief description of the package
description = "Utilities to manipulate nested dictionaries"

# Directory of the package
package_dir = {name : name}

# Which packages are included
packages = [name]


# Run the setup
setup(name = name,
      url = url,
      author = author,
      version = version,
      description = description,
      include_package_data = True,
      package_dir = package_dir,
      packages = packages)