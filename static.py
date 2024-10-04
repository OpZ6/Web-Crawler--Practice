import csv
from collections import defaultdict

def generate_crawl_report():
    # Initialize counters and data structures
    fetch_attempted = 0
    fetch_succeeded = 0
    fetch_failed_or_aborted = 0
    status_code_counts = defaultdict(int)
    total_urls_extracted = 0
    unique_urls = set()
    unique_internal_urls = set()
    unique_external_urls = set()
    file_size_ranges = {
        "< 1KB": 0,
        "1KB ~ <10KB": 0,
        "10KB ~ <100KB": 0,
        "100KB ~ <1MB": 0,
        ">= 1MB": 0
    }
    content_types = defaultdict(int)

    # Process fetch_foxnews.csv
    try:
        with open("fetch_foxnews.csv", "r", encoding="utf-8") as fetch_file:
            reader = csv.DictReader(fetch_file)
            for row in reader:
                fetch_attempted += 1
                status_code = int(row["Status Code"])
                status_code_counts[status_code] += 1
                if 200 <= status_code < 300:
                    fetch_succeeded += 1
                else:
                    fetch_failed_or_aborted += 1
    except FileNotFoundError:
        print("fetch_foxnews.csv not found.")
    except UnicodeDecodeError:
        print("Error reading fetch_foxnews.csv due to encoding issues.")

    # Process visit_foxnews.csv
    try:
        with open("visit_foxnews.csv", "r", encoding="utf-8") as visit_file:
            reader = csv.DictReader(visit_file)
            for row in reader:
                total_urls_extracted += int(row["Number of Outlinks"])
                content_types[row["Content Type"]] += 1
                file_size = int(row["Size (bytes)"])
                
                # Categorize file sizes
                if file_size < 1024:
                    file_size_ranges["< 1KB"] += 1
                elif file_size < 10 * 1024:
                    file_size_ranges["1KB ~ <10KB"] += 1
                elif file_size < 100 * 1024:
                    file_size_ranges["10KB ~ <100KB"] += 1
                elif file_size < 1024 * 1024:
                    file_size_ranges["100KB ~ <1MB"] += 1
                else:
                    file_size_ranges[">= 1MB"] += 1
    except FileNotFoundError:
        print("visit_foxnews.csv not found.")
    except UnicodeDecodeError:
        print("Error reading visit_foxnews.csv due to encoding issues.")

    # Process urls_foxnews.csv
    try:
        with open("urls_foxnews.csv", "r", encoding="utf-8") as urls_file:
            reader = csv.DictReader(urls_file)
            for row in reader:
                url = row["Discovered URL"]
                unique_urls.add(url)
                if row["Is Internal"] == "OK":
                    unique_internal_urls.add(url)
                else:
                    unique_external_urls.add(url)
    except FileNotFoundError:
        print("urls_foxnews.csv not found.")
    except UnicodeDecodeError:
        print("Error reading urls_foxnews.csv due to encoding issues.")

    # Write report to CrawlReport_foxnews.txt
    with open("CrawlReport_foxnews.txt", "w") as report_file:
        report_file.write("Name: /\n")
        report_file.write("USC ID: /\n")
        report_file.write("News site crawled: foxnews.com\n")
        report_file.write("Number of threads: 7\n")

        report_file.write("\nFetch Statistics\n")
        report_file.write("================\n")
        report_file.write(f"# fetches attempted: {fetch_attempted}\n")
        report_file.write(f"# fetches succeeded: {fetch_succeeded}\n")
        report_file.write(f"# fetches failed or aborted: {fetch_failed_or_aborted}\n")

        report_file.write("\nOutgoing URLs:\n")
        report_file.write("==============\n")
        report_file.write(f"Total URLs extracted: {total_urls_extracted}\n")
        report_file.write(f"# unique URLs extracted: {len(unique_urls)}\n")
        report_file.write(f"# unique URLs within News Site: {len(unique_internal_urls)}\n")
        report_file.write(f"# unique URLs outside News Site: {len(unique_external_urls)}\n")

        report_file.write("\nStatus Codes:\n")
        report_file.write("=============")
        for status_code, count in status_code_counts.items():
            report_file.write(f"{status_code}: {count}\n")

        report_file.write("\nFile Sizes:\n")
        report_file.write("===========\n")
        for size_range, count in file_size_ranges.items():
            report_file.write(f"{size_range}: {count}\n")

        report_file.write("\nContent Types:\n")
        report_file.write("==============\n")
        for content_type, count in content_types.items():
            report_file.write(f"{content_type}: {count}\n")

if __name__ == "__main__":
    generate_crawl_report()