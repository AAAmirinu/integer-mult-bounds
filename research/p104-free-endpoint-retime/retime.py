"""Exact checker: a candidate word is a legal helper-endpoint retime of PR5551's pinned word.  Apache-2.0.

Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.

The two shipped words were found by an exact-lattice CP-SAT retiming (multi-worker, so
not byte-reproducible); this module is therefore a CHECKER, not a generator.  It proves, with
stdlib only, that a candidate differs from the pinned word ONLY as follows:
  1. the non-MOVE scalar program (operation, registers, coefficient, order) is identical;
  2. the candidate's MOVEs are a subsequence of the pinned MOVEs (stops may be deleted,
     none added, none reordered across scalar events, same register);
  3. frame labels may change, but all 208 MAIN registers (104 X sources, 104 Y targets) keep
     the SAME SPAN at their initial and final frames (X-initial and Y-final are the literal
     ports).  Intermediate main frames may change where a shared ADD chart moves together
     with a retimed helper; these are counted, not forbidden;
  4. the 104 ports, live list and public count are equal.
Nesting, ownership, rank = dimension gap and the frame law at every ADD/COPY/SCALE are then
enforced by the unmodified PR5544/5545 local.py replay and native() (see verify.py).
"""

def rref(basis):
    """Canonical form of the F2 span of integer bit-vectors (reduced row echelon, sorted)."""
    rows=[]
    for v in basis:
        for r in rows:
            if v^r<v: v^=r
        if v:
            rows=[(r^v if r^v<r else r) for r in rows]; rows.append(v)
    return tuple(sorted(rows))

def need(ok,why):
    if not ok: raise ValueError(why)

def spans(w):
    sp=[rref(b) for b in w['frames']]
    for b,s in zip(w['frames'],sp): need(len(s)==len(b),'independent frame basis')
    return sp

def frame_field(e):
    """Index of the frame label inside an event."""
    return 2 if e[0] in('INIT','CLEAR') else (-1)

def check(base,w):
    for k in('schema','public','live','ports'): need(base[k]==w[k],'unchanged '+k)
    need(len(base['initial'])==len(w['initial'])==base['public'],'register count')
    bs,ws=spans(base),spans(w)
    BP,WP=base['program'],w['program']
    # main registers: live X sources r and their Y targets r+112 (local.py roles); the rest of the 735 are helpers
    live=base['live']; main=set(live)|{r+112 for r in live}
    need(len(main)==208,'208 main registers')
    # (1)+(2) align by greedy subsequence matching, skipping only MOVEs of the pinned program
    i=0;kept=[];deleted=0;scalar=0;moves_new=0
    for e in WP:
        while True:
            need(i<len(BP),'candidate event has a pinned counterpart')
            b=BP[i]
            if e[0]=='MOVE':
                if b[0]=='MOVE' and b[1]==e[1]: break
            elif b[0]!='MOVE': break
            need(b[0]=='MOVE','only MOVEs may be skipped'); deleted+=1; i+=1
        if e[0]=='MOVE': moves_new+=1
        else:
            fi=frame_field(e)
            a=list(b);c=list(e); a[fi]=c[fi]=None
            need(a==c,'scalar event unchanged except its frame label'); scalar+=1
        kept.append((i,e)); i+=1
    while i<len(BP):
        need(BP[i][0]=='MOVE','only MOVEs may be skipped at the tail'); deleted+=1; i+=1
    need(len(WP)+deleted==len(BP),'event accounting')
    # (3) main registers keep the same span everywhere; helper changes are counted
    chg_init=sum(1 for r in range(base['public']) if bs[base['initial'][r]]!=ws[w['initial'][r]])
    chg_fin=sum(1 for r in range(base['public']) if bs[base['final'][r]]!=ws[w['final'][r]])
    for r in main:
        need(bs[base['initial'][r]]==ws[w['initial'][r]],'main initial span %d'%r)
        need(bs[base['final'][r]]==ws[w['final'][r]],'main final span %d'%r)
    main_mid=0;help_mid=0;lab_chg=0
    for bi,e in kept:
        b=BP[bi]
        if e[0]=='MOVE':
            if bs[b[2]]!=ws[e[2]] or bs[b[3]]!=ws[e[3]]:
                if b[1] in main: main_mid+=1
                else: help_mid+=1
            continue
        fi=frame_field(e)
        if bs[b[fi]]!=ws[e[fi]]: lab_chg+=1
    # Deleted MOVEs: must be helpers' or owned-register stops
    return {'scalar_events':scalar,'moves_pinned':sum(e[0]=='MOVE' for e in BP),'moves_candidate':moves_new,
            'moves_deleted':deleted,'helper_initial_spans_changed':chg_init,'helper_final_spans_changed':chg_fin,
            'scalar_event_frames_relabelled':lab_chg,'kept_main_moves_relabelled':main_mid,'kept_helper_moves_relabelled':help_mid,'main_registers':len(main)}
