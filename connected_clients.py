import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
	try:
		with closing(requests.get(url, stream=True)) as resp:
			if is_good_response(resp):
				return resp.content
			else:
				return None
	except RequestException as e:
		log_error('Error during request to {0}: {1}' . format(url, str(e)))
		return None

def is_good_response(resp):
	content_type = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200
    		and content_type is not None
			and content_type.find('html') > -1)

def log_error(e):
	print(e)


def login():
	post_url		= 'http://127.0.0.1/your_post_login_url'
	login_ok_url	= 'http://127.0.0.1/your_sucess_login_url'
	user 			= 'your_user'
	password 		= 'your_password'
	payload 		= {'loginUsername': user, 'loginPassword': password}

	session = requests.Session()
	response = session.post(post_url, payload)

	if (response.url != login_ok_url):
		print('Login error')

def logout():
	logout_url	= 'http://127.0.0.1/your_logout_url'
	response = simple_get(logout_url)

def get_conected_clients():
	url = 'http://127.0.0.1/your_connected_ips_table_url'
	response = simple_get(url)

	if response is not None:
		html = BeautifulSoup(response, 'html.parser')
		connected_client = set()

		# all rows of the third table
		table_rows = html.select('table')[3].findAll('tr')

		# macs
		for index, row in enumerate(table_rows):
			# since third row its the information
			if (index > 2):
				tds 		= row.findAll('td')
				mac 		= tds[0].text
				ip 			= tds[3].text
				host_name	= tds[4].text

				print('Mac: ' + mac + ' Ip: ' + ip + ' Host:' + host_name)

def main():
	login()
	get_conected_clients()
	logout()

# Homenum revelio
main()