from BeautifulSoup import BeautifulSoup 
import urllib2
import os

dataPath = 'rawData'

birdList = [
    'Cyanocitta+cristata',#blue jay
    'Cardinalis+cardinalis',#cardinal
    'Zenaida+macroura', #morning dove
    'Turdus+migratorius',#robin
    'Carduelis+tristis', #gold finch
    'Passexu+domesticus', #house sparrow
    'Quiscalus+quiscula', #common grackle
    'Archilochus+colubris', #ruby throated humming bird
    'Picoides+pubescens', # downy wood pecker
    'Columba+livia', # rock pigeon
    'Sitta+carolinensis', # white breasted nut-hatch
    'Poecile+atricapillus', # Black-capped chickadee
    'Agelaius+phoeniceus', # Red-winged black bird
    'Haemorhous+purpureus', #Purple Finch
    'Baeolophus+bicolor', #tufted titmouse
    ]


def downloadBirdCalls(stub, bird,path):
    print "#"30
    print "DOWNLOADING {0} to {1}".format(bird,path)
    os.chdir(path)
    n = 1
    page = '&pg='
    foundStuff = True
    while foundStuff:
        print "DOING PAGE {0}".format(n)
        url = stub+bird+page+str(n)
        n = n + 1
        url = urllib2.urlopen(url)
        content = url.read()
        soup = BeautifulSoup(content)
        found = soup.findAll("div", {"class": "xc-button-audio"})
        if( len(found) < 1 ):
            foundStuff = False
        for foundSound in found:
            soundUrl = [f[1] for f in foundSound.attrs if f[0]==u'data-xc-filepath']
            grabThis = "wget "
            grabThis = grabThis + soundUrl[0]
            os.system(grabThis)



if not os.path.exists(os.path.join(os.getcwd(), dataPath)):
    os.mkdir(os.path.join(os.getcwd(),dataPath))

os.chdir(os.path.join(os.getcwd(),dataPath))

paths = []

for bird in birdList:
    if not os.path.exists(os.path.join(os.getcwd(), bird)):
        os.mkdir(os.path.join(os.getcwd(),bird))
        print "Creating " + os.path.join(os.getcwd(),bird)
    else:
        print "Found " + os.path.join(os.getcwd(),bird)
    paths.append(os.path.join(os.getcwd(),bird))

stub = "http://www.xeno-canto.org/browse.php?species_nr=&query="

for bird,path in zip(birdList,paths):
    downloadBirdCalls(stub, bird,path)
