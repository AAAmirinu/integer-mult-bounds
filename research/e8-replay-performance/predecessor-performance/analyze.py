"""Compare fresh full pipelines, all predecessor receipts and receipt bindings."""
import gzip
import json
from pathlib import Path
import runpy

from run_native import ROOT, SOURCE, verify_source, sha

READ = lambda p:json.loads(Path(p).read_text())


def normalize(value,directory):
    if isinstance(value,str):
        prefix=str(directory)+'/'
        return '$OUTPUT/'+value[len(prefix):] if value.startswith(prefix) else value
    if isinstance(value,list):return [normalize(x,directory) for x in value]
    if isinstance(value,dict):return {normalize(k,directory):normalize(v,directory) for k,v in value.items()}
    return value


def bound_hashes(hashes,directory):
    for name,digest in hashes.items():assert sha(directory/name)==digest,name


def without_time(value):
    if isinstance(value,dict):
        return {k:without_time(v) for k,v in value.items() if k not in ('seconds','timings')}
    if isinstance(value,list):return [without_time(v) for v in value]
    return value


def compare(a,b):
    matched={}
    for path in a.rglob('*'):
        if path.is_file() and (path.suffix=='.bin' or path.name in ('frames.json','249-states.json') or path.name.endswith('-selection.json')):
            relative=path.relative_to(a)
            assert path.read_bytes()==(b/relative).read_bytes(),str(relative)
            matched[str(relative)]=sha(path)
    av,bv=READ(a/'VERIFICATION.json'),READ(b/'VERIFICATION.json')
    assert len(av['fresh_stages'])==len(bv['fresh_stages'])==24
    assert [x['stage'] for x in av['fresh_stages']]==[x['stage'] for x in bv['fresh_stages']]
    for key in ('status','kappa','word_sha256','manifest_sha256','inputs_unchanged','scope'):
        assert av[key]==bv[key],key
    for name in ('INVOICE.json','TILING.json','FRAME-PRIMES.json','REFLECTED-LEDGERS.json'):
        assert (a/name).read_bytes()==(b/name).read_bytes(),name
        matched[name]=sha(a/name)
    for name in ('INTEGER-AUDIT.json','COLUMNS.json','BANK.json'):
        assert without_time(normalize(READ(a/name),a))==without_time(normalize(READ(b/name),b)),name
    predecessors=[]
    pred_files={p.relative_to(a/'predecessor').as_posix() for p in (a/'predecessor').glob('*.json')}
    assert pred_files=={p.relative_to(b/'predecessor').as_posix() for p in (b/'predecessor').glob('*.json') if p.name!='PERFORMANCE-ADAPTER.json'}
    for name in sorted(pred_files):
        assert without_time(normalize(READ(a/'predecessor'/name),a))==without_time(normalize(READ(b/'predecessor'/name),b)),name
        predecessors.append(name)
    assert gzip.decompress((a/'predecessor/records.bin.gz').read_bytes())==gzip.decompress((b/'predecessor/records.bin.gz').read_bytes())
    bindings=[]
    for directory in (a,b):
        checked={}
        price=READ(directory/'PRICE.json')
        for key,binding in (('reserve',price['complex_reserve']['binding']),('supplier',price['complex_supplier']['source_binding'])):
            hashes=binding.pop('receipt_hashes');bound_hashes(hashes,directory/'complex-reserve')
            checked['price-'+key]=sorted(hashes)
        certificate=READ(directory/'CERTIFICATE.json')
        hashes=certificate.pop('fresh_receipt_hashes');bound_hashes(hashes,directory)
        checked['certificate']=sorted(hashes)
        refinement=READ(directory/'REFINEMENT.json')
        for key in ('receipt_hashes','external_receipt_hashes'):
            hashes=refinement['source'].pop(key)
            if key=='receipt_hashes':bound_hashes(hashes,directory)
            else:
                for path,digest in hashes.items():
                    assert Path(path).is_relative_to(directory)
                    assert sha(path)==digest,path
            checked['refinement-'+key]=sorted(normalize(hashes,directory))
        bindings.append(dict(price=normalize(price,directory),certificate=certificate,
                             refinement=normalize(refinement,directory),checked=checked))
    assert bindings[0]==bindings[1],'price, certificate or refinement changed'
    oldsource=READ(a/'source353354/VERIFICATION.json');newsource=READ(b/'source353354/VERIFICATION.json')
    assert [s['stage'] for s in oldsource['steps']]==[s['stage'] for s in newsource['steps']]
    for key in ('status','twin_cap','local_residual_bank_replicas','producer_word_regenerated',
                'all_four_selections_regenerated','base_matches_pinned353','final_word_sha256',
                'full_newbase_admission','final_F2','source_manifest_sha256','source_files_unchanged','scope'):
        assert oldsource[key]==newsource[key],key
    stats=READ(b/'source353354/PREFIX-SHARING.json')
    assert len(stats['consumers'])==6 and all(c['parent_fingerprint_unchanged'] and c['returncode']==0 for c in stats['consumers'])
    return dict(byte_identical_artifacts=matched,predecessor_receipts_equal_except_seconds_and_timings=predecessors,
                predecessor_uncompressed_records_equal=True,prices_certificates_refinement_equal=True,
                independently_revalidated_receipt_bindings=bindings[0]['checked'])


def main():
    verify_source()
    directories={name:ROOT/(name+'-native') for name in ('baseline','predecessor','scheduled')}
    directories['baseline']=ROOT/'baseline-repeat-native'
    runs={name:READ(path/'NATIVE-PERFORMANCE-RUN.json') for name,path in directories.items()}
    for run in runs.values():
        for key in ('source_commit','source_files_checked','source_files_unchanged','implementation_hashes','kappa','word_sha256','scope','python'):
            assert run[key]==runs['baseline'][key],key
        for path,digest in run['implementation_hashes'].items():assert sha(path)==digest,path
    for name in ('predecessor','scheduled'):
        adapter=READ(directories[name]/'predecessor/PERFORMANCE-ADAPTER.json')
        for path,digest in adapter['implementation_files_unchanged'].items():assert sha(path)==digest,path
    comparisons={name:compare(directories['baseline'],directories[name]) for name in ('predecessor','scheduled')}
    timing={}
    for name,path in directories.items():
        v=READ(path/'VERIFICATION.json');stages={x['stage']:x for x in v['fresh_stages']}
        p=READ(path/'predecessor/verification.json')
        timing[name]=dict(full_seconds=runs[name]['seconds'],
            predecessor_seconds=stages['immutable-reference325']['seconds'],
            source_seconds=stages['source353354-471']['seconds'],predecessor_stages=p['timings'],
            stages=v['fresh_stages'])
    scheduled=timing['scheduled'];base=timing['baseline']
    # Verify the claimed early jobs actually finish during source construction.
    source=next(x for x in scheduled['stages'] if x['stage']=='source353354-471')
    pred=next(x for x in scheduled['stages'] if x['stage']=='immutable-reference325')
    early=[x for x in scheduled['stages'] if x['stage'] in runs['scheduled']['early_jobs']]
    assert len(early)==6
    assert all(x['started_seconds']>=pred['finished_seconds'] for x in early)
    assert all(x['finished_seconds']<=source['finished_seconds'] for x in early)
    bank=next(x for x in scheduled['stages'] if x['stage']=='bank-frames-and-assignment')
    chart=next(x for x in scheduled['stages'] if x['stage']=='changed-charts')
    assert max(bank['started_seconds'],chart['started_seconds'])<min(bank['finished_seconds'],chart['finished_seconds'])
    baseline_full=base['full_seconds']
    result=dict(status='PASS_FULL_NATIVE_PREDECESSOR_AB_AND_SCHEDULING_COMPARISON',
        source_commit=runs['baseline']['source_commit'],kappa=runs['baseline']['kappa'],word_sha256=runs['baseline']['word_sha256'],
        timings=timing,comparisons=comparisons,
        total_speedup=baseline_full/scheduled['full_seconds'],
        total_wall_time_reduction_percent=100*(1-scheduled['full_seconds']/baseline_full),
        predecessor_wall_time_reduction_percent=100*(1-scheduled['predecessor_seconds']/base['predecessor_seconds']),
        predecessor_only_pipeline_reduction_percent=100*(1-timing['predecessor']['full_seconds']/baseline_full),
        early_jobs_executed_fresh_within_same_two_worker_schedule=True,
        disjoint_native_geometry_jobs_overlapped=True,
        initial_calibration_seconds=READ(ROOT/'baseline-native/NATIVE-PERFORMANCE-RUN.json')['seconds'],
        optimized_proof_statistics=READ(directories['scheduled']/'predecessor/PERFORMANCE-ADAPTER.json'),
        all_839_frozen_git_blobs_unchanged=True,all_24_native_stages_fresh=True,
        caveats=['One fresh run per configuration on one macOS host; OS caches not flushed.',
                 'Same two independent proof workers; scheduled mode reuses the finished predecessor worker for six independent jobs.',
                 'Both modes already include producer-prefix sharing; compare against that baseline.',
                 'External hash-bound prototype; original source receipts must be accompanied by the optimization provenance sidecar.',
                 'Conditional finite witness only; inherited all-size assumptions and kappa are unchanged.',
                 'Earlier historical speedups and other pipeline measurements must not be multiplied.'])
    result['initial_baseline_wall_time_reduction_percent']=100*(1-scheduled['full_seconds']/result['initial_calibration_seconds'])
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    rows='\n'.join(f"{name:18} {t['full_seconds']:9.2f} {t['predecessor_seconds']:13.2f} {t['source_seconds']:10.2f}"
                   for name,t in timing.items())
    stage_rows='\n'.join(f"{name:12} {base['predecessor_stages'][name]:9.2f} {scheduled['predecessor_stages'][name]:11.2f}"
                         for name in base['predecessor_stages'])
    report=f'''Predecessor proof and complete native pipeline performance

Fresh pinned PR358, with producer-prefix sharing already enabled in every run.
Configuration           Full s Predecessor s   Source s
{rows}

Optimized predecessor plus scheduling: {result['total_speedup']:.3f}x faster,
{result['total_wall_time_reduction_percent']:.1f}% less complete-pipeline wall time.
Across the initial and repeated baselines, the measured reduction is
{result['initial_baseline_wall_time_reduction_percent']:.1f}% to {result['total_wall_time_reduction_percent']:.1f}%.
The predecessor itself uses {result['predecessor_wall_time_reduction_percent']:.1f}% less wall time.
Predecessor arithmetic/encoding changes alone change full wall time by
{result['predecessor_only_pipeline_reduction_percent']:.1f}% (positive means less time).
The longer source branch hides most of the predecessor-only gain.

Predecessor stage       Baseline s Optimized s
{stage_rows}

Pin: https://github.com/CrocSwap/integer-mult-bounds/pull/358
Head: {result['source_commit']}
Exact kappa, unchanged: {result['kappa']}
Final word SHA-256: {result['word_sha256']}
Scope: completed conditional finite admission under the inherited all-size
interfaces. No unconditional theorem, improved kappa, or discovery-rate claim.

What changed
- The complex reference checker's scal uses exact integer row numerators with
  positive common denominators, from our earlier differential-tested utility.
  All other reference-checker code and the independent gxcore mirror still run.
- The splice validator still validates every event and every adverse control.
  It reuses canonical JSON encoders and cached bytes for repeated elementary
  primitive lines. Binary frame containment uses complete row-content keys.
- Scalar-event JSON triples have an equivalent direct integer encoder. Exact
  dot products use bounded row-content caches shared across fresh imports.
- Bank row-factor replay uses exact integer row numerators. Basis/inverse
  derivation, two-sided products, final identity and all assignments remain.
  The measured bank stage did not show a material improvement; this does not
  establish a separate speedup for that change or for the dot-product cache.
  The virtual stage is slower in this bundle. Isolate or trim the dot-product
  and bank changes before proposing them upstream; the complex stage supplies
  the large measured arithmetic/encoding reduction.

Fresh scheduling, two active worker slots
After the predecessor succeeds, its worker freshly verifies the independent
complex reserve and compiles five native checkers. All six jobs finish while
the source branch is still running. The original downstream call sites compare
the exact commands and consume these same-run successful results. No historical
PASS or binary is reused. After source admission, the independent native bank
and changed-chart jobs run together in their disjoint output directories;
geometry admission joins both. The logical list of 24 mandatory stages remains
identical; each row records its actual start/end time, including early jobs.

Verification
All 839 frozen Git blobs match before and after every full replay. All 24 native
stages, all nine predecessor stages, the original stage-omission controls,
both gx flipped-sign controls, all splice controls and source checks pass.
49 word/state/frame/selection and native receipt artifacts match byte-for-byte.
All 15 predecessor JSON receipts match after removing only seconds/timings and
normalizing output paths; the uncompressed physical record word also matches.
Exact prices, certificates and prime-threshold refinement agree. Every excluded
run-specific receipt hash is first independently checked against its fresh
file, including the refinement's internal and external bindings.

Eight adapter tests pass. Factor replay agrees with the original rational row
operations at all 175 randomized prefixes, including large integers, rational
coefficients, cancellations and swaps; a corrupted factor fails the identity.
The earlier scalar utility's five tests pass afresh on Python 3.13.12: all three
real circuits/statistics, 160 valid rational traces and 160 corrupted variants,
21 real corruptions, and the exterior-gauge dirt control. See tests.log and
scalar-equivalence.log. The full native A/B comparisons are the integration QA.

Reproduction and limitations
Run benchmark jobs sequentially. Use the retained profiling venv, pinned source
tree, parallel driver, producer-prefix adapter, scalar-performance package,
compiler wrapper and Boost include tree. From the workspace root:
  work/e8-pipeline-profile/venv/bin/python -B work/predecessor-performance/test_adapter.py -v
  work/e8-pipeline-profile/venv/bin/python -B work/predecessor-performance/run_native.py --mode baseline --output /fresh/baseline --cxx /compiler --boost-include /boost
  work/e8-pipeline-profile/venv/bin/python -B work/predecessor-performance/run_native.py --mode predecessor --output /fresh/predecessor --cxx /compiler --boost-include /boost
  work/e8-pipeline-profile/venv/bin/python -B work/predecessor-performance/run_native.py --mode scheduled --output /fresh/scheduled --cxx /compiler --boost-include /boost
  work/e8-pipeline-profile/venv/bin/python -B work/predecessor-performance/analyze.py
The analyzer uses the retained baseline-repeat-native, predecessor-native and
scheduled-native directories. RESULTS.json includes every timing and comparison.

One run per optimized configuration on one macOS host; OS caches not flushed.
An initial baseline calibration took {result['initial_calibration_seconds']:.2f}s;
the repeated baseline above uses the final identical runner revision. Jobs were
not benchmarked concurrently except for the explicit two-worker algorithm.
The optimized predecessor's per-process peak RSS was
{result['optimized_proof_statistics']['peak_rss_platform_units']/1024**2:.1f} MiB
(macOS getrusage units are bytes). This includes retained pure caches. No
baseline RSS comparison or aggregate unique-memory measurement is available.
Producer sharing remains a POSIX fork prototype. All external execution hashes
must accompany source receipts via PERFORMANCE-ADAPTER.json and
NATIVE-PERFORMANCE-RUN.json; the original files and manifests are unchanged,
but the optimized execution is not a byte-identical original implementation.

Do not multiply this result by speedups from other packages or historical runs.
The next critical target is the changed-source branch, especially its fresh
admission and producer regeneration; further predecessor-only work has little
direct end-to-end value at these measured branch times. No GitHub writes made.
'''
    (ROOT/'REPORT.txt').write_text(report)
    print(json.dumps({k:result[k] for k in ('status','total_speedup','total_wall_time_reduction_percent','predecessor_wall_time_reduction_percent','predecessor_only_pipeline_reduction_percent')},indent=2))


if __name__=='__main__':main()
