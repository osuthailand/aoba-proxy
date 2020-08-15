def stringToBool(s):
	"""
	Convert a string (True/true/1) to bool

	:param s: string/int value
	:return: True/False
	"""
	return s == "True" or s == "true" or s == "1" or s == 1

def merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z

def set_header():
	headers = {
		'User-Agent': 'osu!',
		'Host': 'osu.ppy.sh',
		'Accept-Encoding': 'gzip, deflate'
	}

	return headers