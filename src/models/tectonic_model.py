import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import cartopy.crs as ccrs

def calculate_stress_distribution(plate_velocity, crustal_thickness, elastic_thickness, poissons_ratio=0.25):
    """
    Calculate tectonic stress distribution on oceanic plates.
    
    Parameters:
    plate_velocity (float): Velocity of tectonic plate in cm/year
    crustal_thickness (float): Thickness of oceanic crust in km
    elastic_thickness (float): Elastic thickness of lithosphere in km
    poissons_ratio (float): Poisson's ratio for crustal material
    
    Returns:
    dict: Stress distribution parameters
    """
    # Convert units
    velocity_m_s = plate_velocity * 1e-2 / 365.25 / 24 / 3600  # cm/s to m/s
    
    # Calculate stress using elastic theory
    stress = (velocity_m_s * crustal_thickness * 1000) / (elastic_thickness * 1000)
    
    # Calculate strain rate
    strain_rate = velocity_m_s / (elastic_thickness * 1000)
    
    # Calculate stress components
    sigma_x = stress * (1 - poissons_ratio)
    sigma_y = stress * (1 - poissons_ratio)
    tau_xy = stress * poissons_ratio
    
    return {
        'maximum_stress': stress,
        'strain_rate': strain_rate,
        'normal_stress_x': sigma_x,
        'normal_stress_y': sigma_y,
        'shear_stress': tau_xy
    }

def simulate_canyon_formation(stress_field, seismic_activity, time_steps=100):
    """
    Simulate canyon formation based on tectonic stress and seismic activity.
    
    Parameters:
    stress_field (dict): Output from calculate_stress_distribution
    seismic_activity (array): Seismic activity data over time
    time_steps (int): Number of time steps for simulation
    
    Returns:
    dict: Canyon formation simulation results
    """
    # Extract stress parameters
    max_stress = stress_field['maximum_stress']
    strain_rate = stress_field['strain_rate']
    
    # Normalize seismic activity
    seismic_normalized = (seismic_activity - np.min(seismic_activity)) / (np.max(seismic_activity) - np.min(seismic_activity))
    
    # Simulate canyon formation probability
    formation_probability = (
        (max_stress / np.max([max_stress, 1e-10])) * 
        (seismic_normalized + 0.1) * 
        (strain_rate / np.max([strain_rate, 1e-15]))
    )
    
    # Apply random variation
    np.random.seed(42)
    noise = np.random.normal(0, 0.1, time_steps)
    formation_probability = np.clip(formation_probability + noise, 0, 1)
    
    # Calculate canyon depth over time
    canyon_depth = np.zeros(time_steps)
    for i in range(1, time_steps):
        # Simplified diffusion model for canyon growth
        canyon_depth[i] = canyon_depth[i-1] + (
            formation_probability[i] * 
            (1 - canyon_depth[i-1]/1000) * 
            0.1  # Growth factor
        )
        canyon_depth[i] = min(canyon_depth[i], 1000)  # Max depth limit
    
    # Create simulation results
    simulation_results = {
        'time_steps': np.arange(time_steps),
        'formation_probability': formation_probability,
        'canyon_depth': canyon_depth,
        'peak_formation_probability': np.max(formation_probability),
        'final_depth': canyon_depth[-1]
    }
    
    return simulation_results