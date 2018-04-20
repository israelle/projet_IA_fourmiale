# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 17:02:54 2018
@author: israelle
"""

import pants
import csv
import geopy.distance
import networkx as nx
import matplotlib.pyplot as plt

nodes = []

def readCSV():

        with open('some_pubs.csv', 'r') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csvReader)
            for row in csvReader:
                    latitude = row[6]
                    longitude = row[7]

                    print("latitude : " + latitude, "longitude : " + longitude)
                    try:
                        if (latitude !='' and  longitude != '' and
                                latitude != '/N' and longitude != '/N' and
                                isinstance(float(latitude), float) and isinstance(float(longitude), float)):
                            nodes.append((float(latitude), float(longitude)))
                    except Exception as ex:
                        print(format(ex))


def deleteOccurence(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def calculDistance(x, y):
    dist = geopy.distance.vincenty(x, y).km
    print(dist)
    return dist


def methodeSolve(solver, world):
    try:
            solution = solver.solve(world)  # best solution
            if solution is None:
                print("solution None")
            # print the best distance by solver
            else:
                print("")
                print(" Best distance : " + format(solution.distance) + " km")
                print("")
                return  solution.tour
    except Exception as ex:
        print("error in methodeSolve(solver, world) : " + format(ex))

def displaySolution(solver, world):
    try:
        if(type(solver) and type(world)):
            methodeSolutions(solver, world)
            noeudsVisite = methodeSolve(solver, world)

            drawGraph(noeudsVisite)
    except Exception as ex:
        print("printSolution : " + format(ex))

def methodeSolutions(solver, world):
    try:
        solutions = solver.solutions(world)
        i = 1
        bestSolution = float("inf")
        for sol in solutions:
            print("")
            print("Distance " + format(i) + " : " + format(sol.distance) + " KM")
            i += 1
            if sol.distance < bestSolution:
                bestSolution = sol.distance

            # print the best distance
            print("")
            print("Best distance solver solutions : " + format(bestSolution) + " km")
            print("")
    except Exception as ex:
        print("error in methodesolutions : " + format(ex))



def drawGraph(noeudsVisite):
    G = nx.Graph()
    for noeud in noeudsVisite:
        G.add_edge(format(noeud[0]), format(noeud[1]), weight=0.6)
    plt.subplot(121)

    node_positions = nx.spring_layout(G)
    nx.draw_networkx(G, pos=node_positions, node_size=100, node_color='red', edge_color="green", with_labels=True,
                     alpha=1)

    edge_labels = nx.get_edge_attributes(G, 'sequence')
    nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_labels, font_size=20)
    nx.draw_networkx_nodes(G, pos=node_positions, node_size=20)
    nx.draw_networkx_edges(G, pos=node_positions, alpha=0.4)

    plt.xticks([])
    plt.yticks([])

    plt.text(0.5, 0.5, G, ha="center", va="center", size=15, alpha=.5)
    plt.title('Affichage des noeuds visitées', size=13)
    plt.axis('off')

    plt.subplot(122)
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    print("Degree sequence", degree_sequence)
    dmax = max(degree_sequence)
    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.title("Courbe")
    plt.ylabel("Degree")
    plt.xlabel("Rank")

    # dessine le graphique dans l'encart
    plt.axes([0.45, 0.45, 0.45, 0.45])
    Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    pos = nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc, pos, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
    plt.xticks([])
    plt.yticks([])
    plt.text(0.5, 0.5, Gcc, ha="center", va="center", size=24, alpha=.5)
    plt.show()

# main program
def main():
    try:
        readCSV()
        world = pants.World()
        solver = pants.Solver()
        displaySolution(solver, world)
    except Exception as ex:
        print("main : " + format(ex))
main()