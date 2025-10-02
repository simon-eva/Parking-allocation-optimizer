# Parking-allocation-optimizer
This project provides a simulation framework for optimizing the allocation of cars to parking spots using an adapted version of the Gale–Shapley stable matching algorithm.
It evaluates and compares two strategies:
- Naive assignment: cars are assigned to the nearest available spot.
- Optimized assignment: stable matching with distance caching and multi-criteria preferences.

# Key features
- Stable matching algorithm adapted to urban parking.
- Multi-criteria preferences: distance, driver type (resident, commuter, tourist), pollution class (Crit’Air), parking duration.
- Parking spot preferences: accessibility, flow, environmental considerations.
- Distance caching (Dijkstra-based) for faster calculations.
- Performance analysis: runtime comparison between naive and optimized approaches.
- Regret metrics: measures satisfaction for cars, spots, and the system.
- Visualization: plots of regret evolution over time.

# How it works
- The city is modeled as a weighted graph.
- Cars are generated with specific attributes (start, destination, type, pollution class, duration).
- Cars and parking spots build preference lists based on multiple factors.
- At each time step (10 minutes), cars enter the system and are matched to available spots.
- Both naive and optimized approaches are executed, and results are compared.

# Results
- The optimized algorithm significantly reduces total regret.
- Distance caching improves runtime performance.
- Generated plots illustrate how regret evolves for both methods.

# Getting started
- Requirements:
    Python 3.8+
    Install dependencies:
  ```bash
  pip install numpy matplotlib
  ```

  # Run the simulation
  ```bash
  python parking_optimisation.py
  ```
  This will:
    - Run both naive and optimized algorithms
    - Compare runtime and regret
    - Display performance plots
 
  # Reference
Gale, D. & Shapley, L.S. (1962). College Admissions and the Stability of Marriage.
