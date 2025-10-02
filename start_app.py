#!/usr/bin/env python3
"""
Script de démarrage pour l'application web de simulation de parking
"""

import sys
import os
import webbrowser
import time
from threading import Timer

def open_browser():
    """Ouvre le navigateur après un délai"""
    webbrowser.open('http://localhost:5000')

if __name__ == "__main__":
    print("🚗 Démarrage du Simulateur d'Optimisation de Parking")
    print("=" * 50)
    
    try:
        # Importer l'application
        from app_web import app
        
        print("✅ Application chargée avec succès")
        print("🌐 Serveur disponible sur: http://localhost:5000")
        print("📊 Interface web prête pour la simulation")
        print("\n💡 Appuyez sur Ctrl+C pour arrêter le serveur")
        print("-" * 50)
        
        # Ouvrir le navigateur après 2 secondes
        Timer(2.0, open_browser).start()
        
        # Démarrer l'application Flask
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("💡 Assurez-vous que toutes les dépendances sont installées:")
        print("   pip install flask numpy matplotlib")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        sys.exit(1)
