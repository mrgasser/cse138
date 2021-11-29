#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    # h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='1.1.1.1/24', defaultRoute="h1-eth0")
    # h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='2.2.2.2/24', defaultRoute="h2-eth0")

    # Create a switch. No changes here from Lab 1.
    # s1 = self.addSwitch('s1')

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    #
    # IMPORTANT NOTES: 
    # - On a single device, you can only use each port once! So, on s1, only 1 device can be
    #   plugged in to port 1, only one device can be plugged in to port 2, etc.
    # - On the "host" side of connections, you must make sure to always match the port you 
    #   set as the default route when you created the device above. Usually, this means you 
    #   should plug in to port 0 (since you set the default route to h#-eth0).
    #
    # self.addLink(s1,h1, port1=8, port2=0)
    # self.addLink(s1,h2, port1=9, port2=0)

    print("setting up topology")

    # add switches
    s1 = self.addSwitch('s1') #floor 1 Switch 1 ID: 1
    s2 = self.addSwitch('s2') #floor 1 Switch ID: 2
    s3 = self.addSwitch('s3') # CORE SWITCH ID: 3
    s4 = self.addSwitch('s4') # Data Center Switch ID:4
    s5 = self.addSwitch('s5') #air-gapped floor s1 ID: 5
    s6 = self.addSwitch('s6') #floor 2 switch 1 ID: 6

    # add hosts Floor 1
    laptop = self.addHost('laptop', mac='00:00:00:00:00:01',
        ip='20.2.1.10/24',defaultRoute='laptop-eth0')       #may need to change Default
    labmachine = self.addHost('labmachine',mac='00:00:00:00:00:02',
        ip='20.2.1.20/24',defaultRoute='labmachine-eth0')
    device1 = self.addHost('device1',mac='00:00:00:00:00:03',
        ip='20.2.1.30/24',defaultRoute='device1-eth0')
    device2 = self.addHost('device2',mac='00:00:00:00:00:04',
        ip='20.2.1.40/24',defaultRoute='device2-eth0')
    
    #floor 2 hosts
    h1 = self.addHost('h1',mac='00:00:00:00:00:05',
        ip='10.2.7.10/24',defaultRoute='h1-eth0')
    h2 = self.addHost('h2',mac='00:00:00:00:00:06',
        ip='10.2.7.20/24',defaultRoute='h2-eth0')
    
    #other hosts
    h_trust = self.addHost('h_trust',mac='00:00:00:00:00:07',
        ip='104.24.32.100/24',defaultRoute='h_trust-eth0')
    h_untrust = self.addHost('h_untrust',mac='00:00:00:00:00:08',
        ip='108.44.83.103/24',defaultRoute='h_untrust-eth0')
    h_server = self.addHost('h_server',mac='00:00:00:00:00:9',
        ip='30.1.4.66/24',defaultRoute='h_server-eth0')

    # Secure clients
    sc1 = self.addHost('sc1',mac='00:00:00:00:00:10',
        ip='40.2.5.10/29',defaultRoute='sc1-eth0')
    sc2 = self.addHost('sc2',mac='00:00:00:00:00:11',
        ip='40.2.5.20/29',defaultRoute='sc2-eth0')
    sc3 = self.addHost('sc3',mac='00:00:00:00:00:12',
        ip='40.2.5.30/29',defaultRoute='sc3-eth0')
    sc4 = self.addHost('sc4',mac='00:00:00:00:00:13',
        ip='40.2.5.40/29',defaultRoute='sc4-eth0')
    sc5 = self.addHost('sc5',mac='00:00:00:00:00:14',
        ip='40.2.5.50/29',defaultRoute='sc5-eth0')
    sc6 = self.addHost('sc6',mac='00:00:00:00:00:15',
        ip='40.2.5.60/29',defaultRoute='sc6-eth0')

    #adding links

    #floor 1 links, Department A
    self.addLink(s1,laptop, port1=8, port2=0) #F1S1 -- Laptop
    self.addLink(s1,labmachine, port1= 9, port2=0) #F1S1 -- Labmachine
    self.addLink(s2, device1, port1=8, port2=0) #F2S2 -- Device1
    self.addLink(s2, device2, port1=9, port2=0) #F2S2 -- Device2

    #floor 2 links, Department B 
    self.addLink(s6, h1, port1=8, port2=0) #F2S1 -- Host1
    self.addLink(s6, h2, port1=9, port2=0) #F2S1 -- Host2

    #air-gapped floor links
    self.addLink(s5, sc1, port1=8, port2=0) # Air Gapped -- sc1
    self.addLink(s5, sc2, port1=9, port2=0) # Air Gapped -- sc1
    self.addLink(s5, sc3, port1=10, port2=0) # Air Gapped -- sc1
    self.addLink(s5, sc4, port1=11, port2=0) # Air Gapped -- sc1
    self.addLink(s5, sc5, port1=12, port2=0) # Air Gapped -- sc1
    self.addLink(s5, sc6, port1=13, port2=0) # Air Gapped -- sc1

    #data center link
    self.addLink(s4, h_server, port1=8, port2=0) #Data center Switch - Web server
    
    #core switch links
    self.addLink(s3, h_trust, port1=8, port2=0) #Core Switch -- Trusted Host
    self.addLink(s3, h_untrust, port1=9, port2=0) #Core Swtich -- untrusted Host
    self.addLink(s3, s1, port1=11, port2=1) #Core Switch -- F1S1
    self.addLink(s3, s2, port1=11, port2=2) #Core Switch -- F1S2
    self.addLink(s3, s6, port1=11, port2=3) #Core Switch -- F2S1
    self.addLink(s3, s5, port1=15, port2=4) #Core Swtich -- air gapped floor
    self.addLink(s3, s4, port1=11, port2=5) #Core Swithc -- Data center switch


def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
