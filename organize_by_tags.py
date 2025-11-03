import json
import ast
from pathlib import Path
from datasets import load_dataset
from collections import defaultdict

def main():
    # Load the dataset
    print("Loading PutnamBench dataset...")
    ds = load_dataset("amitayusht/PutnamBench")
    
    # Create a directory for organized data
    output_dir = Path("formal_agent/data/by_tags")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Dictionary to store problems by tag
    problems_by_tag = defaultdict(list)
    
    # Process each problem in the dataset
    print("Processing problems...")
    for item in ds["train"]:
        # Parse tags (they come as string representation of a list)
        try:
            tags = ast.literal_eval(item["tags"])
        except:
            # If parsing fails, try to handle it as a list already
            tags = item["tags"] if isinstance(item["tags"], list) else []
        
        # Create the problem entry
        problem_entry = {
            "name": item["name"],
            "problem_id": item["name"],  # Using name as problem_id
            "informal_statement": item["informal_statement"],
            "lean4_statement": item["lean4_statement"],
            "tags": tags
        }
        
        # Add this problem to each of its tags
        for tag in tags:
            problems_by_tag[tag].append(problem_entry)
    
    # Save each tag to a separate JSON file
    print(f"\nFound {len(problems_by_tag)} different tags:")
    for tag in sorted(problems_by_tag.keys()):
        print(f"  - {tag}: {len(problems_by_tag[tag])} problems")
    
    print("\nSaving files...")
    for tag, problems in problems_by_tag.items():
        # Clean tag name for filename (replace spaces with underscores, etc.)
        safe_tag = tag.replace(" ", "_").replace("/", "_")
        output_file = output_dir / f"{safe_tag}.json"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(problems, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved {len(problems)} problems to {output_file}")
    
    # Also create a summary file
    summary = {
        "total_problems": len(ds["train"]),
        "tags": {tag: len(problems) for tag, problems in sorted(problems_by_tag.items())},
        "tag_files": {tag: f"by_tags/{tag.replace(' ', '_').replace('/', '_')}.json" 
                      for tag in sorted(problems_by_tag.keys())}
    }
    
    summary_file = output_dir / "summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\nSummary saved to {summary_file}")
    print(f"\nDone! Processed {len(ds['train'])} problems across {len(problems_by_tag)} tags.")

if __name__ == "__main__":
    main()

