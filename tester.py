import urllib2

from BeautifulSoup import *

from urlparse import urljoin

def crawlV2():
    
    seedSite = raw_input("Enter website (enter full path, eg. http://www.reddit.com/): ")
    keyWord = raw_input("Enter keyword: ")

    keyWord1 = unicode(keyWord, 'utf-8')

    specifiedDepth = raw_input("Enter depth: ")


    f = open('db.txt', 'w')

    urlList = [seedSite] # This is the url list of the links that need to be searched
    copyUrlList = [seedSite] # A history of the links already looked at so that any recurrences can be excluded from the search

    depth = 0 # Initial depth

    # for seed website
    c = urllib2.urlopen(seedSite)
    #soup = c.read()  #Read the html doc contained in the url
    soup2 = BeautifulSoup(c) # Use beautiful soup to get the "prettier" parsable version
    links = soup2.findAll('a') #Extract all the links that archor tags!
    tag = ""

    # populate the urlList with all the links from the seed website.
    for link in links:
        tag1 = 0
        if ('href' in dict(link.attrs)):
        
            # Check if the link is the absolute url or the relative url
            if link['href'][0:3] == 'http':
                url = link['href']
                
            else:
                url = urljoin(seedSite , link['href'])

            if url.find("'") != -1:
                continue

            url = url.split('#')[0] # remove location portion

            urlList.append(url) # append the link in the current page to the list
            copyUrlList.append(url) #append the link to the history of the links looked at.

            tag = urlList[len(urlList)-1] #The tag is the last url link. Using this tag, the algorithm will know when to iterate the depth level
  



    while len(urlList) > 0:
    
        a = ""
        for i in urlList:
    
            #if the link is current the tag, that means we have just finished one depth in level
            if (i == tag):
                depth = depth + 1 
                tag = urlList[len(urlList)-1] # reset tag
            
            try:
                c = urllib2.urlopen(i) # open current page
            except:
                print "oops!"
                urlList.remove(i) #if we cant open the page, forget it. Just delete the link from the list.
                break

            read = c.read()
            html = unicode(read, 'utf-8')

            try:
                soup2 = BeautifulSoup(read)
            except:
                print "gosh!"
                urlList.remove(i)
                break
                    
            if html.find(keyWord1) > -1:
                

                f.write(i + '\n')
              
                            
                links = soup2('a') #extract all links from the page
                # if the depth of the crawl is greater than 5, exit!
                if depth > int(specifiedDepth):
                    print "depth exceeded"
                    urlList = []
                    break
    

                for link in links:
                          
                    if ('href' in dict(link.attrs)):
                        url = urljoin(i,link['href'])

                    if url.find("'") != -1:
                        continue

                    url = url.split('#')[0] # remove location portion

                    if url not in copyUrlList:
                        urlList.append(url)
                        copyUrlList.append(url)
                    

            urlList.remove(i) # remove the base url

    f.close()
            
                           
crawlV2()