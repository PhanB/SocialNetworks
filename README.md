Large databases, such as those used in social media networks, are most readily modeled as graphs, where the individuals and institutions are nodes and the connections between them are the edges. In this project, we used a simple text representation of a company-wide email network to generate a directed graph, and then to collect information on the groups within the company. 

## Trade Secrets

##### Q1. The HRS of BN has a contract with the security company Kandella which established that the user woods recently sold a trade secret of HN (design of their new luxurious ladies handbag) on dark Web. It has further been established that the document containing the secret was provided to woods by someone within the company and probably some of negotiations leading to this security incident were conducted by email in December 2017. Find the list of candidates for the leaker (i.e. person who may have signalled to woods that they will provide secret.

In the information from Kandella, they indicated that Woods received the design from someone else within the company and that most likely the parties negotiated via email during the time of the study. Using the assumption that a negotiation would involve two-way communication, we searched for all of Woods neighbors that also had an edge to Woods. Checking in this fashion gave us 10 potential conspirators: Ayers, Banks, Branch, Howe, Hudson, McDaniel, Moreno, Morton, Richardson, West
```
def findNeighbors(G, node):
    neighbors = []
    # For each successor of node
    for successor in G.successors(node):
        # Check if there is also an edge from successor to node
        if G.has_edge(successor,node):
            neighbors.append(successor)

    return neighbors
```

## Clique Size

##### Q2. List all cliques of largest size (remember that in a directed graph a clique of size n involves n(n − 1) directed edges, not n(n−1) 2 edges, as in the undirected graph) . You will need to design an algorithm that computes maximal cliques. Hint: if C clique in our directed graph G then for every C 0 ⊆ C, the graph G restricted to C 0 is also a clique. Use this property to design a recursive algorithm for our task. 

To determine maximum clique size, we used two different methods. In the first method, we built a function that started at a single node and examined each neighbor for inclusion in the clique. If the neighbor had edges to each member of the clique and was not already a member of the clique, it was added to the clique.
``` 
def largestClique(G, cliques):
   
    newCliques = [] # Will hold cliques of size + 1

    # Check if any nodes in a clique has a neighbor that can be added
    for clique in cliques: # For each clique
        for clique_node in clique: # For each node in the clique
            for neighbor in G.successors(clique_node): # For each neighbor
                # Avoid redundancy
                if neighbor in clique:
                    continue
                # Check if this neighbor can be added to the clique
                addToClique = True
                # If all nodes in clique have edges to this neighbor
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
```

To confirm the algorithm above, we then used the Networkx function to_undirected to convert our directed graph to an undirected graph and then the function find_cliques to locate the largest clique for each node. We then iterated through the list to determine both the largest clique size and the number of cliques found of that size. This confirmed our results of 114 cliques of a maximum size of three.


## Locating Butterflies

##### Q3. A butterfly in a digraph G is a subgraph B with five nodes {A, B, C, D, E} having two cliques of size three {A,B,C} and {C,D,E} that are connected through common node C and have no additional edges. Check if the BN network contains a butterfly. If so, compute one.
We used the list we generated in our clique function to determine if a pair of cliques was a butterfly. A butterfly is two cliques of size 3 that share a single point in common with no additional edges from the other edges. Using the function below, we found 30 butterflies.
def findButterflies(G, three_cycles):

    butterflies = []
    
    for cycle1 in three_cycles:
        for cycle2 in three_cycles:
            # Only 1 common element between the 2 sets
            if len(cycle1.intersection(cycle2)) == 1:            
                # If already verified as a butterfly, skip (avoid redundancy)
                if cycle1.intersection(cycle2) in butterflies:
                    continue

                # Count the edges of each node to nodes in the other cycle
                numConnections = []
                for cycle1_node in cycle1:
                    # Check how many predecessors/successors are nodes in cycle2
                    predecessors = set(G.predecessors(cycle1_node))
                    successors = set(G.successors(cycle1_node))
                    c2 = set(cycle2)
                    
                    # Ignore any self pointing edges (butterfly can have self pointing nodes)
					predecessors-= set([cycle1_node])
					successors-= set([cycle1_node])

                    # Find #edges from nodes in cycle2 to cycle1_node-intersect
                    deg_in = len(predecessors.intersection(c2))
                    # Find #edges from cycle1_node to nodes in cycle2-intersect
                    deg_out = len(successors.intersection(c2))
                    # Total edges connecting cycle1_node and cycle2
                    numConnections.append(deg_in + deg_out) 
                if sorted(numConnections) == [2,2,4]:
                    newBF =  set(cycle1).union(cycle2)
                    if newBF not in butterflies: # Don't create duplicates
                        butterflies.append(newBF)

    return butterflies
## Six Degrees of Kevin Bacon - Interconnectivity in the Graph

##### Q4. The company claims that they are a closely knit group with a strong corporate culture, where everyone works equally with everyone else. Does the graph reflect this?
Six degrees of separation is a graph concept in popular culture that each person is at most 6 steps from every other person in the world. In movie culture, this was refined to Six Degrees of Kevin Bacon, due to his large body of work in movies and television. There the idea is that no actor, director or producer is more than 6 steps from Kevin Bacon. 
In our graph, we used two measures of connectedness to simulate the Kevin Bacon concept. The first was to calculate the degree centrality with Networkx. The degree centrality is a calculation of the number of nodes an individual node is connected to, normalized by the maximum number of nodes it could be connected to. This number is normally under one, but in a digraph with self loops that number can sometimes exceed one. 
nconnectedn-1
After iterating through the graph, we determined that two people had the same degree centrality. They are Galvan and Warren, who both have a degree centrality of 0.22122. 
However, the Kevin Bacon question is most often done as the stepwise path from connection to connection. This we simulated using the Networkx function single_source_shortest_path. This allowed us to calculate the number of shortest paths from each node to all other nodes at a defined depth. Initially we calculated this with a depth of 6, but that resulted in nearly 100% of the sources connecting to all other nodes. Eventually we reduced the depth to 2, and then calculated the average number of paths to 998.895. 
```
# Degrees of Kevin Bacon problem as a series of connectivity calculations
# Calculates degree centrality, locates the individuals with the highest levels of degree centrality
# Calculates the # paths to depth 2 using each node as a source, then calculates the average # paths
def defineConnectivity(G):
    degreeList = nx.degree_centrality(G)
    maxDegree = 0
    KBacon = []
    paths = {}
    count = 0
    for dnode in degreeList:  # iterating through the degreeList dictionary
        if degreeList[dnode] > maxDegree: # update maxDegree and count for new maximum
            count = 1
            maxDegree = degreeList[dnode]
            kingBacon = dnode
            if len(KBacon) > 0: # emptying the list before adding a new candidate
                del KBacon[:]
                KBacon.append(dnode)
            else:
                KBacon.append(dnode)
        elif degreeList[dnode] == maxDegree:
            count = count + 1
            KBacon.append(dnode)
        paths[dnode] = len(nx.single_source_shortest_path(G,dnode,2))
    
    total = 0
    count = 0
    for k,v in paths.items():
        total = total + v
        count = count + 1
    avgconnect = total / (count+1)
    print('The Kevin Bacon of our graph is ', KBacon, ' with a maximum degree of ', maxDegree)
    print('There are ', len(KBacon), ' Kevin Bacons in our graph.')
    print('Each node can reach ', avgconnect, ' nodes by depth 2 on average.')
```


The Kevin Bacon question would be more interesting in a larger network, such as FaceBook, in order to map the connections between groups. In our graph, this shows a high degree of connectivity between all of the users, which could be a possible indication of the corporate culture. Additionally, no one user has the highest degree centrality, which indicates that there is not a single point person that acts as the glue to hold the teams together. Based on the graph, the company’s assertions about their culture seem founded.
