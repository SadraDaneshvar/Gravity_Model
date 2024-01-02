<span style="font-family:Times New Roman; font-size:14pt;">
<h1 align="center"><b>Gravity Model Python Implementation: Predictive Transportation Planning</b></h2>
</span>

<span style="font-family: Times New Roman; font-size: 13pt;">
The Gravity Model, crafted by Casey in 1955, stands as the leading method among synthetic distribution models in transportation planning. It mirrors the concept of gravity in physics, where the flow of trips to and from zones is influenced by their activity level (akin to mass) and the distance between them (reflecting travel costs). This approach is particularly valuable as it can generate Origin-Destination matrices without needing prior data. Simple yet powerful, the Gravity Model is vital for analyzing and shaping transportation networks, especially useful in situations where historical travel data isn't available.
</span>

## Overview of the Method

The Furness method offers an algorithmic approach to address the intricacies of the doubly constrained growth-factor problem in transportation planning. The predicted number of trips from zone $i$ to zone $j$, denoted as $T_{ij}$, is given by the formula:

$$ T_{ij} = \alpha \times \frac{P_i \times P_j}{d_{ij}^2} \quad \text{(Similar to the gravitational force formula: } F = G \times \frac{m1 \times m2}{r^2}\text{)} $$

Here, $\alpha$ is a proportionality factor, also known as the calibration parameter. $P_i$ and $P_j$ represent the populations of the origin and destination towns, respectively, while $d_{ij}$ is the distance between these zones. This formula draws a parallel to the gravitational force equation in physics, where the attraction between two objects is proportional to their masses and inversely proportional to the square of the distance between them.

However, the Gravity Model is refined to better reflect urban planning realities. It considers that the number of trips between an origin and a destination zone is influenced by the production capacity of the origin zone, the attractiveness of the destination zone, and the travel costs between them. These factors serve as ideal replacements for the population and distance parameters in the original formula. As a result, the modified formula is presented as follows:

$$ T_{ij} = \rho \times O_i \times D_j \times f(c_{ij}) $$

In this equation, $\rho$ replaces the calibration variable, representing the average trip intensity. $O_i$ is the number of trips originating from zone $i$, indicating its production potential, while $D_j$ is the number of trips destined for zone $j$, reflecting its attraction potential. The function $f(c_{ij})$ represents the accessibility of zone $j$ from $i$, which is a generalized travel cost function. This function, known as the impedance or deterrence function, describes the relative "willingness" to make a trip as a function of travel costs.

Employing principles from physics and adapting them to the nuances of urban travel behavior, the Gravity Model serves as an indispensable tool in predicting and analyzing trip distribution in transportation networks. Its ability to simulate travel patterns in various scenarios, particularly where historical data is lacking, makes it a cornerstone in the field of transportation planning.
