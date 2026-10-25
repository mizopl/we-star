---
id: v3r1t4s-polyomino-order-6-or-odd
type: entity
tags: [v3r1t4s, v3r1t4s/graphs-games-automata, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: graphs-games-automata
kind: standard
tractability: 1.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Polyomino of order 6, or of odd order 5 or more

# Overview

> Bank id `polyomino-order-6-or-odd` · standard · tractability 1.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

The order of a polyomino is the minimum number of congruent copies (rotations and reflections allowed) that tile some rectangle. No (connected) polyomino of odd order greater than 1 is known; order 3 is impossible (Stewart-Wormstein 1992). The smallest even order with no known example is 6. Find a connected, simply connected polyomino of order 6 or of odd order >= 5.

## Success criterion

(1) A connected, simply connected, non-rectangular polyomino P given as a cell set, with edge-connectivity checked. (2) An explicit tiling of an a x b rectangle by N copies, each an exact grid isometry of P (rotations and reflections allowed), with N = 6 or N odd and >= 5. (3) An exhaustive proof that no rectangle is tiled by k copies for any k < N, k >= 2, covering every factorization of k|P| with both sides >= P's minimal width. Two independent methods (DLX and SAT with DRAT-checked UNSAT) must agree. (4) A literature check (Handbook DCG chapter 14, Reid's rectifiable-polyomino pages, Friedman's Math Magic polyomino-order pages) finds no prior example.

## Partial wins

- {"id": "p1", "statement": "A connected polyomino of a known sporadic order (10, 18, 24 or 28) or any other even order not of Golomb's multiple-of-4 type, not appearing on Reid's rectifiable-polyomino pages or in the Handbook, with the explicit tiling and the minimality proof for all smaller counts (DLX plus DRAT-checked SAT, as in criterion (3))."}
- {"id": "p2", "statement": "A connected polyomino whose minimum odd tiling count (smallest odd number of copies tiling some rectangle) is strictly smaller than every value recorded on Reid's and Friedman's live pages, with the explicit odd tiling and a two-method exhaustive proof that no smaller odd count works."}
- {"id": "p3", "statement": "An exhaustive, two-method (DLX + DRAT-checked SAT) census showing that no connected polyomino with at most m cells has order 6 or odd order, for an m strictly larger than any size covered by a published census (literature check required)."}

## Verification

Verify the tiling by checking that the cell multiset equals the rectangle, that each placed copy is an isometric image of P, and that there are no overlaps. For minimality, enumerate all rectangles of area k|P| for k < N with sides at least P's minimum width. Run DLX (an independent Python implementation of Knuth's Algorithm X) and a CNF with pysat, and check DRAT proofs. Both must agree on infeasibility.

## Angles

- Inverse search: enumerate dissections of small rectangles into 6 congruent pieces via SAT (cell-to-piece variables plus congruence-witness variables per piece pair). Then reject pieces that also tile with 2 or 4 copies, which is a cheap DLX check.
- Lift Reid's order-6 heptabolo: refine its triangle grid into squares at scale s and search nearby polyominoes for which the 6-copy tiling survives and 2- and 4-copy tilings die.
- For odd orders: Reid built polyominoes whose smallest odd tiling count is 3(p+2). Search these families for members whose even-count tilings are killed by notches, so the overall minimum becomes odd.
- Use coloring and invariant arguments (Conway-Lagarias tiling groups) as fast filters to prove '2 and 4 copies impossible' before exact cover.

## Pitfalls

- Confusing 'odd-order' (the smallest odd number of copies tiling a rectangle) with 'order' (the overall minimum). Reid's 3(p+2) results are about the former.
- Forgetting that reflections are allowed.
- Missing rectangles in the minimality proof, for example very long thin ones or rectangles that need copies in many orientations.
- The status source is a 2017 handbook. Confirm against Reid's and Friedman's pages.
- Friedman's mathmagic/0299 page concerns 1D disconnected polyominoes, where order 6 and odd orders exist. Those do not count.
- The shape must be connected (edge-adjacent cells). Disconnected or corner-touching shapes are not polyominoes.

## Sources

- http://www.csun.edu/~ctoth/Handbook/chap14.pdf
- https://www.sciencedirect.com/science/article/pii/0097316592900583
- https://stars.library.ucf.edu/cgi/viewcontent.cgi?article=2437&context=etd
- Status source: http://www.csun.edu/~ctoth/Handbook/chap14.pdf

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/polyomino-order-6-or-odd.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `polyomino-order-6-or-odd`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
