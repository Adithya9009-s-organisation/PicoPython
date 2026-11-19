# PicoPython Phase 2 final validation

This report supersedes the earlier "hardware validation pending" statements
in `STDLIB_PHASE2_RESULTS.md`. Physical test outcomes below are user-reported;
the host-side artifact, source, and patch checks were verified separately.
No firmware was flashed during this audit.

## Candidate and hardware validation

- Firmware: MicroPython v1.29.0, RP2 port, candidate board `PICO_PYTHON`.
- Physical device: Raspberry Pi Pico 2, reported by the user. The build
  configuration identifies the image as `pico2` / RP2350 ARM Secure; no
  device serial number or silicon ID was supplied.
- The user reports all nine selected modules passed physical testing, with
  **231 tests passed and zero unexpected failures**. Per-module counts,
  individual test output, and a device-side UF2 readback were not supplied.

| Module | Physical result | Native Phase 2 regression coverage |
|---|---|---|
| `string` | Pass (user-reported) | `test_modules.py`; upstream `string/test_translate.py` |
| `statistics` | Pass (user-reported) | `test_modules.py` |
| `pathlib` | Pass (user-reported) | `test_modules.py` |
| `shutil` | Pass (user-reported) | `test_modules.py` |
| `logging` | Pass (user-reported) | `test_modules.py` |
| `unittest` | Pass (user-reported) | `test_modules.py` |
| `copy` | Pass (user-reported) | `test_modules.py` |
| `functools` | Pass (user-reported) | `test_functools.py` |
| `itertools` | Pass (user-reported) | `test_itertools.py`; upstream `itertools/test_itertools.py` |

The focused native suite also passed `test_functools.py`, `test_itertools.py`,
`test_modules.py`, and the two upstream string/itertools tests. The
`islice`-exhaustion and independent-`tee` regression cases passed.

### GC heap

No post-Phase-2 Pico heap total/free/allocated values were included with the
physical test report. Therefore target heap impact remains unquantified.
For context only, the previously documented pre-Phase-2 firmware observation
was 487,680 B total, 482,016 B free, and 5,664 B allocated after collection;
it is not a measurement of this candidate.

## Firmware artifact and build

- Preserved candidate UF2:
  `builds/stdlib-nine-itertools-fix/firmware.uf2`
- Versioned release path:
  `releases/v1.29.0/PicoPython-v1.29.0-stdlib-nine.uf2`
- Size: **668,160 bytes**
- SHA256: **`bb8ac649cc398b5b33b3683993e6eb7a0363f0f53a6bb8cf26cbe6049ae0ffa1`**
- This is the locally preserved candidate associated with the reported
  hardware validation. The hash was recomputed from the saved UF2; it was not
  read back from the Pico.
- All nine selected modules were verified in the final generated frozen
  module table.
- Build target: `pico2` / `rp2350-arm-s`.
- Candidate ELF text/data/BSS: 344,028 / 0 / 4,508 B.
- Candidate linker FLASH/RAM: 333,792 / 22,612 B.

The paired production-manifest build produced a 626,688 B UF2
(SHA256 `8ff0b4addd351544bd722ccb96e7ccef7bb75853a60bef00418cfceec42e3ef4`),
with ELF text/data/BSS 323,280 / 0 / 4,508 B and linker FLASH/RAM
313,044 / 22,612 B. The candidate delta is +41,472 B UF2 and +20,748 B
linker FLASH; linker RAM and ELF data/BSS are unchanged. The paired baseline
hash differs from the previously published rollback image hash
`2c610c7f061e0989dd80b849f4dfa5deb88392d1d78202897263468b171861a6` despite
the same UF2 size. Earlier Phase 2 reports also recorded different baseline
and candidate measurements; that historical reproducibility discrepancy
remains unresolved. The current candidate artifact's own size and hash are
verified.

## `functools` audit and recommendations

The pinned implementation is at micropython-lib commit
`ee4bb8ff139e24c42b739935fbd8ec7c4d061e02`. Its `functools.py` matches that
commit exactly (SHA256
`f811082eb285d10fc412cfb91f1096a5aa5acb9cc4c67db26a11da67a78d048e`);
there is no PicoPython `functools` source patch.

- **Empty `reduce` without an initializer:** the upstream implementation calls
  `next()` directly, so an empty iterable raises `StopIteration`; CPython
  raises `TypeError` ("reduce() of empty iterable with no initial value").
  Executing the pinned source confirms this difference. **Recommendation:
  fix with a focused exception translation and regression test before claiming
  this edge case is CPython-compatible.** The current passing suite does not
  exercise it.
- **`partial.func` / `.args` introspection:** the upstream implementation
  returns a closure, so those CPython attributes are absent (as are
  `.keywords`). **Recommendation: document as an intentional limitation for
  this release.** Supporting the introspection contract requires replacing
  the closure with a callable object and testing its call/keyword behavior;
  that is broader than a small compatibility fix.
- Other known `functools` differences: `wraps` and `update_wrapper` do not
  copy metadata; `reduce` cannot distinguish an omitted initializer from an
  explicit `None`; `lru_cache` is absent.

## Other known CPython compatibility limits

- `string`: partial upstream API; it lacks CPython's full `Formatter` and
  `Template` features.
- `statistics`: board-owned subset; quantiles and geometric/harmonic means,
  among other APIs, are absent.
- `pathlib`: reduced `Path` implementation; most CPython methods/classes are
  absent and globbing is restricted.
- `shutil`: provides `rmtree`, `copyfileobj`, and `disk_usage`, not the broad
  CPython copy/move/tree API.
- `logging`: lightweight implementation, not the full hierarchy/handler/
  filter API.
- `unittest`: reduced runner and assertions; no full CPython discovery,
  mocking, or assertion surface.
- `copy`: limited to supported MicroPython object protocols; unsupported
  runtime objects may raise `copy.Error`.
- `itertools`: `product` is absent; the candidate-specific `islice` and `tee`
  fixes passed focused regression tests, but the module remains a subset.

## Clean-source and preservation checks

- MicroPython source commit: `0fd6c573ea815774668bbb16b8e197c8822368b2`.
- Both `micropython-v1.29.0-pruned-features.patch` and
  `micropython-v1.29.0-string-moduledefs.patch` were applied in an isolated
  clean worktree and passed `git apply --reverse --check`.
- Patch hashes match the documented values:
  - pruned-features patch:
    `8eb5802e2978c7a97a9dabaf88d4052bf59ac662758295c500c7d783ce65399a`
  - string moduledefs patch:
    `49ae4399f7f73b5a4d9e2261a62937afa88cb8446dec723407ec7b432181e238`
- This resolves the prior clean-source patch-verification uncertainty.
- Candidate and original production `manifest.py` SHA256 values match:
  `3ec02ee13dd6c85254d73ccdafa3f9cbb04c8a5cec1f03b76a218ca8e7598823`.
- The production manifest is unchanged. The original production worktree's
  pre-existing MicroPython submodule, feature-patch, and hardware API-test
  changes were preserved; no release-audit changes were made there. Its
  MicroPython gitlink remains at the pinned commit.
- No modules were added during the release-readiness audit.

## Release-readiness findings

The nine-module candidate has successful user-reported physical testing and
verified source/build artifacts. Before claiming strict CPython compatibility,
fix the empty-`reduce` exception mismatch; document `partial` introspection as
a known subset limitation unless that feature becomes a requirement. The
post-Phase-2 device GC measurement and the historical paired-baseline hash/
size discrepancy remain open evidence gaps.
