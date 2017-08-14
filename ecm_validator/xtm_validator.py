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


# TODO: Occurences handling
def validate_constraints(header):
	"""Validates DOM starting from header.root
	:param header -- Xml header returned from xml_parse
	:returns True -- if no exception occurs
	"""

	class Association:
		def __init__(self, root):
			self.relation_type = self.Type(root.children)
			roles = filter(lambda node: node.name == "role", root.children)
			self.roles = (self.Role(roles[0]), self.Role(roles[1]))
		
		def __str__(self):
			return "%s of type %s" % (self.roles, str(self.relation_type))
		
		def __repr__(self):
			return str(self)
		
		class TopicRef:
			def __init__(self, root):
				self.topic_ref = filter(lambda node: node.name == "topicRef", root.children)[0].attributes['href']
			
			def __str__(self):
				return self.topic_ref.strip('#')
			
			def __repr__(self):
				return str(self)
		
		class Type(TopicRef):
			def __init__(self, root):
				Association.TopicRef.__init__(self, filter(lambda node: node.name == "type", root)[0])
				
		class Role(TopicRef):
			def __init__(self, root):
				Association.TopicRef.__init__(self, root)
				self.role_type = Association.Type(root.children)
			
			def __str__(self):
				return "%s (type: %s)" % (self.topic_ref.strip('#'), str(self.role_type))

	tree = header.root
	topics = {}  # dictionary topicid, topicname
	adj_list = {}  # dictionary node, adjacencies

	# select all the children nodes
	topic_nodes = filter(lambda node: node.name == "topic", tree.children)
	for topic in topic_nodes:
		topic_id = topic.attributes.get('id')
		# selects the "name" node among the children nodes of "topic"
		name_node = filter(lambda node: node.name == "name", topic.children)
		# checks if there's a "name" node
		if len(name_node) > 0:
			# selects the "value" node
			value_node = filter(lambda node: node.name == "value", name_node[0].children)[0]
			# creates the entry in the map
			topics[topic_id] = value_node.children[0]

	#print str(topics)

	### il grafo non presenta cicli
	### il nodo g con ruolo di deepening non ha archi in uscita
	### il nodo q con ruolo di individual non ha archi in uscita che non siano "is_rel"
	'''adj_list = {
		'a': [("is_rel",'b'), ("is_sug",'g'), ("is_rel",'d'),],
		'b': [],
		'c': [("is_rel",'d'),("is_rel",'e')],
		'd': [],
		'e': [("is_rel",'g'), ("is_rel",'f'), ("is_rel",'q')],
		'g': [],
		'f': [("is_item",'q')],
		'q': [("is_rel",'g')]
	}'''

	associations = [Association(_rel) for _rel in filter(lambda node: node.name == "association", tree.children)]
	
	
	#for each graph relation create a representation in an adjacency list
	for relation in filter(lambda ass: topics[str(ass.relation_type)] == "is_rel" or topics[str(ass.relation_type)] == "is_sug" or topics[str(ass.relation_type)] == "is_req" or topics[str(ass.relation_type)] == "is_item",associations):
		#if one of the topics is the generic Primary Notion or Secondary Notion discard the association
		if topics[relation.roles[0].topic_ref.strip('#')] == 'Primary Notion' or topics[relation.roles[0].topic_ref.strip('#')] == 'Secondary Notion':
			continue
		if topics[relation.roles[1].topic_ref.strip('#')] == 'Primary Notion' or topics[relation.roles[1].topic_ref.strip('#')] == 'Secondary Notion':
			continue
			
		#Establish the roles in the associations to give a direction to the adjacency list
		
		rel_type_aux_dict = {
			"is_rel":['linked 1','linked 2'],
			"is_sug":['main','deepening'],
			"is_req":['prerequisite','subsidiary'],
			"is_item":['general','individuals']
		}
		
		def fill_adj_list(rel_type):
			role_1 = topics[str(filter(lambda role: topics[str(role.role_type)] == rel_type_aux_dict[rel_type][0], relation.roles)[0].topic_ref.strip('#'))]
			role_2 = topics[filter(lambda role: topics[str(role.role_type)] == rel_type_aux_dict[rel_type][1], relation.roles)[0].topic_ref.strip('#')]
			if not role_1 in adj_list:
				adj_list[role_1] = []
			if not role_2 in adj_list:
				adj_list[role_2] = []
			adj_list[role_1].append((rel_type,role_2))
		
		if topics[str(relation.relation_type)] == "is_rel":
			fill_adj_list("is_rel")
		
		if topics[str(relation.relation_type)] == "is_sug":
			fill_adj_list("is_sug")
			
		if topics[str(relation.relation_type)] == "is_req":
			fill_adj_list("is_req")
			
		if topics[str(relation.relation_type)] == "is_item":
			fill_adj_list("is_item")
			
	#print adj_list
	
	try:
		top_order = topological(adj_list)
	except CycleException as e:
		print "Cycle between nodes " + str(e.value[0]) + " and " + str(e.value[1])
		return

	primary_notions, secondary_notions, deepening, individual = [], [], [], []

	# traverse top_order to fill aforementioned lists

	# check constraints on those lists:

	for k, v in adj_list.iteritems():
		# if the size of an entry of the adjacency list is greater than
		# the set based off the 2nd member of the tuple (destination of the edge)
		# then that means there's at least 1 relation which has the same destination
		if len(set([y for x, y in v])) < len(v):
			raise NotUniqueException(k)
		# given a certain entry `v` of the adjacency list, choose a sublist `sub_v` containing only "is_sug" relations,
		# then, for each element of `sub_v`, if the size of the adjacency list of this element is different than zero,
		# add it to the output.
		# If the output is not empty, that means at least 1 element of `sub_v` is not a leaf
		if filter(lambda (rel, dest): rel == "is_sug" and len(adj_list[dest]) != 0, v):
			raise NotALeafException()
		# given a certain entry `v` of the adjacency list, choose a sublist `sub_v` containing only "is_item" relations,
		# then, for each element `e` of `sub_v`, let adj_list[e.dest] as `l`, create a list containing only the "is_rel"
		# relations `l_is_rel`. If `l_is_rel` has a different size than `l`, then add it to the output.
		# If the output is not empty, that means at least 1 element of `sub_v` has at least 1 relation which isn't "is_rel"
		if filter(lambda (rel, dest): rel == "is_item" and len([(re,des) for (re,des) in adj_list[dest] if re != "is_rel"]) != 0, v):
			raise IsItemException()
	
	return True
