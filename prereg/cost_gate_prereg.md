# Pre-registration: net-of-cost gate for trading claims (cross-thread rule)

Frozen 30 October 2026, before any result under any specification that adopts it was computed.

## Scope

This rule binds every specification frozen after this one that adopts it by name (the first are Void, Death and Storm), and every later version of an existing thread. It does not alter any specification frozen before it: Apple, Orange, Earth, Moon, Fire, Water (v1 to v3), Wood, Metal and Strife keep their decision rules as frozen, and where they report a cost check it remains a secondary statistic.

It applies to the statistic that a specification names as its tradeable statistic: a mean return earned by a position that could have been entered after the ruling was public. A statistic that is not a return (a mean abs(z), a kappa) is not gated.

## Cost estimate

1. For each traded stock and event, the bid-ask spread is the Corwin and Schultz (2012) high-low estimator, computed on each pair of consecutive days in the 20 trading days ending on day -1 (before the ruling, so the event's own range does not inflate it), with negative two-day estimates set to zero, averaged over the window.
2. Round-trip cost per leg = twice that spread estimate (a deliberate overstatement of a half-spread in and a half-spread out, to cover impact and the estimator's noise in small names).
3. A position with several legs (a pair, a basket) costs the sum over its legs of each leg's round-trip cost times its absolute weight.
4. Short legs carry no borrow cost in this estimate; any specification with a short leg reports that as a limitation.

## Gate

1. Net mean = mean of (gross event return minus that event's round-trip cost) over the events in the tradeable statistic.
2. A specification's Support verdict requires, in addition to its own conditions, that the net mean is above zero. If the gross conditions are met and the net mean is at or below zero, the verdict is reported as SUPPORT (GROSS ONLY), which is not a Support and is not a reason to forward-test as a trade.
3. The gross and net means are both reported, with the median cost per event.

## Known limitations

- Corwin and Schultz is noisy for single stocks and biased in thin names; the 20-day average and the factor of two are fixed here, not tuned.
- Daily closes are the assumed entry and exit; the gate does not price intraday entry.
