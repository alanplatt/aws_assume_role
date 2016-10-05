import unittest
from mock import patch
from aws_assume_role.aws import (get_MFA_token, load_config)


class TestAWS(unittest.TestCase):

    def test_get_MFA_token_good_token(self):
        """
        If passed an integer function should return said integer
        """
        with patch('__builtin__.raw_input', return_value='1234') as _raw_input:
            self.assertEquals(get_MFA_token(), '1234')
            _raw_input.assert_called_once_with("Enter the MFA code: ")

    def test_get_MFA_token_bad_token(self):
        """
        If passed non integer should raise ValueError
        """
        with patch('__builtin__.raw_input', return_value='abc1234'):
            self.assertRaises(ValueError, get_MFA_token, token="abc1234")

    def test_load_config_file_does_not_exist(self):
        """
        If valid file is passed a SafeConfigParser object is returned
        """
        self.assertRaises(IOError, load_config, "/some/file")

    def test_load_config(self):
        """
        If valid file is passed a SafeConfigParser object is returned
        """
        result = load_config(["tests/test_config"])
        self.assertTrue(result.has_section("profile dev"))
        self.assertTrue(result.has_section("profile prod"))
