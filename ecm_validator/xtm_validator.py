from collections import deque

def topological(graph):
    GRAY, BLACK = 0, 1
    order, enter, state = deque(), set(graph), {}
    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k[1], None)
            if sk == GRAY: raise CycleException((node,k[1]))
            if sk == BLACK: continue
            enter.discard(k[1])
            dfs(k[1])
        order.appendleft(node)
        state[node] = BLACK

    while enter: dfs(enter.pop())
    return order
	
class CycleException(Exception):
	def __init__(self,value):
		self.value = value

def validate_constraints(root_node):
	
	'''TO-ADD: Occurrences'''
	
	topics = {} #dictionary topicid, topicname
	adj_list = {} #dictionary node, adjacencies
	
	tree = root_node.root
	
	# here goes the code that traverses the tree
	# fill topics
	# fill adj_list
	
	try: top_order = topological(adj_list)

	except CycleException as e: 
		print "Cycle between nodes " + str(e.value[0]) + " and " + str(e.value[1])
		return
		
	primary_notions, secondary_notions, deepening, individual = [], [], [], []
	
	#traverse top_order to fill aforementioned lists
	#check constraints on those lists
	
	
	return