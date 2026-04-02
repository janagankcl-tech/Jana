# ULCM Cost Dashboard — User Guide

## Starting the Dashboard

Open Terminal and run:

```bash
cd ~/Jana && bash ulcm.sh
```

Your browser will open automatically to `http://localhost:5001/ulcm`.
Press **Ctrl+C** in Terminal to stop it when done.

---

## Layout

```
LEFT SIDEBAR          |  RIGHT PANEL
─────────────────────────────────────────
Parameter sliders     |  8 metric cards
                      |  Patient flow chart
                      |  Cost breakdown + Sessions chart
                      |  Triage split chart
```

---

## Parameters (Left Sidebar)

### Population
| Slider | What it controls |
|--------|-----------------|
| Population size | Total target community |

### HCD Entry — how people get in without screening
| Slider | What it controls |
|--------|-----------------|
| Reach rate | % of population community outreach contacts |
| Sign-up rate | % of those reached who enrol |
| Attendance rate | % of enrolled who show up to session 1 |

> **Key insight:** Removing screening increases all three. Default path: 10,000 → 6,000 reached → 4,200 signed up → 3,150 attend session 1.

### Engagement
| Slider | What it controls |
|--------|-----------------|
| Dropout rate | % who drop out before completing; SMS engagement lowers this |

### Clinical Design
| Control | What it controls |
|---------|-----------------|
| Active ingredient | Psychoeducation (×1.20), Problem solving (×1.15), Peer support (×0.80) |
| First-line sessions | 1 = Single Session Intervention (SSI); diminishing returns after 4 |
| Base remission rate | Background remission rate from phase data |

### Step Care — escalation for non-responders
| Slider | What it controls |
|--------|-----------------|
| Step-up rate | % of first-line non-responders escalated to IPT-G |
| Step-care sessions | Number of sessions in stepped-up treatment |
| Step remission rate | Remission rate at higher intensity |

### Severity Split
Splits the retained population into mild / moderate / severe.
Sliders **auto-normalise** to always sum to 100%.

### Workforce
| Slider | What it controls |
|--------|-----------------|
| Hours / week | Working hours per lay worker per week |
| Weeks / year | Working weeks per year |
| Sessions / hour | How many sessions a worker delivers per hour |

### Costs
| Slider | What it controls |
|--------|-----------------|
| Annual cost / worker | Salary + in-kind costs per lay worker |
| Supervision cost / worker | Per-worker supervision overhead |
| SMS cost / user | Digital engagement cost per person in population |
| Screening cost / user | **Removed cost** — shown greyed out to illustrate saving vs old model |

---

## Metric Cards (Top Right)

| Card | Meaning |
|------|---------|
| Entered System | People who attended at least session 1 |
| Retained | Completed the programme (didn't drop out) |
| Total Remitted | First-line + step-care remissions combined |
| Remission Rate | Total remitted as % of full population |
| Cost per Remission | Total programme cost ÷ remitted |
| Cost per User | Total programme cost ÷ population |
| Workers Needed | Full-time equivalent lay workers required |
| Total Programme Cost | Worker + supervision + SMS costs |

---

## Charts (Right Panel)

### Patient Flow Funnel
Horizontal bars showing the drop-off at each stage:
Population → Reached → Signed up → Session 1 → Retained → Remitted

### Cost Breakdown (doughnut)
Shows where money goes: worker salaries vs supervision vs SMS.
The grey slice shows the **screening cost saving** vs the old model.

### Sessions vs Cost per Remission (line chart)
Sweeps first-line sessions from 1–8 at your current settings.
The **red dot** marks your current selection.
Use this to find the point where adding more sessions stops improving cost-efficiency.

### Triage Split (stacked bar)
Shows mild / moderate / severe breakdown of the retained population.

---

## Things to Explore

- **Minimum viable dose:** Set sessions = 1 and ingredient = problem_solving. How low can cost/remission go?
- **HCD vs screening tradeoff:** Raise reach_rate and signup_rate while reducing screening_cost — watch total cost drop.
- **Scale effects:** Increase population to 100,000 — cost/remission improves as fixed costs spread.
- **Step-care sensitivity:** Raise step_up_rate — more people get higher-intensity treatment. Does it improve remission enough to justify the cost?
