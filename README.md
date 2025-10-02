# Parking Optimization Simulator

A modern web interface for comparing parking allocation algorithms using real-time visualization and performance metrics.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **Algorithm Comparison**: Side-by-side comparison of optimized vs naive parking allocation
- **Real-time Visualization**: Interactive charts showing performance metrics over time
- **Modern Web Interface**: Responsive design with smooth animations
- **Performance Analytics**: Detailed metrics including regret analysis and improvement percentages
- **Easy Configuration**: Adjustable simulation parameters through web interface

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
``bash
git clone https://github.com/yourusername/parking-optimization-simulator.git
cd parking-optimization-simulator
``

2. **Install dependencies**
``bash
pip install -r requirements.txt
``

3. **Launch the application**
``bash
python launch.py
``

4. **Access the interface**
- The application will automatically open in your browser
- Or manually navigate to http://localhost:5000

## Architecture

### Backend
- **Flask**: Web framework for API endpoints
- **NumPy**: Numerical computations and data processing
- **Matplotlib**: Chart generation and visualization
- **Custom Algorithm**: Optimized parking allocation with preference matching

### Frontend
- **HTML5/CSS3**: Modern responsive interface
- **Vanilla JavaScript**: Interactive functionality
- **Real-time Charts**: Dynamic data visualization
- **Progressive Web App**: Mobile-friendly design

## Algorithm Comparison

### Optimized Algorithm
- **Stable Marriage**: Uses stable marriage algorithm for optimal car-spot matching
- **Preference System**: Considers both driver and parking spot preferences
- **Distance Caching**: Pre-computed distance matrix for performance
- **Pollution Awareness**: Factors in vehicle emission standards (Crit'Air)
- **Time-based Optimization**: Adapts to different user types (residents, commuters, tourists)

### Naive Algorithm
- **Distance-based**: Simple minimum distance allocation
- **No Preferences**: Ignores user and spot preferences
- **Baseline Comparison**: Serves as performance benchmark

## Performance Metrics

- **Regret Score**: Measures satisfaction level of parking assignments
- **Total Regret**: Cumulative regret over simulation period
- **Improvement Percentage**: Quantified benefit of optimization
- **Vehicle Count**: Traffic volume analysis over time

## Configuration

### Simulation Parameters
- **Iterations**: Number of simulation cycles (1-50)
- **Algorithm Mode**: Choose comparison type
- **Network Size**: 19 nodes, 5 destinations
- **Vehicle Types**: Residents, commuters, tourists

### Customization
Edit park_opt.py to modify:
- Road network topology (matrix L)
- Destination points (places_to_go)
- Vehicle generation parameters
- Preference calculation functions

## Usage Examples

### Basic Simulation
1. Set iterations to 10 for quick results
2. Select "Optimized vs Naive" comparison
3. Click "Run Simulation"
4. Analyze the generated charts and metrics

### Advanced Analysis
1. Increase iterations to 30+ for stable results
2. Compare different algorithm modes
3. Export results for further analysis

## Development

### Project Structure
`
parking-optimization-simulator/
app_web.py              # Flask application
park_opt.py             # Core optimization algorithms
launch.py               # Application launcher
templates/
index.html          # Web interface
requirements.txt        # Python dependencies
README.md              # This file
`

### Running Tests
``bash
python simple_test.py
``

### Development Mode
``bash
python app_web.py
``

## ‹ API Endpoints

- GET / - Main web interface
- GET /api/get_network_info - Network topology information
- POST /api/run_simulation - Execute parking simulation


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by urban mobility optimization research
- Built with modern web technologies
- Designed for educational and research purposes

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/parking-optimization-simulator/issues) page
2. Create a new issue with detailed description
3. Include system information and error logs


---
