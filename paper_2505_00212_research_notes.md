# Which Agent Causes Task Failures and When?

## 论文信息

- 标题: *Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems*
- arXiv: `2505.00212v3`
- 时间: 2025-06-02 版本
- 链接: <https://arxiv.org/abs/2505.00212>

## 这份笔记的定位

这不是一份纯摘要，也不是逐段翻译。它保留论文的章节顺序，但每一节后面都补一个“研究上意味着什么”，重点回答三件事：

1. 这篇论文到底提出了什么研究问题。
2. 作者的方法和实验说明了什么，没说明什么。
3. 如果把它当成后续课题的起点，最值得继承的是什么。

## 1. Introduction: 从“评估系统”转向“定位失败来源”

论文开篇指出，LLM multi-agent system 的常见研发流程是：

1. 跑 benchmark。
2. 看到任务失败。
3. 人工读 log，判断哪个 agent、哪一步出了关键错误。
4. 再改系统。

作者认为，第 3 步虽然是系统迭代的核心，却基本没有被正面研究。现有工作更多在做更细 benchmark 或更强 agent，但没有系统回答一个更直接的问题：任务失败后，究竟该修谁。

作者因此提出一个新问题：`automated failure attribution`。目标不是再判断任务是否成功，而是自动判断：

- `who`: 哪个 agent 对失败负责；
- `when`: 决定性错误发生在哪一步。

### 研究上意味着什么

这一节最重要的价值不是“动机合理”，而是它把一个工程痛点正式提升成了研究问题。这个转换有两层意义：

- 它把 `evaluation` 和 `improvement` 连接起来了。很多 agent benchmark 只能告诉你系统差，但不能告诉你为什么差。
- 它把“debugging agent systems”从经验性工程劳动，转成一个可以定义、标注、评测的任务。

如果要做相关研究，这篇论文最值得学的是这个问题切法。它不再停留在“让 agent 更强”，而是转向“让系统更可诊断、可修复、可维护”。

## 2. Problem Formulation: decisive error 的定义是全篇核心

作者把多智能体系统建模成 turn-based protocol：每个时间步只有一个 agent 行动。对一条失败轨迹 `τ`，作者定义某个 `(agent i, step t)` 是 `decisive error`，如果把这一步的错误动作改正，并允许后续轨迹相应调整，那么原本失败的轨迹会变成成功。

形式化上，这其实是一个反事实定义：

- 原始轨迹失败；
- 对某个 `i, t` 施加 intervention；
- 如果干预后轨迹成功，则 `(i, t)` 是 decisive error。

如果一条轨迹里有多个 decisive error，作者选择最早发生的那个作为主归因对象。

### 研究上意味着什么

这是论文里最重要也最值得批判性看的部分。

它的优点：

- 定义非常清楚，适合标注和评测。
- 它不是表面上的“最后谁答错了”，而是更接近 root cause。
- “最早 decisive error”让任务从多标签归因为主标签归因，便于构建 benchmark。

它的局限：

- 真实系统失败经常是连锁的，不一定能压缩成单个最早错误点。
- 某些失败更像累积偏差，而不是一步足以扭转全局的 decisive error。
- 它默认可以想象“修正一步后后续轨迹也会正确调整”，这在理论上合理，但在经验上很强。

所以这一定义更适合作为 `benchmarkable approximation of root cause`，而不是完整的系统因果模型。

如果以后做扩展研究，一个自然方向是把单点归因扩展成：

- 多点归因；
- 因果链归因；
- agent-level responsibility distribution，而不只是一对 `(i, t)`。

## 3. The Who&When Dataset: benchmark 贡献比方法贡献更扎实

作者提出数据集 `Who&When`，包含：

- 来自 `127` 个 LLM multi-agent systems 的失败日志；
- 共 `184` 个 failure annotation tasks；
- 每个样本包含 query、失败日志、agent system 信息、人工标注的责任 agent、关键错误步和自然语言解释。

数据同时覆盖两类系统：

- `algorithm-generated systems`
- `hand-crafted systems`

其中手工系统部分包含 `Magentic-One` 这类更接近真实复杂系统的案例。

评估指标有三类：

- `Agent-Level Accuracy`
- `Step-Level Accuracy`
- `Step-Level Accuracy with Tolerance`

最后一个指标承认了一个现实：很多时候精确到某一步太难，但找到大致错误区间依然有用。

### 研究上意味着什么

这一节说明，这篇论文最扎实的贡献其实是 benchmark，而不是 baseline。

原因有三点：

1. 它给 failure attribution 这个方向建立了标准任务接口。
2. 它没有只收集结果标签，还提供了日志、系统信息和自然语言解释，便于后续做 judge、retrieval、reward modeling 或 trace analysis。
3. 它同时覆盖自动生成系统和手工系统，避免 benchmark 只停留在过于理想化的 toy setting。

如果以后你要做 follow-up work，这个数据组织形式非常值得沿用。它天然支持多种研究任务：

- agent-level 归因；
- step-level 归因；
- explanation generation；
- failure clustering；
- system-level weakness profiling。

## 4. 标注流程: 任务本身就很难，不是 baseline 太弱而已

论文的标注不是随意打标签。作者使用三位 expert，分轮次标注、标不确定样本、再交叉讨论修正。论文还给出了两个很有信息量的事实：

- annotator 花费时间很高，三人分别约 `30.9 / 30.2 / 23.2` 小时；
- 不确定比例大约在 `15%` 到 `30%`。

这说明 failure attribution 即使对人来说也并不轻松，尤其当错误是跨 agent、跨多步传播时，主因判断本身就带有解释负担。

### 研究上意味着什么

这部分给了一个很关键的研究信号：低性能不一定只是方法太弱，也可能是任务本身极难。

这会影响你如何解读后面的实验结果。如果一个任务连 expert 都要花很多时间并且存在明显分歧，那么：

- 不能把低准确率简单读成“LLM judge 不行”；
- 更应该把它读成“failure attribution 是一个高难、低冗余信号的推理任务”。

这也意味着，未来工作未必该只追求更高端到端 accuracy，可能还要设计：

- 置信度；
- 多候选归因；
- human-in-the-loop attribution；
- 允许保留不确定性的输出格式。

## 5. Section 4.1: 三种 baseline 本质上是三种上下文使用策略

作者设计了三种自动归因方法。

### 5.1 All-at-Once

把 query 和完整失败日志一次性给 LLM，让它直接输出责任 agent 和关键错误步。

它的隐含假设是：只要全局上下文足够完整，模型就能同时做全局责任判断和局部定位。

### 5.2 Step-by-Step

按时间顺序逐步喂给模型，在每一步判断是否已经发生 decisive error。一旦模型认为当前步已经出错，就停止并输出 agent 与 step。

它的隐含假设是：决定性错误能够在局部时间片上被及时识别。

### 5.3 Binary Search

先判断错误是在前半段还是后半段，再递归缩小范围，直到定位到单步。

它的隐含假设是：错误位置可以被一种近似区间搜索的方式逐步定位。

### 研究上意味着什么

这三种方法其实不是三个复杂算法，而是三个很干净的 baseline 思路：

- `All-at-Once` 代表大感受野、低过程约束；
- `Step-by-Step` 代表局部监控、在线判错；
- `Binary Search` 代表层级定位、折中式搜索。

从研究角度看，这种 baseline 设计是合理的，因为它们把问题拆成了“上下文怎么给 judge model”。但它们也都停留在 prompt-based judgment，没有利用更结构化的信息，比如：

- tool call state；
- environment observation；
- intermediate memory；
- action dependency graph；
- executable interventions。

所以这篇论文的方法部分更像是“建立第一批 baseline”，而不是“提出强解法”。

## 6. Section 4.3: 主结果表明 `who` 比 `when` 容易得多

论文主结果最该记住的是 Table 1。

在 GPT-4o 上：

- `All-at-Once` 在 agent-level 上最好；
- `Step-by-Step` 在 step-level 上最好；
- 但 step-level 总体依然很低，尤其在 hand-crafted system 上非常差。

例如在 hand-crafted systems 上：

- `All-at-Once` 的 agent-level accuracy 约为 `55.17%`；
- `Step-by-Step` 的 step-level accuracy 约为 `7.02%` 到 `8.77%`；
- `All-at-Once` 的某些 step-level 结果甚至低于随机基线。

### 研究上意味着什么

这个结果很关键，因为它把 failure attribution 明确拆成了两个不同难度层次：

- `who` 是粗粒度责任定位；
- `when` 是细粒度时间定位。

前者还能做出一些信号，后者基本还不可用。这个差距说明：

- 归因不是单一任务；
- 责任识别和错误定位需要不同的 inductive bias；
- “能看懂整段日志”不等于“能找到关键一步”。

如果以后做研究，不要再把 `agent attribution` 和 `step attribution` 混着报告。它们应该被分开设计、分开建模、分开评估。

## 7. Section 4.4: context 越长，step attribution 越接近崩溃

作者把 hand-crafted 系统日志按长度分成五档，发现随着上下文变长：

- 三种方法的 agent-level 和 step-level 都下降；
- step-level 对上下文长度更敏感；
- 最长日志上，三种方法的 step-level 几乎都接近 `0%`。

### 研究上意味着什么

这部分结果说明，failure attribution 的难点不是单纯“判断错误”，而是“在长历史里做因果压缩”。

这对后续方法设计有直接启发：

- 不能把长日志原样塞进 judge model 然后期待精确定位；
- 需要更强的检索、摘要、分段、候选筛选机制；
- 需要把“找 suspect region”和“做最终归因”拆成两阶段，而不是一次完成。

从这个角度看，未来比起更大模型，更值得尝试的是：

- hierarchical trace summarization；
- suspicious-step retrieval；
- agent-centric trace compression；
- graph-based dependency pruning。

## 8. Section 4.5: 容错评估改变了结论

作者进一步引入 tolerance step accuracy，在 hand-crafted systems 上考察“如果允许误差在 ±1, ±2, ... ±5 步内，表现会怎样”。

结果是：

- 严格定位时，`Step-by-Step` 更有优势；
- 随着 tolerance 变大，`All-at-Once` 的优势开始显现；
- 到大容忍范围时，宽上下文方法变得更有竞争力。

### 研究上意味着什么

这说明“定位哪一步”本身不是非黑即白的问题。很多实际系统调试不要求你报出精确第 `t` 步，而是希望你缩小到一个可人工检查的区间。

因此后续研究不一定要把任务始终定义成 exact step prediction。还可以考虑：

- suspect window prediction；
- top-k suspect steps；
- coarse-to-fine attribution。

这会让任务更接近真实调试需求，也可能更容易做出实用系统。

## 9. Section 4.6: 单样本不准，但统计层面可能仍然有用

论文做了一个很有价值的观察：虽然 instance-level attribution 的准确率不高，但当结果汇总到系统层面后，三种方法仍能较稳定地指出“哪些 agent 更常成为 decisive error 的来源”。

也就是说，单次失败判断未必可靠，但聚合很多失败日志之后，仍能形成有价值的 system diagnosis signal。

### 研究上意味着什么

这是论文里最容易被忽略、但工程价值很高的一点。

它意味着 automated failure attribution 的第一个落地方向，也许不是替代人做逐条 debug，而是支持：

- 故障 agent 排名；
- 模块脆弱性统计；
- 系统重构优先级判断；
- benchmark 维度下的 agent weakness profiling。

换句话说，failure attribution 不一定先成为一个 `case-level debugger`，它更可能先成为一个 `system-level analytics tool`。

## 10. Section 4.7: 混合方法提升了效果，但代价很高

作者尝试组合 `All-at-Once` 和 `Step-by-Step`：

1. 先用 `All-at-Once` 猜责任 agent；
2. 再只在这个 agent 的相关步骤上用 `Step-by-Step` 做更细定位。

结果是：

- 混合方法在两个指标上都更好；
- 但 token cost 显著提高。

论文报告的 hand-crafted systems 结果中，混合方法 step-level accuracy 达到 `12.28%`，高于单独方法，但总 token 成本最高。

### 研究上意味着什么

这一节说明作者已经触碰到一个重要方向：`hierarchical attribution pipeline`。

也就是先做粗归因，再做细定位。这很可能是这个任务更合理的建模方式，因为：

- 责任 agent 和关键错误步本来就是不同粒度；
- 先缩小 agent 范围，本质上就是在减少 step-level 搜索空间；
- 这比一次直接定位单步更符合系统调试流程。

如果继续往下做，很自然的研究延伸包括：

- coarse-to-fine attribution architecture；
- retrieve-then-judge；
- candidate step reranking；
- cost-aware attribution。

## 11. Section 4.8: 更强 reasoning model 不是直接解法

作者测试了 OpenAI `o1` 和 DeepSeek `R1`。结果并没有出现“更强推理模型显著解决 failure attribution”的现象。

例如在 hand-crafted systems 上：

- GPT-4o 的 `All-at-Once` agent-level 为 `54.31%`；
- OpenAI `o1` 在相同设置下为 `41.38%`；
- `Step-by-Step` 上 `o1` 的 step-level 虽提高到 `13.79%`，但仍远谈不上可用。

作者的结论是：更强 reasoning model 并不能自动带来实用级 failure attribution。

### 研究上意味着什么

这一节非常重要，因为它基本否定了一个偷懒路线：只换更强 judge model。

它提示后续研究应该把重点从“模型更大”转移到“信息和结构更对”：

- 让模型看什么；
- 怎样组织日志；
- 是否能引入状态、工具反馈和环境观察；
- 是否能做外部验证或 counterfactual checking。

这也说明 failure attribution 可能不是纯自然语言判断问题，而是 `reasoning + trace structure + causal inference` 的混合问题。

## 12. Related Work: 这篇论文在现有谱系里的位置

作者把自己放在三条相关工作脉络之间：

- LLM multi-agent systems；
- LLM-as-a-judge；
- process/reward modeling。

这个定位是成立的。它既不像传统 judge 任务那样只看最终输出，也不像 process reward model 那样只评单个模型的推理链，而是面向多 agent、带交互历史、带跨步因果传播的系统归因任务。

### 研究上意味着什么

这篇论文真正占据的生态位可以概括为：

`from output evaluation to system-level causal diagnosis`

这很有价值，因为它把 agent evaluation 从“结果正确性”推进到“失败结构理解”。后续只要沿着这个方向继续细化，理论上能分化出一整条研究线，例如：

- multi-agent process supervision；
- structured failure diagnosis；
- intervention-based agent debugging；
- repair-oriented evaluation。

## 13. 这篇论文最强和最弱的地方

### 最强的地方

- 研究问题切得准，而且足够新。
- `decisive error` 定义使问题可以落地评测。
- `Who&When` 数据集为后续工作提供了一个明确基准。
- 实验结论清楚，不粉饰结果，负结果本身很有价值。

### 最弱的地方

- 数据规模不大，`184` 个样本更适合 benchmark，不足以支撑复杂训练路线。
- 标签是单点主因，不能覆盖多因子失败。
- 方法几乎完全依赖文本日志，没有用到更强结构化系统信号。
- 评估停在 attribution accuracy，没有继续验证“归因能否提升修复效率”。

## 14. 如果把它作为后续课题起点，最值得接什么

如果从研究角度继续推进，这篇论文后面最自然的方向不是“再试几个 prompt”，而是下面几类：

### 方向 A: 结构化 trace 归因

把 failure log 从纯文本展开成结构化轨迹：

- agent id
- tool call
- observation
- state delta
- dependency edges

再做 attribution。核心假设是 step attribution 难，不只是模型弱，也是日志表示太弱。

### 方向 B: coarse-to-fine attribution

先定位责任 agent 或 suspect span，再做局部精判。目标不是一步到位，而是分层缩小搜索空间。

### 方向 C: 可执行的反事实归因

既然论文的定义本质上是 intervention-based，就可以进一步研究：

- 是否能真的重放轨迹；
- 是否能替换某一步动作再执行；
- 是否能通过 executable intervention 验证归因是否成立。

这会把 failure attribution 从“语言判断”推进到“半可验证因果诊断”。

### 方向 D: attribution for repair

把归因和修复连起来评估。比如判断一个 attribution method 的价值，不只看 accuracy，也看：

- 是否更快帮助开发者找到 bug；
- 是否能提高 patch success rate；
- 是否能减少系统迭代成本。

## 15. 总结

这篇论文最重要的贡献，不是提出了一个已经足够强的归因算法，而是把一个真实存在但长期被忽略的问题清楚地定义了出来：

`任务失败后，哪个 agent 在哪一步造成了失败？`

它的实验结果整体偏悲观，但这种悲观是有价值的。论文证明了：

- `who` 和 `when` 是两个显著不同的任务；
- 长上下文中的 step attribution 极难；
- 更强 reasoning model 不是直接答案；
- failure attribution 需要更结构化、更分层、更接近因果推断的方法。

如果把这篇论文当作研究起点，正确的继承方式不是重复它的 baseline，而是继承它的问题定义、benchmark 视角和负结果信号，然后往结构化诊断、层级归因和可验证干预三个方向推进。

## 参考链接

- arXiv 摘要页: <https://arxiv.org/abs/2505.00212>
- arXiv PDF: <https://arxiv.org/pdf/2505.00212>
- 项目仓库: <https://github.com/mingyin1/Agents_Failure_Attribution>
