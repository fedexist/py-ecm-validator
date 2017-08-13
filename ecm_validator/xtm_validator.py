from collections import deque
from xtm_parser import DOM


def topological(graph):
	gray, black = 0, 1
	order, enter, state = deque(), set(graph), {}
	
	def dfs(node):
		state[node] = gray
		for k in graph.get(node, ()):
			sk = state.get(k[1], None)
			if sk == gray:
				raise CycleException((node, k[1]))
			if sk == black:
				continue
			enter.discard(k[1])
			dfs(k[1])
		order.appendleft(node)
		state[node] = black
	
	while enter:
		dfs(enter.pop())
	return order


class CycleException(Exception):
	def __init__(self, value):
		self.value = value


# TODO: define Exceptions behaviour
class NotUniqueException(Exception):
	pass


class NotALeafException(Exception):
	pass


class IsItemException(Exception):
	pass
	

class Association:
	def __init__(self, root):
		self.relation_type = self.Type(root.children[0])
		self.roles = (self.Role(root.children[1]), self.Role(root.children[2]))
	
	def __str__(self):
		return "%s of type %s" % (self.roles, str(self.relation_type))
	
	def __repr__(self):
		return str(self)
	
	class Type:
		def __init__(self, root):
			self.href = root.children[0].attributes['href']
		
		def __str__(self):
			return self.href.strip('#')
		
		def __repr__(self):
			return str(self)
	
	class Role:
		def __init__(self, root):
			self.role_type = Association.Type(root.children[0])
			self.topic_ref = root.children[1].attributes['href']
		
		def __str__(self):
			return "%s (type: %s)" % (self.topic_ref.strip('#'), str(self.role_type))
		
		def __repr__(self):
			return str(self)


# TODO: Occurences handling
def validate_constraints(header):
	"""Validates DOM starting from header.root
	:param header -- Xml header returned from xml_parse
	:returns True -- if no exception occurs
	"""
	
	topics = {}  # dictionary topicid, topicname
	adj_list = {}  # dictionary node, adjacencies
	
	tree = header.root
	
	# TODO:
	# here goes the code that traverses the tree
	# fill topics
	# fill adj_list
	
	associations = [Association(_rel) for _rel in filter(lambda node: node.name == "association", tree.children)]
	
	print str(associations)
	
	try:
		top_order = topological(adj_list)
	except CycleException as e:
		print "Cycle between nodes " + str(e.value[0]) + " and " + str(e.value[1])
		return
	
	primary_notions, secondary_notions, deepening, individual = [], [], [], []
	
	# traverse top_order to fill aforementioned lists
	
	# check constraints on those lists:
	
	for k, v in adj_list:
		# if the size of an entry of the adjacency list is greater than
		# the set based off the 2nd member of the tuple (destination of the edge)
		# then that means there's at least 1 relation which has the same destination
		if len(set([y for x, y in v])) < len(v):
			raise NotUniqueException(k)
		# given a certain entry `v` of the adjacency list, choose a sublist `sub_v` containing only "is_sug" relations,
		# then, for each element of `sub_v`, if the size of the adjacency list of this element is different than zero,
		# add it to the output.
		# If the output is not empty, that means at least 1 element of `sub_v` is not a leaf
		if not filter(lambda rel, dest: len(adj_list[dest]) != 0, filter(lambda rel, dest: rel == "is_sug", v)):
			raise NotALeafException()
		# given a certain entry `v` of the adjacency list, choose a sublist `sub_v` containing only "is_item" relations,
		# then, for each element `e` of `sub_v`, let adj_list[e.dest] as `l`, create a list containing only the "is_rel"
		# relations `l_is_rel`. If `l_is_rel` has a different size than `l`, then add it to the output.
		# If the output is not empty, that means at least 1 element of `sub_v` has at least 1 relation which isn't "is_rel"
		if not filter(lambda rel, dest: len([_v for _k, _v in adj_list[dest] if _v != "is_rel"]) != len(adj_list[dest]),
		              filter(lambda rel, dest: rel == "is_item", v)):
			raise IsItemException()
	
	return True
