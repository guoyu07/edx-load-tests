"""
This module helps manage settings files.  To use this module for your load
tests:

1. Include the following two lines in your locustfile.py:

  from helpers import settings
  settings.init(__name__)

2. Create a settings file: "settings_files/<TEST MODULE NAME>.yml"

3. Anywhere you need to use the settings data, make sure the settings module
   is imported, then use:

  settings.data['SOMETHING']

"""
import os
import yaml
import logging
import copy
from pkg_resources import resource_filename
from pprint import pformat

REDACTED_KEYWORDS = ['password', 'secret']
LOG = logging.getLogger(__name__)
data = None


def _suggests_secret(dict_key):
    """
    Decide if the dict_key suggests that it refers to a value containing sensitive
    secrets.
    """
    return \
        isinstance(dict_key, basestring) and \
        any([kw.lower() in dict_key.lower() for kw in REDACTED_KEYWORDS])


def _get_redacted_data(orig_data):
    """
    Create a deep copy of the orig_data dict such that all secrets are
    overwritten with the string "REDACTED".
    """
    redacted_data = orig_data.copy()  # shallow copy
    for k, v in redacted_data.items():
        if _suggests_secret(k):
            redacted_data[k] = 'REDACTED'
        else:
            if type(v) is dict:
                # The key does not suggest that the value contains secrets, but
                # if the value is a dict it still may contain secrets.
                # N.B. This recursion takes care of making the deep copy.
                redacted_data[k] = _get_redacted_data(v)
    return redacted_data


def init(test_module_full_name, required=[]):
    """
    This is the primary entrypoint for this module.  In short, it initializes
    the global data dict, finds/loads the settings files, and validates the
    data.
    """
    global data
    if data is not None:
        raise RuntimeError('helpers.settings has been initialized twice!')

    # Find the correct settings file under the "settings_files" directory of
    # this package.  The name of the settings file corresponds to the
    # name of the directory containing the locustfile. E.g.
    # "loadtests/lms/locustfile.py" reads settings data from
    # "settings_files/lms.yml".
    test_module_name = test_module_full_name.split('.')[-2]
    settings_filename = \
        resource_filename('settings_files', '{}.yml'.format(test_module_name))
    settings_filename = os.path.abspath(settings_filename)
    LOG.info('using settings file: {}'.format(settings_filename))

    # load the settings file
    with open(settings_filename, 'r') as settings_file:
        data = yaml.load(settings_file)
    redacted_data = _get_redacted_data(data)
    LOG.info('loaded the following public settings:\n{}'.format(
        pformat(redacted_data),
    ))

    # check that the required keys are present
    for key in required:
        if data.get(key) is None:
            raise RuntimeError(
                'the {} parameter is required for {} load tests.'.format(
                    key,
                    test_module_name,
                )
            )
