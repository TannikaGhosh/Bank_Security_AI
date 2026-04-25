import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

# Configuration
REPO_OWNER = "TannikaGhosh"
REPO_NAME = "Bank_Security_AI"
START_DATE = datetime(2026, 4, 20)
END_DATE = datetime(2026, 5, 19)  # 30 days later

def generate_commit_graph():
    # Initialize dictionary with 0s for every day in the range
    commits_by_day = {}
    current = START_DATE
    while current <= END_DATE:
        commits_by_day[current.strftime("%Y-%m-%d")] = 0
        current += timedelta(days=1)

    print(f"Fetching commits for {REPO_OWNER}/{REPO_NAME} from {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}...")
    
    page = 1
    while True:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
        params = {
            "since": START_DATE.isoformat() + "Z", 
            "until": END_DATE.isoformat() + "Z", 
            "per_page": 100, 
            "page": page
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching data: Status Code {response.status_code}")
            print(response.json().get("message", ""))
            break
            
        data = response.json()
        if not data:
            break
            
        for commit in data:
            # Extract date (YYYY-MM-DD) from ISO format (YYYY-MM-DDTHH:MM:SSZ)
            date_str = commit["commit"]["author"]["date"][:10]
            if date_str in commits_by_day:
                commits_by_day[date_str] += 1
                
        page += 1

    # Prepare plot
    dates = list(commits_by_day.keys())
    counts = list(commits_by_day.values())

    plt.figure(figsize=(14, 6))
    
    # Create bar chart
    plt.bar(dates, counts, color='#3498db', edgecolor='black', linewidth=0.5)
    
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Number of Commits", fontsize=12)
    plt.title(f"Commit Activity: {REPO_OWNER}/{REPO_NAME}\n({START_DATE.strftime('%b %d, %Y')} to {END_DATE.strftime('%b %d, %Y')})", fontsize=14)
    
    # Clean up x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(range(max(counts) + 2)) # Ensure y-axis shows integer ticks
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the plot
    output_filename = "commit_activity_april20.png"
    plt.savefig(output_filename, dpi=300)
    print(f"Successfully saved plot to '{os.path.abspath(output_filename)}'")
    
    total = sum(counts)
    print(f"Total commits in period: {total}")

if __name__ == "__main__":
    generate_commit_graph()
