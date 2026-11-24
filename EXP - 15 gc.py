import gc
import sys
import os

log_dir = "EXP15_Output"
os.makedirs(log_dir, exist_ok=True)

def display_memory_usage(label):
    """Display current memory usage and GC stats"""
    print(f"\n--- {label} ---")
    print(f"GC thresholds: {gc.get_threshold()}")
    print(f"GC counts: {gc.get_count()}")
    print(f"Objects tracked by GC: {len(gc.get_objects())}")

    # Force collection and show collected count
    collected = gc.collect()
    print(f"Objects collected: {collected}")

def create_objects(n):
    """Create reference cycles"""
    objects = []
    for i in range(n):
        obj = {"id": i, "data": list(range(100))}
        obj["self_ref"] = obj  # Create a reference cycle
        objects.append(obj)
    return objects

def main():
    print("=" * 50)
    print("MANUAL GARBAGE COLLECTION DEMONSTRATION")
    print("=" * 50)

    print("\nInitial GC settings:")
    print(f"  Thresholds: {gc.get_threshold()}")
    print(f"  Counts: {gc.get_count()}")

    print("\n--- Initial memory state ---")
    gc.collect()
    print(f"Objects tracked: {len(gc.get_objects())}")

    print("\n--- Creating objects with reference cycles ---")
    obj_list = create_objects(1000)
    print(f"Created 1000 objects with self-references")
    print(f"Objects tracked: {len(gc.get_objects())}")

    print("\n--- Deleting references ---")
    del obj_list
    print("Deleted reference to object list")
    print(f"Objects tracked: {len(gc.get_objects())}")

    print("\n--- Manual garbage collection ---")
    collected = gc.collect()
    print(f"Objects collected: {collected}")
    print(f"Objects tracked after GC: {len(gc.get_objects())}")

    print("\n--- GC debugging enabled ---")
    gc.set_debug(gc.DEBUG_STATS)
    collected = gc.collect()
    print(f"Objects collected with debug: {collected}")

    print("\n--- GC debugging disabled ---")
    gc.set_debug(0)
    collected = gc.collect()
    print(f"Objects collected: {collected}")

    print("\n--- Changing GC thresholds ---")
    original_thresholds = gc.get_threshold()
    print(f"Original thresholds: {original_thresholds}")
    gc.set_threshold(500, 5, 5)
    print(f"New thresholds: {gc.get_threshold()}")

    print("\n--- Disabling GC ---")
    gc.disable()
    print(f"GC enabled: {gc.isenabled()}")
    obj_list2 = create_objects(100)
    del obj_list2
    collected = gc.collect()
    print(f"Objects collected (GC disabled): {collected}")

    print("\n--- Re-enabling GC ---")
    gc.enable()
    print(f"GC enabled: {gc.isenabled()}")
    collected = gc.collect()
    print(f"Objects collected (GC re-enabled): {collected}")

    gc.set_threshold(*original_thresholds)
    print(f"\nRestored original thresholds: {gc.get_threshold()}")

    print("\n" + "=" * 50)
    print("DEMONSTRATION COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
