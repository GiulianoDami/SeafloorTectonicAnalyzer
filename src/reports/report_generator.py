import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy import stats
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import os

class ReportGenerator:
    """
    Generates geological reports based on analysis results
    """
    
    def __init__(self):
        self.report_template = """
GEOLIGICAL ANALYSIS REPORT
=========================

Project: SeafloorTectonicAnalyzer
Generated: {timestamp}
Analysis Type: {analysis_type}

SUMMARY
-------
{summary}

KEY FINDINGS
------------
{key_findings}

DATA SUMMARY
------------
{data_summary}

RECOMMENDATIONS
---------------
{recommendations}

ANALYSIS PARAMETERS
-------------------
{parameters}
"""
    
    def generate_report(self, 
                       analysis_type: str,
                       summary: str,
                       key_findings: List[str],
                       data_summary: str,
                       recommendations: List[str],
                       parameters: Dict,
                       output_path: Optional[str] = None) -> str:
        """
        Generate a formatted geological report
        
        Args:
            analysis_type: Type of analysis performed
            summary: Overall summary of findings
            key_findings: List of important findings
            data_summary: Summary of analyzed data
            recommendations: List of recommendations
            parameters: Dictionary of analysis parameters
            output_path: Optional path to save report
            
        Returns:
            Formatted report string
        """
        # Format key findings
        formatted_findings = "\n".join([f"• {finding}" for finding in key_findings])
        
        # Format recommendations
        formatted_recommendations = "\n".join([f"• {rec}" for rec in recommendations])
        
        # Format parameters
        formatted_parameters = "\n".join([f"{k}: {v}" for k, v in parameters.items()])
        
        # Create report
        report = self.report_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            analysis_type=analysis_type,
            summary=summary,
            key_findings=formatted_findings,
            data_summary=data_summary,
            recommendations=formatted_recommendations,
            parameters=formatted_parameters
        )
        
        # Save if path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report)
                
        return report

def generate_geological_report(analysis_type: str,
                              summary: str,
                              key_findings: List[str],
                              data_summary: str,
                              recommendations: List[str],
                              parameters: Dict,
                              output_path: Optional[str] = None) -> str:
    """
    Convenience function to generate a geological report
    
    Args:
        analysis_type: Type of analysis performed
        summary: Overall summary of findings
        key_findings: List of important findings
        data_summary: Summary of analyzed data
        recommendations: List of recommendations
        parameters: Dictionary of analysis parameters
        output_path: Optional path to save report
        
    Returns:
        Formatted report string
    """
    generator = ReportGenerator()
    return generator.generate_report(
        analysis_type=analysis_type,
        summary=summary,
        key_findings=key_findings,
        data_summary=data_summary,
        recommendations=recommendations,
        parameters=parameters,
        output_path=output_path
    )