import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import plotly.graph_objects as go
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class CanyonSimulator:
    """Simulates the formation of underwater canyons based on tectonic forces."""
    
    def __init__(self, plate_thickness=50, shear_modulus=30e9, poissons_ratio=0.25):
        self.plate_thickness = plate_thickness
        self.shear_modulus = shear_modulus
        self.poissons_ratio = poissons_ratio
        
    def calculate_stress_distribution(self, x, y, stress_magnitude=100e6):
        """Calculate stress distribution across a plate."""
        # Simplified stress field model
        stress_field = stress_magnitude * np.exp(-((x - np.mean(x))**2 + (y - np.mean(y))**2) / (2 * 1000000))
        return stress_field
    
    def simulate_canyon_formation(self, stress_field, threshold=50e6):
        """Simulate canyon formation based on stress thresholds."""
        canyons = stress_field > threshold
        return canyons.astype(int)
    
    def generate_canyon_probability_map(self, stress_field, seismic_activity):
        """Generate probability map for canyon formation."""
        probability = (stress_field / np.max(stress_field)) * seismic_activity
        return probability

class SeismicAnalyzer:
    """Analyzes seismic data to predict canyon formation patterns."""
    
    def __init__(self):
        self.seismic_data = None
        
    def load_seismic_data(self, data_source):
        """Load seismic data from various sources."""
        if isinstance(data_source, str):
            # Assume CSV file with columns: 'latitude', 'longitude', 'magnitude', 'depth'
            self.seismic_data = pd.read_csv(data_source)
        elif isinstance(data_source, pd.DataFrame):
            self.seismic_data = data_source
        else:
            raise ValueError("Data source must be a file path or DataFrame")
            
    def analyze_seismic_patterns(self):
        """Analyze seismic activity patterns."""
        if self.seismic_data is None:
            raise ValueError("No seismic data loaded")
            
        # Basic statistics
        stats_dict = {
            'mean_magnitude': self.seismic_data['magnitude'].mean(),
            'max_magnitude': self.seismic_data['magnitude'].max(),
            'total_events': len(self.seismic_data),
            'depth_range': self.seismic_data['depth'].max() - self.seismic_data['depth'].min()
        }
        
        # Correlation between magnitude and depth
        correlation = self.seismic_data['magnitude'].corr(self.seismic_data['depth'])
        stats_dict['magnitude_depth_correlation'] = correlation
        
        return stats_dict
    
    def predict_canyon_likelihood(self, stress_field, seismic_activity):
        """Predict likelihood of canyon formation using seismic data."""
        # Simple linear relationship model
        likelihood = stress_field * seismic_activity
        return likelihood / np.max(likelihood)

class ReportGenerator:
    """Generates comprehensive reports on seafloor analysis results."""
    
    def __init__(self):
        self.analysis_results = {}
        
    def add_analysis_result(self, name, result):
        """Add analysis result to report."""
        self.analysis_results[name] = result
        
    def generate_summary_report(self):
        """Generate a summary report of all analyses."""
        report = "Seafloor Canyon Analysis Report\n"
        report += "=" * 40 + "\n\n"
        
        for key, value in self.analysis_results.items():
            report += f"{key}:\n"
            if isinstance(value, dict):
                for k, v in value.items():
                    report += f"  {k}: {v}\n"
            else:
                report += f"  {value}\n"
            report += "\n"
            
        return report
    
    def save_report(self, filename):
        """Save report to file."""
        with open(filename, 'w') as f:
            f.write(self.generate_summary_report())

class TopographyVisualizer:
    """Visualizes underwater topography data."""
    
    def __init__(self):
        self.topography_data = None
        
    def load_topography_data(self, data_source):
        """Load topography data."""
        if isinstance(data_source, str):
            # Assume NetCDF or similar format
            # For simplicity, we'll create sample data
            self.topography_data = self._create_sample_topography()
        elif isinstance(data_source, np.ndarray):
            self.topography_data = data_source
        else:
            raise ValueError("Data source must be a file path or NumPy array")
            
    def _create_sample_topography(self):
        """Create sample topography data for demonstration."""
        x = np.linspace(-100, 100, 100)
        y = np.linspace(-100, 100, 100)
        X, Y = np.meshgrid(x, y)
        # Simulated seafloor topography with a canyon
        Z = -1000 * np.exp(-((X-20)**2 + (Y-30)**2)/2000) - 500 * np.exp(-((X+30)**2 + (Y+20)**2)/1500)
        return Z
        
    def plot_topography_2d(self, figsize=(10, 8)):
        """Plot 2D topography visualization."""
        if self.topography_data is None:
            raise ValueError("No topography data loaded")
            
        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(self.topography_data, extent=[-100, 100, -100, 100], 
                       cmap='terrain', origin='lower')
        ax.set_title('Underwater Topography')
        ax.set_xlabel('Longitude (km)')
        ax.set_ylabel('Latitude (km)')
        plt.colorbar(im, label='Depth (m)')
        return fig, ax
        
    def plot_topography_3d(self):
        """Plot 3D topography visualization using Plotly."""
        if self.topography_data is None:
            raise ValueError("No topography data loaded")
            
        x = np.linspace(-100, 100, self.topography_data.shape[1])
        y = np.linspace(-100, 100, self.topography_data.shape[0])
        X, Y = np.meshgrid(x, y)
        
        fig = go.Figure(data=[go.Surface(z=self.topography_data, x=X, y=Y)])
        fig.update_layout(title='3D Underwater Topography',
                         scene=dict(xaxis_title='Longitude (km)',
                                   yaxis_title='Latitude (km)',
                                   zaxis_title='Depth (m)'))
        return fig
        
    def plot_with_cartopy(self, projection=ccrs.PlateCarree()):
        """Plot topography using Cartopy for geographic context."""
        if self.topography_data is None:
            raise ValueError("No topography data loaded")
            
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(1, 1, 1, projection=projection)
        
        # Add coastlines and boundaries
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        
        # Create meshgrid for plotting
        lons = np.linspace(-180, 180, self.topography_data.shape[1])
        lats = np.linspace(-90, 90, self.topography_data.shape[0])
        LON, LAT = np.meshgrid(lons, lats)
        
        # Plot topography
        contour_levels = np.arange(-5000, 0, 500)
        contours = ax.contour(LON, LAT, self.topography_data, levels=contour_levels,
                             colors='black', linewidths=0.5, alpha=0.7)
        ax.contourf(LON, LAT, self.topography_data, levels=contour_levels, 
                   cmap='Blues_r', transform=ccrs.PlateCarree())
        
        ax.set_title('Underwater Topography Map')
        return fig, ax