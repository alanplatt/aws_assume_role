# aws_assume_role #

This is a refactor with added MFA support of a [script](https://gist.github.com/mlrobinson/944fd0e2ad4926ba71c9) by [mlrobinson](https:/
Thanks for the inspiration!

Python script to switch between aws profiles and set up your shell environment. Supports MFA.

The configuration required for this script is that same as for the aws cli(including MFA)
Basically that means if you can use MFA via the AWS CLI then this script should also work for you.
Please see the config examples below for usage.

### Assumptions ###
You have a working python and python virtualenv installed.


### Setup ###

As we are setting the environment variables of the current shell we must run the script in an eval statement.

Add the following two secions to either your .bashrc or .bash_profile
```
alias awscon='_awscon'
```

This function includes the setup required for the script. It will create a python virtual environment then
install the required pips. This keeps the requirements for this script seperate from your working environement.
```
_awscon() {

  AWS_ASSUME_ROLE_DIR="/Users/arqiva/workarea/aws_assume_role"
  VENV_NAME=".venv"
  if ! [ -e "${AWS_ASSUME_ROLE_DIR}/${VENV_NAME}/bin/activate" ]; then
    echo "Creating virtualenv..."
    virtualenv "${AWS_ASSUME_ROLE_DIR}/${VENV_NAME}"
  fi
  source "${AWS_ASSUME_ROLE_DIR}/${VENV_NAME}/bin/activate"
  pip install -q -r "${AWS_ASSUME_ROLE_DIR}/requirements.txt"

  eval $(python ${aws_assume_role_dir}/aws_assume_role.py --profile $1 --MFAtoken $2)
}
```

##Example configs##
~/.aws/credentials
```
[default]
aws_access_key_id=AKSUPERSECRETKEYXXYQ
aws_secret_access_key=iGXXXXACCESSKEYFFFFFFSD23423423423423MMX
region = eu-west-1
```

~/.aws/config
```
[profile prod]
role_arn = arn:aws:iam::099999999999:role/users/some_role
mfa_serial = arn:aws:iam::999999999982:mfa/user.name
source_profile = default
output = json
region = eu-west-1

[profile dev]
role_arn = arn:aws:iam::942222222276:role/users/some_role
mfa_serial = arn:aws:iam::111231231232:mfa/user.name
output = json
source_profile = default
region = eu-west-1
```

