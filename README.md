# GETAWSCRED v1.0, get CLI credentials from AWS SSO login page

<div class="highlight highlight-source-shell"><pre>
usage: getawscred.py [-h] [-f CREDENTIALS FILE] [-p PROFILE] [-r] [-s] SSOSITE SSOUSERNAME AWSACCOUNT AWSUSERNAME
positional arguments:
  SSOSITE              SSO site, i.e. "company-aws-sso.awsapps.com"
  SSOUSERNAME          SSO username
  AWSACCOUNT           AWS account, can be part of name if it is unique, i.e. "Company Infra"
  AWSUSERNAME          AWS username, can be part of name if it is unique, i.e. "power"
optional arguments:
  -h, --help           show this help message and exit
  -f CREDENTIALS FILE  Credential's file with path, default is ~/.aws/credentials
  -p PROFILE           Name of aws profile in credential's file, default is the awsaccount name
  -r                   Recreate cookie file
  -s                   Show credentials instead of writing to file
</pre></div>

The python script uses Selenium as headless browser in order to mimic SSO authentication against aws site.<br>
It is able to detect a requirement of MFA code and prompts for entering it. The cookie file allows preserve the MFA authentication.<br>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_donations" />
<input type="hidden" name="business" value="YZ33E5NSWUE6G" />
<input type="hidden" name="currency_code" value="USD" />
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
</form>


