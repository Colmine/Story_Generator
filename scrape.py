import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scrape:
    def __init__(self):
        cOptions = Options()
        cOptions.add_argument("--binary=C:\\Users\\coleg\\chromedriver.exe")
        cOptions.add_argument("--incognito")
        cOptions.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=cOptions, executable_path='C:\\Users\\coleg\\chromedriver.exe')
        self.mDepth = 10
        self.eAction = {
            "End Game and Leave Comments",
            "Click here to End the Game and Leave Comments",
            "See How Well You Did (you can still back-page afterwards if you like)",
            "You have died.",
            "You have died",
            "Epilogue",
            "Save Game",
            "Your quest might have been more successful...",
            "5 - not the best, certainly not the worst",
            "The End! (leave comments on game)",
            "6 - it's worth every cent",
            "You do not survive the journey to California",
            "Quit the game.",
            "7 - even better than Reeses' Cups®",
            "8 - it will bring you enlightenment",
            "End of game! Leave a comment!",
            "Better luck next time",
            "click here to continue",
            "Rating And Leaving Comments",
            "You do not survive your journey to California",
            "Your Outlaw Career has come to an end",
            "Thank you for taking the time to read my story",
            "You have no further part in the story, End Game and Leave Comments",
            "",
            "You play no further part in this story. End Game and Leave Comments",
            "drivers",
            "Alas, poor Yorick, they slew you well",
            "My heart bleeds for you",
            "To End the Game and Leave Comments click here",
            "Call it a day",
            "Check the voicemail.",
            "reset",
            "There's nothing you can do anymore...it's over.",
            "To Be Continued...",
            "Thanks again for taking the time to read this",
            "If you just want to escape this endless story you can do that by clicking here",
            "Boo Hoo Hoo",
            "End.",
            "Pick up some money real quick",
            "",
            "Well you did live a decent amount of time in the Army",
            "End Game",
            "You have survived the Donner Party's journey to California!",
        }
        self.texts = set()

    def goToURL(self, url):
        self.texts = set()
        self.driver.get(url)
        time.sleep(0.5)

    def getText(self):
        divEls = self.driver.find_elements_by_css_selector("div")
        text = divEls[3].text
        return text

    def getLinks(self):
        return self.driver.find_elements_by_css_selector("a")

    def goBack(self):
        self.getLinks()[0].click()
        time.sleep(0.2)

    def clickAction(self, links, actionNum):
        links[actionNum + 4].click()
        time.sleep(0.2)

    def getActions(self):
        return [link.text for link in self.getLinks()[4:]]

    def numActions(self):
        return len(self.GetLinks()) - 4

    def buildTreeHelp(self, pStory, actNum, depth, oldActs):
        depth += 1
        resultAct = {}

        act = oldActs[actNum]
        print("Action is ", repr(act))
        resultAct["action"] = act

        links = self.getLinks()
        if actNum + 4 >= len(links):
            return None

        self.clickAction(links, actNum)
        result = self.getText()
        if result == pStory or result in self.texts:
            self.goBack()
            return None
        self.texts.add(result)
        print(len(self.texts))
        resultAct["result"] = result

        actions = self.getActions()
        resultAct["action_results"] = []
        for i, action in enumerate(actions):
            if actions[i] not in self.eAction:
                subActResult = self.buildTreeHelp(result, i, depth, actions)
                if resultAct is not None:
                    resultAct["action_results"].append(subActResult)

        self.goBack()
        return resultAct

    def buildStoryTree(self, url):
        scrape.goToURL(url)
        text = scrape.getText()
        actions = self.getActions()
        storyDict = {}
        storyDict["tree_id"] = url
        storyDict["context"] = ""
        storyDict["first_story_block"] = text
        storyDict["action_results"] = []

        for i, action in enumerate(actions):
            if action not in self.eAction:
                action_result = self.buildTreeHelp(text, i, 0, actions)
                if action_result is not None:
                    storyDict["action_results"].append(action_result)
            else:
                print("done")

        return storyDict

def save_tree(tree, filename):
    with open(filename, "w") as fp:
        json.dump(tree, fp)

scrape = Scrape()

urls = [
    #Sci-fi
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=16683",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7393",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=12123",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=29489",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=18988",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7566",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=59241",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=56763",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=40712",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=6823",
    #Fantasy
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=54639",
    #"http://chooseyourstory.com/story/viewer/default.aspx?StoryId=12792",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=60539",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=61596",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=34838",
    #"http://chooseyourstory.com/story/viewer/default.aspx?StoryId=58936",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=61827",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=51334",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=64095",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=10634",
    #Mystery
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=63577",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=31353",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=56501",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=60431",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=65762",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=60002",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=5466",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=9411",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=64248",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=6376",
    #Grim-dark fantasy
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=10638",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=64921",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7397",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=8041",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=63635",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=37696",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=65138",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=65273",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=45866",
    "http://chooseyourstory.com/story/viewer/default.aspx?StoryId=64785",

]


for i in range(25, len(urls)):
    print("****** Extracting Adventure ", urls[i], " ***********")
    tree = scrape.buildStoryTree(urls[i])
    save_tree(tree, "C:\\Users\\coleg\\OneDrive\\Desktop\\VisualStudio\\CS436\\stories\\story" + str(i) + ".json")

print("done")