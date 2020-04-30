import re

class Post:
    def __init__(self, title, subhead, preview, date, imageSrc, copy):
        self.title = title
        self.subhead = subhead
        self.preview = preview
        self.date = date
        self.imageSrc = imageSrc
        self.copy = splitCopyToBlocks(copy)

    def getTitle(self):
        return self.title
    def setTitle(self, title):
        self.title = title

    def getSubhead(self):
        return self.subhead
    def setSubhead(self, subhead):
        self.subhead = subhead

    def getPreview(self):
        return self.preview
    def setPreview(self, preview):
        self.preview = preview

    def getDate(self):
        return self.date
    def setDate(self, date):
        self.date = date

    def getImageSrc(self):
        return self.imageSrc
    def setImageSrc(self, imageSrc):
        self.imageSrc = imageSrc

    def getCopy(self):
        return self.copy
    def setCopy(self, copy):
        self.copy = splitCopyToBlocks(copy)


def splitCopyToBlocks(copy):
    blocks = []
    for x in copy.split('\n'):
        if len(x) > 1:
            blocks.append(x)
    return blocks


def parseForLinks(copy):
    postCopy = []
    for x in copy:
        p = x['block']
        regExStr ="(\[[^\]]+\]\([A-Za-z0-9]+\.[A-Za-z]+[\/]?[^\)]+?\))"
        x = re.findall(regExStr, p)
        if len(x) > 0:
            for y in x:
                link = re.findall("(\[[^\]]+\])",y)
                link = link[0].strip('[').strip(']')
                url = re.findall("(\([A-Za-z0-9]+\.[A-Za-z]+[\/]?[^\)]+?\))",y)
                url = url[0].strip('(').strip(')')
                urlString = "<a href=\"http://" + url + "\">" + link + "</a>"
                print(urlString)
                p = p.replace(y, urlString)
            postCopy.append({'codeBlock':p})
        else:
            postCopy.append({'block': p})
    return postCopy


    