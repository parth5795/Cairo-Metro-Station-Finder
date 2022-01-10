from django.shortcuts import render
import networkx as nx
import json
from django.shortcuts import render
# Create your views here.

# gets the line information and stored them into a variable
line1 = json.loads(open('main/Line1.json').read())
line2 = json.loads(open('main/Line2.json').read())
line3 = json.loads(open('main/Line3.json').read())
stations = line1+line2+line3
#C:\Users\parth\Cairo-Metro-Station-Finder\MetroStation\main\Line3.json

# create a graph of the metro stations
metroStationsNetwork = nx.Graph()

metroStationsNetwork.add_nodes_from(line1, line=1)
metroStationsNetwork.add_nodes_from(line2, line=2)
metroStationsNetwork.add_nodes_from(line3, line=3)

for edge in zip(line1, line1[1:]):
    metroStationsNetwork.add_edge(*edge)

for edge in zip(line2, line2[1:]):
    metroStationsNetwork.add_edge(*edge)

for edge in zip(line3, line3[1:]):
    metroStationsNetwork.add_edge(*edge)

# this function will return the shortest path between two stations
def shortestPath(source, destination):
    return nx.shortest_path_length(metroStationsNetwork, source, destination)

# This function will return the path between two stations
def getPath(source, destination):
    paths =  [x for x in nx.all_shortest_paths(metroStationsNetwork, source, destination)]

    if len(paths) > 1:
        scores = [0 for i in paths]

        for i, path in enumerate(paths):
            prevLine = metroStationsNetwork.nodes[path[0]]['line'] if path[0] not in ['Al-Shohadaa', 'Attaba', 'Sadat'] else None

            for station in path[1:]:
                if station in ['Al-Shohadaa', 'Attaba', 'Sadat']:
                    continue

                currentLine = metroStationsNetwork.nodes[station]['line']
                if currentLine != prevLine and not prevLine is None:
                    scores[i] += 1

                prevLine = currentLine

        if min(scores) == max(scores):
            return tuple(path for path in paths)
        
        else:
            return paths[scores.index(min(scores))]

    else:
        return paths[0]

# This function will convert the list to appropriate string format
def listToString(list):
    string = ''
    for item in list:
        string += item + ' -> '
    return string[:-4]

def index(request):
    if request.method == 'POST':
        try:
            source = request.POST.get('Source')
            destination = request.POST.get('Destination')
            path = listToString(getPath(source, destination))
            numberofStations = shortestPath(source, destination)
            return render(request, 'main/index.html', {'path': path, 'numberofStations': numberofStations,'stations': stations})
        except:
            return render(request, 'main/index.html', {'error': 'Source and Destination are not valid', 'stations': stations})    
    return render(request, 'main/index.html', {'stations':stations})
