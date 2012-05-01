import pygame
import reddit
import json
import datetime

class Text:
    x = 0
    y = 0
    size = 16
    text = ''
    alignment = 'l'
    def __init__(self, textp='', sizep=16, xp=0, yp=0, color=(255,255,255)):
        self.text = textp
        self.x = xp
        self.y = yp
        self.size = sizep
        self.font = pygame.font.Font('Exocet2.ttf', self.size)
        self.rText = self.font.render(self.text, True, color)
    def setPos(self, xp, yp):
        self.x = xp
        self.y = yp
    def setAlignment(self, align):
        self.alignment = align
    def getWidth(self):
        return self.rText.get_width()
    def getHeight(self):
        return self.rText.get_height()
    def render(self, surface):
        pos = self.rText.get_rect()
        pos.y = self.y
        if (self.alignment == 'l'):
            pos.x = self.x
        elif (self.alignment == 'c'):
            pos.x = self.x - int(float(self.rText.get_width()) / 2)
        elif (self.alignment == 'r'):
            pos.x = self.x - self.rText.get_width()
        surface.blit(self.rText, pos)

class Infographic:
    totalFlair = 0
    totalSubscribers = 0
    totalBarbarian = 0
    totalDemonHunter = 0
    totalWitchDoctor = 0
    totalMonk = 0
    totalWizard = 0

    prevTotalFlair = 0
    prevTotalSubscribers = 0
    prevTotalBarbarian = 0
    prevTotalDemonHunter = 0
    prevTotalWitchDoctor = 0
    prevTotalMonk = 0
    prevTotalWizard = 0

    # Remove these after d3 comes out
    totalUSWest = 0
    totalUSEast = 0
    totalEurope = 0
    totalAsia = 0
    totalBeta = 0
    totalReddit = 0

    prevTotalUSWest = 0
    prevTotalUSEast = 0
    prevTotalEurope = 0
    prevTotalAsia = 0
    prevTotalBeta = 0
    prevTotalReddit = 0
    # and uncomment these
    """
    totalAmericas = 0
    totalEurope = 0
    totalAsia = 0
    """

    def __init__(self):
        self.r = reddit.Reddit(user_agent='/r/diablo flair infographic bot')
        configFile = open('config.cfg', 'r')
        user = configFile.readline().rstrip('\n')
        password = configFile.readline().rstrip('\n')
        configFile.close()
        print 'Logging in as ' + user + '...'
        self.r.login(user, password)
        subJSON = self.r._request(page_url="http://www.reddit.com/r/diablo/about.json")
        subList = json.loads(subJSON)
        self.totalSubscribers = subList['data']['subscribers']

    def grabPreviousFlairInformation(self):
        saveFile = open('prevFlair.dat', 'r')
        self.prevTotalFlair = int(saveFile.readline())
        self.prevTotalSubscribers = int(saveFile.readline())
        self.prevTotalBarbarian = int(saveFile.readline())
        self.prevTotalDemonHunter = int(saveFile.readline())
        self.prevTotalWitchDoctor = int(saveFile.readline())
        self.prevTotalMonk = int(saveFile.readline())
        self.prevTotalWizard = int(saveFile.readline())
        self.prevTotalUSWest = int(saveFile.readline())
        self.prevTotalUSEast = int(saveFile.readline())
        self.prevTotalEurope = int(saveFile.readline())
        self.prevTotalAsia = int(saveFile.readline())
        self.prevTotalBeta = int(saveFile.readline())
        self.prevTotalReddit = int(saveFile.readline())
        saveFile.close()

    def grabFlairInformation(self):
        """Temp garbage values to eliminate the costly polling process"""
        """
        self.totalFlair = 16000
        self.totalSubscribers = 42134
        self.totalBarbarian = 2500
        self.totalDemonHunter = 1900
        self.totalWitchDoctor = 2000
        self.totalMonk = 2100
        self.totalWizard = 1500
        self.totalUSWest = 2500
        self.totalUSEast = 3500
        self.totalEurope = 2600
        self.totalAsia = 200
        self.totalBeta = 300
        self.totalReddit = 1500
        """
        n = ''
        done = False
        while not done:
            flairJSON = self.r._request(page_url="http://www.reddit.com/r/diablo/api/flairlist.json", url_data={"limit":1000,"after":n,"uh":self.r.modhash})
            print 'Requested another page, n=' + n
            flairList = json.loads(flairJSON)
            try:
                n = flairList['next']
            except KeyError:
                done = True
            for user in flairList['users']:
                #print user['flair_css_class']
                #print len(user['flair_css_class'])
                if (not user['flair_css_class'] == None):
                    sliced = user['flair_css_class'].split('-')
                    userClass= sliced[0]
                    if (len(sliced) > 1):
                        userRealm = sliced[1]
                        if (userRealm.find(' ') > -1):
                            userRealm = userRealm[:userRealm.find(' ')]
                        self.totalFlair += 1 # only count those with valid, full flair
                    else:
                        userRealm = 'none'

                    if (userClass == 'barb'): self.totalBarbarian += 1
                    elif (userClass == 'monk'): self.totalMonk += 1
                    elif (userClass == 'wizard'): self.totalWizard += 1
                    elif (userClass == 'witchdoc'): self.totalWitchDoctor += 1
                    elif (userClass == 'demonhunt'): self.totalDemonHunter += 1

                    if (userRealm == 'uswest'): self.totalUSWest += 1
                    elif (userRealm == 'useast'): self.totalUSEast += 1
                    elif (userRealm == 'europe'): self.totalEurope += 1
                    elif (userRealm == 'asia'): self.totalAsia += 1
                    elif (userRealm == 'beta'): self.totalBeta += 1
                    elif (userRealm == 'reddit'): self.totalReddit += 1
                    #else: print userRealm


    def saveFlairInformation(self):
        if  self.totalFlair == self.prevTotalFlair and \
            self.totalSubscribers == self.prevTotalSubscribers and \
            self.totalBarbarian == self.prevTotalBarbarian and \
            self.totalDemonHunter == self.prevTotalDemonHunter and \
            self.totalWitchDoctor == self.prevTotalWitchDoctor and \
            self.totalMonk == self.prevTotalMonk and \
            self.totalWizard == self.prevTotalWizard and \
            self.totalUSWest == self.prevTotalUSWest and \
            self.totalUSEast == self.prevTotalUSEast and \
            self.totalEurope == self.prevTotalEurope and \
            self.totalAsia == self.prevTotalAsia and \
            self.totalBeta == self.prevTotalBeta and \
            self.totalReddit == self.prevTotalReddit:
                pass #there was no change in information...
        else:
            saveFile = open('prevFlair.dat', 'w')
            saveFile.write(str(self.totalFlair)+'\n')
            saveFile.write(str(self.totalSubscribers)+'\n')
            saveFile.write(str(self.totalBarbarian)+'\n')
            saveFile.write(str(self.totalDemonHunter)+'\n')
            saveFile.write(str(self.totalWitchDoctor)+'\n')
            saveFile.write(str(self.totalMonk)+'\n')
            saveFile.write(str(self.totalWizard)+'\n')
            saveFile.write(str(self.totalUSWest)+'\n')
            saveFile.write(str(self.totalUSEast)+'\n')
            saveFile.write(str(self.totalEurope)+'\n')
            saveFile.write(str(self.totalAsia)+'\n')
            saveFile.write(str(self.totalBeta)+'\n')
            saveFile.write(str(self.totalReddit))
            saveFile.close()

    def getDominantClass(self):
        maximum = max([self.totalBarbarian, self.totalDemonHunter, self.totalMonk, self.totalWitchDoctor, self.totalWizard])
        if (self.totalBarbarian == maximum): return 'barb'
        if (self.totalMonk == maximum): return 'monk'
        if (self.totalDemonHunter == maximum): return 'demonhunt'
        if (self.totalWitchDoctor == maximum): return 'witchdoc'
        if (self.totalWizard == maximum): return 'wizard'

    def generate(self):
        pygame.init()
        base = pygame.image.load('base.png')
        fill = pygame.image.load('fill.png')
        head = pygame.image.load('head.png')
        dominantClass = pygame.image.load(self.getDominantClass() + '-crest.png')
        fillWidth = 396
        screen = pygame.display.set_mode(base.get_size())
        screen.blit(base,(0,0))

        #Barbarian
        fill = pygame.transform.scale(fill, (int((float(self.totalBarbarian)/(self.totalFlair))*fillWidth),24))
        screen.blit(fill, (320, 120))
        screen.blit(head, (320 + fill.get_width() - 18, 120))
        Text(str(int(float(self.totalBarbarian)/float(self.totalFlair)*100)) + '%', 24, 320 + fill.get_width() + 10, 120, (255,255,255)).render(screen)
        numBarbarian = Text(str(self.totalBarbarian), 12, 320 + fill.get_width(), 151, (209,1,1))
        numBarbarian.setAlignment('c')
        numBarbarian.render(screen)

        #Demon Hunter
        fill = pygame.transform.scale(fill, (int((float(self.totalDemonHunter)/(self.totalFlair))*fillWidth),24))
        screen.blit(fill, (320, 179))
        screen.blit(head, (320 + fill.get_width() - 18, 179))
        Text(str(int(float(self.totalDemonHunter)/float(self.totalFlair)*100)) + '%', 24, 320 + fill.get_width() + 10, 179, (255,255,255)).render(screen)
        numDemonHunter = Text(str(self.totalDemonHunter), 12, 320 + fill.get_width(), 210, (209,1,1))
        numDemonHunter.setAlignment('c')
        numDemonHunter.render(screen)

        #Monk
        fill = pygame.transform.scale(fill, (int((float(self.totalMonk)/(self.totalFlair))*fillWidth),24))
        screen.blit(fill, (320, 237))
        screen.blit(head, (320 + fill.get_width() - 18, 237))
        Text(str(int(float(self.totalMonk)/float(self.totalFlair)*100)) + '%', 24, 320 + fill.get_width() + 10, 237, (255,255,255)).render(screen)
        numMonk = Text(str(self.totalMonk), 12, 320 + fill.get_width(), 268, (209,1,1))
        numMonk.setAlignment('c')
        numMonk.render(screen)

        #WitchDoctor
        fill = pygame.transform.scale(fill, (int((float(self.totalWitchDoctor)/(self.totalFlair))*fillWidth),24))
        screen.blit(fill, (320, 295))
        screen.blit(head, (320 + fill.get_width() - 18, 295))
        Text(str(int(float(self.totalWitchDoctor)/float(self.totalFlair)*100)) + '%', 24, 320 + fill.get_width() + 10, 295, (255,255,255)).render(screen)
        numWitchDoctor = Text(str(self.totalWitchDoctor), 12, 320 + fill.get_width(), 326, (209,1,1))
        numWitchDoctor.setAlignment('c')
        numWitchDoctor.render(screen)

        #Wizard
        fill = pygame.transform.scale(fill, (int((float(self.totalWizard)/(self.totalFlair))*fillWidth),24))
        screen.blit(fill, (320, 353))
        screen.blit(head, (320 + fill.get_width() - 18, 353))
        Text(str(int(float(self.totalWizard)/float(self.totalFlair)*100)) + '%', 24, 320 + fill.get_width() + 10, 353, (255,255,255)).render(screen)
        numWizard = Text(str(self.totalWizard), 12, 320 + fill.get_width(), 384, (209,1,1))
        numWizard.setAlignment('c')
        numWizard.render(screen)

        #FlairTotal
        fill = pygame.transform.scale(fill, (int((float(self.totalFlair)/(self.totalSubscribers))*fillWidth),24))
        screen.blit(fill, (320, 528))
        screen.blit(head, (320 + fill.get_width() - 18, 528))
        Text(str(int(float(self.totalFlair)/float(self.totalSubscribers)*100)) + '%', 24, 320 + fill.get_width() + 10, 528, (255,255,255)).render(screen)
        numFlair = Text(str(self.totalFlair), 12, 320 + fill.get_width(), 559, (209,1,1))
        numFlair.setAlignment('c')
        numFlair.render(screen)

        #Display dominant Class
        screen.blit(dominantClass, (screen.get_width() - dominantClass.get_width(),100))
        dominantClassText = Text('DOMINATING CLASS', 18, 847, 133, (247,202,93))
        dominantClassText.render(screen)

        #Title
        now = datetime.datetime.now()
        titleText = Text('R/DIABLO FLAIR STATISTICS INFOGRAPHIC | ' + now.strftime('%m - %d - %Y %I:%M%p'), 18, 220, 54, (247, 202, 93))
        titleText.render(screen)

        #Class number legends
        Text('0', 18, 320, 96, (102,102,102)).render(screen)
        Text('0', 18, 320, 404, (102,102,102)).render(screen)
        Text('0', 18, 320, 582, (102,102,102)).render(screen)
        legendTotalFlairCount = Text(str(self.totalFlair), 18, 716, 96, (102,102,102))
        legendTotalFlairCount.setAlignment('r')
        legendTotalFlairCount.render(screen)
        legendTotalFlairCount.setPos(716, 404)
        legendTotalFlairCount.render(screen)

        legendTotalSubscriberCount = Text(str(self.totalSubscribers), 18, 716, 582, (102,102,102))
        legendTotalSubscriberCount.setAlignment('r')
        legendTotalSubscriberCount.render(screen)

        #Stat change for subscriber count
        if ((self.totalSubscribers - self.prevTotalSubscribers) > 0):
            Text('+' + str(int(float(self.totalSubscribers - self.prevTotalSubscribers)/float(self.prevTotalSubscribers)*100)) + '% +' + str(self.totalSubscribers-self.prevTotalSubscribers), 12, 726, 572, (1,209,1)).render(screen)
        elif((self.totalSubscribers - self.prevTotalSubscribers) < 0):
            Text('-' + str(int(float(self.prevTotalSubscribers - self.totalSubscribers)/float(self.prevTotalSubscribers)*100)) + '% -' + str(self.totalSubscribers-self.prevTotalSubscribers), 12, 726, 572, (209,1,1)).render(screen)

        #Stat change for flair count
        if ((self.totalFlair - self.prevTotalFlair) > 0):
            Text('+' + str(int(float(self.totalFlair - self.prevTotalFlair)/float(self.prevTotalFlair)*100)) +'%', 12, numFlair.x - int(float(numFlair.getWidth() / 2)), 508, (1,209,1)).render(screen)
        elif ((self.totalFlair - self.prevTotalFlair) < 0):
            Text('-' + str(int(float(self.prevTotalFlair - self.totalFlair)/float(self.prevTotalFlair)*100)) +'%', 12, numFlair.x - int(float(numFlair.getWidth() / 2)), 508, (209,1,1)).render(screen)

        #Regional stats
        #USWest
        textUSWest = Text(str(int(float(self.totalUSWest)/float(self.totalFlair)*100)) + '%', 18, 271, 790, (255,255,255))
        textUSWest.setAlignment('c')
        textUSWest.render(screen)
        Text(str(self.totalUSWest), 12, textUSWest.x - int(float(textUSWest.getWidth()) / 2), textUSWest.y + 20, (255,255,255)).render(screen)

        #USEast
        textUSEast = Text(str(int(float(self.totalUSEast)/float(self.totalFlair)*100)) + '%', 18, 359, 790, (255,255,255))
        textUSEast.setAlignment('c')
        textUSEast.render(screen)
        Text(str(self.totalUSEast), 12, textUSEast.x - int(float(textUSEast.getWidth()) / 2), textUSEast.y + 20, (255,255,255)).render(screen)

        #Europe
        textEurope = Text(str(int(float(self.totalEurope)/float(self.totalFlair)*100)) + '%', 18, 620, 790, (255,255,255))
        textEurope.setAlignment('c')
        textEurope.render(screen)
        Text(str(self.totalEurope), 12, textEurope.x - int(float(textEurope.getWidth()) / 2), textEurope.y + 20, (255,255,255)).render(screen)

        #Asia
        textAsia = Text(str(int(float(self.totalAsia)/float(self.totalFlair)*100)) + '%', 18, 811, 790, (255,255,255))
        textAsia.setAlignment('c')
        textAsia.render(screen)
        Text(str(self.totalAsia), 12, textAsia.x - int(float(textAsia.getWidth()) / 2), textAsia.y + 20, (255,255,255)).render(screen)

        #Credits and stuff
        Text('* DATA MAY BE OFF DUE TO ROUNDING', 12, 219, 1105, (4,95,88)).render(screen)
        Text('* PUT TOGETHER BY XIPHIRX AND PYTHON', 12, 219, 1117, (4,95,88)).render(screen)
        Text(str(self.totalBeta) + ' (' + str(int(float(self.totalBeta)/float(self.totalFlair)*100)) + '%) REPORTED BETA PLAYERS', 24, 219, 1059, (4,95,88)).render(screen)

        #Save the image
        pygame.image.save(screen, 'infographics/' +now.strftime('%m-%d-%Y-') + 'Infographic.png')

        pygame.display.update()
        while True:
            event = pygame.event.poll()
            if (event.type == pygame.QUIT):
                break
        pygame.quit()



rdiablo = Infographic()
rdiablo.grabPreviousFlairInformation()
rdiablo.grabFlairInformation()

print ' Quick Stats'
print ' -----------------------------------------'
print '| Total Barbarian: ' + str(rdiablo.totalBarbarian)
print '| Total Monk: ' + str(rdiablo.totalMonk)
print '| Total Witch Doctor: ' + str(rdiablo.totalWitchDoctor)
print '| Total Demon Hunter: ' + str(rdiablo.totalDemonHunter)
print '| Total Wizard: ' + str(rdiablo.totalWizard)
print ' -----------------------------------------'
print ' Quick Realm Stats:'
print ' -----------------------------------------'
print '| Total USWest: ' + str(rdiablo.totalUSWest)
print '| Total USEast: ' + str(rdiablo.totalUSEast)
print '| Total Europe: ' + str(rdiablo.totalEurope)
print '| Total Asia: ' + str(rdiablo.totalAsia)
print '| Total Beta: ' + str(rdiablo.totalBeta)
print '| Total Reddit: ' + str(rdiablo.totalReddit)
print ' -----------------------------------------'
print ' -----------------------------------------'
print '| Total flair users: ' + str(rdiablo.totalFlair)
print ' -----------------------------------------'

rdiablo.saveFlairInformation()
rdiablo.generate()
