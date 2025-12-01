#!/usr/bin/env python3
"""
Diagnostic script to check model file status and provide helpful information.
"""
import os
import sys

def check_model():
    """Check if model file exists and provide diagnostic information."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(app_dir, "Final_Model.h5")
    
    print("=" * 60)
    print("Model File Diagnostic Check")
    print("=" * 60)
    print(f"Application directory: {app_dir}")
    print(f"Expected model path: {model_path}")
    print(f"Model file exists: {os.path.exists(model_path)}")
    print()
    
    if os.path.exists(model_path):
        file_size = os.path.getsize(model_path)
        print(f"✓ Model file found!")
        print(f"  File size: {file_size / (1024*1024):.2f} MB")
        print()
        print("The model file is present. If you're still seeing errors,")
        print("check the server logs for TensorFlow loading issues.")
    else:
        print("✗ Model file NOT found!")
        print()
        print("The model file 'Final_Model.h5' is missing.")
        print()
        print("Next steps:")
        print("1. Locate your trained model file (Final_Model.h5)")
        print("2. Copy it to this directory:")
        print(f"   {app_dir}")
        print()
        print("3. If you need to train the model, you'll need:")
        print("   - Training dataset")
        print("   - Training script")
        print("   - TensorFlow/Keras installed")
        print()
        print("4. If deploying, make sure to include the model file:")
        print("   - Remove *.h5 from .gitignore, OR")
        print("   - Use: git add -f Final_Model.h5")
        print()
        
        # Check for similar files
        print("Checking for similar files...")
        all_files = os.listdir(app_dir)
        h5_files = [f for f in all_files if f.endswith('.h5') or f.endswith('.hdf5')]
        if h5_files:
            print(f"Found similar files: {', '.join(h5_files)}")
            print("You might want to rename one of these to Final_Model.h5")
        else:
            print("No .h5 or .hdf5 files found in the directory.")
    
    print("=" * 60)

if __name__ == "__main__":
    check_model()

