from board import Board
import random
totalPacketsCount = 0
packetCount = 500
b = Board()
b.printBoard()
b.printAllThreeNeighboursDetail()
b.printAllPowersDetail()
b.initializeCompromisedNode()
sourceId = random.randint(0,122)
print("Source Id:",sourceId)
if sourceId == 0:
    sourceId += 1
elif sourceId == 122:
    sourceId -= 1
b.initializeAttacker()
for i in range(packetCount):
    print("*-*"*100)
    print("PACKET NO :{}".format(i+1).center(300,'-'))
    print("*-*"*100)

    phantomElementOne,allNodeDetail,isCompromisedNodeCaughtInFlooding,isAttackerCaught = b.getPhantomSquare(sourceId,True)
    print(b.sourceNode.id)
    if isAttackerCaught:

        continue
    if isCompromisedNodeCaughtInFlooding:
        print("Compromised node detected while flooding packet in phantom Square 1")
        b.successfulPacketsCount += 1
        totalPacketsCount += 1
        continue
    else:
        print("Phantom Node:",phantomElementOne.id)
        print("Phantom Node's power:",phantomElementOne.power)
        b.visualizeCoordinate()
        b.printAllPowersDetail()
        #Source ID to Phantom Node - I
        print("SourceID:",sourceId,"PhantomElementId:",phantomElementOne.id)
        if phantomElementOne.id == -1:
            print("Packet Reached BaseStationReached!")
            b.successfulPacketsCount += 1
            totalPacketsCount += 1
            continue
        baseStationReached,failure,isCompromisedNode = b.shortestPath(allNodeDetail[sourceId],allNodeDetail[phantomElementOne.id])
        # if isCompromisedNode return to base station through forwardRandomWalk
        print(baseStationReached,failure,isCompromisedNode)
        print("Current Source id:",b.sourceNode.id)
        if isCompromisedNode:
            print("Compromised Node is detected while sending packet to phantom Node 1")
            b.forwardRandomWalk(b.sourceNode)
            totalPacketsCount += 1
            # Redirect this directly to base station through forward random Walk
            continue
        elif failure:
            print("Packet got stuck, Node has no power to transfer packet further")
            # b.failurePacketsCount += 1
            totalPacketsCount += 1
            continue
        elif baseStationReached:
            print("Packet reached basestation successfully!")
            b.successfulPacketsCount += 1
            totalPacketsCount += 1
            continue
        else:
            phantomElementTwo, allNodeDetail,isCompromisedNodeCaughtInFlooding,isAttackerCaught = b.getPhantomSquare(phantomElementOne.id,False)
            print(phantomElementTwo,allNodeDetail)
            print(isCompromisedNodeCaughtInFlooding)
            if isAttackerCaught:
                continue
            if isCompromisedNodeCaughtInFlooding:
                print("Packet Reached base station while flooding in Phantom Square 2")
                b.forwardRandomWalk(b.sourceNode)
                totalPacketsCount += 1
                continue


            elif phantomElementTwo.id == -1:
                print("Packet has reached the base station Successfully! in phantom Square 2")
                b.successfulPacketsCount += 1
                totalPacketsCount += 1
                continue
            print("packet no:", i + 1)
            # Now sending packet from PhantomElementOne to PhantomElementTwo.
            print("SourceID:", sourceId, "PhantomElementTwoId:", phantomElementTwo.id)
            baseStationReached,failure,isCompromisedNode = b.shortestPath(allNodeDetail[phantomElementOne.id],allNodeDetail[phantomElementTwo.id])

            print(baseStationReached, failure, isCompromisedNode)
            print("Current Source id:", b.sourceNode.id)
            if baseStationReached:
                print("Packet has reached the base station!")
                b.successfulPacketsCount += 1
                totalPacketsCount += 1
                continue
            elif failure:
                print("Some Node hasn't have power to transfer packet further")
                b.failurePacketsCount += 1
                continue
            elif isCompromisedNode:
                print("Directly send to base station! Compromised node detected while sending packet to phantomNodeTwo")
                b.forwardRandomWalk(b.sourceNode)

                totalPacketsCount += 1
                continue
            else:
                IntermediateNodes = b.packetSplittingFourPieces(b.sourceNode)
                print([x.id for x in IntermediateNodes if x.id != b.sourceNode.id])
                if len([x.id for x in IntermediateNodes if x.id != b.sourceNode.id]) == len(IntermediateNodes):
                    totalPacketsCount += len([x.id for x in IntermediateNodes if x.id != b.sourceNode.id])
                else:
                    totalPacketsCount += len([x.id for x in IntermediateNodes if x.id != b.sourceNode.id])
                # send to four intermediate nodes!.

                b.printBoardById()
                IntermediateNodes = [x for x in IntermediateNodes if x.id != b.sourceNode.id]

                for s in range(len(IntermediateNodes)):
                    IntermediateNodes[s].p = b.sourceNode.p
                    baseStationReached,failure,isCompromisedNode = b.shortestPath(b.sourceNode,IntermediateNodes[s])
                    if baseStationReached:
                        b.successfulPacketsCount += 1
                        continue
                    elif failure:
                        continue
                    elif isCompromisedNode:
                        b.forwardRandomWalk(IntermediateNodes[s])


                print("Forward Random Walk starting...")
                for f in range(len(IntermediateNodes)):
                    b.forwardRandomWalk(IntermediateNodes[f])
                print(b.sourceNode.id)


print(b.sourceNode.p)
print("Successfull Packets Count : " ,b.successfulPacketsCount)
if totalPacketsCount == 0:
    totalPacketsCount = packetCount
print("Total Packets Count: ",b.successfulPacketsCount + b.failurePacketsCount)
# print("Failure Packets Count : ",totalPacketsCount - b.successfulPacketsCount)
print("Recorded failure Packets Count:",b.failurePacketsCount)

print('Attacker ID:',b.attackerNode.id)