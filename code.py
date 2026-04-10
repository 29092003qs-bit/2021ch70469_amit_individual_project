import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class SandpileModel:
    def __init__(self, size=50, connectivity=4):
        self.size = size
        self.connectivity = connectivity
        # Set stability threshold based on connectivity (4 or 8)
        self.threshold = connectivity 
        self.grid = np.zeros((size, size), dtype=int)
        self.avalanche_sizes = []

    def add_grain(self, x=None, y=None):
        if x is None or y is None:
            x, y = np.random.randint(0, self.size, 2)
        self.grid[x, y] += 1
        
        if self.grid[x, y] >= self.threshold:
            size = self.topple()
            if size > 0:
                self.avalanche_sizes.append(size)
            return size
        return 0

    def topple(self):
        size = 0
        
        # Define neighbor coordinates based on chosen connectivity
        if self.connectivity == 4:
            neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)] # von Neumann
        else:
            neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] # Moore

        while np.any(self.grid >= self.threshold):
            toppling_sites = np.argwhere(self.grid >= self.threshold)
            size += len(toppling_sites)
            
            new_grid = self.grid.copy()
            for x, y in toppling_sites:
                new_grid[x, y] -= self.threshold
                # Distribute to neighbors (grains fall off the edge if out of bounds)
                for dx, dy in neighbors:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        new_grid[nx, ny] += 1
            self.grid = new_grid
        return size

    def run(self, steps=10000, burn_in=5000):
        print(f"[{self.connectivity}-Conn] Running burn-in for {burn_in} steps to reach critical state...")
        for _ in range(burn_in):
            self.add_grain()
            
        # Reset lists to only capture steady-state avalanches AFTER burn-in
        self.avalanche_sizes = []

        print(f"[{self.connectivity}-Conn] Running main simulation for {steps} steps...")
        for i in range(steps):
            self.add_grain()
            if (i + 1) % 5000 == 0:
                print(f"Step {i + 1}/{steps} completed.")

def run_and_plot_both():
    # Parameters matching the LaTeX report
    grid_size = 50
    main_steps = 20000
    burn_in_steps = 5000

    # 1. Run 4-neighbor model
    model4 = SandpileModel(size=grid_size, connectivity=4)
    model4.run(steps=main_steps, burn_in=burn_in_steps)

    # 2. Run 8-neighbor model
    model8 = SandpileModel(size=grid_size, connectivity=8)
    model8.run(steps=main_steps, burn_in=burn_in_steps)

    # 3. Plotting Results
    plt.figure(figsize=(15, 5))
    
    # Graph A: Power-Law Distribution (Comparing both)
    plt.subplot(1, 3, 1)
    for model, color, label in [(model4, 'b', 'Conn=4 (von Neumann)'), (model8, 'r', 'Conn=8 (Moore)')]:
        if model.avalanche_sizes:
            counts = Counter(model.avalanche_sizes)
            sizes = sorted(counts.keys())
            freqs = [counts[s] for s in sizes]
            plt.loglog(sizes, freqs, marker='o', linestyle='', color=color, markersize=4, alpha=0.6, label=label)
            
    plt.title("Avalanche Size Distribution")
    plt.xlabel("Avalanche Size (S)")
    plt.ylabel("Frequency P(S)")
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.legend()

    # Graph B: Final Grid (4-conn)
    plt.subplot(1, 3, 2)
    plt.imshow(model4.grid, cmap='YlOrRd', interpolation='nearest')
    plt.colorbar(label='Grains')
    plt.title(f"Final Grid (4-Neighbors)")

    # Graph C: Final Grid (8-conn)
    plt.subplot(1, 3, 3)
    plt.imshow(model8.grid, cmap='YlOrRd', interpolation='nearest')
    plt.colorbar(label='Grains')
    plt.title(f"Final Grid (8-Neighbors)")
    
    plt.tight_layout()
    plt.savefig("sandpile_results.png", dpi=300)
    print("Results successfully saved to sandpile_results.png!")

if __name__ == "__main__":
    run_and_plot_both()
