import sys
from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon
#from PyQt4.QtCore import QString


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.musicSources = []
        self.mediaObject = Phonon.MediaObject(self)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObjectResolver = Phonon.MediaObject(self)
        self.musicInformationTable = self.musicInformationTableLabel()
        self.timeLcd = self.timeLcdLabel()
        self.stopAction = self.stopAction()
        self.playAction = self.playAction()
        self.pauseAction = self.pauseAction()
        self.initMedia()
        self.initUI()

    def initMedia(self):
        self.mediaObject.setTickInterval(1000)
        self.connect(self.mediaObject, QtCore.SIGNAL('tick(qint64)'), self.musicPlayedTime)
        self.connect(self.mediaObject, QtCore.SIGNAL('stateChanged(Phonon::State, Phonon::State)'),
                     self.playStateChanged)
        self.connect(self.mediaObjectResolver, QtCore.SIGNAL('stateChanged(Phonon::State, Phonon::State)'),
                     self.musicStateChanged)
        self.connect(self.mediaObject, QtCore.SIGNAL('currentSourceChanged(Phonon::MediaSource)'),
                     self.musicSourceChanged)
        self.connect(self.mediaObject, QtCore.SIGNAL('aboutToFinish()'), self.aboutToFinish)
        Phonon.createPath(self.mediaObject, self.audioOutput)

    def musicPlayedTime(self, time):
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.timeLcd.display(displayTime.toString('mm:ss'))

    def playStateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            if self.mediaObject.errorType() == Phonon.FatalError:
                QtGui.QMessageBox.warning(self, 'Fatal Error', self.mediaObject.errorString())
            else:
                QtGui.QMessageBox.warning(self, 'Error', self.mediaObject.errorString())
        elif newState == Phonon.PlayingState:
            self.playAction.setEnabled(False)
            self.pauseAction.setEnabled(True)
            self.stopAction.setEnabled(True)
        elif newState == Phonon.StoppedState:
            self.stopAction.setEnabled(False)
            self.playAction.setEnabled(True)
            self.pauseAction.setEnabled(False)
            self.timeLcd.display('00:00')
        elif newState == Phonon.PausedState:
            self.pauseAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.playAction.setEnabled(True)

    def musicSourceChanged(self, source):
        self.musicInformationTableLabel().selectRow(self.musicSources.index(source))
        self.timeLcd.display('00:00')

    def musicStateChanged(self, newState):
        if newState == Phonon.ErrorState:
            QtGui.QMessageBox.warning(self, 'Error opening files',
                                      self.mediaObjectResolver.errorString())

            while self.musicSources and self.musicSources.pop() != self.mediaObjectResolver.currentSource():
                pass
            return
        if newState != Phonon.StoppedState and newState != Phonon.PausedState:
            return
        if self.mediaObjectResolver.currentSource().type() == Phonon.MediaSource.Invalid:
            return
        metaData = self.mediaObjectResolver.metaData()
        title = metaData.get('TITLE', [str()])[0]
        #if title.isEmpty():   here is a bug
        title = self.mediaObjectResolver.currentSource().fileName()
        titleItem = QtGui.QTableWidgetItem(title)
        titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)
        artist = metaData.get('ARTIST', [str()])[0]
        artistItem = QtGui.QTableWidgetItem(artist)
        artistItem.setFlags(artistItem.flags() ^ QtCore.Qt.ItemIsEditable)
        album = metaData.get('ALBUM', [str()])[0]
        albumItem = QtGui.QTableWidgetItem(album)
        albumItem.setFlags(albumItem.flags() ^ QtCore.Qt.ItemIsEditable)
        year = metaData.get('DATE', [str()])[0]
        yearItem = QtGui.QTableWidgetItem(year)
        yearItem.setFlags(yearItem.flags() ^ QtCore.Qt.ItemIsEditable)

        currentRow = self.musicInformationTable.rowCount()
        self.musicInformationTable.insertRow(currentRow)
        self.musicInformationTable.setItem(currentRow, 0, titleItem)
        self.musicInformationTable.setItem(currentRow, 1, artistItem)
        self.musicInformationTable.setItem(currentRow, 2, albumItem)
        self.musicInformationTable.setItem(currentRow, 3, yearItem)

        if not self.musicInformationTable.selectedItems():
            self.musicInformationTable.selectRow(0)
            self.mediaObject.setCurrentSource(self.mediaObjectResolver.currentSource())
        source = self.mediaObjectResolver.currentSource()
        index = self.musicSources.index(self.mediaObjectResolver.currentSource()) + 1
        if len(self.musicSources) > index:
            self.mediaObjectResolver.setCurrentSource(self.musicSources[index])
        else:
            self.musicInformationTableLabel().resizeColumnsToContents()
            if self.musicInformationTableLabel().columnWidth(0) > 300:
                self.musicInformationTableLabel().setColumnWidth(0, 300)

    def aboutToFinish(self):
        index = self.musicSources.index(self.mediaObject.currentSource()) + 1
        if len(self.musicSources) > index:
            self.mediaObject.enqueue(self.musicSources[index])

    def initUI(self):
        self.resize(500, 300)
        self.setupTitle()
        self.setupWindowButton()
        self.setupControlButton()
        self.setuplabels()

    def setupTitle(self):
        self.setWindowTitle('Life Player')

    def setupWindowButton(self):
        self.fileMenuButton()
        self.aboutMenuButton()

    def fileMenuButton(self):
        fileMenu = self.menuBar().addMenu('&File')
        fileMenu.addAction(self.addFileAction())
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction())

    def exitAction(self):
        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.connect(exit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        return exit

    def addFileAction(self):
        addFile = QtGui.QAction('Add Files', self)
        addFile.setShortcut('Ctrl+F')
        addFile.connect(addFile, QtCore.SIGNAL('triggered()'), self.addFiles)
        return addFile

    def addFiles(self):
        files = QtGui.QFileDialog.getOpenFileNames(self,
                'Select Music Files',
                QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation))
        #if files is not None:
            #return
        index = len(self.musicSources)
        for string in files:
            self.musicSources.append(Phonon.MediaSource(string))
        if self.musicSources:
            self.mediaObjectResolver.setCurrentSource(self.musicSources[index])

    def aboutMenuButton(self):
        aboutMenu = self.menuBar().addMenu('Help')
        aboutMenu.addAction(self.aboutAction())
        aboutMenu.addSeparator()
        aboutMenu.addAction(self.aboutQtAction())

    def aboutAction(self):
        aboutAction = QtGui.QAction('About', self)
        aboutAction.setShortcut('Ctrl+B')
        aboutAction.connect(aboutAction, QtCore.SIGNAL('triggered()'), self.about)
        return aboutAction

    def about(self):
        QtGui.QMessageBox.information(self, ('About Life Player'),
            ('The Life Player example shows how to use Phonon '
             'the multimedia framework that comes with Qt to '
             'create a simple music player.'))

    def aboutQtAction(self):
        aboutQt = QtGui.QAction('About Qt', self)
        aboutQt.setShortcut('Ctrl+Q')
        aboutQt.connect(aboutQt, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('aboutQt()'))
        return aboutQt

    def setupControlButton(self):
        self.musicControlButton()

    def musicControlButton(self):
        bar = QtGui.QToolBar()
        bar.addAction(self.playAction)
        bar.addAction(self.pauseAction)
        bar.addAction(self.stopAction)
        return bar

    def playAction(self):
        playAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), 'Play', self)
        playAction.setShortcut('Ctrl+P')
        playAction.setDisabled(True)
        playAction.connect(playAction, QtCore.SIGNAL('triggered()'), self.mediaObject, QtCore.SLOT('play()'))
        return playAction

    def pauseAction(self):
        pauseAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPause), 'Pause', self)
        pauseAction.setShortcut('Ctrl+A')
        pauseAction.setDisabled(True)
        pauseAction.connect(pauseAction, QtCore.SIGNAL('triggered()'), self.mediaObject, QtCore.SLOT('pause()'))
        return pauseAction

    def stopAction(self):
        stopAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaStop), 'Stop', self)
        stopAction.setShortcut('Ctrl+S')
        stopAction.setDisabled(True)
        stopAction.connect(stopAction, QtCore.SIGNAL('triggered()'), self.mediaObject, QtCore.SLOT('stop()'))
        return stopAction

    def setuplabels(self):
        widget = QtGui.QWidget()
        widget.setLayout(self.mainLayout())
        self.setCentralWidget(widget)

    def timeLcdLabel(self):
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkGray)
        timeLcd = QtGui.QLCDNumber()
        timeLcd.setPalette(palette)
        timeLcd.display('00:00')
        return timeLcd

    def timeAndMusicSeekLayout(self):
        seekerLayout = QtGui.QHBoxLayout()
        seekerLayout.addWidget(self.musicSeekSlider())
        seekerLayout.addWidget(self.timeLcd)
        return seekerLayout

    def musicSeekSlider(self):
        seekSlider = Phonon.SeekSlider(self)
        seekSlider.setMediaObject(self.mediaObject)
        return seekSlider

    def volumeLabel(self):
        volumeLabel = QtGui.QLabel()
        volumeLabel.setPixmap(QtGui.QPixmap('images/volume.png'))
        return volumeLabel

    def volumeSlider(self):
        volumeSlider = Phonon.VolumeSlider(self)
        volumeSlider.setAudioOutput(self.audioOutput)
        volumeSlider.setSizePolicy(QtGui.QSizePolicy.Maximum,
                                   QtGui.QSizePolicy.Maximum)
        return volumeSlider

    def playbackLayout(self):
        playbackLayout = QtGui.QHBoxLayout()
        playbackLayout.addWidget(self.musicControlButton())
        playbackLayout.addStretch()
        playbackLayout.addWidget(self.volumeLabel())
        playbackLayout.addWidget(self.volumeSlider())
        return playbackLayout

    def musicClicked(self, row, column):
        oldState = self.mediaObject.state()
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        self.mediaObject.setCurrentSource(self.musicSources[row])
        if oldState == Phonon.PlayingState:
            self.mediaObject.play()

    def musicInformationTableLabel(self):
        headers = ['Title', 'Artist', 'Album', 'Year']
        musicTable = QtGui.QTableWidget(0, 4)
        musicTable.setHorizontalHeaderLabels(headers)
        musicTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        musicTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        musicTable.connect(musicTable, QtCore.SIGNAL('cellPressed(int, int)'), self.musicClicked)
        return musicTable

    def mainLayout(self):
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.musicInformationTable)
        mainLayout.addLayout(self.timeAndMusicSeekLayout())
        mainLayout.addLayout(self.playbackLayout())
        return mainLayout


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

