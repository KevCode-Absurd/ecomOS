# Example CRO card: estimate test sample size

**Task:** Estimate required sample size per variant before planning an experiment.

**Source-supported method:** n = 16 × variance / absolute-effect² per variant. The stated settings are 95% significance (alpha 0.05, two-sided) and 80% power. For a conversion rate, variance is p(1-p). Delta is an absolute effect, not a percentage relative lift.

**Illustration:** At p = 0.02 and delta = 0.002 (a 10% relative lift), the formula gives 78,400 visitors per variant, approximately 156,800 total for two equally sized variants. This is arithmetic using the source's planning formula, not an observed brand result.

**Brand inputs the operator must obtain:** Baseline conversion probability, minimum worthwhile absolute effect, eligible traffic, allocation and feasible duration. These input checks are operating policy; they are not presented as additional source claims.

**What the agent can do next:** Calculate a planning estimate once those inputs are supplied, state its assumptions, and explain whether the available traffic could support the proposed experiment. Keep any decision to launch separate from the estimate.

**Evidence:** [Private Drive source](https://drive.google.com/file/d/1-erJBJ6iVbCFgrxQ0SjuTi9kbLRL2jmF/view). The structured record stores exact paragraph offsets and the source version hash.

**Review:** A separate OpenAI check found the corrected card source-supported with no missing qualifiers. It replaced a draft that omitted confidence, power and variance assumptions. Underlying source attribution and statistical validity have not been independently verified. The card remains unpublished while folder review continues.
