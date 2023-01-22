from .models import *
from .utils import *

def getSourcePoints():
    nonDeliveredProducts = product.objects.filter(assigned=False)
    sourceList = []
    for i in nonDeliveredProducts:
        LocationInstance = Location.objects.get(productID = i.productID, locationtype = True)
        sourceList.append([float(LocationInstance.latitude), float(LocationInstance.longitude)])
    return sourceList

def getDestinationPoints():
    nonDeliveredProducts = product.objects.filter(assigned=False)
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

def getcurrentPoint(path):
    for i, item in enumerate(path):
        itemDelivered = product.objects.get(productID=item[0]).delivered
        if itemDelivered == True:
            continue
        else:
            return i
    return len(path)

def getLocations(driverPath, currentPoint):
    newPath = driverPath[0:currentPoint]
    locations = []
    for i, item in enumerate(driverPath[currentPoint:]):
        if item[1] == "s":
            location = Location.objects.get(productID=item[0], locationtype=True)
            locations.append(location)
        elif item[1] == "d":
            location = Location.objects.get(productID=item[0], locationtype=False)
            locations.append(location)
    return (newPath, locations)

def driverDetails():
    drivers = Driver.objects.filter(active=True)
    driverDetails = {}
    for i in drivers:
        driverPath = i.path
        currentPoint = getcurrentPoint(driverPath)
        details = getLocations(driverPath, currentPoint)
        locations = details[1]
        newpath = details[0]
        instance = {
            "originalPath" : driverPath,
            "newPath" : newpath,
            "locations" : locations,
            "driver" : i,
            "currentPoint" : currentPoint
        }
        driverDetails[i.person] = instance
    return driverDetails

def dynamicPointAddition():
    nonDeliveredProducts = product.objects.filter(assigned=False)
    drivers = driverDetails()
    for i in nonDeliveredProducts:
        sourceLocation = Location.objects.get(productID=i.productID, locationtype=True)
        destinationLocation = Location.objects.get(productID=i.productID, locationtype=False)
        tempMap = {}
        for j in drivers.keys():
            comp1 = [10000000, -1]
            for k, item in enumerate(drivers[j]["locations"]):
                distance = euclid_dist(item.latitude, item.longitude, sourceLocation.latitude, sourceLocation.longitude)
                if (k != len(drivers[j]["locations"])-1):
                    distance = distance + euclid_dist(sourceLocation.latitude, sourceLocation.longitude, drivers[j]["locations"][k+1].latitude, drivers[j]["locations"][k+1].longitude)
                    distance = distance - euclid_dist(item.latitude, item.longitude, drivers[j]["locations"][k+1].latitude, drivers[j]["locations"][k+1].longitude)
                if (distance < comp1[0]):
                    comp1[0] = distance 
                    comp1[1] = k
            comp2 = [10000000, -1]
            for k, item in enumerate(drivers[j]["locations"][comp1[1]:]):
                if (k == 0):
                    distance = euclid_dist(sourceLocation.latitude, sourceLocation.longitude, destinationLocation.latitude, destinationLocation.longitude)
                else:
                    distance = euclid_dist(item.latitude, item.longitude, sourceLocation.latitude, sourceLocation.longitude)
                if (k != len(drivers[j]["locations"][comp1[1]:])-1):
                    distance = distance + euclid_dist(destinationLocation.latitude, destinationLocation.longitude, drivers[j]["locations"][comp1[1]:][k+1].latitude, drivers[j]["locations"][comp1[1]:][k+1].longitude)
                    if k == 0:
                        distance = distance - euclid_dist(sourceLocation.latitude, sourceLocation.longitude, drivers[j]["locations"][comp1[1]:][k+1].latitude, drivers[j]["locations"][comp1[1]:][k+1].longitude)
                    else:
                        distance = distance - euclid_dist(item.latitude, item.longitude, drivers[j]["locations"][k+1].latitude, drivers[j]["locations"][k+1].longitude)
                if (distance < comp2[0]):
                    comp2[0] = distance 
                    comp2[1] = k
            tempMap[j] = {
                "driver" : i,
                "distance" : comp1[0]+comp2[0],
                "index1" : comp1[1],
                "index2" : comp2[1]
            }
        mn = 10000000
        driver = None
        for j in tempMap.keys():
            if (tempMap[j]["distance"] < mn):
                mn = tempMap[j]["distance"]
                driver = j
        a = drivers[driver]["currentPoint"]
        b = tempMap[driver]["index1"]
        c = tempMap[driver]["index2"]
        sourceProductList = [[sourceLocation.productID, "s"]]
        destinationProductList = [[destinationLocation.productID, "d"]]
        sourcePointList = [sourceLocation]
        destinationPointList = [destinationLocation]
        drivers[driver]["originalPath"] = drivers[driver]["originalPath"][0:a+b+1] + sourceProductList + drivers[driver]["originalPath"][a+b+1:a+b+c+1] + destinationProductList + drivers[driver]["originalPath"][a+b+c+1:]
        drivers[driver]["locations"] = drivers[driver]["locations"][0:b+1] + sourcePointList + drivers[driver]["locations"][b+1:b+c+1] + destinationPointList + drivers[driver]["locations"][b+c+1:]
    return drivers