import pulp

# ---- Data -----
jobs = ['J1', 'J2']
machines = ['M1', 'M2', 'M3']

# Job routes (Sequence of machines for each job )
job_route = {
        'J1': ['M1', 'M2', 'M3'],
        'J2': ['M2', 'M3', 'M1']
}

# Processing times (job, machine)
proc_time = {
        ('J1', 'M1'): 3, ('J1', 'M2'): 2, ('J1', 'M3'): 4,
        ('J2', 'M2'): 2, ('J2', 'M3'): 3, ('J2', 'M1'): 5
}

# ----- Model ------
prob = pulp.LpProblem("NoWaitJobShopScheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts(
    "start",
    [(j, m) for j in jobs for m in job_route[j]],
    lowBound=0
)
Cmax = pulp.LpVariable("Makespan", lowBound=0)

# Sequencing binaries: y[i,k,m] = 1 if job i precedes job k on machine m
y = pulp.LpVariable.dicts(
    "y",
    [(i, k, m) for i in jobs for k in jobs if i != k for m in machines],
    cat="Binary"
)

# ------ Objective --------
prob += Cmax, "Minimize_Makespan"

# ------ Constraints ---------

# 1. No-wait: next operation starts immediately after previous finishes
for j in jobs:
    for idx in range(len(job_route[j]) - 1):
        m1, m2 = job_route[j][idx], job_route[j][idx + 1]
        prob += (
            start[(j, m2)] == start[(j, m1)] + proc_time[(j, m1)], 
                  f"NoWait_{j}_{m1}_to_{m2}"
        )

# 2. Makespan definition (last operation must finish before Cmax)
for j in jobs:
    last_m = job_route[j][-1]
    prob += (
        start[(j, last_m)] + proc_time[(j, last_m)] <= Cmax,
        f"Makespan_{j}"
    )

# 3. Machine capacity: no two jobs overlap on the same machine
M = 1000  # Big-M
for m in machines:
    jobs_on_m = [j for j in jobs if m in job_route[j]]
    for i in jobs_on_m:
        for k in jobs_on_m:
            if i != k:
                proc_i, proc_k = proc_time[(i, m)], proc_time[(k, m)]
                prob += (
                    start[(i, m)] + proc_i <= start[(k, m)] + M * (1 - y[(i, k, m)]),
                    f"NoOverlap_{i}_{k}_{m}_1"
                )
                prob += (
                    start[(k, m)] + proc_k <= start[(i, m)] + M * y[(i, k, m)],
                    f"NoOverlap_{i}_{k}_{m}_2"
                 )

# ------- Solve --------
solver = pulp.PULP_CBC_CMD(msg=True)
prob.solve(solver)

# --------- Results ----------
print("Status:", pulp.LpStatus[prob.status])
print("Optimal Makespan:", pulp.value(Cmax))

for j in jobs:
    print(f"\nSchedule for {j}:")
    for m in job_route[j]:
        s = pulp.value(start[(j, m)])
        f = s + proc_time[(j, m)]
        print(f"    {m}: Start={s:.2f}, Finish={f:.2f}")