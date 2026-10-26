📊 Sorting Lab — Interactive Sorting Algorithm Visualizer

Visualize. Understand. Compare. Sort.

Sorting Lab is an interactive Python web application built with Streamlit that brings sorting algorithms to life through animated bar charts, step-by-step execution, and performance comparisons.

Explore five classic sorting algorithms, experiment with different datasets, track comparisons and swaps, and understand how each algorithm behaves on the same input.

✨ Features
🎬 Step-by-step visualization — Watch elements move as sorting progresses.
⚡ Playback controls — Play, reset, navigate through individual steps, and adjust animation speed.
📈 Compare five algorithms — Analyze Bubble, Selection, Insertion, Merge, and Quick Sort.
📊 Performance metrics — Track comparisons and swaps or writes during execution.
🎲 Multiple data patterns — Generate random, nearly sorted, reversed, or few-unique-value datasets.
✍️ Custom input — Enter your own comma-separated integers to test different scenarios.
🧠 Complexity reference — Explore best-, average-, and worst-case time complexity, space complexity, and stability.
💻 Built-in source code — Inspect a clean Python implementation of every algorithm.
🔄 Shared datasets — Use the same input across algorithm pages for consistent comparisons.
🎨 Color-coded charts — Identify active elements and completed sorting states visually.
🛠️ Tech Stack
Technology	Purpose
Python	Core logic and sorting algorithms
Streamlit	Interactive web application
Matplotlib	Sorting visualizations
Pandas	Comparison tables and performance data
🚀 Getting Started
Prerequisites
Python 3.9 or later recommended
pip (Python package installer)
1. Clone the repository
bash
git clone https://github.com/Anshxyz0/sorting-lab.git
cd sorting-lab

2. Install dependencies
bash
python -m pip install streamlit matplotlib pandas


Alternatively, if you use a requirements.txt file:

bash
python -m pip install -r requirements.txt

3. Launch the application
bash
python -m streamlit run sorting_lab_v2.py


Streamlit will provide a local URL, usually:

text
http://localhost:8501


Open that URL in your browser to start exploring Sorting Lab.

🧮 Algorithms Included
Algorithm	Best Case	Average Case	Worst Case	Extra Space	Stable
🫧 Bubble Sort	O(n)	O(n²)	O(n²)	O(1)	Yes
🎯 Selection Sort	O(n²)	O(n²)	O(n²)	O(1)	No
🃏 Insertion Sort	O(n)	O(n²)	O(n²)	O(1)	Yes
🔀 Merge Sort	O(n log n)	O(n log n)	O(n log n)	O(n)	Yes
⚡ Quick Sort	O(n log n)	O(n log n)	O(n²)	O(log n)*	No

*Quick Sort's auxiliary space is typically O(log n) on average with balanced recursion, but can reach O(n) in the worst case due to recursion depth.

🖥️ Explore the Application
🏠 Home

Get an overview of all five algorithms, their complexity characteristics, and the current dataset.

🎬 Individual Algorithm Pages

Explore each algorithm independently:

View its explanation and complexity metrics.
Watch the sorting process using the bar chart.
Move through execution steps with the slider.
Adjust playback speed or reset the visualization.
Inspect the final sorted output and Python implementation.
📈 Compare All

Run all five algorithms against the same input and compare their operation counts with tables and bar charts.

🎲 Experiment with Data

Choose a generated dataset or provide custom numbers. Try different input patterns to see how the algorithms behave under different conditions.

📚 What You'll Learn

Sorting Lab is designed as a hands-on learning tool for students, beginners, and anyone exploring algorithms.

By experimenting with it, you can understand:

How comparison-based sorting algorithms work.
Why input order affects performance.
The difference between time and space complexity.
What algorithm stability means.
Why Merge Sort has predictable 
𝑂
(
𝑛
log
⁡
𝑛
)
 time complexity.
Why Quick Sort can be fast on average but degrade to 
𝑂
(
𝑛
2
)
.
Why operation counts are useful for comparing algorithm behavior.

Learning tip: Try the same dataset with all five algorithms, then switch between reversed and nearly sorted data to observe how the operation counts change.

📁 Project Structure
text
sorting-lab/
├── sorting_lab_v2.py   # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

⚙️ Input Validation
Generated datasets contain 5–40 elements.
Custom datasets must contain 2–40 whole numbers.
Custom values are entered as comma-separated integers.
🔮 Future Improvements

Potential enhancements include:

Add more algorithms, such as Heap Sort, Counting Sort, and Radix Sort.
Add execution-time benchmarking across larger datasets.
Compare algorithms across multiple input patterns automatically.
Add educational quizzes and complexity challenges.
Support exporting comparison results.
Improve accessibility and visualization customization.
🤝 Contributing

Suggestions, bug reports, and improvements are welcome.

Fork the repository.
Create a feature branch.
Make your changes.
Submit a pull request describing your improvement.

For small projects or learning exercises, even a documentation improvement or a clear bug report can be valuable.

📄 License

This project is available under the MIT License if you choose to distribute it under that license. To make this official, add a LICENSE file containing the MIT License text and your copyright details.

👨‍💻 Author

Anshxyz0

GitHub: @Anshxyz0

⭐ If you find Sorting Lab useful for learning sorting algorithms, consider giving the repository a star!

Made with Python, Streamlit, and a passion for algorithms.