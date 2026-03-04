"""All help text, theory explanations, and documentation for the dashboard."""

# ─── Sidebar tooltip help strings ────────────────────────────────────────────

HELP_AI_CAP_MAX = (
    "The upper bound of AI capability on the logistic S-curve. "
    "Higher values mean AI eventually becomes more productive. "
    "At 1.0, a fully-capable AI matches the best human worker in a fully-applicable sector."
)

HELP_AI_GROWTH_RATE = (
    "Controls how steeply AI capability rises during the growth phase. "
    "Higher values produce a sharper transition from low to high capability. "
    "Think of this as the pace of AI research breakthroughs."
)

HELP_AI_INFLECTION = (
    "The simulation period at which AI capability growth is fastest "
    "(the midpoint of the S-curve). Earlier values mean AI arrives sooner; "
    "later values delay the automation wave."
)

HELP_INNOVATION_RATE = (
    "Rate at which automation creates entirely new job categories. "
    "Higher values reflect an optimistic view where AI-driven productivity "
    "opens new markets and roles (e.g., AI trainers, prompt engineers)."
)

HELP_TRANSACTION_COST = (
    "Base cost of negotiating an automation deal between a firm and a worker. "
    "This is the core Coase Theorem lever: at 0, the theorem predicts efficient "
    "outcomes regardless of who holds rights. As TC rises, bargaining breaks down "
    "and deadweight loss appears."
)

HELP_INFO_ASYMMETRY = (
    "How much the firm knows about true AI productivity vs. what the worker knows. "
    "Higher asymmetry increases effective transaction costs because parties cannot "
    "accurately value the deal, leading to more failed negotiations."
)

HELP_LEGAL_FRICTION = (
    "Administrative and legal costs of formalizing an automation agreement — "
    "regulatory compliance, contract drafting, dispute resolution. "
    "Reflects the institutional environment's efficiency."
)

HELP_COORDINATION_COST = (
    "Per-worker cost of coordinating a multi-worker automation deal. "
    "Scales with the number of affected workers in the firm, capturing the "
    "difficulty of collective bargaining situations."
)

HELP_BARGAINING_POWER = (
    "Worker's share (β) of the net surplus in Nash bargaining. "
    "β=0.5 splits surplus evenly. β=1.0 gives all surplus to workers. "
    "The Coase Theorem predicts that β affects distribution but not efficiency "
    "when transaction costs are zero."
)

HELP_N_WORKERS = (
    "Total number of worker agents. More workers provide smoother statistical "
    "patterns but increase computation time."
)

HELP_N_FIRMS = (
    "Number of firm agents. Firms are distributed across sectors and each "
    "evaluates automation for its workforce independently."
)

HELP_MATCHING_EFFICIENCY = (
    "Efficiency parameter of the Cobb-Douglas matching function. "
    "Higher values mean unemployed workers find vacancies faster, "
    "reflecting a well-functioning labor market with good job boards, "
    "mobility, and information."
)

HELP_RETRAINING_DURATION = (
    "Number of periods a displaced worker spends retraining before "
    "becoming eligible for re-employment. Longer durations increase "
    "structural unemployment during automation transitions."
)

HELP_LABOR_SHARE = (
    "The Cobb-Douglas labor share (α) in production. "
    "Determines how much of output goes to labor vs. capital. "
    "Higher α means wages are a larger fraction of productivity."
)

HELP_MONOPSONY = (
    "Wage markdown due to employer market power. "
    "When firms are the dominant buyer of labor, they pay below "
    "marginal product. 0 = perfectly competitive; 0.5 = severe monopsony."
)

HELP_JOB_CREATION_MULT = (
    "How strongly automation drives new job creation. "
    "Set to 0 to model permanent displacement (no new jobs from automation). "
    "Higher values reflect the 'creative destruction' view where automation "
    "creates more jobs than it destroys."
)

HELP_N_PERIODS = "Number of time steps to simulate. Longer runs show long-term equilibrium effects."

HELP_RANDOM_SEED = (
    "Seed for the random number generator. Same seed = identical results, "
    "useful for comparing scenarios that differ only in parameter changes."
)


# ─── Scenario descriptions ───────────────────────────────────────────────────

SCENARIO_DESCRIPTIONS = {
    "Custom": "All parameters set to defaults. Adjust any slider to explore.",
    "Zero Transaction Costs": (
        "**Coase Theorem ideal case.** All friction removed (TC=0, no asymmetry, "
        "no legal costs, no coordination costs). The theorem predicts that total "
        "surplus is maximized and is *invariant* to worker bargaining power β. "
        "Try varying β — the split changes but total output does not."
    ),
    "High Friction": (
        "**Coase Theorem breakdown.** High transaction costs, information asymmetry, "
        "and legal friction. Many efficient automation deals are blocked, creating "
        "deadweight loss. Compare with Zero TC to see the theorem in action."
    ),
    "Strong Worker Rights": (
        "Workers have β=0.8 bargaining power with low transaction costs. "
        "Workers capture most of the automation surplus as compensation. "
        "Firms still automate when profitable, but workers are well-compensated."
    ),
    "Rapid AI Growth": (
        "AI capability grows twice as fast and peaks earlier (period 30 vs. 50). "
        "Simulates a sudden AI breakthrough. Watch for a sharp automation wave "
        "followed by labor market adjustment."
    ),
}


# ─── Tab intro text ──────────────────────────────────────────────────────────

TAB_OVERVIEW_INTRO = (
    "High-level view of the simulation economy. The KPI cards show the final-period "
    "snapshot, while charts track dynamics over the full simulation run. "
    "In **Compare Mode**, a saved scenario overlays as dashed lines for direct comparison."
)

TAB_COASE_INTRO = """
This tab focuses on the **Coase Theorem prediction**: if property rights are well-defined
and transaction costs are zero, parties bargain to an efficient outcome regardless of the
initial allocation of rights.

In this simulation, **workers hold the right to employment**. Firms must compensate workers
to automate their positions. The surplus from automation is split according to Nash
bargaining, minus any transaction costs.

- **Worker Compensation**: The portion of surplus paid to displaced workers (β × net surplus)
- **Firm Gain**: The portion retained by the automating firm ((1−β) × net surplus)
- **Deadweight Loss**: Surplus destroyed when transaction costs block efficient deals

**Key experiment**: Compare "Zero Transaction Costs" with "High Friction" — total surplus
should be maximized (and constant across β values) only when TC=0.
"""

TAB_SECTOR_INTRO = (
    "Each sector has different AI applicability — Tech (0.8) and Manufacturing (0.7) automate "
    "fastest, while Creative (0.3) and Healthcare (0.4) are more resistant. "
    "Watch how automation waves ripple through sectors sequentially rather than simultaneously."
)

TAB_DISTRIBUTION_INTRO = (
    "Examine how automation affects the *distribution* of wages across workers. "
    "Use the period slider to see how the distribution evolves. "
    "Look for hollowing out of middle-wage jobs and potential polarization between "
    "high-skill and low-skill workers."
)


# ─── Theory & Guide tab content ─────────────────────────────────────────────

THEORY_COASE = """
## The Coase Theorem

The **Coase Theorem** (Ronald Coase, 1960) states that if:
1. **Property rights are well-defined** — it's clear who has the right to what
2. **Transaction costs are zero** (or sufficiently low)
3. Parties can **bargain freely**

Then the initial allocation of property rights **does not affect economic efficiency**.
Parties will negotiate to the outcome that maximizes total surplus, regardless of who
starts with the rights. The initial allocation only affects *who gets paid*.

### Application to AI Job Displacement

In this simulation, **workers hold the "right to employment"** — firms cannot simply
replace workers with AI. Instead, firms must negotiate: they offer compensation to workers
in exchange for the right to automate their position.

- If the AI is more productive than the worker, there is a **positive surplus** from automation
- This surplus is split between the worker (compensation) and the firm (profit gain)
- The split is determined by **bargaining power (β)**

**The Coase prediction**: With zero transaction costs, the *total* amount of automation
and total surplus should be the same whether β=0.1 or β=0.9. Only the *distribution* changes.

### When Coase Breaks Down

The theorem fails when transaction costs are significant:
- **Information asymmetry**: Firms may overstate AI capability; workers may overstate their value
- **Legal friction**: Negotiating and enforcing agreements is costly
- **Coordination costs**: When automation affects many workers, collective bargaining is harder
- **Bounded rationality**: Real agents don't always find the optimal deal

When TC > 0, some deals where surplus > 0 but surplus < TC are **blocked** — creating
deadweight loss. The simulation tracks these blocked transactions explicitly.
"""

THEORY_MODEL = """
## Economic Model

### Agents

The simulation contains three types of agents:

| Agent | Count | Key Attributes |
|-------|-------|---------------|
| **Workers** | 1000 (default) | Sector, skill level (0–1), wage, employment status, retraining timer, bargaining power |
| **Firms** | 50 (default) | Sector, workforce, automation level, AI capability |
| **Sectors** | 5 | Manufacturing, Services, Tech, Healthcare, Creative — each with different AI applicability |

### AI Capability Growth

AI capability follows a **logistic S-curve**:

```
ai_cap(t) = max_cap / (1 + exp(-growth_rate × (t - inflection)))
```

This creates three phases:
1. **Early** (t ≪ inflection): AI is weak, little automation occurs
2. **Transition** (t ≈ inflection): Rapid capability growth, automation wave
3. **Mature** (t ≫ inflection): AI plateaus, market adjusts to new equilibrium

### Coasian Bargaining

For each worker position, the firm calculates:

1. **Gross Surplus**:
   `S = (AI_capability × sector_applicability − worker_skill × wage) × horizon`

2. **Transaction Cost**:
   `TC = base_TC × (1 + info_asymmetry + legal_friction + coordination × n_workers)`

3. **Nash Bargaining Solution** (if S > TC):
   - Worker receives: `β × (S − TC)`
   - Firm retains: `(1 − β) × (S − TC)`

4. **Decision**: Automate if S > TC (net surplus is positive)

If S > 0 but S ≤ TC, the deal is **blocked** and the entire surplus S becomes deadweight loss.

### Labor Market Clearing

Unemployed workers are matched to vacancies using a **Cobb-Douglas matching function**:

```
Matches = efficiency × Unemployed^0.5 × Vacancies^0.5
```

Wages are set at the marginal product of labor, adjusted for monopsony power:

```
Wage = productivity × (0.5 + skill) × labor_share × (1 − monopsony_markdown) × base_wage
```

### Job Creation

Automation creates new jobs through innovation:

```
New jobs = base_creation + multiplier × automation_level × innovation_rate × 100
```

This captures the idea that automation, while displacing existing jobs, also creates
new categories of work through productivity gains and new markets.
"""

THEORY_PHASES = """
## Simulation Time Step

Each period executes five phases in order:

### Phase 1 — AI Capability Growth
The global AI capability advances along the logistic S-curve. All firms share
the same capability level (representing available technology).

### Phase 2 — Firm Automation Decisions
Each firm evaluates every worker position through Coasian bargaining:
- Compute the surplus from replacing the worker with AI
- Compute total transaction costs
- If surplus exceeds costs, the deal goes through:
  - Worker is displaced but receives compensation
  - Worker enters a retraining period
  - Firm's automation level increases
- If costs exceed surplus, the position is preserved (potentially with deadweight loss)

### Phase 3 — Labor Market Clearing
Unemployed workers (who have finished retraining) are matched to available vacancies.
Higher-skilled workers are matched first. Wages for all employed workers gradually
converge toward equilibrium.

### Phase 4 — Job Creation
New vacancies are created based on the overall automation level and innovation rate.
This represents the positive employment effects of automation-driven economic growth.

### Phase 5 — State Updates
Retraining timers count down. Workers completing retraining receive a small
skill boost (+0.05), reflecting acquired new capabilities.
"""

THEORY_SECTORS = """
## Sector Dynamics

The five sectors differ in how amenable they are to AI automation:

| Sector | AI Applicability | Base Wage | Interpretation |
|--------|:---:|:---:|------|
| **Tech** | 0.8 | 1.4 | Highly automatable — coding, data analysis, system administration |
| **Manufacturing** | 0.7 | 1.0 | Robots and AI-driven production lines |
| **Services** | 0.5 | 0.8 | Mixed — some tasks automate easily, others require human interaction |
| **Healthcare** | 0.4 | 1.2 | Diagnosis aids automate, but patient care resists |
| **Creative** | 0.3 | 0.9 | Most resistant — artistic judgment, novel creation, emotional expression |

Higher-applicability sectors experience automation waves earlier and more intensely.
Workers in these sectors receive larger compensation packages (more surplus to split)
but face higher displacement rates.
"""

THEORY_EXPERIMENTS = """
## Suggested Experiments

### 1. The Coase Theorem Test
1. Run with **"Zero Transaction Costs"** preset and β=0.2. Save the scenario.
2. Run again with β=0.8. Enable Compare Mode.
3. **Expected**: Total surplus curves overlap almost perfectly. Only the worker/firm
   split changes. This is the Coase Theorem in action.

### 2. Transaction Costs Break Efficiency
1. Run with **"Zero Transaction Costs"** preset. Save.
2. Run with **"High Friction"** preset.
3. **Expected**: Total surplus is lower under High Friction. Blocked transactions
   appear. Deadweight loss accumulates. Efficiency depends on β.

### 3. Automation Wave Dynamics
1. Run with **"Rapid AI Growth"**. Note the sharp dip in employment around period 30.
2. Run with default settings. Note the more gradual transition around period 50.
3. **Expected**: Faster AI creates a sharper disruption but reaches the same long-run equilibrium.

### 4. Creative Destruction vs. Permanent Displacement
1. Run with default settings (job_creation_multiplier=0.1). Save.
2. Run with job_creation_multiplier=0.0.
3. **Expected**: Without new job creation, employment never recovers.
   This tests the "lump of labor" scenario.

### 5. Monopsony Power
1. Run with monopsony_markdown=0.0 (competitive labor market). Save.
2. Run with monopsony_markdown=0.4 (strong employer power).
3. **Expected**: Wages are significantly lower under monopsony, even with the same
   productivity and automation levels.
"""

THEORY_GLOSSARY = """
## Glossary

| Term | Definition |
|------|-----------|
| **Bargaining Power (β)** | Worker's share of the net surplus in Nash bargaining. β=0 means the firm takes everything; β=1 means the worker takes everything. |
| **Blocked Transaction** | An automation deal where gross surplus > 0 but net surplus ≤ 0 due to transaction costs. The efficient outcome is prevented. |
| **Cobb-Douglas Matching** | A standard labor economics function where matches depend on both the number of unemployed workers and available vacancies, with diminishing returns to each. |
| **Deadweight Loss** | Total surplus destroyed because transaction costs prevented an otherwise efficient deal. The Coase Theorem predicts this is zero when TC=0. |
| **Gross Surplus** | The total productivity gain from replacing a worker with AI, before subtracting transaction costs. |
| **Logistic S-Curve** | A sigmoid growth function that starts slow, accelerates, then plateaus. Used here to model AI capability growth. |
| **Monopsony** | A market where a single buyer (employer) has market power, allowing them to pay below marginal product. The markdown parameter controls severity. |
| **Nash Bargaining Solution** | A game-theoretic solution where two parties split a surplus according to their relative bargaining power, given that both prefer a deal to no deal. |
| **Net Surplus** | Gross surplus minus transaction costs. Must be positive for a deal to proceed. |
| **Property Rights** | In this simulation, workers hold the "right to employment" — firms cannot unilaterally automate without compensating affected workers. |
| **Reservation Wage** | The minimum wage a worker will accept. Below this, the worker prefers unemployment (or retraining). |
| **Transaction Costs** | All costs of negotiating and completing an automation deal: information gathering, legal fees, coordination overhead. |
"""
