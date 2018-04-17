import networkx as nx
import matplotlib.pyplot as plt
import os.path

from matplotlib import pylab
from networkx.algorithms import approximation

DATA_FILE = 'dataset.txt'

# Given a file name
# Returns 1 if file exists, 0 otherwise
def fileExists(filename):
	if not os.path.exists(filename):
		return 0
	else:
		return 1

# Given a file name with structure of each line being [Sender, Recipient1, Recipient2, ...]
# Returns a directed graph
def createGraphFromFile(filename):

	G = nx.DiGraph()

	with open(filename) as FileObj:

		for line in FileObj:

			# Split each line into sender/recipients
			tokens = line.split(' ')
			
			if len(tokens) < 2:
				continue

			sender = tokens[0]
			recipients = tokens[1:-1] # -1 ignores the \n at end of each line


			# Create a directed edge from sender to each recipient
			if sender not in G:
				#print("Adding sender:", sender)
				G.add_node(sender)

			for recipient in recipients:

				if recipient not in G:
					#print("Adding recipient:", recipient)
					G.add_node(recipient)

				#print("Adding edge:", sender, recipient)
				G.add_edge(sender, recipient)

	return G
# Given graph and a node
# Returns a list of neighboring nodes, in which neighbors are bidirectionally connected
def findNeighbors(G, node):
	neighbors = []
	# For each successor of node
	for successor in G.successors(node):
		# Check if there is also an edge from successor to node
		if G.has_edge(successor,node):
			neighbors.append(successor)

	return neighbors


# Given the graph and a list of cliques (use sets because order does not matter in a clique)
# Returns a list of the largest cliques	
def largestClique(G, cliques):

	#print('Clique size:', len(cliques[0]), 'Number of cliques:', len(cliques))

	newCliques = [] # Will hold cliques of size + 1

	# See if any of the nodes in a clique has a neighbor that can be added to increase clique size by 1
	for clique in cliques: # For each clique
		for clique_node in clique: # For each node in the clique
			for neighbor in G.successors(clique_node): # For each neighbor of the node
				# Avoid redundancy
				if neighbor in clique:
					continue

				# Check if this neighbor can be added to the clique
				addToClique = True
				# If all nodes in the clique have an edges to/from this neighbor
				for node in clique:
					if not ( G.has_edge(node, neighbor) and G.has_edge(neighbor,node) ):
						addToClique = False
						break
				if addToClique:
					# Make sure not to add duplicates
					newSet = clique.union([neighbor])
					if newSet not in newCliques:
						newCliques.append(newSet)

				# Simpler algorithm but poor performance
				# # If the neighbors of node in question contains the clique, add it to the clique
				# if set(findNeighbors(G, neighbor)).intersection(clique) == clique: # If intersection is the clique itself
				# 		# Make sure not to add duplicates
				# 		newSet = clique.union([neighbor])
				# 		if newSet not in newCliques:
				# 			newCliques.append(newSet)

	# Base case: cannot increase size of any clique
	if len(newCliques) < 1:
		return cliques

	# Run again with our cliques of size + 1
	return largestClique(G, newCliques)


# Given the graph (G) and a list of 3-cycles (three_cycles)
# Returns a list of butterflies in the graph if any
def findButterflies(G, three_cycles):

	butterflies = []

	
	for cycle1 in three_cycles:
		for cycle2 in three_cycles:
			if len(cycle1.intersection(cycle2)) == 1: # Only 1 common element between the 2 sets
				
				# If these cycles have already verified as a butterfly, skip (avoid redundancy)
				if cycle1.intersection(cycle2) in butterflies:
					continue

				# Count the edges of each node to nodes in the other cycle
				numConnections = []
				for cycle1_node in cycle1:
					# Check to see if any (and how many) predecessors/successors are nodes in cycle2
					predecessors = set(G.predecessors(cycle1_node))
					successors = set(G.successors(cycle1_node))
					c2 = set(cycle2)

					deg_in = len(predecessors.intersection(c2)) # Using set intersection, find how many edges are there from nodes in cycle 2 to cycle1_node
					deg_out = len(successors.intersection(c2)) # Using set intersection, find how many edges from cycle1_node to nodes in cycle 2
					numConnections.append(deg_in + deg_out) # Total edges connecting cycle1_node and cycle2

				if sorted(numConnections) == [2,2,4]:
					newBF =  set(cycle1).union(cycle2)
					if newBF not in butterflies: # Don't create duplicates
						butterflies.append(newBF)
			
	return butterflies

# Given a graph (G) calculate the maximum out degree for any 

def main():

	# Check if data file exists
	if not fileExists(DATA_FILE):
		print('Error:', DATA_FILE, 'cannot be read. Make sure it is a valid file and try again.')
		return 0

	print("Creating graph...")
	G = createGraphFromFile(DATA_FILE)

	print("Graph created with", G.number_of_nodes(), "nodes and", G.number_of_edges(), "edges.")

	# Find the list of candidates for the leaker (woods)
	candidates = findNeighbors(G, 'WOODS')
	print('There are', len(candidates),'potential leakers:',candidates)
	
    # Build candidate graph and display
	H = nx.DiGraph()
	H.add_node('WOODS')
	H.add_nodes_from(candidates)
	for node in candidates:
		H.add_edge('WOODS', node)
		H.add_edge(node, 'WOODS')
	nx.draw(H, with_labels=True)
	plt.show()
	
	# Create a list of the nodes
	allNodes = []
	for node in G.nodes:
		if len(node) < 1 or node == '\n':
			continue
		allNodes.append(set([node])) # Cast to list before set otherwise will be a character-wise set, rather than a string-wise set

	# Find the largest clique
	print("Determining largest clique size...")
	largest = largestClique(G, allNodes)
	print('The largest clique size is',len(largest[0]),'with',len(largest),'cliques.')

	# Networkx code to determine maximum clique size - used to confirm largestClique function
	# H = G.to_undirected(reciprocal=True)
	# maxClique = nx.find_cliques(H)
	# maxLength = 0
	# count = 0
	# for clique in maxClique:
	# 	if len(clique) > maxLength:
	# 		maxLength = len(clique)
	# 		count = 0
	# 	if len(clique) == maxLength:
	# 		count = count + 1
	# print('Using find_clique the largest size is', maxLength, 'with', count, 'total cliques.')

	# Locating isolates - result was 0, so commented out.
	# solo = nx.isolates(G)
	# print('There are ',len(list(solo)), ' isolates in the network.')
	
	# Find the butterflies in the graph
	butterflies = findButterflies(G, largest)
	print("There are", len(butterflies), "butterflies in the graph.")
	#print("The butterflies are:")
	#for butterfly in butterflies:
	#	print(butterfly)

	#nx.write_gexf(G, "test.gexf") #Write to file to be read into Grephi for visualization

    # Degrees of Kevin Bacon
	degreeList = nx.degree_centrality(G)
	maxDegree = 0
	KBacon = []
	count = 0
	for dnode in degreeList:
		if degreeList[dnode] > maxDegree:
			count = 1
			maxDegree = degreeList[dnode]
			kingBacon = dnode
			if len(KBacon) > 0:
				del KBacon[:]
				KBacon.append(dnode)
			else:
				KBacon.append(dnode)
		elif degreeList[dnode] == maxDegree:
			count = count + 1
			KBacon.append(dnode)
			degree = len(nx.single_source_shortest_path(G,dnode,2))

	print('The Kevin Bacon of our graph is ', KBacon, ' with a maximum degree of ', maxDegree)
	print('There are ', count, ' Kevin Bacons in our graph.')

if __name__ == "__main__":
	main()