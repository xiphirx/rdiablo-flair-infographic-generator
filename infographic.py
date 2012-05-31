import pygame
import reddit
import json
import datetime
import pickle
import operator

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
    classes = ['barb', 'monk', 'wizard', 'witchdoc', 'demonhunt']
    realms = ['americas', 'europe', 'asia', 'reddit']
    imageOffsets = {'barb': 120, \
                    'demonhunt': 179, \
                    'monk': 237, \
                    'witchdoc': 295, \
                    'wizard': 353, \
                    'total': 528, \
                    'americas': (310, 790), \
                    'europe': (620, 790), \
                    'asia': (811, 790), \
                    'reddit': (582, 1030)}
    totalClass = dict.fromkeys(classes, 0)
    totalRealm = dict.fromkeys(realms, 0)
    totalFlair = 0
    totalSubscribers = 0

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
        (self.prevTotalClass, self.prevTotalRealm, self.prevTotalSubscribers, self.prevTotalFlair) = pickle.load(open('prevData.pickle', 'rb'))

    def grabFlairInformation(self):
        """Temp garbage values to eliminate the costly polling process"""
        """
        self.totalFlair = 18679
        self.totalSubscribers = 65373
        self.totalClass['barb'] = 3959
        self.totalClass['demonhunt'] = 3566
        self.totalClass['witchdoc'] = 3390
        self.totalClass['monk'] = 3912
        self.totalClass['wizard'] = 3848
        self.totalRealm['americas'] = 11601
        self.totalRealm['europe'] = 4212
        self.totalRealm['asia'] = 248
        self.totalRealm['reddit'] = 2614
        """
        n = ''
        done = False
        while not done:
            flairJSON = self.r._request(page_url="http://www.reddit.com/r/diablo/api/flairlist.json", url_data={"limit":1000,"after":n,"uh":self.r.modhash})
            print 'Requested initial page of flair data' if (n == '') else 'Requested an additional page of flair data, n = ' + n
            flairList = json.loads(flairJSON)
            try:
                n = flairList['next']
            except KeyError:
                done = True
            for user in flairList['users']:
                if (user['flair_css_class']):
                    sliced = user['flair_css_class'].split('-')
                    userClass = sliced[0]
                    if (len(sliced) > 1):
                        userRealm = sliced[1]
                        if (userRealm.find(' ') > -1):
                            userRealm = userRealm[:userRealm.find(' ')]
                        self.totalFlair += 1 # only count those with valid, full flair
                    else:
                        userRealm = 'none'

                    if userClass in self.classes:
                        self.totalClass[userClass] += 1

                    if userRealm in self.realms:
                        self.totalRealm[userRealm] += 1

    def saveFlairInformation(self):
        pickle.dump((self.totalClass, self.totalRealm, self.totalSubscribers, self.totalFlair), open('prevData.pickle', 'wb'))

    def getDominantClass(self):
        return max(self.totalClass.iteritems(), key = operator.itemgetter(1))[0]

    def generate(self):
        pygame.init()
        base = pygame.image.load('base.png')
        fill = pygame.image.load('fill.png')
        head = pygame.image.load('head.png')
        dominantClass = pygame.image.load(self.getDominantClass() + '-crest.png')
        fillWidth = 396
        screen = pygame.display.set_mode(base.get_size())
        screen.blit(base,(0,0))

        #Title
        now = datetime.datetime.now()
        titleText = Text('R/DIABLO FLAIR STATISTICS INFOGRAPHIC | ' + now.strftime('%m - %d - %Y %I:%M%p'), 18, 220, 54, (247, 202, 93)).render(screen)

        #Display dominant Class
        screen.blit(dominantClass, (screen.get_width() - dominantClass.get_width(),100))
        dominantClassText = Text('DOMINATING CLASS', 18, 847, 133, (247,202,93)).render(screen)

        # Display individual class stats
        for playerClass in self.classes:
            width = int((float(self.totalClass[playerClass]) / self.totalFlair) * fillWidth)
            fill = pygame.transform.scale(fill, (width, 24))
            screen.blit(fill, (320, self.imageOffsets[playerClass]))
            screen.blit(head, (320 + fill.get_width() - 18, self.imageOffsets[playerClass]))
            Text(str(int(float(self.totalClass[playerClass])/float(self.totalFlair)*100)) + '%', 24, 320 + fill.get_width() + 10, self.imageOffsets[playerClass], (255,255,255)).render(screen)
            numClass = Text(str(self.totalClass[playerClass]), 12, 320 + fill.get_width(), self.imageOffsets[playerClass] + 31, (209,1,1))
            numClass.setAlignment('c')
            numClass.render(screen)
       
        #FlairTotal
        fill = pygame.transform.scale(fill, (int((float(self.totalFlair)/(self.totalSubscribers))*fillWidth),24))
        screen.blit(fill, (320, 528))
        screen.blit(head, (320 + fill.get_width() - 18, 528))
        Text(str(int(float(self.totalFlair)/float(self.totalSubscribers)*100)) + '%', 24, 320 + fill.get_width() + 10, 528, (255,255,255)).render(screen)
        numFlair = Text(str(self.totalFlair), 12, 320 + fill.get_width(), 559, (209,1,1))
        numFlair.setAlignment('c')
        numFlair.render(screen)

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
        for userRealm in self.realms:
            textRealm = Text(str(int(float(self.totalRealm[userRealm])/float(self.totalFlair)*100)) + '%', 18, self.imageOffsets[userRealm][0], self.imageOffsets[userRealm][1], (255,255,255))
            textRealm.setAlignment('c')
            textRealm.render(screen)
            Text(str(self.totalRealm[userRealm]), 12, textRealm.x - int(float(textRealm.getWidth()) / 2), textRealm.y + 20, (255,255,255)).render(screen)
       
        #Credits and stuff
        Text('* DATA MAY BE OFF DUE TO ROUNDING', 12, 219, 1165, (4,95,88)).render(screen)
        Text('* PUT TOGETHER BY XIPHIRX AND PYTHON', 12, 219, 1177, (4,95,88)).render(screen)

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
for userClass, num in rdiablo.totalClass.items():
    print '| Total ' + userClass + ': ' + str(num)
print ' -----------------------------------------'
print ' Quick Realm Stats:'
print ' -----------------------------------------'
for userRealm, num in rdiablo.totalRealm.items():
    print '| Total ' + userRealm + ': ' + str(num)
print ' -----------------------------------------'
print ' -----------------------------------------'
print '| Total flair users: ' + str(rdiablo.totalFlair)
print ' -----------------------------------------'

#rdiablo.saveFlairInformation()
rdiablo.generate()
