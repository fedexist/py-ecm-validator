from xtm_parser import XmlSyntaxError, xml_parse
from xtm_validator import validate_constraints, ValidationError
import sys
import codecs
import argparse
import re

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser("Arguments for parser")
parser.add_argument("-d", "--debug", help="Debug flags, accepted in whatever order:'i' for input debug;"
                                          "'l' for lexer debug; 'p' for parser debug;'o' for output debug. "
                                          "Example '-d iplo', '-d olpi'.", type=str)
parser.add_argument("-f", "--file", help="Input file", required=True)

accepted_debug_flags = ["i", "l", "p", "o"]

args = parser.parse_args()
if args.debug is not None:
	debug_flags = list(args.debug)
else:
	debug_flags = []

filename = args.file

flags = filter(lambda _flag: _flag in accepted_debug_flags, debug_flags)

DEBUG = {
	'i': 'INPUT',
	'l': 'LEXER',
	'p': 'PARSER',
	'o': 'OUTPUT'
}
debug = {}

if debug_flags and flags:
	for _flag in flags:
		debug[DEBUG[_flag]] = True

with codecs.open(filename, "r", "utf-8") as data:
	print "Parsing file %(filename)s..." % locals()
	# Remove comments from the xml
	formatted_data = re.sub(ur'<!--.*-->|<!--.*\n.*-->', '', data.read(), re.UNICODE)
	try:
		root = xml_parse(formatted_data, debug=debug)
	except XmlSyntaxError as e:
		print e
		exit(e.error_code)
	print "Validating file %(filename)s..." % locals()
	# print tree(root)
	try:
		validate_constraints(root)
		print "File validated. No error found!"
	except ValidationError as e:
		print e
		exit(e.error_code)
