from time import sleep
import time
import mq
import devcontrol
import mailman


# main function logic
def main():

    f = open('prev.txt', 'r')               # opens text file that keeps track of last level read (1 = Normal was last run)
    prev = f.read(1)                        # reads first character of the file (should only ever be a single number)
    print(prev)                             # debug
    f.close()                               # close the file for now
    
    # read the sensor
    level = mq.readSensor( mq.spi, mq.cs, mq.mcp, mq.channel0 )
    print( 'MQ-135 has been read' )
    
    # if level is too toxic, invoke lambda and block
    if level > 300:
        statString = 'Too High' 
        print( 'levels too high, blocking devices' )
        mailman.sendRequestSNS()                                        # invoke Lambda through API Gateway
        mailman.updateTable( level, statString )                       # sends data to front-end
        if prev == '1':
            time.sleep(5)                                                # wait 5 seconds to make sure table updates
            devcontrol.deny_cluster()                                       # block MAC addresses through router
            o = open('prev.txt', 'w')
            o.write('0')                                                    # let program know last level reading was over
            print(o.read())
            o.close

        print( 'done' )
    else:
        statString = 'Normal'
        print( 'levels acceptable, allowing devices' )
        mailman.updateTable( level, statString )
        if prev == '0':
            time.sleep(5)
            devcontrol.allow_cluster()                                      # allow MAC addresses through router
            n = open('prev.txt', 'w')
            print(n.read())
            n.write('1')                                                    # let program know last level reading was normal

        print( 'done' )


# testing DynamoDB request
def test():
    level = mq.readSensor( mq.spi, mq.cs, mq.mcp, mq.channel0 )
    statString = "test status"
    mailman.updateTable( level, statString )

if __name__ == '__main__':
    main()

# test()
