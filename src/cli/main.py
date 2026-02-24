import argparse
import sys
from typing import List

def main() -> int:
    parser = argparse.ArgumentParser(
        description="SeafloorTectonicAnalyzer - Analyze and visualize underwater canyon formation"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Run tectonic analysis on oceanic plates"
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Generate visualizations of underwater topography"
    )
    parser.add_argument(
        "--predict",
        action="store_true",
        help="Predict potential new canyon formations"
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default="data/",
        help="Path to input data directory (default: data/)"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default="output/",
        help="Path to output directory (default: output/)"
    )
    
    args = parser.parse_args()
    
    # Validate at least one action is specified
    if not any([args.analyze, args.visualize, args.predict]):
        print("Error: At least one action must be specified.")
        print("Use --help for usage information.")
        return 1
    
    # Import project-specific modules
    try:
        from ..analysis.tectonic_model import run_tectonic_analysis
        from ..visualization.topography_visualizer import generate_topography_visualization
        from ..prediction.canyon_predictor import predict_canyon_formations
    except ImportError as e:
        print(f"Import error: {e}")
        return 1
    
    # Execute selected actions
    try:
        if args.analyze:
            print("Running tectonic analysis...")
            run_tectonic_analysis(args.data_path, args.output_path)
        
        if args.visualize:
            print("Generating visualizations...")
            generate_topography_visualization(args.data_path, args.output_path)
        
        if args.predict:
            print("Predicting canyon formations...")
            predict_canyon_formations(args.data_path, args.output_path)
            
    except Exception as e:
        print(f"Error during execution: {e}")
        return 1
    
    print("Analysis complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())