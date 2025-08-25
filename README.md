# 🛟 No-Wait-Job-Shop-Scheduling-MILP-Optimiser-using-Python
This repository represents Job scheduling MILP optimiser with no intermediate storage - JIT lines

---

## 🚉 Problem Context
In **Just-In-Time production lines** or **continuous flow processes**, intermediate buffers are **not allowed**. This means:
- **Material cannot wait** between processing stages
- **All job stages must start immediately** when the previous stage finishes (synchronized pipeline)
- Any deviation can lead to stoppages or waste

This optimizer implements a **No-wait Job shop scheduling MILP**, ensuring **tight synchronization** across machines and minimizing the **makespan** while preventing intermediate storage

---

## 🗾 Problem Features
- **Jobs**L Multiple jobs, each with multiple sequential operations
- **Machines**: Operations assigned to machines with given processing times
- **No-wait Constraint**: The start of operation *k+1* for a job = finish of operation *k*
- **Objective**: Minimize total makespan for all jobs while respecting machine availability

---

## 🏟 Technologies used
- Python 13 > PuLP library
- Visual Studio Code
- ChatGPT & Perplexity

--- 

## 🎡 Requirements
- Production Planning & Detailed Scheduling
- Knowledge of Prompt Engineering
- Basic of Coding

