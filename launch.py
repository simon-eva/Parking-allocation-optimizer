#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur simple pour l'application de simulation de parking
"""

import sys
import os
import webbrowser
import time
from threading import Timer

def open_browser():
    """Ouvre le navigateur après un délai"""
    try:
        webbrowser.open('http://localhost:5000')
        print("Navigateur ouvert sur http://localhost:5000")
    except Exception as e:
        print(f"Impossible d'ouvrir le navigateur: {e}")
        print("Ouvrez manuellement: http://localhost:5000")

def main():
    print("=" * 60)
    print("    SIMULATEUR D'OPTIMISATION DE PARKING")
    print("    Interface Web Interactive")
    print("=" * 60)
    print()
    print("Fonctionnalites:")
    print("  - Comparaison algorithme optimise vs naif")
    print("  - Visualisation graphique en temps reel")
    print("  - Interface web moderne")
    print("  - Metriques de performance detaillees")
    print()
    print("Demarrage en cours...")
    print()
    
    try:
        # Import de l'application
        from app_web import app
        
        print("Serveur demarre avec succes!")
        print("URL: http://localhost:5000")
        print()
        print("Le navigateur va s'ouvrir automatiquement...")
        print("Appuyez sur Ctrl+C pour arreter")
        print("-" * 60)
        
        # Programmer l'ouverture du navigateur
        Timer(2.0, open_browser).start()
        
        # Démarrer l'application Flask
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\nArret du serveur...")
        print("Au revoir!")
        
    except ImportError as e:
        print(f"Erreur d'importation: {e}")
        print("Installez les dependances:")
        print("  pip install flask numpy matplotlib")
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()
