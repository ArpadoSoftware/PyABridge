import time
from . import ABridgeAdapter as ab
import threading
import json
from pydispatch import dispatcher
from random import randrange


class ABridge(object):
    VERSION = '1.0.3'
    MAX_CONNECT_RETRIES = 1000000

    SIGNAL_INDEX_READY = 1
    SIGNAL_LANE_READY = 2
    SIGNAL_DATA_READY = 3
    SIGNAL_STOP = 4

    def __init__(self, **options):
        self.indexAddr = 'ipc:///tmp/aBridgeIndex'
        self.dataAddrPrefix = 'ipc:///tmp/aBridge'
        self.dataAddr = None
        self.sa = ab.SocketAdapter()
        self.isIndexReady = False
        self.isDataReady = False
        self.laneAssigned = False
        self.lane = None
        self.hasStop = False
        self.id = 'ABridge%i' % randrange(100000, 999999)

        for key in options:
            setattr(self, key, options[key])

        print('[PyABridge] version %s' % self.VERSION)

        dispatcher.connect(
            self.onSignal, signal=self.SIGNAL_INDEX_READY, sender=self.id)
        dispatcher.connect(
            self.onSignal, signal=self.SIGNAL_LANE_READY, sender=self.id)

    def onSignal(self, message=None):
        if message['sender'] != self.id:
            return

        if message['signal'] == self.SIGNAL_INDEX_READY:
            self.onIndexReady(message)

        if message['signal'] == self.SIGNAL_LANE_READY:
            self.onLaneReady(message)

        if message['signal'] == self.SIGNAL_STOP:
            self.hasStop = True

    def onIndexReady(self, message=None):
        pass

    def onLaneReady(self, message=None):
        pass

    def setDataCallback(self, callback=None):
        self.dataCallback = callback

    def onDataReady(self, data=None):
        return self.dataCallback(data)

    def stop(self):
        dispatcher.send(message={'signal': self.SIGNAL_STOP, 'sender': self.id},
                        signal=self.SIGNAL_STOP, sender=self.id)

    def start(self):
        print('[PyABridge] starting new thread...')

        self.hasStop = False

        self.runThread = threading.Thread(name=self.id, target=self._run)
        self.runThread.setDaemon(False)
        self.runThread.start()

    def _run(self):
        cr = 0

        print('[PyABridge] thread started')

        dispatcher.connect(
            self.onSignal, signal=self.SIGNAL_STOP, sender=self.id)

        while not self.hasStop and not self.isIndexReady and cr <= self.MAX_CONNECT_RETRIES:
            cr += 1
            self.isIndexReady = self.sa.initIndexSocket(self.indexAddr)

            time.sleep(0.000001)

        print('[PyABridge] index ready at %s' % self.indexAddr)

        dispatcher.send(message={'signal': self.SIGNAL_INDEX_READY, 'sender': self.id},
                        signal=self.SIGNAL_INDEX_READY, sender=self.id)

        while not self.hasStop and not self.laneAssigned:
            try:
                checkInMsg = self.sa.recvIndexMsg()
                self.lane = int(float(checkInMsg))

                self.sa.sendIndexMsg(str(self.lane))
                self.laneAssigned = True
            except KeyboardInterrupt:
                pass
            finally:
                time.sleep(0.000001)

        self.dataAddr = '%s%i' % (self.dataAddrPrefix, self.lane)

        print('[PyABridge] connecting to data lane at %s' % self.dataAddr)

        cr = 0

        while not self.hasStop and not self.isDataReady and cr <= self.MAX_CONNECT_RETRIES:
            cr += 1
            self.isDataReady = self.sa.initDataSocket(self.dataAddr)

            time.sleep(0.000001)

        dispatcher.send(message={'signal': self.SIGNAL_LANE_READY,
                                 'sender': self.id, 'lane': self.lane},
                        signal=self.SIGNAL_LANE_READY, sender=self.id)

        print('[PyABridge] data lane ready at %s' % self.dataAddr)

        while not self.hasStop:
            try:
                dataMsg = self.sa.recvDataMsg()
                msgIn = json.loads(dataMsg)

                # process data here
                msgOut = self.onDataReady(data=msgIn)

                self.sa.sendDataMsg(json.dumps(msgOut))
            except (KeyboardInterrupt, Exception):
                pass
            finally:
                time.sleep(0.000001)

        self.finish()

    def finish(self):
        self.sa.closeIndexSocket()
        self.sa.closeDataSocket()

        self.dataAddr = None
        self.laneAssigned = False
        self.isIndexReady = False
        self.isDataReady = False
