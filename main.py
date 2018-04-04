import networkx as nx
import matplotlib.pyplot as plt
import os.path

from matplotlib import pylab

DATA_FILE = 'dataset.txt'

def fileExists(filename):
	if not os.path.exists(filename):
		return 0
	else:
		return 1

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


			#print('sender:', sender, 'recipients:', recipients)

			# Create a directed edge from sender to each recipient
			if sender not in G:
				G.add_node(sender)
				#print("Adding sender:", sender)

			for recipient in recipients:

				if recipient not in G:
					#print("Adding recipient:", recipient)
					G.add_node(recipient)

				#print("Adding edge:", sender, recipient)
				G.add_edge(sender, recipient)

	return G


def main():

	# Check if data file exists
	if not fileExists(DATA_FILE):
		print('Error:', DATA_FILE, 'cannot be read. Make sure it is a valid file and try again.')
		return 0

	G = createGraphFromFile(DATA_FILE)

	nx.write_gexf(G, "test.gexf")



if __name__ == "__main__":
	main()