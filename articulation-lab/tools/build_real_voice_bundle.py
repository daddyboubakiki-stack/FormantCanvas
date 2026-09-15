#!/usr/bin/env python3
"""Build redistribution-safe vowel samples for Articulation Lab v0.4.3.

Japanese source files contain several very short kana repetitions separated by silence,
so midpoint cropping is unsafe. This build detects a genuinely voiced token, keeps a
small onset/offset margin, duration-equalizes it toward ~0.50 s with pitch-preserving
`atempo`, and active-RMS matches every exported button sample.

English buttons mostly use the CC0 isolated IPA-vowel reference. KIT /ɪ/ is intentionally
an exception: v0.4.3 takes the naturally short vowel nucleus from Dvortygirl's US-English
"kid" recording, excludes the /k/ aspiration and /d/ closure, does not time-stretch it,
and applies only short edge fades plus level matching.

The build fails closed when a bundled teaching sample is suspiciously quiet or loud.
"""
from __future__ import annotations
import argparse, array, audioop, json, math, subprocess, sys, wave
from pathlib import Path

IPA_SEQUENCE = ["a","æ","ɛ","e̞","e","ɪ","i","y","ʏ","ø","ø̞","œ","ɶ","ä","ɐ","ɜ","ə","ɘ","ɪ̈","ɨ","ʉ","ʊ̈","ɵ̞","ɞ","ɞ̞","ɒ̈","ɑ","ʌ","ɤ̞","ɤ","ʊ","ɯ","u","o","o̞","ɔ","ɒ"]
# /ɪ/ is deliberately omitted here; it is built from the US-English word "kid" below.
IPA_EXPORTS = {6:"i.wav",2:"epsilon.wav",1:"ae.wav",27:"turned_v.wav",16:"schwa.wav",26:"alpha.wav",35:"open_o.wav",30:"U.wav",32:"u.wav"}
JP_EXPORTS = {"a":"jp_a.ogg","i":"jp_i.ogg","u":"jp_u.ogg","e":"jp_e.ogg","o":"jp_o.ogg"}
TARGET_ACTIVE_RMS_DBFS = -16.5
JP_TARGET_DURATION = 0.50
KIT_START = 0.205
KIT_DURATION = 0.110


def run(*args):
    return subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


def duration(path):
    return float(run("ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(path)))


def decode_analysis(src, dst):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),"-ac","1","-ar","16000","-c:a","pcm_s16le",str(dst)], check=True)


def pcm_frames(path, frame_ms=10):
    with wave.open(str(path),"rb") as wf:
        raw=wf.readframes(wf.getnframes()); rate=wf.getframerate()
        if wf.getnchannels()!=1 or wf.getsampwidth()!=2: raise RuntimeError("analysis WAV must be mono 16-bit PCM")
    n=max(2,int(rate*frame_ms/1000)*2); out=[]
    for pos in range(0,len(raw),n):
        chunk=raw[pos:pos+n]
        if len(chunk)<2: continue
        r=audioop.rms(chunk,2)
        out.append(-120.0 if r<=0 else 20*math.log10(r/32768.0))
    return out


def close_gaps(active, max_gap):
    out=active[:]; i=0
    while i<len(out):
        if out[i]: i+=1; continue
        j=i
        while j<len(out) and not out[j]: j+=1
        if i>0 and j<len(out) and j-i<=max_gap:
            for k in range(i,j): out[k]=True
        i=j
    return out


def segments(active, min_frames):
    out=[]; i=0
    while i<len(active):
        if not active[i]: i+=1; continue
        j=i+1
        while j<len(active) and active[j]: j+=1
        if j-i>=min_frames: out.append((i,j))
        i=j
    return out


def render_clip(src,dst,start,dur,stretch=1.0,fade_in=0.018,fade_out=0.040):
    """Trim before tempo processing so stretched audio is not truncated."""
    dst.parent.mkdir(parents=True,exist_ok=True)
    total=duration(src); start=max(0.0,start); dur=min(dur,max(0.05,total-start))
    stretch=max(0.5,min(4.0,float(stretch))); tempo=1.0/stretch
    filters=[f"atrim=duration={dur:.6f}","asetpts=PTS-STARTPTS"]
    while tempo<0.5:
        filters.append("atempo=0.5"); tempo/=0.5
    if abs(tempo-1.0)>1e-4: filters.append(f"atempo={tempo:.6f}")
    expected=max(0.05,dur*stretch)
    fade_in=max(0.0,min(float(fade_in),expected*.25))
    fade_out=max(0.0,min(float(fade_out),expected*.30))
    if fade_in>0: filters.append(f"afade=t=in:st=0:d={fade_in:.4f}")
    if fade_out>0: filters.append(f"afade=t=out:st={max(0.0,expected-fade_out):.4f}:d={fade_out:.4f}")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{start:.4f}","-i",str(src),"-ac","1","-ar","24000","-af",",".join(filters),"-c:a","pcm_s16le",str(dst)],check=True)


def _level_stats(path):
    with wave.open(str(path),"rb") as wf:
        params=wf.getparams(); raw=wf.readframes(wf.getnframes())
    s=array.array("h"); s.frombytes(raw)
    if sys.byteorder!="little": s.byteswap()
    fl=max(1,int(params.framerate*.01)); frames=[]
    for i in range(0,len(s),fl):
        c=s[i:i+fl]
        if not c: continue
        rms=math.sqrt(sum(float(v)*v for v in c)/len(c))
        db=-120 if rms<=0 else 20*math.log10(rms/32768)
        frames.append((i,min(len(s),i+fl),db))
    maxdb=max((x[2] for x in frames),default=-120); threshold=max(-45,maxdb-24)
    active=[x for x in frames if x[2]>threshold]
    ss=0.0; n=0
    for a,b,_ in active:
        for v in s[a:b]: ss+=float(v)*v; n+=1
    rms=math.sqrt(ss/max(1,n)) if n else 0.0
    active_db=-120 if rms<=0 else 20*math.log10(rms/32768)
    peak=max((abs(v) for v in s),default=0)/32768
    peak_db=-120 if peak<=0 else 20*math.log10(peak)
    return params,s,threshold,active_db,peak,peak_db


def level_match(path,target=TARGET_ACTIVE_RMS_DBFS):
    params,s,threshold,db,peak,peak_db=_level_stats(path)
    if db<=-119: return {"reason":"no_active_frames","appliedGainDb":0,"postActiveRmsDbfs":db,"postPeakDbfs":peak_db}
    wanted=10**((target-db)/20); head=(10**(-1.5/20))/max(peak,1e-9)
    gain=max(.25,min(wanted,head,16.0))
    for i,v in enumerate(s): s[i]=int(max(-32768,min(32767,round(v*gain))))
    if sys.byteorder!="little": s.byteswap()
    with wave.open(str(path),"wb") as wf: wf.setparams(params); wf.writeframes(s.tobytes())
    _,_,post_threshold,post_db,_,post_peak_db=_level_stats(path)
    return {
        "activeRmsBeforeDbfs":db,"targetActiveRmsDbfs":target,"thresholdDbfs":threshold,
        "appliedGainDb":20*math.log10(gain),"peakBeforeDbfs":peak_db,
        "postThresholdDbfs":post_threshold,"postActiveRmsDbfs":post_db,"postPeakDbfs":post_peak_db
    }


def validate_export(path, *, kind, label):
    d=duration(path); _,_,_,active_db,_,peak_db=_level_stats(path)
    if kind=="japanese" and not (0.38 <= d <= 0.62):
        raise RuntimeError(f"{label}: Japanese button duration {d:.3f}s outside 0.38..0.62s")
    if kind=="kit" and not (0.09 <= d <= 0.16):
        raise RuntimeError(f"{label}: natural KIT nucleus duration {d:.3f}s outside 0.09..0.16s")
    if active_db < -19.0:
        raise RuntimeError(f"{label}: post-normalization active RMS too quiet ({active_db:.2f} dBFS)")
    if active_db > -14.0:
        raise RuntimeError(f"{label}: post-normalization active RMS too loud ({active_db:.2f} dBFS)")
    if peak_db < -15.0:
        raise RuntimeError(f"{label}: suspiciously low peak ({peak_db:.2f} dBFS)")
    return {"duration":d,"activeRmsDbfs":active_db,"peakDbfs":peak_db}


def detect_jp(src,work,key):
    wav=work/f"jp_{key}_analysis.wav"; decode_analysis(src,wav); dbs=pcm_frames(wav)
    peak=max(dbs); choices=[]
    for drop in (16,18,20,22,24,26,28):
        th=max(-52,peak-drop)
        for gap in (2,3,4,5):
            segs=[s for s in segments(close_gaps([d>th for d in dbs],gap),4) if s[1]-s[0]<=80]
            for a,b in segs:
                level=sum(dbs[a:b])/(b-a); score=(b-a)+.12*(level-th)-(.15 if a==0 or b>=len(dbs) else 0)
                choices.append((score,th,gap,a,b,segs))
    if not choices: raise RuntimeError(f"no voiced token: {key}")
    score,th,gap,a,b,segs=max(choices,key=lambda x:x[0])
    return (a*.01,b*.01),{"frameMs":10,"peakDbfs":peak,"thresholdDbfs":th,"closedGapMs":gap*10,"selectedStart":a*.01,"selectedEnd":b*.01,"selectedDuration":(b-a)*.01,"detectedSegments":[{"start":x*.01,"end":y*.01,"duration":(y-x)*.01} for x,y in segs],"selectionScore":score}


def build_jp(src,dst,work,key):
    total=duration(src); (a,b),det=detect_jp(src,work,key); token=b-a
    start=max(0,a-.035); end=min(total,b+.035); raw=end-start
    stretch=min(4.0,max(1.0,JP_TARGET_DURATION/max(.08,raw)))
    render_clip(src,dst,start,raw,stretch)
    level=level_match(dst)
    validation=validate_export(dst,kind="japanese",label=f"JP /{key}/")
    return {
        "sourceDuration":total,"clipStart":start,"clipDurationBeforeStretch":raw,
        "selectedVoicedDuration":token,"targetDuration":JP_TARGET_DURATION,"stretchFactor":stretch,
        "outputDuration":duration(dst),"processing":"voiced-token-detection + pitch-preserving atempo + active-RMS match",
        "detection":det,"levelMatch":level,"validation":validation
    }


def detect_ipa(src,work):
    wav=work/"all_ipa_analysis.wav"; decode_analysis(src,wav); dbs=pcm_frames(wav); choices=[]
    for th in (-45,-42,-40,-38,-36,-34,-32,-30,-28,-26,-24):
        for gap in (4,6,8,10,12,15,18,22):
            seg=[s for s in segments(close_gaps([d>th for d in dbs],gap),14) if s[1]-s[0]<=160]
            choices.append((abs(len(seg)-37),th,gap,seg))
    score,th,gap,segs=min(choices,key=lambda x:(x[0],abs(x[1]+34),x[2]))
    if len(segs)!=37: raise RuntimeError(f"IPA segmentation failed: {len(segs)}")
    sec=[(a*.01,b*.01) for a,b in segs]
    return sec,{"frameMs":10,"thresholdDbfs":th,"closedGapMs":gap*10,"detectedCount":len(segs),"expectedCount":37,"candidateScore":score,"segments":[{"index":i,"ipa":IPA_SEQUENCE[i],"start":a,"end":b,"duration":b-a} for i,(a,b) in enumerate(sec)]}


def build_kit(src,dst):
    # Manual boundary inspection of En-us-kid.ogg:
    # ~0.09–0.20 s = /k/ release/aspiration; ~0.205–0.315 s = voiced KIT nucleus;
    # after ~0.32 s the /d/ closure begins. Preserve the natural short duration.
    render_clip(src,dst,KIT_START,KIT_DURATION,stretch=1.0,fade_in=.006,fade_out=.010)
    level=level_match(dst)
    validation=validate_export(dst,kind="kit",label="US English KIT /ɪ/ from kid")
    return {
        "sourceFile":"en_us_kid.ogg","sourceWord":"kid","sourceDuration":duration(src),
        "clipStart":KIT_START,"clipDuration":KIT_DURATION,"stretchFactor":1.0,
        "processing":"manual acoustic boundary selection + 6 ms fade-in + 10 ms fade-out + active-RMS match; no time-stretch",
        "output":"en_us_word_reference/I.wav","outputDuration":duration(dst),
        "levelMatch":level,"validation":validation
    }


def build(args):
    src=Path(args.source_dir); out=Path(args.output_dir); work=Path(args.work_dir)
    out.mkdir(parents=True,exist_ok=True); work.mkdir(parents=True,exist_ok=True)
    report={"version":"v0.4.3","normalizationTargetActiveRmsDbfs":TARGET_ACTIVE_RMS_DBFS,"japanese":{},"ipaReference":{},"englishWordReference":{}}
    for key,fn in JP_EXPORTS.items():
        info=build_jp(src/fn,out/"jp_reference"/f"{key}.wav",work,key)
        info.update({"sourceFile":fn,"output":f"jp_reference/{key}.wav"}); report["japanese"][key]=info
    ipa=src/"all_ipa.ogg"; segs,det=detect_ipa(ipa,work); report["ipaReference"]={"detection":det,"exports":{}}
    total=duration(ipa)
    for idx,fn in IPA_EXPORTS.items():
        a,b=segs[idx]; clip=min(.60,max(.38,(b-a)+.05)); center=(a+b)/2; start=max(0,min(total-clip,center-clip/2))
        dst=out/"ipa_reference"/fn; render_clip(ipa,dst,start,clip); lvl=level_match(dst)
        validation=validate_export(dst,kind="english",label=f"IPA /{IPA_SEQUENCE[idx]}/")
        report["ipaReference"]["exports"][IPA_SEQUENCE[idx]]={
            "sequenceIndex":idx,"segmentStart":a,"segmentEnd":b,"clipStart":start,"clipDuration":clip,
            "output":f"ipa_reference/{fn}","outputDuration":duration(dst),"levelMatch":lvl,"validation":validation
        }
    report["englishWordReference"]["ɪ"]=build_kit(src/"en_us_kid.ogg",out/"en_us_word_reference"/"I.wav")
    (out/"build-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    return report


def main():
    p=argparse.ArgumentParser(); p.add_argument("--source-dir",required=True); p.add_argument("--output-dir",required=True); p.add_argument("--work-dir",required=True)
    print(json.dumps(build(p.parse_args()),ensure_ascii=False,indent=2))


if __name__=="__main__": main()
