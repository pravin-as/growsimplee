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
    for i in range(len(clusters)):
        clst = clusters[i]
        possible_pts = []
        ans = []
        for j in clst:
            possible_pts.append([j,"s"])
        start = [0,0]    
        while len(possible_pts) > 0:
            ind = 0
            mn = 10000000 
            for k in range(len(possible_pts)):
                dis = euclid_dist(start[0], start[1], possible_pts[k][0][0], possible_pts[k][0][1])
                if mn > dis:
                    ind = k
                    mn = dis
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
    return result

def master():
    a = getSourcePoints()
    b = getDestinationPoints()
    means = CalculateMeans(5, a)
    clusters = FindClusters(means, a)
    res = pathForSourceClusters(clusters)
    return [clusters, res]