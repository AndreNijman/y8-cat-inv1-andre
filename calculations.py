import math

class Distance:
    def distance(point1, point2):
        distance = ((point2[0]-point1[0])*(point2[0]-point1[0]))+((point2[1]-point1[1])*(point2[1]-point1[1]))**1/2
        return distance

    def midpoint(point1, point2):
        MX = (point1[0]+point2[0])/2
        MY = (point1[1]+point2[1])/2
        return [MX, MY]

    def gradient(point1, point2):
        rise = point2[1]-point1[1]
        run = point2[0]-point1[0]
        gradient = rise/run
        return gradient
    
    
    