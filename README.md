# Smart Timetable Generator — Genetic Algorithm

A portfolio-ready desktop application that generates conflict-aware academic timetables using a **Genetic Algorithm**.

## Features
- Genetic Algorithm optimization
- Teacher and room clash penalties
- Room-capacity constraints
- Configurable population and generations
- Tkinter desktop GUI
- SQLite persistence
- Excel export
- PDF export
- Matplotlib fitness visualization
- Reproducible sample dataset

## Architecture
`CSV Data → Population → Fitness → Selection → Crossover → Mutation → Best Timetable → GUI/SQLite/Exports`

Each chromosome contains one gene per course:
`Gene = (Course, Time Slot, Room)`

Fitness:
`fitness = 1 / (1 + total_penalty)`

## Run on Windows
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Click **Generate Timetable**, then use **Export Excel** or **Export PDF**.

## Project Structure
```text
smart-timetable-generator/
├── data/
├── results/
├── src/
│   ├── ga_engine.py
│   ├── utils.py
│   └── exporters.py
├── main.py
├── requirements.txt
└── README.md
```

## Skills Demonstrated
Python • Genetic Algorithms • Optimization • Constraint Handling • Tkinter • SQLite • Matplotlib • Excel/PDF Automation • OOP

## Future Improvements
Student-group constraints, teacher availability, breaks, multi-objective optimization, timetable heatmaps, unit tests and CI.

**GitHub:** https://github.com/jonathan6378/smart-timetable-generator
