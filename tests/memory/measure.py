import gc

gc.collect()
print("GC heap total:", gc.mem_free() + gc.mem_alloc())
print("GC heap free:", gc.mem_free())
print("GC heap allocated:", gc.mem_alloc())
