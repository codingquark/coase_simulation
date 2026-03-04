from simulation.config import SimulationConfig

PRESETS = {
    "Custom": SimulationConfig(),
    "Zero Transaction Costs": SimulationConfig(
        transaction_cost=0.0,
        info_asymmetry=0.0,
        legal_friction=0.0,
        coordination_cost=0.0,
    ),
    "High Friction": SimulationConfig(
        transaction_cost=0.3,
        info_asymmetry=0.5,
        legal_friction=0.4,
        coordination_cost=0.1,
    ),
    "Strong Worker Rights": SimulationConfig(
        worker_bargaining_power=0.8,
        transaction_cost=0.05,
    ),
    "Rapid AI Growth": SimulationConfig(
        ai_growth_rate=0.2,
        ai_inflection_point=30.0,
        ai_cap_max=1.0,
    ),
}


def get_preset_names():
    return list(PRESETS.keys())


def get_preset(name: str) -> SimulationConfig:
    return PRESETS.get(name, SimulationConfig())
