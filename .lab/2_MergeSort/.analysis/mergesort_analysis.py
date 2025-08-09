#!/usr/bin/env python3
"""
Merge Sort vs Quick Sort Performance Analysis
Compares the running time of Merge Sort and Quick Sort algorithms
on different input sizes and generates CSV and graphical results.
"""

import subprocess
import time
import random
import csv
import matplotlib.pyplot as plt
import math
import os
import sys

class SortingAnalyzer:
    def __init__(self):
        # Use larger minimum input sizes to reduce overhead impact
        self.input_sizes = [10,100, 500, 1000, 5000, 10000]
        self.mergesort_path = "/home/anmol/ds/.lab/2_MergeSort/mergesort.out"
        self.quicksort_path = "/home/anmol/ds/.lab/1_QuickSort/quicksort.out"
        self.results = []
        
    def generate_random_data(self, size):
        """Generate a list of random integers of given size"""
        return [random.randint(1, size * 10) for _ in range(size)]
    
    def measure_execution_time(self, executable_path, data):
        """Measure the execution time of a sorting algorithm with improved accuracy"""
        try:
            # Prepare input data as string
            input_data = f"{len(data)}\n" + " ".join(map(str, data)) + "\n"
            
            # Warm-up run to minimize cold start effects
            subprocess.run(
                [executable_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=10
            )
            
            # Measure multiple runs and take the minimum (best case)
            times = []
            for _ in range(3):  # Take 3 measurements
                start_time = time.perf_counter()
                
                process = subprocess.run(
                    [executable_path],
                    input=input_data,
                    text=True,
                    capture_output=True,
                    timeout=30
                )
                
                end_time = time.perf_counter()
                
                if process.returncode != 0:
                    print(f"Error running {executable_path}: {process.stderr}")
                    return None
                
                times.append((end_time - start_time) * 1000)  # Convert to milliseconds
            
            # Return the minimum time (best performance, least affected by system noise)
            execution_time = min(times)
            return execution_time
            
        except subprocess.TimeoutExpired:
            print(f"Timeout occurred for {executable_path} with input size {len(data)}")
            return None
        except Exception as e:
            print(f"Error measuring execution time: {e}")
            return None
    
    def run_analysis(self):
        """Run the complete analysis for all input sizes"""
        print("Starting Merge Sort vs Quick Sort Performance Analysis...")
        print("Improvements: Larger input sizes, warm-up runs, multiple measurements")
        print("=" * 70)
        
        for size in self.input_sizes:
            print(f"\nTesting with input size: {size:,}")
            
            # Generate multiple test datasets and average the results
            merge_times = []
            quick_times = []
            
            # Use more iterations for better statistical accuracy
            iterations = 7 if size <= 5000 else 5  # More iterations for smaller sizes
            
            for i in range(iterations):
                print(f"  Iteration {i+1}/{iterations}")
                
                # Generate random data (use different seed for each iteration)
                random.seed(42 + i + size)  # Vary the seed
                data = self.generate_random_data(size)
                
                # Measure Merge Sort time
                merge_time = self.measure_execution_time(self.mergesort_path, data.copy())
                if merge_time is not None:
                    merge_times.append(merge_time)
                
                # Measure Quick Sort time
                quick_time = self.measure_execution_time(self.quicksort_path, data.copy())
                if quick_time is not None:
                    quick_times.append(quick_time)
            
            # Calculate statistics (use median for more robust results)
            if merge_times and quick_times:
                # Remove outliers (top and bottom 10%) for cleaner results
                merge_times_clean = sorted(merge_times)[1:-1] if len(merge_times) > 3 else merge_times
                quick_times_clean = sorted(quick_times)[1:-1] if len(quick_times) > 3 else quick_times
                
                avg_merge_time = sum(merge_times_clean) / len(merge_times_clean)
                avg_quick_time = sum(quick_times_clean) / len(quick_times_clean)
                
                # Also calculate median for comparison
                median_merge = sorted(merge_times)[len(merge_times)//2]
                median_quick = sorted(quick_times)[len(quick_times)//2]
            else:
                avg_merge_time = avg_quick_time = 0
                median_merge = median_quick = 0
            
            # Store results
            self.results.append({
                'input_size': size,
                'merge_sort_time_ms': avg_merge_time,
                'quick_sort_time_ms': avg_quick_time,
                'merge_sort_median_ms': median_merge,
                'quick_sort_median_ms': median_quick,
                'iterations': min(len(merge_times), len(quick_times))
            })
            
            print(f"  Average Merge Sort time: {avg_merge_time:.4f} ms (median: {median_merge:.4f})")
            print(f"  Average Quick Sort time: {avg_quick_time:.4f} ms (median: {median_quick:.4f})")
            
            if avg_merge_time > 0 and avg_quick_time > 0:
                ratio = avg_merge_time / avg_quick_time
                faster = "Quick Sort" if ratio > 1 else "Merge Sort"
                print(f"  {faster} is {abs(ratio-1)*100:.1f}% faster")
                
                # Show standard deviation for data quality assessment
                if len(merge_times) > 1:
                    merge_std = (sum((x - avg_merge_time)**2 for x in merge_times) / len(merge_times))**0.5
                    quick_std = (sum((x - avg_quick_time)**2 for x in quick_times) / len(quick_times))**0.5
                    print(f"  Standard deviation - Merge: {merge_std:.4f}ms, Quick: {quick_std:.4f}ms")
    
    def save_to_csv(self, filename="sorting_comparison_improved.csv"):
        """Save results to CSV file"""
        csv_path = os.path.join(os.path.dirname(__file__), filename)
        
        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = ['input_size', 'merge_sort_time_ms', 'quick_sort_time_ms', 
                         'merge_sort_median_ms', 'quick_sort_median_ms', 'iterations']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results[1:]:
                writer.writerow(result)
        
        print(f"\nResults saved to: {csv_path}")
        return csv_path
    
    def generate_graph(self, filename="sorting_comparison_improved.png"):
        """Generate comparison graph with improved visualization"""
        if not self.results:
            print("No results to plot!")
            return
        print(self.results)
        # Prepare data for plotting
        input_sizes = [r['input_size'] for r in self.results[1:]]
        merge_times = [r['merge_sort_time_ms'] for r in self.results[1:]]
        quick_times = [r['quick_sort_time_ms'] for r in self.results[1:]]
        print(input_sizes)
        # Create the plot with better styling
        plt.figure(figsize=(12, 8))
        
        # Plot lines with better styling
        plt.plot(input_sizes, merge_times, 'bo-', label='Merge Sort', 
                linewidth=3, markersize=10, alpha=0.8)
        plt.plot(input_sizes, quick_times, 'ro-', label='Quick Sort', 
                linewidth=3, markersize=10, alpha=0.8)
        
        # Customize the plot
        plt.xlabel('Input Size (number of elements)', fontsize=14)
        plt.ylabel('Execution Time (milliseconds)', fontsize=14)
        plt.title('Merge Sort vs Quick Sort Performance Comparison', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Use linear scale for cleaner visualization
        plt.xscale('linear')
        plt.yscale('linear')
        
        # Add value annotations with better positioning
        for i, (size, merge_time, quick_time) in enumerate(zip(input_sizes, merge_times, quick_times)):
            plt.annotate(f'{merge_time:.3f}ms', 
                        (size, merge_time), 
                        textcoords="offset points", 
                        xytext=(0,15), 
                        ha='center', fontsize=10, 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
            plt.annotate(f'{quick_time:.3f}ms', 
                        (size, quick_time), 
                        textcoords="offset points", 
                        xytext=(0,-20), 
                        ha='center', fontsize=10,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))
        
        plt.tight_layout()
        
        # Save the plot
        graph_path = os.path.join(os.path.dirname(__file__), filename)
        plt.savefig(graph_path, dpi=300, bbox_inches='tight')
        print(f"Graph saved to: {graph_path}")
        
        # Show the plot
        plt.show()
    
    def print_summary(self):
        """Print a summary of the analysis"""
        print("\n" + "="*60)
        print("PERFORMANCE ANALYSIS SUMMARY")
        print("="*60)
        
        for result in self.results:
            size = result['input_size']
            merge_time = result['merge_sort_time_ms']
            quick_time = result['quick_sort_time_ms']
            
            print(f"\nInput Size: {size:,} elements")
            print(f"Merge Sort: {merge_time:.4f} ms")
            print(f"Quick Sort: {quick_time:.4f} ms")
            
            if merge_time > 0 and quick_time > 0:
                if quick_time < merge_time:
                    improvement = ((merge_time - quick_time) / merge_time) * 100
                    print(f"Quick Sort is {improvement:.1f}% faster")
                else:
                    improvement = ((quick_time - merge_time) / quick_time) * 100
                    print(f"Merge Sort is {improvement:.1f}% faster")
        
        print("\nTime Complexity Analysis:")
        print("- Merge Sort: O(n log n) - Guaranteed")
        print("- Quick Sort: O(n log n) average, O(n²) worst case")

def main():
    """Main function to run the analysis"""
    # Check if executables exist
    analyzer = SortingAnalyzer()
    
    if not os.path.exists(analyzer.mergesort_path):
        print(f"Error: Merge sort executable not found at {analyzer.mergesort_path}")
        print("Please compile mergesort.cpp first.")
        return
    
    if not os.path.exists(analyzer.quicksort_path):
        print(f"Error: Quick sort executable not found at {analyzer.quicksort_path}")
        print("Please compile quicksort.cpp first.")
        return
    
    # Set random seed for reproducible results
    random.seed(42)
    
    try:
        # Run the analysis
        analyzer.run_analysis()
        
        # Save results to CSV
        analyzer.save_to_csv()
        
        # Generate graph
        analyzer.generate_graph()
        
        # Print summary
        analyzer.print_summary()
        
        print("\nAnalysis completed successfully!")
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
    except Exception as e:
        print(f"\nError during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
