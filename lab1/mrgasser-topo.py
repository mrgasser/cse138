#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
class MyTopology(Topo):
  """
  A basic topology
  """
  def __init__(self):
    Topo.__init__(self)

    #create users
    user1 = self.addHost("User1")
    user2 = self.addHost("User2")
    laptop = self.addHost("Laptop")
    phone = self.addHost("Phone")
    ipad = self.addHost("Ipad")
    server1 = self.addHost("Server1")
    server2 = self.addHost("Server2")

    #create switches
    switch1 = self.addSwitch("Switch1")
    switch2 = self.addSwitch("Switch2")
    switch3 = self.addSwitch("Switch3")

    #create liks
    self.addLink(user1, switch1, delay='10ms')
    self.addLink(user2, switch1, delay='10ms')
    self.addLink(laptop, switch1, delay='15ms')
    self.addLink(switch1, switch2, delay='10ms')
    self.addLink(phone, switch2, delay='10ms')
    self.addLink(ipad, switch2, delay='10ms')
    self.addLink(switch2, switch3, delay='10ms')
    self.addLink(switch3, server1, delay='10ms')
    self.addLink(switch3, server2, delay='20ms')


if __name__ == '__main__':
  """
  If this script is run as an executable (by chmod +x), this is
  what it will do
  """
  topo = MyTopology() ## Creates the topology
  net = Mininet( topo=topo, link = TCLink) ## Loads the topology
  net.start() ## Starts Mininet
  # Commands here will run on the simulated topology
  CLI(net)
  net.stop() ## Stops Mininet