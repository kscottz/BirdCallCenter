from BeautifulSoup import BeautifulSoup 
import urllib2
import os
url = urllib2.urlopen("http://www.xeno-canto.org/browse.php?species_nr=&query=Cyanocitta+cristata")
content = url.read()
soup = BeautifulSoup(content)
found = soup.findAll("div", {"class": "xc-button-audio"})
for foundSound in found:
    soundUrl = [f[1] for f in foundSound.attrs if f[0]==u'data-xc-filepath']
    grabThis = "wget "
    grabThis = grabThis + soundUrl[0]
    print soundUrl[0]
    os.system(grabThis)
