import json
import csv
from scipy.stats import spearmanr

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_percent_overlap(yahoo_urls, google_urls):
    """Calculate the percentage of overlap between two lists of URLs."""
    overlap = set(yahoo_urls) & set(google_urls)  # Common URLs
    num_overlap = len(overlap)
    return num_overlap, (num_overlap / 10) * 100  # Overlap count and percentage (always divided by 10)

def calculate_spearman(yahoo_urls, google_urls):
    """Calculate Spearman correlation coefficient for matching URLs between two lists."""
    common_urls = list(set(yahoo_urls) & set(google_urls))  # Find common URLs
    n = len(common_urls)
    
    if n == 1:
        # Special case: when only one URL matches, set rho to 1 if ranks are identical, 0 otherwise
        yahoo_rank = yahoo_urls.index(common_urls[0]) + 1
        google_rank = google_urls.index(common_urls[0]) + 1
        return 1.0 if yahoo_rank == google_rank else 0.0

    if n < 2:
        return 0.0  # Return 0 for no overlap or insufficient data
    
    # Get ranks of the common URLs in both Yahoo and Google results
    yahoo_ranks = [yahoo_urls.index(url) + 1 for url in common_urls]
    google_ranks = [google_urls.index(url) + 1 for url in common_urls]

    # Compute Spearman rank correlation
    return spearmanr(yahoo_ranks, google_ranks).correlation

def generate_csv_output(yahoo_data, google_data, output_file):
    """Compare Yahoo and Google datasets and write the results to a CSV file."""
    total_overlap = 0
    total_percent_overlap = 0
    total_spearman = 0
    spearman_count = 0  # For averaging Spearman coefficient where it's valid

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Queries', 'Number of Overlapping of Results', 'Percent Overlap', 'Spearman Coefficient']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        queries = list(yahoo_data.keys())  # Get queries from Yahoo data
        print(len(queries))
        max_queries = 100  # We want exactly 100 rows
        for i in range(max_queries):
            query = f"Query {i + 1}"
            if i < len(queries):
                actual_query = queries[i]
                yahoo_urls = yahoo_data[actual_query]
                google_urls = google_data.get(actual_query, [])

                # Calculate the number of overlaps and percentage overlap
                num_overlap, percent_overlap = calculate_percent_overlap(yahoo_urls, google_urls)

                # Calculate Spearman coefficient
                spearman_coefficient = calculate_spearman(yahoo_urls, google_urls)
            else:
                # If there are fewer than 100 queries, fill the remaining with placeholder values
                num_overlap = 0
                percent_overlap = 0.0
                spearman_coefficient = 0.0

            # Track totals for averages
            total_overlap += num_overlap
            total_percent_overlap += percent_overlap
            if spearman_coefficient is not None:
                total_spearman += spearman_coefficient
                spearman_count += 1

            # Write the result to CSV
            writer.writerow({
                'Queries': query,
                'Number of Overlapping of Results': num_overlap,
                'Percent Overlap': f"{percent_overlap:.1f}",
                'Spearman Coefficient': f"{spearman_coefficient:.2f}" if spearman_coefficient is not None else '0.00'
            })

        # Calculate averages
        avg_overlap = total_overlap / max_queries
        avg_percent_overlap = total_percent_overlap / max_queries
        avg_spearman = total_spearman / spearman_count if spearman_count > 0 else 0

        # Write average row
        writer.writerow({
            'Queries': 'Averages',
            'Number of Overlapping of Results': f"{avg_overlap:.1f}",
            'Percent Overlap': f"{avg_percent_overlap:.1f}",
            'Spearman Coefficient': f"{avg_spearman:.2f}"
        })

        print(f"Results saved to {output_file}")

def main():
    # Load JSON data
    yahoo_file = 'tmp.json'  # Replace with actual file path
    google_file = 'Google_Result2.json'  # Replace with actual file path
    yahoo_data = load_json(yahoo_file)
    google_data = load_json(google_file)

    # Generate the CSV output
    output_file = 'hw1.csv'
    generate_csv_output(yahoo_data, google_data, output_file)

    print(f'Results saved to {output_file}')

if __name__ == "__main__":
    main()
