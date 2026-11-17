path = "picopython_acceptance_marker.tmp"
with open(path, "w") as marker:
    marker.write("PicoPython filesystem persistence test\n")

print("Marker written. Soft-reset or power-cycle before running verify_marker.py.")
