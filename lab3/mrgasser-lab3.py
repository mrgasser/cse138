#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class lab3_topo(Topo):
  def build(self):

    of_s1 = self.addSwitch('switch1')
    c1 = self.addHost('c1',mac='00:00:00:00:00:01',ip='20.0.1.10/24')
    c2 = self.addHost('c2',mac='00:00:00:00:00:02',ip='20.0.1.11/24')
    c3 = self.addHost('c3',mac='00:00:00:00:00:03',ip='20.0.1.12/24')
    c4 = self.addHost('c4',mac='00:00:00:00:00:04',ip='20.0.1.13/24')
    s1 = self.addHost('s1',mac='00:00:00:00:00:05',ip='20.0.1.1/24')
    s2 = self.addHost('s2',mac='00:00:00:00:00:06',ip='20.0.1.2/24')
    s3 = self.addHost('s3',mac='00:00:00:00:00:07',ip='20.0.1.3/24')

    self.addLink(c1,of_s1)
    self.addLink(c2,of_s1)
    self.addLink(c3,of_s1)
    self.addLink(c4,of_s1)
    self.addLink(s1,of_s1)
    self.addLink(s2,of_s1)
    self.addLink(s3,of_s1)


def configure():
  topo = lab3_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  #h1, h2, h3 = net.get('h1', 'h2', 'h3')
  
  CLI(net)

  net.stop()


if __name__ == '__main__':
  configure()
