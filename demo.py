#!/usr/bin/env python3
"""
Démonstration de l'interface web de simulation de parking
"""

import webbrowser
import time
import os
from threading import Timer

def open_browser():
    """Ouvre le navigateur web"""
    print("Ouverture du navigateur...")
    webbrowser.open('http://localhost:5000')

def main():
    print("=" * 60)
    print("    SIMULATEUR D'OPTIMISATION DE PARKING")
    print("    Interface Web Interactive")
    print("=" * 60)
    print()
    print("Cette application compare deux algorithmes:")
    print("  1. Algorithme OPTIMISE - Utilise des preferences et cache")
    print("  2. Algorithme NAIF - Attribution par distance minimale")
    print()
    print("Fonctionnalites:")
    print("  - Visualisation en temps reel")
    print("  - Graphiques comparatifs")
    print("  - Metriques de performance")
    print("  - Interface moderne et responsive")
    print()
    print("=" * 60)
    print()
    
    try:
        from app_web import app
        
        print("Demarrage du serveur web...")
        print("URL: http://localhost:5000")
        print()
        print("Le navigateur s'ouvrira automatiquement dans 3 secondes...")
        print("Appuyez sur Ctrl+C pour arreter le serveur")
        print()
        print("-" * 60)
        
        # Programmer l'ouverture du navigateur
        Timer(3.0, open_browser).start()
        
        # Démarrer l'application
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\nArret du serveur...")
    except Exception as e:
        print(f"Erreur: {e}")
        print("Assurez-vous que toutes les dependances sont installees:")
        print("  pip install flask numpy matplotlib")

if __name__ == "__main__":
    main()
