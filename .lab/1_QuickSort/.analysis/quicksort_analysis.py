#!/usr/bin/env python3
"""
QuickSort Performance Analysis Script

This script analyzes the performance of the quicksort.cpp implementation
by running it with different input sizes and measuring execution time.
It generates a comprehensive graph showing time complexity.
"""

import subprocess
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

class QuickSortAnalyzer:
    def __init__(self, executable_path="../quicksort.out"):
        self.executable_path = executable_path
        self.results = []
        
    def generate_test_data(self, size):
        """Generate random test data of specified size"""
        return [random.randint(1, 10000) for _ in range(size)]
    
    def run_quicksort(self, data):
        """Run the quicksort executable with given data and measure time"""
        try:
            # Prepare input string
            input_str = f"{len(data)}\n" + " ".join(map(str, data)) + "\n"
            
            # Measure execution time
            start_time = time.perf_counter()
            
            # Run the executable
            process = subprocess.run(
                [self.executable_path],
                input=input_str,
                text=True,
                capture_output=True,
                timeout=30  # 30 second timeout
            )
            
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            if process.returncode != 0:
                print(f"Error running executable: {process.stderr}")
                return None
                
            return execution_time
            
        except subprocess.TimeoutExpired:
            print(f"Timeout for size {len(data)}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def analyze_performance(self, sizes, trials=3):
        """Analyze performance for different input sizes"""
        print(f"Analyzing QuickSort performance with random data...")
        print(f"Testing sizes: {sizes}")
        print(f"Trials per size: {trials}")
        print("-" * 50)
        
        results = []
        
        for size in sizes:
            print(f"Testing size: {size:>6}", end=" ")
            
            times = []
            for trial in range(trials):
                # Generate fresh data for each trial
                data = self.generate_test_data(size)
                execution_time = self.run_quicksort(data)
                
                if execution_time is not None:
                    times.append(execution_time)
                    print(".", end="", flush=True)
                else:
                    print("X", end="", flush=True)
            
            if times:
                avg_time = np.mean(times)
                std_time = np.std(times) if len(times) > 1 else 0
                results.append({
                    'size': size,
                    'avg_time': avg_time,
                    'std_time': std_time,
                    'min_time': min(times),
                    'max_time': max(times),
                    'trials': len(times)
                })
                print(f" -> {avg_time:.6f}s (±{std_time:.6f}s)")
            else:
                print(" -> FAILED")
        
        return results
    
    def plot_results(self, results, save_path="quicksort_analysis.png"):
        """Plot the performance analysis results"""
        plt.figure(figsize=(12, 8))
        
        if not results:
            print("No results to plot")
            return
            
        sizes = [r['size'] for r in results]
        avg_times = [r['avg_time'] for r in results]
        std_times = [r['std_time'] for r in results]
        
        # Plot with error bars
        plt.errorbar(sizes, avg_times, yerr=std_times, 
                    label="Random Data",
                    color='blue', marker='o', markersize=6,
                    capsize=3, capthick=1, linewidth=2)
        
        plt.xlabel('Input Size (n)', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.title('QuickSort Performance Analysis\nTime Complexity vs Input Size (Random Data)', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Use log scale if needed
        if max(avg_times) > 1:
            plt.yscale('log')
            plt.ylabel('Execution Time (seconds) - Log Scale', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Graph saved as: {save_path}")
    
    def generate_comprehensive_report(self, results):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*60)
        print("QUICKSORT PERFORMANCE ANALYSIS REPORT - RANDOM DATA")
        print("="*60)
        
        if not results:
            print("No results to report")
            return
            
        print(f"\nRANDOM DATA:")
        print("-" * 30)
        print(f"{'Size':>8} {'Avg Time':>12} {'Std Dev':>12} {'Min Time':>12} {'Max Time':>12}")
        print("-" * 68)
        
        for r in results:
            print(f"{r['size']:>8} {r['avg_time']:>12.6f} {r['std_time']:>12.6f} "
                  f"{r['min_time']:>12.6f} {r['max_time']:>12.6f}")
        
        # Calculate growth rate
        if len(results) >= 2:
            first_result = results[0]
            last_result = results[-1]
            size_ratio = last_result['size'] / first_result['size']
            time_ratio = last_result['avg_time'] / first_result['avg_time']
            
            print(f"\nGrowth Analysis:")
            print(f"Size increased by factor: {size_ratio:.2f}")
            print(f"Time increased by factor: {time_ratio:.2f}")
            
            # Estimate complexity (rough approximation)
            if size_ratio > 1:
                complexity_factor = np.log(time_ratio) / np.log(size_ratio)
                print(f"Estimated complexity: O(n^{complexity_factor:.2f})")

def main():
    # Check if executable exists
    executable_path = "../quicksort.out"
    if not os.path.exists(executable_path):
        print(f"Error: Executable not found at {executable_path}")
        print("Please compile quicksort.cpp first:")
        print("g++ -std=c++17 -O2 -Wall quicksort.cpp -o quicksort.out")
        return
    
    analyzer = QuickSortAnalyzer(executable_path)
    
    # Define test sizes - comprehensive range for detailed analysis
    small_sizes = list(range(10, 101, 10))           # 10, 20, ..., 100
    medium_sizes = list(range(200, 1001, 100))       # 200, 300, ..., 1000
    large_sizes = list(range(2000, 10001, 1000))     # 2000, 3000, ..., 10000
    extra_large_sizes = list(range(15000, 50001, 5000))  # 15000, 20000, ..., 50000
    
    # Combine all sizes
    all_sizes = small_sizes + medium_sizes + large_sizes + extra_large_sizes
    
    # Test different data types
    data_types = ["random", "sorted", "reverse", "duplicate"]
    
    all_results = {}
    
    for data_type in data_types:
        print(f"\n{'='*50}")
        print(f"Testing with {data_type.upper()} data")
        print('='*50)
        
        results = analyzer.analyze_performance(all_sizes, data_type, trials=3)
        all_results[data_type] = results
        
        if not results:
            print(f"No results obtained for {data_type} data")
    
    # Generate plots and report
    if any(all_results.values()):
        analyzer.plot_results(all_results, "quicksort_comprehensive_analysis.png")
        analyzer.generate_comprehensive_report(all_results)
        
        # Additional plot for just random data with more detail
        if all_results.get("random"):
            plt.figure(figsize=(10, 6))
            results = all_results["random"]
            sizes = [r['size'] for r in results]
            times = [r['avg_time'] for r in results]
            stds = [r['std_time'] for r in results]
            
            plt.errorbar(sizes, times, yerr=stds, marker='o', capsize=3)
            plt.xlabel('Input Size (n)')
            plt.ylabel('Execution Time (seconds)')
            plt.title('QuickSort Performance - Random Data\nDetailed Analysis')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig("quicksort_random_detailed.png", dpi=300, bbox_inches='tight')
            plt.show()
    else:
        print("No successful test results obtained!")

if __name__ == "__main__":
    main()
