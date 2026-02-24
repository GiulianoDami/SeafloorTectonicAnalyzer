import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
import plotly.graph_objects as go
import plotly.express as px
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class TopographyVisualizer:
    """Handles plotting and visualization of underwater topography and canyon profiles"""
    
    def __init__(self):
        self.fig = None
        self.ax = None
        
    def plot_topography_2d(self, x_coords, y_coords, elevation_data, title="Underwater Topography"):
        """Plot 2D topography map"""
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        contour_plot = self.ax.contourf(x_coords, y_coords, elevation_data, levels=20, cmap='terrain')
        self.ax.set_title(title)
        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('Latitude')
        plt.colorbar(contour_plot, ax=self.ax, label='Elevation (m)')
        plt.tight_layout()
        return self.fig, self.ax
        
    def plot_canyon_cross_section(self, distance, elevation, title="Canyon Cross-Section"):
        """Plot cross-sectional profile of a canyon"""
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.plot(distance, elevation, 'b-', linewidth=2)
        self.ax.fill_between(distance, elevation, alpha=0.3)
        self.ax.set_title(title)
        self.ax.set_xlabel('Distance along canyon (km)')
        self.ax.set_ylabel('Elevation (m)')
        self.ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return self.fig, self.ax

def plot_canyon_profile(distance, elevation, title="Canyon Profile", save_path=None):
    """
    Create a detailed profile plot of an underwater canyon
    
    Parameters:
    distance (array): Distance along canyon
    elevation (array): Elevation data
    title (str): Plot title
    save_path (str): Optional path to save the figure
    
    Returns:
    tuple: (figure, axes)
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot main profile
    ax.plot(distance, elevation, 'k-', linewidth=2, label='Canyon Profile')
    
    # Fill area under curve
    ax.fill_between(distance, elevation, alpha=0.3, color='lightblue')
    
    # Add labels and formatting
    ax.set_xlabel('Distance Along Canyon (km)')
    ax.set_ylabel('Elevation (m)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax

def generate_formation_heatmap(stress_data, probability_data, title="Formation Probability Heatmap"):
    """
    Generate a heatmap showing probability of canyon formation
    
    Parameters:
    stress_data (array): Stress distribution data
    probability_data (array): Formation probability values
    title (str): Heatmap title
    
    Returns:
    plotly.graph_objects.Figure: Interactive heatmap
    """
    # Create DataFrame for easier handling
    df = pd.DataFrame({
        'stress': stress_data.flatten(),
        'probability': probability_data.flatten()
    })
    
    # Create heatmap using Plotly
    fig = px.density_heatmap(
        df,
        x='stress',
        y='probability',
        title=title,
        labels={'x': 'Stress Magnitude (MPa)', 'y': 'Formation Probability'},
        nbinsx=30,
        nbinsy=30
    )
    
    fig.update_layout(
        width=800,
        height=600,
        title_x=0.5
    )
    
    return fig