# GETAWSCRED v1.0, get CLI credentials from AWS SSO login page
Automatic 
<code>
  usage: getawscred.py [-h] [-f CREDENTIALS FILE] [-p PROFILE] [-r] [-s]
                     SSOSITE SSOUSERNAME AWSACCOUNT AWSUSERNAME

GETAWSCRED v1.0, get CLI credentials from AWS SSO login page

positional arguments:
  SSOSITE              SSO site, i.e. "company-aws-sso.awsapps.com"
  SSOUSERNAME          SSO username
  AWSACCOUNT           AWS account, can be part of name if it is unique, i.e.
                       "Company Infra"
  AWSUSERNAME          AWS username, can be part of name if it is unique, i.e.
                       "power"

optional arguments:
  -h, --help           show this help message and exit
  -f CREDENTIALS FILE  Credential's file with path, default is
                       ~/.aws/credentials
  -p PROFILE           Name of aws profile in credential's file, default is
                       the awsaccount name
  -r                   Recreate cookie file
  -s                   Show credentials instead of writing to file
</code>
