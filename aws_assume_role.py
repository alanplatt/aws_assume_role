#!/usr/bin/env python

import sys
import getpass
from aws_assume_role.parse_arguments import parse_args
from aws_assume_role.aws import (get_MFA_token, load_config, validate_config,
                                 connect_to_sts_region, set_shell_environment_variables,
                                 assume_aws_role, unset_shell_environment_variables)

def main(argv):
    args = parse_args(argv)
    profile = args.profile
    mfa_token = None
    mfa_serial_number = None
    session_name = '%s-%s' % (getpass.getuser(), profile)

    #The syntax of the aws cli config file requires the keyword profile before a profile
    if not profile == 'default':
        profile = "profile " + profile


    if args.MFA or args.MFAtoken:
        mfa_token = get_MFA_token(args.MFAtoken[0])
        config = load_config(["~/.aws/credentials", "~/.aws/config"])
        mfa_serial_number = config.get(profile, 'mfa_serial')
    else:
        config = load_config(["~/.aws/credentials"])

    validate_config(profile, config)

    region = config.get(profile, 'region')
    aws_access_key = config.get(args.AWSaccount, 'aws_access_key_id')
    aws_secret_key = config.get(args.AWSaccount, 'aws_secret_access_key')
    role_arn = config.get(profile, 'role_arn')


    sts_connection = connect_to_sts_region(aws_access_key, aws_secret_key)
    assumedRoleObject = assume_aws_role(sts_connection=sts_connection,
                                        role_arn=role_arn,
                                        role_session_name=session_name,
                                        mfa_serial_number=mfa_serial_number,
                                        mfa_token=mfa_token)

    unset_shell_environment_variables()

    set_shell_environment_variables(assumedRoleObject.credentials.access_key,
                                    assumedRoleObject.credentials.secret_key,
                                    assumedRoleObject.credentials.session_token,
                                    region,
                                    session_name,
                                    assumedRoleObject.credentials.expiration,
                                    profile
                                    )

if __name__ == "__main__":
    main(sys.argv[1:])
