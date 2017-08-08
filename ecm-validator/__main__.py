import xtm_parser
import xtm_validator
import sys

with open(sys.argv[1]) as data:
	print "Parsing file %(data)s..." % locals()
	root = xtm_parser.xml_parse(data)
	print "Validating file %(data)s..." % locals()
	xtm_validator.validate_constraints(root)
