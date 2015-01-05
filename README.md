Cascades
========

Simulates a cascade model based largely on Krackhardt's model for innovation cascades.

========
GENERAL:
In order to use this software, you will need the numpy, sympy, and wxPython modules.
The program can be launched by calling the main.py file in terminal.

FUNCTION:
This program simulates the diffusion of an innovation or idea across a fragmented population. The population is modeled as a collection of smaller populations, called islands (and represented visually as graph vertices). These islands are assumed to be of approximately the same size. Any pair of islands may or may not interact with each other, but if they do interact, this interaction is relatively weak compared to the interaction within an island. Connections between islands are represented by graph edges, and reflect migration between islands. We assume to begin with a standard rate of migration -- called viscosity -- between any pairs of islands (an improvement on this algorithm would allow for unique rates of migration between each pair of connected islands.

Initially, there is some percentage of the population in each island that adopts innovation x. Note that as individuals migrate between islands, some number of individuals will mate with others previously belonging to another island, which will alter the distribution of adoption of x in the broader population. Furthermore, social forces will encourage individuals within each subgroup to adapt their behavior based upon the percentage of adoption within the island to which they belong. In particular, individuals will periodically search through some number of members of their island in order to seek out like-minded individuals. If they find such a like-minded individual, it is assumed that they will not change their mind about x. However, if an individual finds himself or herself isolated, there is some probability that they will change their mind about x, reflecting the social forces around them. Based on the probability of finding a like-minded individual and the probability of that an isolated individual will change their opinion about the innovation, there will be some new distribution of adoption of the innovation.

The program simulates changes in adoption of an innovation (given a population and a starting state) across the population after rounds of migration and conversion. The details of the equations on which this simulation is done are omitted here, but interested individuals can contact jenna.kainic@yale.edu for more information.

USAGE:
Once the program is launched, you will have to set the parameters before you can run a cascade. Set these values by typing them in to the text boxes and pressing the “set” buttons.
  -Sigma is the probability that an isolated adopter will convert to non-adoption.
  -Tau is the probability that an isolated non-adopter will convert to adoption.
  -La is the number of other people an adopter will search through in the attempt to find a like-minded individual.
  -Ln is the number of other people a non-adopter will search through in the attempt to find a like-minded
  individual.
  -Viscosity is the rate of migration between connected islands.

Note that sigma, tau, and viscosity should be numbers between 0 and 1. Note further that viscosity v must be small enough so that v*(maximum degree) <= 1, where maximum degree is the largest number of islands any one island in the population is adjacent to. La and Ln should be integers. As it is currently coded, the program does not accept zero values for any of these parameters as a precaution against arithmetic errors, though this could be changed if desired. 

Next, draw your population and set initial adoption density values. Create an island by clicking on the main frame in the applet. When you make an island, a small textbox will appear in the upper left hand corner of that frame. You can set the island’s initial density of adopters by typing a value between 0 and 1 into this textbox and pressing return. To add a connection between two islands, click on one of the islands, and then the other. 

“Clear values” will clear all of the density values in the islands, and reset all to zero.

“Clear graph” will clear the entire population structure.

“Advance n generations” will show the new densities after n cycles of migration and conversion have occurred.

Note on using the program: the display window will only show density values up to one decimal point, but the density values up to 4 decimal points are printed in terminal.

AREAS FOR IMPROVEMENT
Note on the code itself: you may notice functions "update info" and "beta crit" that appear to be doing nothing since "update info" simply returns “True” and "beta crit" is never called. The intended purpose of "beta crit" is to calculate stable population densities. The function as it is currently written does this, except that there is currently a problem with solving polynomial systems in sympy. Namely, sympy does not recognize floating point zeros, and as a result will often not be able to solve polynomial systems with coefficients as floating points. One possible solution is to use the flag ‘domain = ‘QQ’ ‘ to set all coefficients and solutions to rational numbers, but testing this solution did not terminate. I have included as comments calls that should be made in order to run beta_crit and display this information in a text box. This way, if this problem is fixed, the user can remove these comments and make the associated calls in their place. It is possible that an alternative solution would be to pipe to a function in MatLab or Mathematica.

