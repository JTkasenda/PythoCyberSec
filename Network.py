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
    
def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(src, dst)
            kmlPts = kmlPts +   KML
        except:
            pass

    return kmlPts

def main():
    f = open("Networks.pcap", "rb")
    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Documen>\n'\
    '<Style id="transBluePoly">'\
    '<LineStyle>\n'\
    '<width>1.5</width>'\
    '<color>5014006</color>'\
    '</LineStyle>'\
    '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc = kmlheader+plotIPs(pcap)+kmlfooter
    print(kmldoc)


    if __name__ == '__main__':
        main()