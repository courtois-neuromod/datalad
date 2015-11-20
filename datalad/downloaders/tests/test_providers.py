# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Tests for data providers"""

from ..providers import ProvidersInformation
from ...tests.utils import eq_
from ...tests.utils import assert_in
from ...tests.utils import assert_equal


def test_ProvidersInformation_OnStockConfiguration():
    pi = ProvidersInformation()
    eq_(sorted(pi.providers.keys()), ['crcns', 'crcns-nersc', 'hcp-s3', 'hcp-web', 'hcp-xnat', 'openfmri'])
    for n, fields in pi.providers.items():
        assert_in('url_re', fields)

    # and then that we didn't screw it up -- cycle few times to verify that we do not
    # somehow remove existing providers while dealing with that "heaplike" list
    for i in range(3):
        provider = pi.get_matching_provider('https://crcns.org/data....')
        assert_equal(provider['name'], 'crcns')

        provider = pi.get_matching_provider('https://portal.nersc.gov/project/crcns/download/bogus')
        assert_equal(provider['name'], 'crcns-nersc')

    assert_equal(pi.needs_authentication('http://google.com'), None)
    assert_equal(pi.needs_authentication('http://crcns.org/'), True)
    assert_equal(pi.needs_authentication('http://openfmri.org/'), False)