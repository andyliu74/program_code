# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

from main import main as main_func


def main():
	main_func()


if __name__ == "__main__":
	try:
		main()
	except:
		import traceback
		print traceback.format_exc()