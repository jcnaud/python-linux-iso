#!/usr/bin/env python
# coding: utf-8

import os
import sys
import requests_mock
import pytest

try:
    # Package Import
    from linuxiso.custom.core import Custom  # noqa
    from linuxiso.ressources.tools import load_conf  # noqa
except Exception:
    # Local import
    DIR_PWD = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(DIR_PWD, ".."))
    from linuxiso.custom.core  import Custom  # noqa
    from linuxiso.ressources.tools import load_conf  # noqa

requests_mock.mock.case_sensitive = True
