# /usr/bin/python
from zssdk import *
import argparse

parser = argparse.ArgumentParser(description='create ipsec')
parser.add_argument('publicL3Uuid')
parser.add_argument('l3uuid')
parser.add_argument('peerAddress')
parser.add_argument('ipsecPassword')
parser.add_argument('peerCidrs')

args = parser.parse_args()

configure(hostname="10.86.4.243", context_path="/zstack")     ############TO BE changed

login = LogInByAccountAction()
login.accountName = "admin"          ############TO BE changed
login.password = "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"          ############TO BE changed
res = login.call()
session = res.value.inventory

try:
    queryL3 = QueryL3NetworkAction()
    queryL3.sessionId = session.uuid
    queryL3.conditions = ["uuid=%s" % args.l3uuid]
    res = queryL3.call()
    l3s = res.value.inventories
    print "l3 network: %s" % l3s

    createVip = CreateVipAction()
    createVip.name = "vip-for-ipsec"
    createVip.sessionId = session.uuid
    createVip.l3NetworkUuid = args.publicL3Uuid
    res = createVip.call()
    vip = res.value.inventory
    print "vip: %s" % vip

    createIpsec = CreateIPsecConnectionAction()
    createIpsec.sessionId = session.uuid
    createIpsec.name = "ipsec-1"
    createIpsec.transformProtocol = "ah"
    createIpsec.authMode = "psk"
    createIpsec.authKey = args.ipsecPassword
    createIpsec.ikeAuthAlgorithm = "md5"
    createIpsec.ikeEncryptionAlgorithm = "aes-256"
    createIpsec.ikeDhGroup = 2
    createIpsec.policyAuthAlgorithm = "sha1"
    createIpsec.policyEncryptionAlgorithm = "aes-128"
    createIpsec.policyMode = "tunnel"
    createIpsec.pfs = "dh-group19"
    createIpsec.vipUuid = vip.uuid
    createIpsec.l3NetworkUuid = args.l3uuid
    createIpsec.peerAddress = args.peerAddress
    createIpsec.peerCidrs = [args.peerCidrs]
    res = createIpsec.call()
    ipsec = res.value.inventory
    print "vip router: %s" % ipsec
except Exception as e:
    print "error %s" %e

logout = LogOutAction()
logout.sessionUuid = session.uuid
logout.call()




