import numpy as np, math, json, pathlib
def spectral_case(m,k,s):
    n=m*k
    K=np.zeros((n,n),float)
    for i in range(n): K[i,(i+s)%n]=1.0
    P=np.zeros((n,n),float)
    for b in range(m): P[b*k:(b+1)*k,b*k:(b+1)*k]=1.0/k
    U=np.zeros((n,m),float)
    for b in range(m): U[b*k:(b+1)*k,b]=1.0/math.sqrt(k)
    A=(np.eye(n)-P)@K@P@U
    r=s%k; alpha2=r*(k-r)/(k*k); alpha=math.sqrt(alpha2)
    pred_trace=2*m*alpha2
    pred_norm=2*alpha if m%2==0 else (2*alpha*math.cos(math.pi/(2*m)) if alpha>0 else 0.0)
    actual_trace=float(np.trace(A.T@A))
    actual_norm=float(np.linalg.norm(A,2))
    return abs(actual_trace-pred_trace), abs(actual_norm-pred_norm)

def main():
    max_t=0.0; max_n=0.0; cases=0
    for k in range(2,12):
        for m in range(2,15):
            for s in range(1,m*k):
                if s%k==0: continue
                et,en=spectral_case(m,k,s)
                max_t=max(max_t,et); max_n=max(max_n,en); cases+=1
    print(f"total={cases}")
    print(f"Trace max err {max_t:.3e}")
    print(f"Op-norm max err {max_n:.3e}")
    receipt={"contract":"SV-001-V2","cases":cases,"max_trace_err":max_t,"max_norm_err":max_n,"status":"REPLAYED" if cases==5720 and max_t<1e-12 and max_n<1e-12 else "FAILED","governance":"C4=BLOCKED"}
    pathlib.Path("receipts").mkdir(exist_ok=True)
    pathlib.Path("receipts/SV-001-V2.json").write_text(json.dumps(receipt,indent=2))
    assert cases==5720 and max_t<1e-12 and max_n<1e-12
    print("REPLAY HARNESS v13.1: ALL CHECKS PASS - 5720-case exact")
if __name__=="__main__": main()
