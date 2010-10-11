import re, random
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
##################################################################################################FOX
PLUGIN_PREFIX     = "/video/Fox"

FOX_URL                     = "http://www.fox.com"
FOX_FULL_EPISODES_SHOW_LIST = "http://www.fox.com/full-episodes/"
CACHE_INTERVAL              = 3600
FOX_FEED                    = "http://www.fox.com/fod"
DEBUG                       = False
foxart                      ="art-default.png"
foxthumb                    ="icon-default.png"

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "FOX","icon-default.png", "art-default.png")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
  
  MediaContainer.art        =R(foxart)
  DirectoryItem.thumb       =R(foxthumb)
  WebVideoItem.thumb        =R(foxthumb)

####################################################################################################
#def MainMenu():
#    dir = MediaContainer(mediaType='video') 
#    dir.Append(Function(DirectoryItem(all_shows, "All Shows"), pageUrl = #FOX_FULL_EPISODES_SHOW_LIST))
#    return dir
    
####################################################################################################
def MainMenu():
    dir = MediaContainer(mediaType='video')
#    dir = MediaContainer(title2=sender.itemTitle)
    pageUrl=FOX_FULL_EPISODES_SHOW_LIST
    content = XML.ElementFromURL(pageUrl, True)
    Log(content.xpath('//div[@class="showInfo"]'))
    for item in content.xpath('//li[@class="episodeListItem"]/div[@class="showInfo"]'):

      titles=item.xpath("a")
      Log(titles)
      titleUrl=FOX_URL + titles[1].get('href')
      Log(titleUrl)

      Log(titleUrl)
      title=item.xpath("h3")[0].text
      summary=item.xpath("h4")[0].text
      thumb=""
      Log(thumb)

      
      
      Log(titleUrl)
      if (titleUrl.count('americasmostwanted')) ==0:
        dir.Append(Function(DirectoryItem(VideoPage, title,summary), pageUrl = titleUrl))
    return dir 

####################################################################################################
def VideoPage(sender, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    Log(pageUrl)
    content = XML.ElementFromURL(pageUrl, isHTML="True")
    for item2 in content.xpath('//ul[@id="fullEpisodesList"]/li[contains(@class,"episode")]/ul'):


      vidUrl=FOX_URL+item2.xpath('li[@class="episodeName"]/span/a')[0].get('href')
      Log(vidUrl)
      title2 = item2.xpath('li[@class="episodeName"]/span/a')[0].text
      Log(title2)
      Log(item2.xpath('li[@class="episodeNumber"]')[0].text)
      title1 = item2.xpath('li[@class="episodeName"]/span/a')[0].text
      summary=item2.xpath('li[@class="description"]')[0].get('href')
      airdate=item2.xpath('li[@class="airDate"]')[0].text
      title2=title2 + " - " + airdate
      
      
      content2 = XML.ElementFromURL(vidUrl,True)
      pageUrl2=pageUrl
      pageUrl2=pageUrl2.replace("/","%2F")
      pageUrl2=pageUrl2.replace(":","%3A")
      pageUrl2=pageUrl2+"&%40"
      

      videoID = content2.xpath('//div[@id="player"]//object/param[@name="@videoPlayer"]')[0].get("value")
      bgcolor = content2.xpath('//div[@id="player"]//object/param[@name="bgcolor"]')[0].get("value")
      bgcolor=bgcolor.replace("#","%23")
      width = content2.xpath('//div[@id="player"]//object/param[@name="width"]')[0].get("value")
      height = content2.xpath('//div[@id="player"]//object/param[@name="height"]')[0].get("value")
      playerID = content2.xpath('//div[@id="player"]//object/param[@name="playerID"]')[0].get("value")
      publisherID = content2.xpath('//div[@id="player"]//object/param[@name="publisherID"]')[0].get("value")
      isVid = content2.xpath('//div[@id="player"]//object/param[@name="isVid"]')[0].get("value")
      videoPlayer = content2.xpath('//div[@id="player"]//object/param[@name="@videoPlayer"]')[0].get("value")
      wmode = content2.xpath('//div[@id="player"]//object/param[@name="wmode"]')[0].get("value")
      adZone = content2.xpath('//div[@id="player"]//object/param[@name="adZone"]')[0].get("value")
      showCode = content2.xpath('//div[@id="player"]//object/param[@name="showCode"]')[0].get("value")
      omnitureAccountID = content2.xpath('//div[@id="player"]//object/param[@name="omnitureAccountID"]')[0].get("value")
      dynamicStreaming = content2.xpath('//div[@id="player"]//object/param[@name="dynamicStreaming"]')[0].get("value")
      optimizedContentLoad = content2.xpath('//div[@id="player"]//object/param[@name="optimizedContentLoad"]')[0].get("value")
      convivaEnabled = content2.xpath('//div[@id="player"]//object/param[@name="convivaEnabled"]')[0].get("value")
      convivaID = content2.xpath('//div[@id="player"]//object/param[@name="convivaID"]')[0].get("value")
      

      
      truevidUrl="http://admin.brightcove.com/viewer/us1.24.00.06a/BrightcoveBootloader.swf?purl=" + pageUrl2 + "videoPlayer=" + videoID + "&adZone=" + adZone + "&autoStart=true" + "&bgcolor=" + bgcolor + "&convivaEnabled=" + convivaEnabled + "&convivaID=" + convivaID + "&dynamicStreaming=" + dynamicStreaming + "&flashID=myExperience" + "&height=" + height + "&isVid=" + isVid + "&omnitureAccountID=" + omnitureAccountID + "&optimizedContentLoad=" + optimizedContentLoad + "&playerID=" + playerID + "&publisherID=" + publisherID + "&showcode=" + showCode + "&width=" + width +"&wmode=" + wmode
      
      Log(truevidUrl)

      dir.Append(WebVideoItem(truevidUrl, title=title2, subtitle=title1,summary=summary))
    return dir
