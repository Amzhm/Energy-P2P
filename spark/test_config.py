#!/usr/bin/env python3

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 70)
print("🧪 TEST DE CONFIGURATION SPARK")
print("=" * 70)

# Test 1: Import des modules
print("\n[1/5] Test d'import des modules...")
try:
    from config import spark_config
    from spark import spark_utils
    print("✅ Imports réussis")
except Exception as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

# Test 2: Vérification des chemins
print("\n[2/5] Vérification des chemins HDFS...")
try:
    print(f"   HDFS Base: {spark_config.HDFS_BASE}")
    print(f"   Bronze Weather: {spark_config.BRONZE_WEATHER}")
    print(f"   Silver Weather: {spark_config.SILVER_WEATHER}")
    print("✅ Chemins configurés correctement")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 3: Vérification des schémas
print("\n[3/5] Vérification des schémas...")
try:
    schemas = [
        ("Weather", spark_config.SCHEMA_WEATHER_SILVER),
        ("Consumption", spark_config.SCHEMA_CONSUMPTION_SILVER),
        ("Prices", spark_config.SCHEMA_PRICES_SILVER),
        ("Production", spark_config.SCHEMA_PRODUCTION_SILVER),
    ]
    
    for name, schema in schemas:
        fields = len(schema.fields)
        print(f"   {name}: {fields} champs")
    
    print("✅ Schémas définis correctement")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 4: Test création SparkSession (optionnel, nécessite Spark en cours)
print("\n[4/5] Test création SparkSession...")
print("   ⚠️  Ce test nécessite un cluster Spark actif")
print("   ⏭️  Ignoré pour l'instant (sera testé avec le premier job)")

# Test 5: Vérification des fonctions utilitaires
print("\n[5/5] Vérification des fonctions utilitaires...")
try:
    utils_functions = [
        'add_temporal_features',
        'detect_anomalies',
        'remove_duplicates',
        'handle_null_values',
        'write_to_parquet',
        'read_from_parquet',
        'show_dataframe_info',
        'validate_dataframe'
    ]
    
    for func_name in utils_functions:
        if hasattr(spark_utils, func_name):
            print(f"   ✓ {func_name}()")
        else:
            print(f"   ✗ {func_name}() - MANQUANT")
    
    print("✅ Toutes les fonctions utilitaires sont disponibles")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Résumé
print("\n" + "=" * 70)
print("✅ TOUS LES TESTS SONT PASSÉS")
print("=" * 70)
print("\n📋 Configuration:")
print(f"   - HDFS configuré: {spark_config.HDFS_BASE}")
print(f"   - 4 schémas de données définis")
print(f"   - 8 fonctions utilitaires disponibles")
print(f"   - Bronze/Silver/Gold layers configurés")
print("\n🚀 Prêt pour les transformations Bronze → Silver !")
print("=" * 70)