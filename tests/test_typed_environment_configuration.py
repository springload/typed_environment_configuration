#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `typed_environment_configuration` package."""


import unittest
import os

from typed_environment_configuration import *

_ENVVARS = [BoolVariable("DEBUG"), StringVariable("DEFAULT_STRING", default="")]

_PREFIXED_ENVVARS = [
    StringVariable("PREFIXED_VERSION"),
    StringListVariable("PREFIXED_DEFAULT_LIST", default=""),
]

v = vars()

class TestTyped_environment_configuration(unittest.TestCase):
    """Tests for `typed_environment_configuration` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        os.environ["DEBUG"] = "True"
        os.environ["PREFIXED_VERSION"] = "1.2.3"

        FillVars(_ENVVARS, v)
        FillVars(_PREFIXED_ENVVARS, v, prefix="PREFIXED_")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_BoolVariable(self):
        """Tests that setting boolean variable in env creates a python variable DEBUG=True"""
        self.assertEqual(DEBUG, True)

    def test_PrefixedVariable(self):
        """Tests a prefixed variable"""
        self.assertEqual(VERSION, "1.2.3")

    def test_DefaultVariable(self):
        """Tests a default variable"""
        self.assertEqual(DEFAULT_LIST, [])
