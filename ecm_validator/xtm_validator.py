from collections import deque

def topological(graph):
    GRAY, BLACK = 0, 1
    order, enter, state = deque(), set(graph), {}
    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k[1], None)
            if sk == GRAY: raise ValueError("cycle") #will be changed to CycleException
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
	
	tree = root_node.node
	
	# here goes the code that traverses the tree
	# fill topics
	# fill adj_list
	
	try: top_order = topological(adj_list)
	except ValueError: 
		print "Cycle!" ##poi si può modificare il topological sort per dare un'idea di dove sia il ciclo
		return
		
	primary_notions, secondary_notions, deepening, individual = [], [], [], []
	#traverse top_order to fill aforementioned lists
	#check constraints on those lists
	
	
	return