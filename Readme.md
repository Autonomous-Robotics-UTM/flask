# Racecar Flask Server

Uses Dash for graphing and Flask for hosting the server

## Graphing

The server is capable of:

* Plotting a live graph of the car's joystick controls over time while it is running with the ability to:
    * Reset the graph but keep data intact as it plots
    * See the last n values on the graph for clearer data
    * Upload csv files onto the live graph for comparison
    * Pause the live graph as its graphing to look at any data
* Saves that graph as a csv in a folder called csv
* Second graph available for looking at any of the past live graphs that have happened
    * Graphs are labeled by the time they were plotted
    

## Console

Terminal code repurposed from https://github.com/ethanhuang0526/javascript-iframe-demo maintained by Open Exchange Rates.

The console is capable of:

* Sending commands to the server's system and getting the stdout back
    * Used to run racecar commands and launch necessary ROS files while not needing to be on the system itself

