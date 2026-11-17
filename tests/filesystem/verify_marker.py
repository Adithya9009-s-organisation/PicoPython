path = "picopython_acceptance_marker.tmp"
with open(path) as marker:
    assert marker.read() == "PicoPython filesystem persistence test\n"

print("PicoPython filesystem persistence test: PASS")
