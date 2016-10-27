 #!/bin/bash
xterm -e "bash -c \"python Lsr.py G 2000 test/TopologyCase/configG.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py H 2001 test/TopologyCase/configH.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py I 2002 test/TopologyCase/configI.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py J 2003 test/TopologyCase/configJ.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py K 2004 test/TopologyCase/configK.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py L 2005 test/TopologyCase/configL.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py M 2006 test/TopologyCase/configM.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py N 2007 test/TopologyCase/configN.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py O 2008 test/TopologyCase/configO.txt; exec bash\"" &
xterm -e "bash -c \"python Lsr.py P 2009 test/TopologyCase/configP.txt; exec bash\"" &
