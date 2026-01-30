import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def load_benchmark_data():
    benchmarks_dir = Path("benchmarks")
    all_data = []

    csv_files = sorted(benchmarks_dir.glob("benchmark_results_*.csv"))

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            all_data.append(df)
            print(f"Loaded {csv_file.name}: {len(df)} graphs with {df['num_nodes'].iloc[0]} nodes")
        except Exception as e:
            print(f"Error loading {csv_file.name}: {e}")

    # combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df

def calculate_statistics(df):
    algorithms = ['brute_force', 'christofides', 'nearest_neighbour', 'genetic', 'ant_colony']

    stats = []

    for num_nodes in sorted(df['num_nodes'].unique()):
        node_data = df[df['num_nodes'] == num_nodes]

        stat_row = {'num_nodes': num_nodes}

        for algo in algorithms:
            time_col = f'{algo}_time'
            weight_col = f'{algo}_weight'

            if time_col in node_data.columns:
                avg_time = node_data[time_col].mean()
                avg_weight = node_data[weight_col].mean()

                stat_row[f'{algo}_avg_time'] = avg_time
                stat_row[f'{algo}_avg_weight'] = avg_weight

        stats.append(stat_row)

    stats_df = pd.DataFrame(stats)
    return stats_df

def calculate_optimality_gap(df):
    small_graphs = df[df['num_nodes'] <= 9]
    algorithms = ['christofides', 'nearest_neighbour', 'genetic', 'ant_colony']

    optimality_stats = []

    for num_nodes in sorted(small_graphs['num_nodes'].unique()):
        node_data = small_graphs[small_graphs['num_nodes'] == num_nodes]

        if 'brute_force_weight' not in node_data.columns or node_data['brute_force_weight'].isna().all():
            continue

        stat_row = {'num_nodes': num_nodes}

        for algo in algorithms:
            weight_col = f'{algo}_weight'

            if weight_col in node_data.columns:
                differences = ((node_data[weight_col] - node_data['brute_force_weight']) /
                             node_data['brute_force_weight'] * 100)

                avg_diff = differences.mean()
                stat_row[f'{algo}_avg_optimality_gap_%'] = avg_diff

        optimality_stats.append(stat_row)

    optimality_df = pd.DataFrame(optimality_stats)
    return optimality_df

def plot_runtime_vs_nodes(stats_df):
    plt.figure(figsize=(12, 7))

    algorithms = ['brute_force', 'christofides', 'nearest_neighbour', 'genetic', 'ant_colony']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    markers = ['o', 's', '^', 'D', 'v']

    for algo, color, marker in zip(algorithms, colors, markers):
        time_col = f'{algo}_avg_time'

        if time_col in stats_df.columns:
            data = stats_df[['num_nodes', time_col]].dropna()

            if not data.empty:
                plt.plot(data['num_nodes'], data[time_col],
                        marker=marker, color=color, linewidth=2, markersize=8,
                        label=algo.replace('_', ' ').title())

    plt.xlabel('Liczba węzłów', fontsize=12, fontweight='bold')
    plt.ylabel('Średni czas (s)', fontsize=12, fontweight='bold')
    plt.title('Średni czas vs liczba węzłów', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()

    output_file = 'runtime_vs_nodes.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved runtime plot to {output_file}")
    plt.close()

def plot_weight_vs_nodes(stats_df):
    plt.figure(figsize=(12, 7))

    algorithms = ['brute_force', 'christofides', 'nearest_neighbour', 'genetic', 'ant_colony']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    markers = ['o', 's', '^', 'D', 'v']

    for algo, color, marker in zip(algorithms, colors, markers):
        weight_col = f'{algo}_avg_weight'

        if weight_col in stats_df.columns:
            # Filter out NaN values
            data = stats_df[['num_nodes', weight_col]].dropna()

            if not data.empty:
                plt.plot(data['num_nodes'], data[weight_col],
                        marker=marker, color=color, linewidth=2, markersize=8,
                        label=algo.replace('_', ' ').title())

    plt.xlabel('Liczba węzłów', fontsize=12, fontweight='bold')
    plt.ylabel('Średnia waga ścieżki', fontsize=12, fontweight='bold')
    plt.title('Średnia waga ścieżki vs liczba węzłów', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = 'weight_vs_nodes.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved weight plot to {output_file}")
    plt.close()

def print_summary_tables(stats_df, optimality_df):
    print("\n" + "="*80)
    print("BENCHMARK ANALYSIS SUMMARY")
    print("="*80)

    print("\n--- AVERAGE RUNTIME (seconds) ---\n")
    runtime_cols = ['num_nodes']
    algorithms = ['brute_force', 'christofides', 'nearest_neighbour', 'genetic', 'ant_colony']

    for algo in algorithms:
        time_col = f'{algo}_avg_time'
        if time_col in stats_df.columns:
            runtime_cols.append(time_col)

    runtime_display = stats_df[runtime_cols].copy()
    runtime_display.columns = ['Nodes'] + [col.replace('_avg_time', '').replace('_', ' ').title()
                                            for col in runtime_cols[1:]]
    print(runtime_display.to_string(index=False, float_format=lambda x: f'{x:.6f}'))

    print("\n--- AVERAGE SOLUTION WEIGHT ---\n")
    weight_cols = ['num_nodes']

    for algo in algorithms:
        weight_col = f'{algo}_avg_weight'
        if weight_col in stats_df.columns:
            weight_cols.append(weight_col)

    weight_display = stats_df[weight_cols].copy()
    weight_display.columns = ['Nodes'] + [col.replace('_avg_weight', '').replace('_', ' ').title()
                                           for col in weight_cols[1:]]
    print(weight_display.to_string(index=False, float_format=lambda x: f'{x:.2f}'))

    if not optimality_df.empty:
        print("\n--- AVERAGE OPTIMALITY GAP (% above optimal) ---")
        print("(For graphs with 5-9 nodes, compared to Brute Force optimal solution)\n")

        optimality_display = optimality_df.copy()
        optimality_display.columns = ['Nodes'] + [col.replace('_avg_optimality_gap_%', '').replace('_', ' ').title()
                                                   for col in optimality_df.columns[1:]]
        print(optimality_display.to_string(index=False, float_format=lambda x: f'{x:.2f}%'))

    print("\n" + "="*80)

def main():
    df = load_benchmark_data()
    stats_df = calculate_statistics(df)
    optimality_df = calculate_optimality_gap(df)

    print_summary_tables(stats_df, optimality_df)

    print("\nGenerating plots")
    plot_runtime_vs_nodes(stats_df)
    plot_weight_vs_nodes(stats_df)


if __name__ == "__main__":
    main()
