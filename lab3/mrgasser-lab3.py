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
    client1 = self.addHost("Client1", ip="20.1.1.10/24")
    client2 = self.addHost("Client2", ip="20.1.1.11/24")
    client3 = self.addHost("Client3", ip="20.1.1.12/24")
    client4 = self.addHost("Client4", ip="20.1.1.13/24")
    server1 = self.addHost("Server1", ip="20.1.1.1/24")
    server2 = self.addHost("Server2", ip="20.1.1.2/24")
    server3 = self.addHost("Server3", ip="20.1.1.3/24")

    #create openflow switch
    openflow_switch = self.addSwitch("of_switch")

    #create liks
    self.addLink(client1, openflow_switch)
    self.addLink(client2, openflow_switch)
    self.addLink(client3, openflow_switch)
    self.addLink(client4, openflow_switch)
    self.addLink(server1, openflow_switch)
    self.addLink(server2, openflow_switch)
    self.addLink(server3, openflow_switch)


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