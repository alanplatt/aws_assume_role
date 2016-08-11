import argparse


def parse_args(argv):
    """
    Parse all command line arguments and return a dict
    """
    parser = argparse.ArgumentParser(description='''Switch between aws
                                     profiles and export shell variables.''')
    parser.add_argument('--profile',
                        metavar='PROFILE',
                        nargs='?',
                        default='default',
                        const='default',
                        help='The profile in AWS config of the role to assume')
    parser.add_argument('--MFA',
                        action='store_true',
                        help='Ask for MFA token')
    parser.add_argument('--MFAtoken',
                        metavar='TOKEN',
                        nargs=1,
                        help='Set MFA token from command line')

    return parser.parse_args(argv)
