import os


class TreeCommand():

    '''
        The TreeCommand just like the tree command in windows.
        It Graphically displays the directory structure of a path or of the disk in a drive.
    '''

    def __init__(self, path='', depth=0, currentPosition=0):
        '''
        :param path: the path you want to be graphically displayed
        :param depth: depth represents the depth of the folder
        :param currentPosition: position of the dirs in os.walk()
        :param dirs: dirs in os.walk()
        :return:has no return value
        '''
        self.path = path
        self.depth = depth
        self.currentPosition = currentPosition
        self.dirs = []

    def increaseDepth(self):
        '''
        when meet a folder in a folder, just use this function to increase depth
        :return: self.depth
        '''
        self.depth += 1

    def position(self):
        '''
        get the position of self.dirs
        :return: self.currentPosition
        '''
        return self.currentPosition

    def decreaseDepth(self):
        '''
        when the sub-folder is end, use this function to decrease depth
        :return: self.depth
        '''
        self.depth -= 1

    def movePosition(self, step=1):
        '''
        move the position of self.dirs
        :param step: the distance you want to move
        :return: self.currentPosition
        '''
        self.currentPosition += step

    def constString(self):
        '''
        to be used to display the graph
        :return: string
        '''
        return '|    ' * self.depth + '|---'

    def setupPath(self):
        '''
        init the self.path, self.dirs and print the path
        :return: has no return value
        '''
        for root, dirs, files in os.walk(self.path):
            self.dirs.append(dirs)
        print(self.path)

    def pathAnalysis(self):
        '''
        This is the core algorithm in TreeCommand
        when the path has a sub-folder, it recursively call itself
        And the self.position() control the path, so it can move front
        :return: has no return value
        '''
        count = 0
        dirs = self.dirs[self.position()]
        subDirs = self.dirs
        while len(dirs) > count:
            print(self.constString(), dirs[count])
            self.movePosition()
            if len(subDirs[self.position()]) == 0:
                count += 1
            else:
                self.increaseDepth()
                self.pathAnalysis()
                count += 1
        self.decreaseDepth()


def test():
    treeCommandTestCreation()

def treeCommandTestCreation():
    testPathAnalysis()
    testIncreaseDepth()
    testDecreaseDepth()
    testMovePosition()
    testPosition()
    testConstString()

def testPathAnalysis():
    test = TreeCommand('G:/pp')
    test.setupPath()
    test.pathAnalysis()

def testIncreaseDepth():
    test = TreeCommand()
    assert test.depth == 0
    test.increaseDepth()
    assert test.depth == 1

def testDecreaseDepth():
    test = TreeCommand()
    assert test.depth == 0
    test.increaseDepth()
    assert test.depth == 1
    test.decreaseDepth()
    assert test.depth == 0

def testMovePosition():
    test = TreeCommand()
    assert test.position() == 0
    test.movePosition()
    assert test.position() == 1
    test.movePosition(99)
    assert test.position() == 100

def testPosition():
    test = TreeCommand('G:/pp')
    assert test.position() == 0
    test.movePosition()
    assert test.position() == 1
    test.movePosition(3)
    assert test.position() == 4

def testConstString():
    test = TreeCommand()
    assert test.constString() == '|---'
    test.increaseDepth()
    assert test.constString() == '|    ' + '|---'
    test.decreaseDepth()
    assert test.constString() == '|---'

if __name__ == '__main__':
    test()