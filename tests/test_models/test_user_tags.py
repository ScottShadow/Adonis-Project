#!/usr/bin/python3
"""
Contains the UserTagsDocs classes
"""
import inspect
import models
from models import tag
from models.base import Tag
import pycodestyle
import unittest
Tag = tag.Tag
module_doc = models.tag.__doc__