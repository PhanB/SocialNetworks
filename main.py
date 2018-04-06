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

	# Base case: cannot increase size of any clique
	if len(newCliques) < 1:
		return cliques

	# Run again with our cliques of size + 1
	return largestClique(G, newCliques)



def main():

	# Check if data file exists
	if not fileExists(DATA_FILE):
		print('Error:', DATA_FILE, 'cannot be read. Make sure it is a valid file and try again.')
		return 0

	print("Creating graph...")
	G = createGraphFromFile(DATA_FILE)

	

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
	H = G.to_undirected(reciprocal=True)
	maxClique = nx.find_cliques(H)
	maxLength = 0
	count = 0
	for clique in maxClique:
		if len(clique) > maxLength:
			maxLength = len(clique)
			count = 0
		if len(clique) == maxLength:
			count = count + 1
	print('Using find_clique the largest size is', maxLength, 'with', count, 'total cliques.')

	#print(G.number_of_nodes(), G.number_of_edges())

	#nx.write_gexf(G, "test.gexf") #Write to file to be read into Grephi for visualization



if __name__ == "__main__":
	main()