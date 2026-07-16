import sys
print("=== AQARION TOOLCHAIN VERIFY ALL ===")
from src.registry_loader import main as reg_main
from src.dependency_graph import main as graph_main
from src.manifest import main as manifest_main
from src.lean_bridge import main as lean_main
from src.zocpu_attack import main as zocpu_main
try:
    rh = reg_main()
    gh = graph_main()
    mh = manifest_main()
    lean_main()
    zocpu_main()
    print("\n=== ALL AQTC 001-007 PASS ===")
    print(f"Registry hash: {rh}")
    print(f"Graph hash: {gh}")
    print(f"Manifest hash: {mh}")
    sys.exit(0)
except Exception as e:
    print(f"VERIFY FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

