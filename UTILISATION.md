# Guide d'Utilisation - Simulateur d'Optimisation de Parking

## Démarrage Rapide

### 1. Installation des dépendances
```bash
pip install flask numpy matplotlib
```

### 2. Lancement de l'application
```bash
python demo.py
```
ou
```bash
python start_app.py
```

### 3. Accès à l'interface
- L'application s'ouvre automatiquement dans votre navigateur
- URL: http://localhost:5000

## Utilisation de l'Interface

### Panneau de Contrôle (Gauche)

#### Informations du Réseau
- **Nœuds**: Nombre d'intersections dans le réseau routier (19)
- **Arêtes**: Nombre de routes connectant les intersections
- **Destinations**: Lieux d'intérêt disponibles (5)
- **Matrice**: Taille de la matrice de distances

#### Paramètres de Simulation
- **Nombre d'itérations**: Combien de cycles de simulation (1-50)
- **Algorithme**: Choisir la comparaison à effectuer
  - "Optimisé vs Naïf" (recommandé)
  - "Optimisé seulement"
  - "Naïf seulement"

### Panneau de Résultats (Droite)

#### Métriques de Performance
- **Regret Moyen (Optimisé)**: Performance de l'algorithme intelligent
- **Regret Moyen (Naïf)**: Performance de l'algorithme de base
- **Amélioration (%)**: Pourcentage d'amélioration de l'algorithme optimisé
- **Total Voitures**: Nombre maximum de voitures simulées

#### Graphiques
1. **Évolution du Regret**: Compare les deux algorithmes dans le temps
2. **Regret Total**: Regret cumulé sur toute la simulation
3. **Nombre de Voitures**: Évolution du trafic

## Interprétation des Résultats

### Le Regret
- **Définition**: Mesure de satisfaction des préférences des conducteurs
- **Plus bas = Meilleur**: Un regret faible indique une meilleure attribution
- **Calcul**: Basé sur la différence entre la place souhaitée et obtenue

### Comparaison des Algorithmes

#### Algorithme Optimisé
- Utilise les préférences des conducteurs et des places
- Cache les distances pour améliorer les performances
- Algorithme de mariage stable pour l'attribution
- Prend en compte la pollution (Crit'Air)

#### Algorithme Naïf
- Attribution basée uniquement sur la distance minimale
- Pas d'optimisation des préférences
- Sert de référence pour mesurer l'amélioration

### Facteurs Influençant les Résultats
- **Type de conducteur**: Résident, pendulaire, touriste
- **Heure de la journée**: Influence les préférences temporelles
- **Pollution du véhicule**: Critère Crit'Air
- **Distance aux destinations**: Proximité des lieux d'intérêt

## Conseils d'Utilisation

### Pour de Meilleurs Résultats
1. **Commencez avec 10 itérations** pour un aperçu rapide
2. **Augmentez à 20-30 itérations** pour des résultats plus stables
3. **Évitez plus de 50 itérations** (temps de calcul long)

### Analyse des Graphiques
- **Tendances**: Observez l'évolution dans le temps
- **Écarts**: Plus l'écart est grand, plus l'optimisation est efficace
- **Stabilité**: Des courbes lisses indiquent un algorithme stable

### Dépannage

#### L'application ne démarre pas
- Vérifiez que Python est installé
- Installez les dépendances: `pip install flask numpy matplotlib`
- Vérifiez que le port 5000 n'est pas utilisé

#### Erreurs de simulation
- Réduisez le nombre d'itérations
- Redémarrez l'application
- Vérifiez les logs dans la console

#### Graphiques ne s'affichent pas
- Actualisez la page
- Vérifiez la connexion internet (pour les polices)
- Essayez un autre navigateur

## Personnalisation

### Modifier le Réseau
Éditez le fichier `park_opt.py`:
- Matrice `L`: Distances entre intersections
- `places_to_go`: Destinations disponibles

### Ajuster les Paramètres
- Nombre de voitures par cycle
- Types de conducteurs
- Critères de pollution
- Fonctions temporelles

## Support Technique

En cas de problème:
1. Consultez les logs dans la console
2. Vérifiez que toutes les dépendances sont installées
3. Redémarrez l'application
4. Contactez le support si nécessaire
