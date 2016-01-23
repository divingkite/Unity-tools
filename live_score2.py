import sys
import appindicator
import re
import gtk
import urllib2
import imaplib
import json
import socks
import socket

PING_FREQ = 60 #seconds for updating info.

class Score:
    def __init__(self):
        
        self.ind = appindicator.Indicator("NAME OF THE INDICATOR",
                                          "PATH FOR THE ICON OF THE APPLICATION WHEN ACTIVE",
                                          appindicator.CATEGORY_APPLICATION_STATUS)
        # sets the status of the application to active 
        self.ind.set_status(appindicator.STATUS_ACTIVE) 
        
        # sets the icon when status of application is set to attention, can also be set for passive condition                            
        self.ind.set_attention_icon("PATH FOR THE ICON OF THE APPLICATION WHEN IN ATTENTION")
        
        # sets up the menu for our application
        self.menu_setup()
        self.ind.set_menu(self.menu)
        self.match_id = 0   # Identity of a particular match 

    def connectTor(self):
        # sets the connections for using tor
        socks.setdefaultproxy( socks.PROXY_TYPE_SOCKS5, "127.0.0.1",PORT,True )
        socket.socket = socks.socksocket
 
    def url_opener(self,url):
        # select your mode of connection to the internet 
        # self.connectTor()
        # proxy = urllib2.ProxyHandler( { 'http':'http://proxyuser:proxypwd@proxy.server.com:port','https':'https://proxyuser:proxypwd@proxy.server.com:port' } )
        
        auth = urllib2.HTTPBasicAuthHandler()
        opener = urllib2.build_opener( auth, urllib2.HTTPHandler ) # add proxy parameter to the function if proxy is used 
                                                                   # opener = urllib2.build_opener( proxy,auth, urllib2.HTTPHandler )
        urllib2.install_opener(opener)
        link_file = urllib2.urlopen(url)
        return link_file

    def menu_setup(self):
        # menu_setup function as used in __init__
        self.menu = gtk.Menu()
        self.quit_item = gtk.MenuItem("Quit")         # defines the name to be displayed on  the menu list
        self.quit_item.connect("activate",self.quit)  # uses the self.quit function when we click on "Quit" option
        self.quit_item.show()
        self.menu.append(self.quit_item)
        
        # Addition of the list of matches
        match_list = self.get_match_list()
        for match in match_list:
            self.menu_item = gtk.MenuItem( "%s"%( match['title']) )
            self.menu_item.connect("activate" ,self.get_score, match['unique_id']) # we can pass here other parameters as required
            self.menu_item.show()
            self.menu.append( self.menu_item )
        
    def get_score(self,widget,match_id ):
        # gets the current score for a particular match 
        # this function is called when a particular match is selected
        
        self.match_id = match_id
        url = "http://crm.wherrelz.com/api/cricketScore?unique_id=" + str(self.match_id)
        link_file = self.url_opener(url)
        data = json.loads(link_file.read())
        self.ind.set_label( data['score'])                       # used to print in unity-bar set_label( string )

    def get_score_help(self):
        url = "http://crm.wherrelz.com/api/cricketScore?unique_id=" + str(self.match_id)
        link_file = self.url_opener(url)
        data = json.loads(link_file.read())
        self.ind.set_label( data['score'])                       # used to print in unity-bar set_label( string )
        return True      # Always return true if you want your callback function to be called again by gtk.timeout_add function
                 
    def get_match_list(self):
        # Returns the match list, which may be live or ended 
        url = "http://crm.wherrelz.com/api/cricket/"
        link_file = self.url_opener(url)
        data = json.loads(link_file.read())
        return data['data']
    
    def main(self):
        gtk.timeout_add(PING_FREQ * 1000, self.get_score_help )
        gtk.main()

    def quit(self, widget):   
        # quit function used in menu_setup
        sys.exit(0)
    
if __name__ == "__main_":
    indicator = Score()
    indicator.main()
