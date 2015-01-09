#!/usr/bin/python
# -*- coding: utf8 -*-

""" 
WDR Rockpalast
Copyright (C) 2012 Xycl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""


# os imports
import urllib, urllib2, re, os, sys
from HTMLParser import HTMLParser

# xbmc imports
import xbmcplugin, xbmcgui, xbmc


        
def smart_unicode(s):
    """credit : sfaxman"""
    if not s:
        return ''
    try:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                s = unicode(str(s), 'UTF-8')
        elif not isinstance(s, unicode):
            s = unicode(s, 'UTF-8')
    except:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                s = unicode(str(s), 'ISO-8859-1')
        elif not isinstance(s, unicode):
            s = unicode(s, 'ISO-8859-1')
    return s


def smart_utf8(s):
    return smart_unicode(s).encode('utf-8')

    
def log(msg, level=xbmc.LOGDEBUG):

    if type(msg).__name__=='unicode':
        msg = msg.encode('utf-8')

    filename = smart_utf8(os.path.basename(sys._getframe(1).f_code.co_filename))
    lineno  = str(sys._getframe(1).f_lineno)

    try:
        module = "function " + sys._getframe(1).f_code.co_name
    except:
        module = " "

    xbmc.log(str("[%s] line %5d in %s %s >> %s"%("plugin.video.wdrrockpalast", int(lineno), filename, module, msg.__str__())), level)   
    
    
def show_main_entry():
    
    url = 'http://www1.wdr.de/fernsehen/kultur/rockpalast/videos/rockpalastvideos_konzerte100.html'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match_years=re.compile('<h2 .*?class="colored">(\d+)</a></h2>(.*?)<h2 ',re.DOTALL).findall(link)
    for year, block in match_years:    
        match=re.compile('<li class="teaserCont.*?<img src="(.*?)".*?/>.*?<a href="(.*?)".*?>(.*?)</a>',re.DOTALL).findall(block)
        for img,url,name in match:
            name = name.strip(' \t\n\r')
            #name = name.decode('ISO-8859-1').encode('utf-8')
            log("Found concert name: %s"%name)
            log("Found concert url:  %s"%url)
            add_dir(HTMLParser().unescape(name + " ("+str(year) +")"), 'HTTP://www1.wdr.de'+url, 1, 'HTTP://www1.wdr.de'+img) #'HTTP://www.wdr.de/tv/rockpalast/codebase/img/audioplayerbild_512x288.jpg')
    
    
    url = 'http://www1.wdr.de/fernsehen/kultur/rockpalast/videos/rockpalastvideos_festivals100.html'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match_years=re.compile('<h2 .*?class="colored">(\d+)</a></h2>(.*?)<h2 ',re.DOTALL).findall(link)
    for year, block in match_years:
        match=re.compile('<li class="teaserCont.*?<img src="(.*?)".*?/>.*?<a href="(.*?)".*?>(.*?)</a>',re.DOTALL).findall(block)
    
        for img,url,name in match:
            name = name.strip(' \t\n\r')
            #year = year.strip(' \t\n\r')
            #name = name.decode('ISO-8859-1').encode('utf-8')
            #log("Found concert year: %s"%year)
            log("Found concert name: %s"%name)
            log("Found concert url:  %s"%url)
            add_dir(HTMLParser().unescape(name + " ("+str(year) +")"), 'HTTP://www1.wdr.de'+url, 1, 'HTTP://www1.wdr.de'+img) #'HTTP://www.wdr.de/tv/rockpalast/codebase/img/audioplayerbild_512x288.jpg')
            #add_dir(HTMLParser().unescape(name), 'HTTP://www1.wdr.de'+url, 1, 'HTTP://www1.wdr.de'+img) #'HTTP://www.wdr.de/tv/rockpalast/codebase/img/audioplayerbild_512x288.jpg')
            
                
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_concerts(url):

    #print "----------------------"
    #print url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    video_page=response.read()
    response.close()
    
    #channels=re.compile('channels : \[.*?{.*?bezeichnung : "(Liveauftritte|Konzerte)",(.*?)\].*?},', re.DOTALL).findall(video_page)
    
    """
    for channel, content in channels:
        #print channel
    
        video_urls=re.compile('thumbnail: "(.*?)",.*?headline: "(.*?)",.*?link: "(.*?)"',re.DOTALL).findall(content)
        try:
            for img, title, url in video_urls:
                #print url
                add_dir(HTMLParser().unescape(title), 'HTTP://www1.wdr.de'+url, 2, 'HTTP://www1.wdr.de'+img)
        except:
            pass
    """
    video_urls=re.compile('thumbnail: "(.*?)",.*?headline: "(.*?)",.*?link: "(.*?)"',re.DOTALL).findall(video_page)
    try:
        for img, title, url in video_urls:
            #print url
            add_dir(HTMLParser().unescape(title), 'HTTP://www1.wdr.de'+url, 2, 'HTTP://www1.wdr.de'+img)
    except:
        pass    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
def play_video(from_url, name):

    #print "play_video"
    #print from_url
    
    req = urllib2.Request(from_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    video_page=response.read()
    response.close()
    #print "-------------------"
    #print video_page
    #print "-------------------"

                                           
    video_urls=re.compile('<a rel="adaptiv" type="application/vnd.apple.mpegURL" href="(.*?)">',re.DOTALL).findall(video_page)
    #print video_urls
    #return
    try:
        for video_url in video_urls:
        
            # load page containing the video
            listitem = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage='HTTP://www.wdr.de/tv/rockpalast/codebase/img/audioplayerbild_512x288.jpg')
            listitem.setInfo('video', {'Title': name})
            #xbmc.Player(xbmc.PLAYER_CORE_AUTO).play( 'http://adaptiv.wdr.de/i/medstdp/ww/fsk0/59/594170/,594170_6290932,594170_6290931,594170_6290930,594170_6290934,.mp4.csmil/master.m3u8', listitem) 
            xbmc.Player(xbmc.PLAYER_CORE_AUTO).play( video_url, listitem) 
            return
    except:
        pass

def get_params():
    """ extract params from argv[2] to make a dict (key=value) """
    param_dict = {}
    try:
        if sys.argv[2]:
            param_pairs=sys.argv[2][1:].split( "&" )
            for params_pair in param_pairs:
                param_splits = params_pair.split('=')
                if (len(param_splits))==2:
                    param_dict[urllib.unquote_plus(param_splits[0])] = urllib.unquote_plus(param_splits[1])
    except:
        pass
    return param_dict


def add_dir(name, url, mode, iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)

    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
        
              
params=get_params()

url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass


if mode==None or url==None or len(url)<1:
    show_main_entry()
       
elif mode==1:
    show_concerts(url)
    
elif mode==2:
    play_video(url, name)

