import sys

#Put "number1" space and "number" line jump 
def jumptab(number, number1):
    i = 0
    rslt = ""
    while (i < number):
        rslt = rslt + '\n'
        i += 1
    i = 0
    while (i < number1):
        rslt = rslt + "  "
        i += 1
    return (rslt)

#Part of configtx.yaml
def createChannelProfile(orgName, profileName):
    rslt = jumptab(0, 1) + profileName + ":"
    rslt += jumptab(1, 2) + "Consortium: ComposerConsortium"
    rslt += jumptab(1, 2) + "Application:"
    rslt += jumptab(1, 3) + "<<: *ApplicationDefaults"
    rslt += jumptab(1, 3) + "Organizations:"
    i = 2
    while (i < len(orgName)):
        rslt += jumptab(1, 5) + "- *" + orgName[i]
        i += 2
    return (rslt)

#Part of configtx.yaml
def createProfiles(orgName, profileName, ordererName):
    rslt = jumptab(0, 1) + profileName + ":"
    rslt += jumptab(1, 2) + "Orderer:"
    rslt += jumptab(1, 3) + "<<: *OrdererDefaults"
    rslt += jumptab(1, 3) + "Organizations:"
    rslt += jumptab(1, 4) + "- *" + ordererName
    rslt += jumptab(1, 2) + "Consortiums:"
    rslt += jumptab(1, 3) + "ComposerConsortium:"
    rslt += jumptab(1, 4) + "Organizations:"
    i = 2
    while (i < len(orgName)):
        rslt += jumptab(1, 5) + "- *" + orgName[i]
        i += 2
    return (rslt)

#Part of configtx.yaml
def createOrganisations(name, opt, host):
    rslt = jumptab(0, 1) + "- &" + name
    rslt = rslt + jumptab(2, 3) + "Name: " + name 
    if (opt == 1):
        rslt = rslt + jumptab(2, 3) + "ID: " + name + "MSP"
        rslt = rslt + jumptab(2, 3) + "MSPDir: crypto-config/peerOrganizations/" + name + "." + host + ".com/msp"
    else:
        rslt = rslt + jumptab(2, 3) + "ID: OrdererMSP"
        rslt = rslt + jumptab(2, 3) + "MSPDir: crypto-config/ordererOrganizations/" + host + ".com/msp"
    rslt = rslt + jumptab(2, 3) + "AdminPrincipal: Role.MEMBER"
    if (opt == 1):
        rslt = rslt + jumptab(2, 3) + "AnchorPeers:"
        rslt = rslt + jumptab(2, 4) + "- Host: peer0." + name + "." + host + ".com"
        rslt = rslt + jumptab(1, 4) + "  Port: 7051"
    return (rslt)

#Part of configtx.yaml
def createOrderer(typeorderer, messageCount, absoluteMaxBytes, preferredMaxBytes, host):
    rslt = jumptab(2, 0) + "Orderer: &OrdererDefaults"
    rslt += jumptab(2, 1) + "OrdererType: " + typeorderer
    rslt += jumptab(2, 1) + "Addresses:"
    rslt += jumptab(1, 2) + "- " + "orderer." + host + ".com:7050"
    rslt += jumptab(2, 1) + "BatchTimeout: 2s"
    rslt += jumptab(2, 1) + "BatchSize:"
    rslt += jumptab(2, 2) + "MaxMessageCount: " + messageCount
    rslt += jumptab(1, 2) + "AbsoluteMaxBytes: " + absoluteMaxBytes
    rslt += jumptab(1, 2) + "PreferredMaxBytes: " + preferredMaxBytes
    rslt += jumptab(2, 1) + "Kafka:"
    rslt += jumptab(1, 2) + "Brokers:"
    rslt += jumptab(1, 3) + "- kafka0:9092"
    rslt += jumptab(1, 3) + "- kafka1:9092" 
    rslt += jumptab(1, 3) + "- kafka2:9092" 
    rslt += jumptab(1, 3) + "- kafka3:9092"
    rslt += jumptab(2, 1) + "Organizations:"
    return (rslt)

#Part of configtx.yaml
def setOrg(tab):
    rslt = jumptab(2, 0) + createOrganisations("OrdererOrg", 0, tab[0])
    i = 2
    while (i < len(tab)):
        rslt += jumptab(2, 0) + createOrganisations(tab[i], 1, tab[0])
        i += 2
    return (rslt)

#Call functions in order to create crypto-config.yaml
def createCryptoconfig(tab):
    buffer = ordererOrgConfig(tab[0])
    buffer += jumptab(2, 0) + "PeerOrgs:"
    i = 2
    while (i < len(tab)):
        buffer += jumptab(2, 1) + "- Name: " + tab[i]
        buffer += jumptab(1, 1) + "  Domain: " + tab[i] + "." + tab[0] + ".com"
        buffer += jumptab(2, 2) + "Template:"
        buffer += jumptab(1, 3) + "Count: " + tab[i + 1]
        buffer += jumptab(2, 2) + "Users:"
        buffer += jumptab(1, 3) + "Count: 3"
        i += 2
    return (buffer)

#Part of crypto-config.yaml - OrdererOrgs section
def ordererOrgConfig(host):
    rslt = "OrdererOrgs:"
    rslt += jumptab(2, 1) + "- Name: Orderer"
    rslt += jumptab(1, 1) + "  Domain: " + host + ".com"
    rslt += jumptab(2, 2) + "Specs:"
    rslt += jumptab(1, 3) + "- Hostname: orderer"
    return (rslt)

#Call functions in order to create configtx.yaml
def createConfigtx(tabName):
    buffer = "Organizations:"
    buffer += setOrg(tabName)
    buffer += createOrderer("kafka", "10", "98 MB", "512 KB", tabName[0])
    buffer += jumptab(2, 0) + "Application: &ApplicationDefaults"
    buffer += jumptab(2, 1) + "Organizations:"
    buffer += jumptab(2, 0) + "Profiles:"
    buffer += jumptab(2, 0) + createProfiles(tabName, "ProfileTest", "OrdererOrg")
    buffer += jumptab(2, 0) + createChannelProfile(tabName, "ChannelTest")
    return (buffer) 

#Ask user for network mapping
def getArg():
    orgName = [input("Your network name : ")]
    orgName.append(input("Your first channel name : "))
    orgName.append(input("First org name : "))
    orgName.append(str(getNumber()))
    while (input("Do you want to create another organisation ? (y/N) ") == 'y' ):
        name = ""
        while sameName(orgName, name) == 0:
            if (name != ""):
                print("Name already used by another org")
            name = input("New org name : ")
        orgName.append(name)
        orgName.append(str(getNumber()))
    return (orgName)

#Get number of peer
def getNumber():
    peerNb = -1
    while peerNb < 0:
        while True:
            try:
                peerNb = int(input("Number of peer : "))
                break
            except:
                print("Please enter a number")
        if peerNb < 0:
            print("Please enter a positive number")
    return (peerNb)

#Error handling
def sameName(tab, name):
    i = 2
    if name == "":
        return (0)
    while i < len(tab):
        if tab[i] == name:
            return (0)
        i += 2
    return (1)

#Docker-compose.yaml header
def headerDockerFile(network):
    rslt = "version: '2'"
    rslt += jumptab(2,0) + "networks:"
    rslt += jumptab(1, 1) + network + ":"
    rslt += jumptab(2, 0) + "services:"
    return (rslt)

#Part of docker-compose.yaml - CA section
def caDockerFile(arch, hostname, rank, network):
    rslt = jumptab(2, 1) + "ca." + hostname + ":"
    rslt += jumptab(1, 2) + "image: hyperledger/fabric-ca:latest"
    rslt += jumptab(1, 2) + "environment:"
    rslt += jumptab(1, 3) + "- FABRIC_CA_HOME=/etc/hyperledger/fabric-ca-server"
    rslt += jumptab(1, 3) + "- FABRIC_CA_SERVER_CA_NAME=ca." + hostname
    rslt += jumptab(1, 2) + "ports:"
    rslt += jumptab(1, 3) + "- \"" + str((7 + rank)) + "054:7054\""
    rslt += jumptab(1, 2) + "command: sh -c 'fabric-ca-server start --ca.certfile /etc/hyperledger/fabric-ca-server-config/ca." + hostname + "-cert.pem --ca.keyfile /etc/hyperledger/fabric-ca-server-config/*_sk -b admin:adminpw -d'"
    rslt += jumptab(1, 2) + "volumes:"
    rslt += jumptab(1, 3) + "- ./crypto-config/peerOrganizations/" + hostname + "/ca/:/etc/hyperledger/fabric-ca-server-config"
    rslt += jumptab(1, 2) + "container_name: ca." + hostname
    rslt += jumptab(1, 2) + "networks:"
    rslt += jumptab(1, 3) + "- " + network
    return (rslt)

#Useful function for create docker-compose.yaml
def container_name(value):
    return (jumptab(1, 2) + "container_name: " + value)

#Useful function for create docker-compose.yaml
def image(value):
    return (jumptab(1, 2) + "image: " + value)

#Useful function for create docker-compose.yaml
def working_dir(value):
    return (jumptab(1, 2) + "working_dir: " + value)

#Useful function for create docker-compose.yaml
def command(value):
    return (jumptab(1, 2) + "command: " + value)

#Useful function for create docker-compose.yaml
def list_value(value):
    return (jumptab(1, 3) + "- " + value)

#Part of docker-compose.yaml - Zookeeper section
def zookeeperDockerFile(network, rank):
    rslt = jumptab(2, 1) + "zookeeper" + str(rank) + ":"
    rslt += container_name("zookeeper" + str(rank))
    rslt += jumptab(1, 2) + "extends:"
    rslt += jumptab(1, 4) + "file: docker-compose-base.yml"
    rslt += jumptab(1, 4) + "service: zookeeper"
    rslt += jumptab(1, 2) + "environment:"
    rslt += list_value("ZOO_MY_ID=" + str((rank + 1)))
    rslt += list_value("ZOO_SERVERS=server.1=zookeeper0:2888:3888 server.2=zookeeper1:2888:3888 server.3=zookeeper2:2888:3888")
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Part of docker-compose.yaml - Kafka section
def kafkaDockerFile(network, rank):
    rslt = jumptab(2, 1) + "kafka" + str(rank) + ":"
    rslt += container_name("kafka" + str(rank))
    rslt += jumptab(1, 2) + "extends:"
    rslt += jumptab(1, 4) + "file: docker-compose-base.yml"
    rslt += jumptab(1, 4) + "service: kafka"
    rslt += jumptab(1, 2) + "environment:"
    rslt += list_value("KAFKA_BROKER_ID=" + str(rank))
    rslt += list_value("KAFKA_ZOOKEEPER_CONNECT=zookeeper0:2181,zookeeper1:2181,zookeeper2:2181")
    rslt += list_value("KAFKA_MESSAGE_MAX_BYTES=103809024")
    rslt += list_value("KAFKA_REPLICA_FETCH_MAX_BYTES=103809024")
    rslt += list_value("KAFKA_REPLICA_FETCH_RESPONSE_MAX_BYTES=103809024")
    rslt += jumptab(1, 2) + "depends_on:"
    rslt += list_value("zookeeper0")
    rslt += list_value("zookeeper1")
    rslt += list_value("zookeeper2")
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Part of docker-compose.yaml - Orderer section
def ordererDockerFile(hostname, rank, network, arch):
    rslt = jumptab(2, 1) + "orderer." + hostname + ":"
    rslt += container_name("orderer." + hostname)
    rslt += image("hyperledger/fabric-orderer:latest")
    rslt += working_dir("/opt/gopath/src/github.com/hyperledger/fabric")
    rslt += command("orderer")
    rslt += jumptab(1, 2) + "environment:"
    rslt += list_value("CONFIGTX_ORDERER_ORDERERTYPE=kafka")
    rslt += list_value("CONFIGTX_ORDERER_KAFKA_BROKERS=[kafka0:9092,kafka1:9092,kafka2:9092,kafka3:9092]")
    rslt += list_value("ORDERER_KAFKA_RETRY_SHORTINTERVAL=1s")
    rslt += list_value("ORDERER_KAFKA_RETRY_SHORTTOTAL=30s")
    rslt += list_value("ORDERER_KAFKA_VERBOSE=true")
    rslt += list_value("ORDERER_GENERAL_LOGLEVEL=debug")
    rslt += list_value("ORDERER_GENERAL_LISTENADDRESS=0.0.0.0")
    rslt += list_value("ORDERER_GENERAL_GENESISMETHOD=file")
    rslt += list_value("ORDERER_GENERAL_GENESISFILE=/etc/hyperledger/configtx/genesis.block")
    rslt += list_value("ORDERER_GENERAL_LOCALMSPID=OrdererMSP")
    rslt += list_value("ORDERER_GENERAL_LOCALMSPDIR=/etc/hyperledger/msp/orderer/msp")
    rslt += jumptab(1, 2) + "ports:"
    rslt += list_value(str((7 + rank)) + "050:7050")
    rslt += jumptab(1, 2) + "volumes:"
    rslt += list_value("./channel-artifacts:/etc/hyperledger/configtx")
    rslt += list_value("./crypto-config/ordererOrganizations/" + hostname + "/orderers/" + "orderer." + hostname +  "/msp:/etc/hyperledger/msp/orderer/msp")
    rslt += jumptab(1, 2) + "depends_on:"
    rslt += list_value("kafka0")
    rslt += list_value("kafka1")
    rslt += list_value("kafka2")
    rslt += list_value("kafka3")
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Part of docker-compose.yaml - Coucdh section
def couchDBDockerFile(arch, network, rank):
    rslt = jumptab(2, 1) + "couchdb" + str(rank) + ":"
    rslt += container_name("couchdb" + str(rank))
    rslt += image("hyperledger/fabric-couchdb:latest")
    rslt += jumptab(1, 2) + "ports:"
    rslt += list_value(str((rank + 5)) + "984:5984")
    rslt += jumptab(1, 2) + "environment:"
    rslt += jumptab(1, 3) + "DB_URL: http://localhost:" + str((rank + 5)) + "984/member_db"
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Part of docker-compose.yaml - Peer section
def peerDockerFile(hostname, rank, network, arch, idd, name):
    rslt = jumptab(2, 1) + "peer" + str(idd) + "." + hostname + ":"
    rslt += container_name("peer" + str(idd) + "." + hostname)
    rslt += image("hyperledger/fabric-peer:latest")
    rslt += working_dir("/opt/gopath/src/github.com/hyperledger/fabric")
    rslt += command("peer node start")
    rslt += jumptab(1, 2) + "environment:"
    rslt += list_value("CORE_LOGGING_LEVEL=debug")
    rslt += list_value("CORE_CHAINCODE_LOGGING_LEVEL=DEBUG")
    rslt += list_value("CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock")
    rslt += list_value("CORE_PEER_ID=peer" + str(idd) + "." + hostname)
    rslt += list_value("CORE_PEER_ADDRESS=peer" + str(idd) + "." + hostname + ":7051")
    rslt += list_value("CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=$NETWORK_NAME")
    rslt += list_value("CORE_PEER_LOCALMSPID=" + name + "MSP")
    rslt += list_value("CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp")
    rslt += list_value("CORE_LEDGER_STATE_STATEDATABASE=CouchDB")
    rslt += list_value("CORE_LEDGER_STATE_COUCHDBCONFIG_COUCHDBADDRESS=couchdb" + str(rank) + ":5984")
    rslt += jumptab(1, 2) + "ports:"
    rslt += list_value(str((7 + rank)) + "051:7051")
    rslt += list_value(str((7 + rank)) + "053:7053")
    rslt += jumptab(1, 2) + "volumes:"
    rslt += list_value("/var/run/:/host/var/run/")
    rslt += list_value("./channel-artifacts:/etc/hyperledger/configtx")
    rslt += list_value("./crypto-config/peerOrganizations/" + hostname + "/peers/peer" + str(idd) + "." + hostname + "/msp:/etc/hyperledger/peer/msp")
    rslt += list_value("./crypto-config/peerOrganizations/" + hostname + "/users:/etc/hyperledger/msp/users")
    rslt += jumptab(1, 2) + "depends_on:"
    if (arch != "test"):
        rslt += list_value("orderer." + network + ".com")
    rslt += list_value("couchdb" + str(rank))
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Call functions in order to create docker-composer.yaml
def createDockerFile(tab):
    network = tab[0]
    arch = tab[1]
    orgNB = int((len(tab) - 2) / 2)
    buffer = headerDockerFile(network)
    buffer += ordererDockerFile(network + ".com", 0, network, "$ARCH")
    for i in range (0, 4):
        buffer += kafkaDockerFile(network, i)
    for i in range (0, 3):
        buffer += zookeeperDockerFile(network, i)
    rank = 0
    index = 3
    for k in range (0, orgNB):
        buffer += caDockerFile("$ARCH", tab[index - 1] + "." + network + ".com", k, network)
        for i in range (0, int(tab[index])):
            buffer += peerDockerFile(tab[index - 1] + "." + network + ".com", rank, network, "$ARCH", i, tab[index - 1])
            buffer += couchDBDockerFile("$ARCH", network, rank)
            rank += 1
        index += 2
    return (buffer)

#Part of launch.sh
def createGenNeeded(channelId, tab):
    orgNB = int((len(tab) - 2) / 2)
    index = 2
    rslt = "function gen_needed(){\nexport CHANNEL_NAME=" + channelId + "\nexport FABRIC_CFG_PATH=$PWD\n./cryptogen generate --config=./crypto-config.yaml\n./configtxgen -profile ProfileTest -outputBlock ./channel-artifacts/genesis.block\n"
    rslt += "./configtxgen -profile ChannelTest -outputCreateChannelTx ./channel-artifacts/channel.tx   -channelID " + channelId
    for i in range (0, orgNB):
        rslt += jumptab(1, 0) + "./configtxgen -profile ChannelTest -outputAnchorPeersUpdate ./channel-artifacts/" + tab[index] + "MSPanchors.tx -channelID " + channelId + " -asOrg " + tab[index]
        index += 2
    rslt += "\n"
    rslt += "}\n"
    return (rslt)

#Part of launch.sh
def createConst():
    rslt = "function clean_it() {\ndocker rm -f $(docker ps -a -q)\nrm -rf crypto-config/*\nrm -rf channel-artifacts/*\n}\n\nfunction start_network() {\ndocker-compose -f docker-compose.yml up -d && docker ps\n}\n\nclean_it\ngen_needed\nstart_network\nsleep 20\njoin_channel"
    return (rslt)

#Part of launch.sh
def createJoinChannel(tab, channelId):
    index = 3
    orgNB = int((len(tab) - 2) / 2)
    rslt = "function join_channel() {\ndocker exec peer0." + tab[2] + "." + tab[0] + ".com peer channel create -o orderer." + tab[0] + ".com:7050 -c " + channelId + " -f /etc/hyperledger/configtx/channel.tx"
    rslt += jumptab(1, 0) + "docker exec peer0." + tab[2] + "." + tab[0] + ".com cp " + channelId + ".block /etc/hyperledger/configtx"
    for i in range (0, orgNB):
        for k in range (0, int(tab[index])):
            rslt += jumptab(1, 0) + "docker exec -e \"CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@" + tab[index - 1] + "." + tab[0] + ".com/msp\" peer" + str(k) + "." + tab[index - 1] + "." + tab[0] + ".com peer channel join -b /etc/hyperledger/configtx/" + channelId + ".block"
        index += 2
    rslt += "\n}"
    return (rslt)

#Call functions in order to create launch.sh
def createScript(tab):
    buffer = "#!/bin/bash"
    buffer += jumptab(2, 0) + createGenNeeded(tab[1], tab)
    buffer += jumptab(2, 0) + createJoinChannel(tab, tab[1])
    buffer += jumptab(2, 0) + createConst()
    return (buffer)

#Main function
def createNewOrg():
    tab = getArg()
    script = open("launch.sh", "w")
    scriptBuffer = createScript(tab)
    script.write(scriptBuffer)
    script.close()
    dockerCompose = open("docker-compose.yml", "w")
    cryptoConfig = open("crypto-config.yaml", "w")
    configtx = open("configtx.yaml", "w")
    composeBuffer = createDockerFile(tab)
    cryptoBuffer = createCryptoconfig(tab)
    configtxBuffer = createConfigtx(tab)
    dockerCompose.write(composeBuffer)
    dockerCompose.close()
    cryptoConfig.write(cryptoBuffer)
    cryptoConfig.close()
    configtx.write(configtxBuffer)
    configtx.close()


createNewOrg()
