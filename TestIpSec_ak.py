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

configure(hostname="172.20.11.134", context_path="/zstack")     ############TO BE changed

accessKeyId="EU337ZiLgNPYW7Ytmdhi"
accessKeySecret="j9nx0ftrURdzJruCXU2jbOAAyiiccM61PESGfN6U"

try:
    queryL3 = QueryL3NetworkAction()
    queryL3.conditions = ["uuid=%s" % args.l3uuid]
    queryL3.accessKeyId = accessKeyId
    queryL3.accessKeySecret = accessKeySecret
    res = queryL3.call()
    l3s = res.value.inventories
    print "l3 network: %s" % l3s

    createVip = CreateVipAction()
    createVip.name = "vip-for-ipsec"
    createVip.l3NetworkUuid = args.publicL3Uuid
    createVip.accessKeyId = accessKeyId
    createVip.accessKeySecret = accessKeySecret
    res = createVip.call()
    vip = res.value.inventory
    print "vip: %s" % vip

    createIpsec = CreateIPsecConnectionAction()
    createIpsec.accessKeyId = accessKeyId
    createIpsec.accessKeySecret = accessKeySecret
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




