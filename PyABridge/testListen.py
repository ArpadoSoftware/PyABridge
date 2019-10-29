
import sys
import time
import pynng
import json
import zlib


def main():
    surv = pynng.Surveyor0(listen='ipc:///tmp/aBridgeIndex')

    try:
        laneAssigned = False
        lane = 1

        while not laneAssigned:
            try:
                surv.send(zlib.compress(str.encode(str(lane)), 0))

                try:
                    checkIn = surv.recv(block=True)
                    checkInMsg = zlib.decompress(
                        checkIn, wbits=zlib.MAX_WBITS | 16)
                    laneAssigned = True

                    print('lane is now %i' % lane)
                except:
                    pass
            except (KeyboardInterrupt, Exception) as err:
                print(err) if str(err) != 'Try again' else ''
            finally:
                time.sleep(0.000001)

        req = pynng.Req0(listen='ipc:///tmp/aBridge%i' % lane)
        print('data socket ready')

        while True:
            try:
                msgOut = str.encode(json.dumps({
                    'inputsL': [],
                    'inputsR': []
                }))
                zMsgOut = zlib.compress(msgOut, 0)
                req.send(zMsgOut)

                zMsgIn = req.recv(block=True)
                msgIn = zlib.decompress(zMsgIn, wbits=zlib.MAX_WBITS | 16)
                msgIn = json.loads(msgIn)

                print(msgIn)
            except (Exception, pynng.exceptions.TryAgain):
                pass
            finally:
                time.sleep(0.000001)
    except KeyboardInterrupt:
        pass
    finally:
        req.close()
        surv.close()


if __name__ == "__main__":
    main()
