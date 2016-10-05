import unittest
from aws_assume_role.parse_arguments import parse_args


class TestParseArguments(unittest.TestCase):

    def test_parse_args_with_no_options(self):
        """
        If options are given then we expect a valid arguments object
        """
        result = parse_args([])
        self.assertEquals(result.MFA, False)
        self.assertEquals(result.MFAtoken, None)
        self.assertEquals(result.profile, 'default')
        self.assertEquals(result.AWSaccount, 'default')

    def test_parse_args_with_valid_options(self):
        """
        If valid options are given then we expect a valid arguments object
        """
        result = parse_args(['--profile', 'bv_prod', '--MFAtoken', '073690'])
        self.assertEquals(result.MFA, False)
        self.assertEquals(result.MFAtoken[0], '073690')
        self.assertEquals(result.profile, 'bv_prod')
        self.assertEquals(result.AWSaccount, 'default')
