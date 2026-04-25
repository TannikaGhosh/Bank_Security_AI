import os
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import Counter

# --- Configuration ---
# Replace with your actual GitHub username
GITHUB_USERNAME = "TannikaGhosh" # Using the directory name as default guess, user can change
REPO_NAME = "Bank_Security_AI"
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/commits"

def fetch_commits_data():
    """Fetches commit data from GitHub API or generates sample data on failure."""
    print(f"Fetching commit data for {GITHUB_USERNAME}/{REPO_NAME}...")
    
    try:
        response = requests.get(API_URL)
        
        # Check for rate limits or other errors
        if response.status_code == 200:
            commits = response.json()
            if not commits:
                print("No commits found. Using sample data.")
                return generate_sample_commit_data()
            
            dates = []
            for commit in commits:
                # GitHub returns date in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
                date_str = commit['commit']['author']['date']
                date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                # We only care about the date part for daily counts
                dates.append(date_obj.date())
            
            return dates
            
        elif response.status_code == 403 or response.status_code == 404:
            print(f"Failed to fetch from GitHub API (Status: {response.status_code}).")
            print("This could be due to rate limits or the repository not being public yet.")
            print("Using sample data for demonstration instead.")
            return generate_sample_commit_data()
        else:
            print(f"Unexpected error: {response.status_code}. Using sample data.")
            return generate_sample_commit_data()

    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        print("Using sample data.")
        return generate_sample_commit_data()

def generate_sample_commit_data():
    """Generates synthetic commit data for the last 30 days for demonstration."""
    dates = []
    today = datetime.now().date()
    
    # Simulate commits over the past 30 days
    # Let's add more commits closer to today
    for i in range(30):
        current_date = today - timedelta(days=i)
        # More commits on recent days (randomized somewhat)
        num_commits = (30 - i) // 5 + 1
        for _ in range(num_commits):
            dates.append(current_date)
            
    return dates

def plot_commit_activity(dates):
    """Plots a line chart of daily commit counts and saves it."""
    print("Generating commit activity plot...")
    
    # Count commits per day
    date_counts = Counter(dates)
    
    # Sort by date
    sorted_dates = sorted(date_counts.keys())
    counts = [date_counts[d] for d in sorted_dates]
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, counts, marker='o', linestyle='-', color='#0366d6', linewidth=2)
    
    # Customize the plot
    plt.title('Commit Activity Over Time (Last 30 Days)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Commits', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format x-axis dates nicely (rotate for readability)
    plt.gcf().autofmt_xdate()
    
    # Ensure layout fits well
    plt.tight_layout()
    
    # Save the plot
    output_file = 'github_commits.png'
    plt.savefig(output_file, dpi=300)
    print(f"Saved commit plot to '{output_file}'.")
    plt.close()

def scan_file_types(directory):
    """Recursively scans the directory and counts file extensions."""
    print(f"Scanning directory '{directory}' for file types...")
    
    ignored_dirs = {'venv', '__pycache__', '.git', 'node_modules', '.idea'}
    file_extensions = []
    
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to ignore certain directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            # Get the file extension
            _, ext = os.path.splitext(file)
            if ext:
                # Normalize extension (lowercase, no dot)
                file_extensions.append(ext.lower())
            elif file.startswith('.') and len(file) > 1:
                 # Handle files like .gitignore as just '.gitignore' type or 'config'
                 file_extensions.append(file)
            else:
                 file_extensions.append('no_extension')
                
    return Counter(file_extensions)

def plot_file_types(extension_counts):
    """Plots a pie chart of file type distributions and saves it."""
    print("Generating file type distribution plot...")
    
    # Filter out very rare extensions for a cleaner pie chart
    total_files = sum(extension_counts.values())
    
    labels = []
    sizes = []
    other_count = 0
    
    for ext, count in extension_counts.items():
        # Only show individual slices for types that make up > 2% of the project
        if count / total_files > 0.02:
            labels.append(ext)
            sizes.append(count)
        else:
            other_count += count
            
    if other_count > 0:
        labels.append('other')
        sizes.append(other_count)
        
    # Sort slices by size descending
    sorted_pairs = sorted(zip(sizes, labels), reverse=True)
    sizes, labels = zip(*sorted_pairs)

    # Create the pie chart
    plt.figure(figsize=(8, 8))
    
    # Define a nice color palette
    colors = plt.cm.Set3.colors
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1})
    
    plt.title('Project File Type Distribution', fontsize=14)
    plt.tight_layout()
    
    # Save the plot
    output_file = 'file_types.png'
    plt.savefig(output_file, dpi=300)
    print(f"Saved file type plot to '{output_file}'.")
    plt.close()

if __name__ == "__main__":
    print("--- Starting GitHub Activity Plot Generation ---")
    
    # 1. Generate and plot commit activity
    commit_dates = fetch_commits_data()
    if commit_dates:
        plot_commit_activity(commit_dates)
    
    # 2. Generate and plot file type distribution
    project_dir = os.getcwd()
    ext_counts = scan_file_types(project_dir)
    if ext_counts:
        plot_file_types(ext_counts)
        
    print("--- Finished successfully! ---")
