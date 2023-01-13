from .models import *
from .utils import *

def getSourcePoints():
    nonDeliveredProducts = product.objects.filter(delivered=False)
    sourceList = []
    for i in nonDeliveredProducts:
        LocationInstance = Location.objects.get(productID = i.productID, locationtype = True)
        sourceList.append([float(LocationInstance.latitude), float(LocationInstance.longitude)])
    return sourceList

def getDestinationPoints():
    nonDeliveredProducts = product.objects.filter(delivered=False)
    destList = []
    for i in nonDeliveredProducts:
        LocationInstance = Location.objects.get(productID = i.productID, locationtype = False)
        destList.append([float(LocationInstance.latitude), float(LocationInstance.longitude)])
    return destList

def pathForSourceClusters(clusters):
    result = []
    distanceTravelled = 0
    for i in range(len(clusters)):
        clst = clusters[i]
        possible_pts = []
        ans = []
        for j in clst:
            possible_pts.append(tuple([tuple(j),"s"]))
        possible_pts = list(set(possible_pts))
        start = [0,0]    
        while len(possible_pts) > 0:
            ind = 0
            mn = 10000000 
            for k in range(len(possible_pts)):
                dis = euclid_dist(start[0], start[1], possible_pts[k][0][0], possible_pts[k][0][1])
                if mn > dis:
                    ind = k
                    mn = dis
            distanceTravelled = distanceTravelled + mn
            if (possible_pts[ind][1] == "s"):
                productIDs = Location.objects.filter(latitude=possible_pts[ind][0][0], longitude=possible_pts[ind][0][1], locationtype=True)
                for k in productIDs:
                    ans.append([k.productID, "s"])
                    productDestination = Location.objects.get(productID = k.productID, locationtype=False)
                    possible_pts.append([[productDestination.latitude, productDestination.longitude], k.productID])
            else:
                ans.append([possible_pts[ind][1], "d"])
            start = [possible_pts[ind][0][0], possible_pts[ind][0][1]]
            possible_pts.remove(possible_pts[ind])
        result.append(ans)
    return {"distanceTravelled" : distanceTravelled, "result" : result}

def pathForDestinationClusters(clusters):
    result = []
    distanceTravelled = 0
    for i in range(len(clusters)):
        clst = clusters[i]
        possible_pts = []
        ans = []
        for j in clst:
            productIDs = Location.objects.filter(latitude=j[0], longitude=j[1], locationtype=False)
            for k in productIDs:
                possible_pts.append(((k.latitude, k.longitude), "s", k.productID))
        possible_pts = list(set(possible_pts))
        start = [0,0]    
        while len(possible_pts) > 0:
            ind = 0
            mn = 10000000 
            for k in range(len(possible_pts)):
                dis = euclid_dist(start[0], start[1], possible_pts[k][0][0], possible_pts[k][0][1])
                if mn > dis:
                    ind = k
                    mn = dis
            distanceTravelled = distanceTravelled + mn
            if (possible_pts[ind][1] == "s"):
                ans.append([possible_pts[ind][2], "s"])
                productDestination = Location.objects.get(productID=possible_pts[ind][2], locationtype=False)
                possible_pts.append([[productDestination.latitude, productDestination.longitude], "d", possible_pts[ind][2]])
            else:
                ans.append([possible_pts[ind][2], "d"])
            start = [possible_pts[ind][0][0], possible_pts[ind][0][1]]
            possible_pts.remove(possible_pts[ind])
        result.append(ans)
    return {"distanceTravelled" : distanceTravelled, "result" : result}

def master():
    sourcePoints = getSourcePoints()
    destinationPoints = getDestinationPoints()
    sourcemeans = CalculateMeans(5, sourcePoints)
    destinationmeans = CalculateMeans(5, destinationPoints)
    sourceclusters = FindClusters(sourcemeans, sourcePoints)
    destinationclusters = FindClusters(destinationmeans, destinationPoints)
    sourceresult = pathForSourceClusters(sourceclusters)
    destinationresult = pathForDestinationClusters(destinationclusters)
    if sourceresult["distanceTravelled"] > destinationresult["distanceTravelled"]:
        finalResult = destinationresult
    else:
        finalResult = sourceresult
    return finalResult