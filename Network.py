import dpkt
import socket
import pygeoip


gi = pygeoip.GeoIP("GeoLiteCity.dat")

def retKML(dstip,scrip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name("x.xxx.xxx.xxx")
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f, %6f\n%6f, %6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''
    
    