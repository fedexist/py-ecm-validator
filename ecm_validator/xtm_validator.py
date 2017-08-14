from collections import deque


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


class ValidationError(Exception):
	pass


class CycleException(ValidationError):
	def __init__(self, value):
		self.message = "CycleException: Cycle between nodes %s and %s" % (str(value[0]), str(value[1]))
	
	def __str__(self):
		return self.message


# TODO: define Exceptions behaviour
class NotUniqueException(ValidationError):
	pass


class NotALeafException(ValidationError):
	pass


class IsItemException(ValidationError):
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
		
		# def __str__(self):
		#	return "%s of type %s" % (self.roles, str(self.relation_type))
		
		# def __repr__(self):
		#	return str(self)
		
		class TopicRef:
			def __init__(self, root):
				self.topic_ref = filter(lambda node: node.name == "topicRef", root.children)[0].attributes['href']
			
			def __str__(self):
				return str(topics.get(self.topic_ref.strip('#')))
			
			def __repr__(self):
				return str(self)
		
		class Type(TopicRef):
			def __init__(self, root):
				Association.TopicRef.__init__(self, filter(lambda node: node.name == "type", root)[0])
		
		class Role(TopicRef):
			def __init__(self, root):
				Association.TopicRef.__init__(self, root)
				self.role_type = Association.Type(root.children)
			
			# def __str__(self):
			#	return "%s (type: %s)" % (str(topics.get(self.topic_ref.strip('#'))), str(self.role_type))
	
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
	
	# print str(topics)
	
	# il grafo non presenta cicli
	# il nodo g con ruolo di deepening non ha archi in uscita
	# il nodo q con ruolo di individual non ha archi in uscita che non siano "is_rel"
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
	
	# for each graph relation create a representation in an adjacency list
	for relation in filter(lambda ass: str(ass.relation_type) in rel_type_aux_dict.keys(), associations):
		# if one of the topics is the generic Primary Notion or Secondary Notion discard the association
		
		if str(relation.roles[0]) in ['Primary Notion', 'Secondary Notion'] \
				or str(relation.roles[1]) in ['Primary Notion', 'Secondary Notion']:
			continue
		
		# Establish the roles in the associations to give a direction to the adjacency list
		
		rel_type_aux_dict = {
			"is_rel": ['linked 1', 'linked 2'],
			"is_sug": ['main', 'deepening'],
			"is_req": ['prerequisite', 'subsidiary'],
			"is_item": ['general', 'individuals']
		}
		
		def fill_adj_list(rel_type):
			role_1 = str(filter(lambda role: str(role.role_type) == rel_type_aux_dict[rel_type][0], relation.roles)[0])
			role_2 = str(filter(lambda role: str(role.role_type) == rel_type_aux_dict[rel_type][1], relation.roles)[0])
			
			if role_1 not in adj_list:
				adj_list[role_1] = []
			if role_2 not in adj_list:
				adj_list[role_2] = []
			adj_list[role_1].append((rel_type, role_2))
		
		fill_adj_list(str(relation.relation_type))
	
	# print adj_list
	
	top_order = topological(adj_list)
	
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
		if filter(lambda (rel, dest): rel == "is_item" and
					len([(re, des) for (re, des) in adj_list[dest] if re != "is_rel"]) != 0, v):
			raise IsItemException()
