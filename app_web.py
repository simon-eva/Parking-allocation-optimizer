from flask import Flask, render_template, jsonify, request
import json
import copy
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from math import *
from collections import defaultdict
from numpy.polynomial import Polynomial
import time

# Import your existing parking optimization code
# We'll import the functions we need directly to avoid conflicts
import park_opt

app = Flask(__name__)

class ParkingSimulator:
    def __init__(self):
        self.L = [[0, 4, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [4, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 1, 0, 2.5, 0, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 2.5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 2, 0, 0, 0, 1, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 1.5, 0, 1, 0, 2, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 1, 0, 2, 0, 3, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], 
                  [2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0.5, 0, 0, 0, 3, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0.5, 0, 0, 0, 1, 0, 2, 0, 0, 0, 2, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 2, 0, 0.5, 0, 0, 0, 2, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 2, 2], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2.5, 0, 1, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0.5, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0.5, 0, 1], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0]]
        
        self.places_to_go = [[3,0.5,6,0.5,3],[6,1.5,7,1.5,2],[12,1,18,1,1],[13,2,14,1.5,3],[0,1,8,1,5]]
        self.init_cache()
        
    def init_cache(self):
        """Initialize distance cache"""
        # Set the global variables in park_opt module
        park_opt.L = self.L
        park_opt.places_to_go = self.places_to_go
        park_opt.init_distance_cache(self.L)
        
    def run_simulation(self, num_iterations=10):
        """Run the parking optimization simulation"""
        try:
            # Set global variables for the imported functions
            park_opt.L = self.L
            park_opt.places_to_go = self.places_to_go
            
            result = park_opt.complete_algo(self.L)
            return {
                'success': True,
                'regret_optimized': result[0],
                'regret_naive': result[1],
                'total_regret_optimized': result[2],
                'total_regret_naive': result[3],
                'place_regret_optimized': result[4],
                'place_regret_naive': result[5],
                'num_cars_optimized': result[6],
                'num_cars_naive': result[7]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_plots(self, data):
        """Generate matplotlib plots and return as base64 encoded images"""
        plots = {}
        
        try:
            t = [10*i for i in range(len(data['regret_optimized']))]
            
            # Plot 1: Regret comparison
            plt.figure(figsize=(10, 6))
            plt.plot(t, data['regret_optimized'], marker='.', color='red', label='Optimisé', linewidth=2)
            plt.plot(t, data['regret_naive'], marker='.', color='blue', label='Naïf', linewidth=2)
            plt.title('Évolution du Regret au fil du temps', fontsize=16, fontweight='bold')
            plt.xlabel('Temps (minutes)', fontsize=12)
            plt.ylabel('Regret', fontsize=12)
            plt.legend(fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Save to base64
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plots['regret'] = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            # Plot 2: Total regret comparison
            plt.figure(figsize=(10, 6))
            plt.plot(t, data['total_regret_optimized'], marker='.', color='red', label='Optimisé', linewidth=2)
            plt.plot(t, data['total_regret_naive'], marker='.', color='blue', label='Naïf', linewidth=2)
            plt.title('Regret Total au fil du temps', fontsize=16, fontweight='bold')
            plt.xlabel('Temps (minutes)', fontsize=12)
            plt.ylabel('Regret Total', fontsize=12)
            plt.legend(fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plots['total_regret'] = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            # Plot 3: Number of cars over time
            plt.figure(figsize=(10, 6))
            plt.plot(t, data['num_cars_optimized'], marker='o', color='green', label='Voitures (Optimisé)', linewidth=2)
            plt.plot(t, data['num_cars_naive'], marker='s', color='orange', label='Voitures (Naïf)', linewidth=2)
            plt.title('Nombre de voitures au fil du temps', fontsize=16, fontweight='bold')
            plt.xlabel('Temps (minutes)', fontsize=12)
            plt.ylabel('Nombre de voitures', fontsize=12)
            plt.legend(fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plots['cars'] = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
        except Exception as e:
            print(f"Error generating plots: {e}")
            
        return plots

# Global simulator instance
simulator = ParkingSimulator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run_simulation', methods=['POST'])
def run_simulation():
    """API endpoint to run the parking simulation"""
    try:
        data = request.get_json()
        iterations = data.get('iterations', 10)
        
        # Run simulation
        result = simulator.run_simulation(iterations)
        
        if result['success']:
            # Generate plots
            plots = simulator.generate_plots(result)
            result['plots'] = plots
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_network_info')
def get_network_info():
    """Get information about the road network"""
    try:
        network_info = {
            'nodes': len(simulator.L),
            'edges': sum(1 for i in range(len(simulator.L)) for j in range(len(simulator.L)) if simulator.L[i][j] > 0) // 2,
            'places_to_go': len(simulator.places_to_go),
            'matrix_size': f"{len(simulator.L)}x{len(simulator.L[0])}"
        }
        return jsonify(network_info)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
