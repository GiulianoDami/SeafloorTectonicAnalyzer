import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple, Dict, Any
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import cartopy.crs as ccrs

class SeismicAnalyzer:
    """
    A class to analyze seismic data for canyon formation risk assessment.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the SeismicAnalyzer with seismic data.
        
        Parameters:
        data (pd.DataFrame): DataFrame containing seismic data with columns:
                            'magnitude', 'depth', 'distance_from_plate_boundary',
                            'stress_tensor_xx', 'stress_tensor_yy', 'stress_tensor_xy'
        """
        self.data = data
        
    def calculate_stress_intensity(self) -> np.ndarray:
        """
        Calculate stress intensity from stress tensor components.
        
        Returns:
        np.ndarray: Array of stress intensities
        """
        stress_xx = self.data['stress_tensor_xx'].values
        stress_yy = self.data['stress_tensor_yy'].values
        stress_xy = self.data['stress_tensor_xy'].values
        
        # Calculate von Mises stress (stress intensity)
        stress_intensity = np.sqrt(0.5 * ((stress_xx - stress_yy)**2 + 
                                          4 * stress_xy**2) + 
                                  (stress_xx + stress_yy)**2 / 4)
        
        return stress_intensity
    
    def assess_seismic_risk(self) -> Dict[str, Any]:
        """
        Assess seismic risk based on multiple parameters.
        
        Returns:
        Dict[str, Any]: Dictionary containing risk assessment results
        """
        # Calculate stress intensity
        stress_intensity = self.calculate_stress_intensity()
        
        # Calculate seismic probability based on magnitude and depth
        magnitude = self.data['magnitude'].values
        depth = self.data['depth'].values
        
        # Normalize magnitude and depth for risk calculation
        normalized_mag = (magnitude - magnitude.min()) / (magnitude.max() - magnitude.min())
        normalized_depth = (depth - depth.min()) / (depth.max() - depth.min())
        
        # Risk score combines stress intensity, magnitude, and depth
        risk_score = (
            0.4 * (stress_intensity - stress_intensity.min()) / 
            (stress_intensity.max() - stress_intensity.min()) +
            0.3 * normalized_mag +
            0.3 * (1 - normalized_depth)
        )
        
        # Categorize risk levels
        risk_levels = []
        for score in risk_score:
            if score >= 0.8:
                risk_levels.append('Very High')
            elif score >= 0.6:
                risk_levels.append('High')
            elif score >= 0.4:
                risk_levels.append('Moderate')
            elif score >= 0.2:
                risk_levels.append('Low')
            else:
                risk_levels.append('Very Low')
                
        return {
            'risk_scores': risk_score,
            'risk_levels': risk_levels,
            'max_stress': stress_intensity.max(),
            'avg_stress': stress_intensity.mean(),
            'stress_std': stress_intensity.std()
        }

def assess_canyon_risk(seismic_data: pd.DataFrame, 
                      threshold: float = 0.6) -> Tuple[np.ndarray, Dict[str, int]]:
    """
    Assess canyon formation risk based on seismic data.
    
    Parameters:
    seismic_data (pd.DataFrame): DataFrame containing seismic data
    threshold (float): Risk threshold for canyon formation (default 0.6)
    
    Returns:
    Tuple[np.ndarray, Dict[str, int]]: Risk predictions and summary statistics
    """
    analyzer = SeismicAnalyzer(seismic_data)
    risk_assessment = analyzer.assess_seismic_risk()
    
    # Predict canyon formation risk (1 = likely, 0 = unlikely)
    predictions = (risk_assessment['risk_scores'] >= threshold).astype(int)
    
    # Count risk levels
    risk_counts = {
        'Very High': sum(1 for x in risk_assessment['risk_levels'] if x == 'Very High'),
        'High': sum(1 for x in risk_assessment['risk_levels'] if x == 'High'),
        'Moderate': sum(1 for x in risk_assessment['risk_levels'] if x == 'Moderate'),
        'Low': sum(1 for x in risk_assessment['risk_levels'] if x == 'Low'),
        'Very Low': sum(1 for x in risk_assessment['risk_levels'] if x == 'Very Low')
    }
    
    return predictions, risk_counts