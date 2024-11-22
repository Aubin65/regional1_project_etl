"""
Fichier contenant le DAG de récupération des données
"""

# Import des librairies nécessaires
from airflow.decorators import dag, task  # noqa
import pendulum  # noqa
import pymongo  # noqa
import pandas as pd  # noqa
import os  # noqa
