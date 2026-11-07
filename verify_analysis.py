"""Reproduce analytical identities and a 3-seed snapshot; no input fitting.
Run: python verify_analysis.py (matplotlib/numpy required by original modules).
"""
from pathlib import Path
import importlib.util
import json
import math
import statistics
import sys
from types import SimpleNamespace
from simulation_metrics import measure, CAL

ROOT=Path(__file__).resolve().parent
def load(filename):
    path=next(ROOT.rglob(filename))
    spec=importlib.util.spec_from_file_location(path.stem,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def main():
    eng=load('iteration3_sim.py')
    versions=['baseline','iteration 1','iteration 2','iteration 3']
    expected=[599+1/6,434.995373327,349.853619137,61.44646381]
    for i,name in enumerate(versions):
        cfg=eng.CONFIGS[name]
        assert math.isclose(eng.expected_work(cfg),expected[i],abs_tol=.002),(name,eng.expected_work(cfg))
        assert 0<=eng.expected_incidence(cfg)<=1
    assert math.isclose(eng.BUDGET_MIN,14150.4)
    assert math.isclose(CAL*22,30.4)
    assert math.isclose(eng.expected_incidence(eng.CONFIGS['baseline']),.88)
    for script in ['iteration1_sim.py','iteration2_sim.py','rework_simulation.py']:
        mod=load(script)
        config=mod.SCENARIOS[2][1] if script=='rework_simulation.py' else mod.CONFIGS['baseline']
        assert math.isclose(mod.expected_work(config),eng.expected_work(eng.CONFIGS['baseline']))
    # Exact rectangular occupancy, departure counting and clipping at window edges.
    videos=[SimpleNamespace(arrival=.5,delivered=2.,segments=[(.5,1.5,'work','work')]),
            SimpleNamespace(arrival=2.5,delivered=None,segments=[(2.5,3.5,'work','work')])]
    sim=SimpleNamespace(videos=videos)
    m=measure(sim,1.,4.,5.,600.,321.6,25.)
    assert math.isclose(m['mean_wip'],2.5/3)
    assert m['cohort_size']==1 and m['censored']==1 and not m['stable']
    assert math.isclose(m['throughput'],22/3)
    assert math.isclose(m['busy_util'],1.5/6)
    snapshot={}
    for name in versions:
        runs=[eng.run_scenario(name,eng.CONFIGS[name],lam=17.5,months=36,warmup=16,seed=seed) for seed in (11,12,13)]
        for r in runs:
            assert r['metrics']['stable'] and not r['metrics']['censored'],(name,r['metrics'])
        mean=lambda key:statistics.mean(r[key] for r in runs)
        snapshot[name]=dict(expected_work=eng.expected_work(eng.CONFIGS[name]),
                            expected_incidence=eng.expected_incidence(eng.CONFIGS[name]),
                            lead=mean('mean_lead'),p90=mean('p90_lead'),
                            work=mean('mean_work'),rework=mean('rework_share'),
                            capacity=mean('capacity'),wip=mean('mean_wip'),
                            lead_range=[min(r['mean_lead'] for r in runs),max(r['mean_lead'] for r in runs)])
    payload=dict(demand_per_month=17.5,seeds=[11,12,13],months=36,warmup=16,cutoff_months=3,
                 calendar_days_per_working_day=CAL,available_minutes=eng.BUDGET_MIN,versions=snapshot)
    out=ROOT/'single source of truth/model-results.json'
    out.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload,indent=2))
    print('PASS: work expectations, gate incidence, copied baseline identity, calendar units, exact WIP/throughput/censoring and stable 3-seed snapshot.')

if __name__=='__main__':main()
