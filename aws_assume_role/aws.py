import os
import pipes
from ConfigParser import SafeConfigParser
from boto.sts import STSConnection

class ConfigException(Exception):
    def __init__(self, msg):
        self.message = msg

def get_MFA_token(token=False):
    if not token:
        token = raw_input("Enter the MFA code: ")

    try:
        return int(token)
    except:
        raise ValueError('You must inter an integer as an MFA token')

def load_config(files):
    filenames = []
    for file in files:
        filenames.append(os.path.expanduser(file))

    config = SafeConfigParser()
    if not cmp(filenames, config.read(filenames)):
        return config
    else:
        raise IOError("{} not found!".format(filenames))

def connect_to_sts_region(aws_access_key, aws_secret_key):
    try:
        return STSConnection(aws_access_key, aws_secret_key)
    except:
        raise

def assume_aws_role(sts_connection, role_arn, role_session_name, mfa_serial_number=None, mfa_token=None):
    try:
        return sts_connection.assume_role(role_arn=role_arn,
                                          role_session_name=role_session_name,
                                          mfa_serial_number=mfa_serial_number,
                                          mfa_token=mfa_token)
    except:
        raise

def unset_shell_environment_variables():
    print "unset AWS_DEFAULT_REGION;"
    print "unset AWS_SESSION_NAME;"
    print "unset AWS_ACCESS_KEY_ID;"
    print "unset AWS_SECRET_ACCESS_KEY;"
    print "unset AWS_SESSION_TOKEN;"
    print "unset AWS_SESSION_EXPIRATION;"

def set_shell_environment_variables(access_key, secret_key, session_token,
                                    region, session_name, expiration,
                                    profile):
    print "export AWS_ACCESS_KEY_ID={};".format(pipes.quote(str(access_key)))
    print "export AWS_SECRET_ACCESS_KEY={};".format(pipes.quote(str(secret_key)))
    print "export AWS_SESSION_TOKEN={};".format(pipes.quote(str(session_token)))
    print "export AWS_DEFAULT_REGION={};".format(pipes.quote(str(region)))
    print "export AWS_SESSION_NAME={};".format(pipes.quote(str(session_name)))
    print "export AWS_SESSION_EXPIRATION={};".format(pipes.quote(str(expiration)))
    print "echo Account {} is setup for use.;".format(profile)

def test_config(profile, config):
    """
    Test to see if the config that has been passed has the variables required
    """
    if not config.has_section('default'):
        print "echo Missing 'default' section from the credentials file.;"
        exit(1)

    for option in ['aws_access_key_id', 'aws_secret_access_key']:
        if not config.has_option('default', option):
            print "echo Missing {} from 'default' section of the credentials file.;".format(option)
            exit(2)

    if not profile == 'default':

        if not config.has_option(profile, 'region'):
            print config.get(profile, 'region')
            print "echo {} profile does not have 'region' set".format(profile)
            exit(3)

        if not config.has_section(profile):
            print "echo Account '{}' does not exist in the credentials file.;".format(profile)
            exit(4)
        for option in ['source_profile', 'role_arn']:
            if not config.has_option(profile, option):
                print "echo Profile '{}' is missing the required option, '{}'
                       in the config file.;".format(profile, option)
                exit(5)
    return True
