#v1.5.2

import sys, getpass, time, pickle, pathlib, signal, argparse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException  
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
#
class SelWeb:
	def __init__(self, url, checkel='none'):
		options = webdriver.ChromeOptions()
		options.binary_location = '/usr/bin/google-chrome'
		options.add_argument('headless')
		options.add_argument('--no-sandbox')
		options.add_argument("user-data-dir="+str(Path.home())+"/.getawscred")
		prefs = {"profile.managed_default_content_settings.images": 2}
		options.add_experimental_option("prefs", prefs)
		self.driver = webdriver.Chrome(options=options)
		self.driver.implicitly_wait(5)
		self.driver.get(url)
		if checkel != 'none':
			while True:
				try:
					WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, checkel)))
				except TimeoutException:
					print("Loading took too much time!")
					self.tearDown()
					sys.exit()
				except StaleElementReferenceException:
					continue
				break
			
	def FindEl(self, element):
		try:
			x1=self.driver.find_element_by_xpath(element)
		except NoSuchElementException:
			x1=None
		return(x1)
		
	def FindEls(self, element):
		try:
			x1=self.driver.find_elements_by_xpath(element)
		except NoSuchElementException:
			x1=object()
		return(x1)

	def FindAccUserClick(self, element1, click1, lookfor, msg1):
		_awsacc = self.FindEls(element1)
		if element1 is not click1:
			_awscli = self.FindEls(click1)
		else:
			_awscli = _awsacc
		i = []
		for y in _awsacc:
			i.append(y.text.split("\n")[0])
		for ii in i:
			if lookfor in ii:
				_awscli[i.index(ii)].click()
				return True
		print(msg1)
		return False

	def tearDown(self):
		self.driver.close()
		self.driver.quit()
		
class element_has_css_class(object):
  """"An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, css_class):
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if self.css_class in element.get_attribute("class"):
        return element
    else:
        return False

def run_program():
	parser = argparse.ArgumentParser(description='GETAWSCRED v1.0, get CLI credentials from AWS SSO login page')
	parser.add_argument('ssosite', metavar='SSOSITE', type=str,	help='SSO site, i.e. "company-aws-sso.awsapps.com"')
	parser.add_argument('username', metavar='SSOUSERNAME', type=str, help='SSO username')
	parser.add_argument('awsaccount', metavar='AWSACCOUNT', type=str, help='AWS account, can be part of name if it is unique, i.e. "Company Infra"')
	parser.add_argument('awsusername', metavar='AWSUSERNAME', type=str, help='AWS username, can be part of name if it is unique, i.e. "power"')
	parser.add_argument('-f', metavar='CREDENTIALS FILE', type=str, help="Credential's file with path, default is ~/.aws/credentials", dest="credfile")
	parser.add_argument('-p', metavar='PROFILE', type=str, help="Name of aws profile in credential's file, default is the awsaccount name", dest="awsprofile")
	parser.add_argument('-r', help="Recreate cookie file", dest="delcook", action='store_true')
	parser.add_argument('-s', help="Show credentials instead of writing to file", dest="shcred", action='store_true')

	args = parser.parse_args()

	awsweb = SelWeb('https://'+args.ssosite+'/start#/', '//*[@id="main-container"]')

	baduser = False
	while awsweb.driver.title == "Amazon Web Services (AWS) Sign-In":
		record = awsweb.FindEl("//input[contains(@id,'input')]")
		record.clear()
		if awsweb.FindEl("//*[text()='Username']"):
			if (args.username is None) or baduser:
				record_input = input("Enter username:")
			else:
				record_input = args.username
		elif awsweb.FindEl("//*[text()='Password']"):
			record_input = getpass.getpass("Enter password:")
		elif awsweb.FindEl("//*[text()='MFA code']"):
			record_input = input("Enter MFA code:")

		record.send_keys(record_input)
		awsweb.FindEl("//button[@type='submit']").click()
		time.sleep(2)

	while awsweb.driver.title == "Your applications":
		element1 = awsweb.FindEl("//portal-application[starts-with(@id,'app-')]")
		hoverover = ActionChains(awsweb.driver).move_to_element(element1).click().perform()
		time.sleep(2)
		if awsweb.FindAccUserClick("//portal-instance","//portal-instance",args.awsaccount,"There is no such AWS account - "+args.awsaccount) is not True:
			break
		time.sleep(2)
		if awsweb.FindAccUserClick("//portal-profile","//a[@id='temp-credentials-button']",args.awsusername,"There is no such aws user - "+args.awsusername) is not True:
			break
		time.sleep(2)
		k12key = awsweb.FindEl("//div[@id='cli-cred-file-code']")
		k12keylist = k12key.text.split("\n")
		if args.awsprofile:
			k12keylist[0] = '['+args.awsprofile+']'
		if 'Click to copy this text' in k12keylist:
			k12keylist.remove('Click to copy this text')
		if not args.shcred:
			flag=1
			if args.credfile:
				credfile=args.credfile
			else:
				credfile=str(Path.home())+"/.aws/credentials"
			try:
				with open(credfile, 'r+') as iofile:
					lines = iofile.readlines()
					for index, line in enumerate(lines):
						line=line.strip("\n")
						if line.startswith(k12keylist[0]):
							flag = 0
						if line.startswith("[") and not line.startswith(k12keylist[0]):
							flag = 1
						if flag:
							k12keylist.append(line.strip('\n'))
					iofile.seek(0)
					iofile.truncate()
					for line in k12keylist:
						iofile.write(line+'\n')
					print("Credentials file - "+credfile+" has been updated.")
			except FileNotFoundError:
				print("Error: No such file - " + credfile)
		else:
			for i in k12keylist:
				print(i)
		break

	awsweb.tearDown()

def exit_gracefully(signum, frame):
	# restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
	# signal.signal(signal.SIGINT, original_sigint)
	try:
		awsweb
	except NameError:
		pass
	else:
		awsweb.tearDown()
	print("\nQuiting...")
	sys.exit(1)
	# restore the exit gracefully handler here

if __name__ == '__main__':
	# store the original SIGINT handler
	# original_sigint = signal.getsignal(signal.SIGINT)
	signal.signal(signal.SIGINT, exit_gracefully)
	run_program()

