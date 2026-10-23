<div align="center">

<p>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="REAL Lab: Reasoning, Embodied, Agentic, and Lifelong-learning AI at Zhejiang University" src="assets/banner-light.svg" width="100%">
</picture>
</p>

<p>
  <a href="https://zju-real.github.io"><img alt="Website" src="https://img.shields.io/badge/Website-zju--real.github.io-1D4ED8?style=flat-square&logo=googlechrome&logoColor=white" align="top"></a>
  <a href="https://scholar.google.com/citations?user=UT3NzFAAAAAJ"><img alt="Google Scholar" src="https://img.shields.io/badge/Google%20Scholar-Publications-4285F4?style=flat-square&logo=googlescholar&logoColor=white" align="top"></a>
  <a href="https://huggingface.co/ZJU-REAL"><img alt="Hugging Face" src="assets/badge-huggingface.svg" align="top"></a>
  <img alt="" src="assets/spacer.svg" width="1" height="30" align="top">
  <br>
  <a href="https://github.com/ZJU-REAL"><img alt="Total stars" src="https://img.shields.io/github/stars/ZJU-REAL?style=social&label=Stars" align="absbottom"></a>
  &nbsp;
  <a href="https://github.com/ZJU-REAL"><img alt="Follow ZJU-REAL" src="https://img.shields.io/github/followers/ZJU-REAL?style=social&label=Follow" align="absbottom"></a>
</p>

**浙江大学 REAL Lab** · 推理 · 具身 · 智能体 · RSI

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg">
  <img alt="" src="assets/divider-light.svg" width="100%">
</picture>

**REAL Lab** at Zhejiang University builds AI systems that **reason reliably**, **inhabit physical bodies**, **act autonomously** as agents, and **learn continuously** throughout their lifetime, bridging the gap between virtual intelligence and physical intelligence.


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/research-map-dark.svg">
  <img alt="REAL research map: how Reasoning, Embodied, Agentic, and Lifelong-learning AI connect" src="assets/research-map-light.svg" width="100%">
</picture>

## Open-source systems

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/microsoft/JARVIS"><img src="assets/covers/hugginggpt.jpg" alt="HuggingGPT" width="100%"></a>
<b><a href="https://github.com/microsoft/JARVIS">HuggingGPT</a></b> &nbsp; <img src="https://img.shields.io/github/stars/microsoft/JARVIS?style=social" alt="stars" align="absmiddle"><br>
<sub>An LLM as controller and the Hugging Face hub as executors: plan, pick expert models, run them, and compose the answer.</sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/ZJU-REAL/HugAgentOS"><img src="assets/covers/hugagentos.jpg" alt="HugAgentOS" width="100%"></a>
<b><a href="https://github.com/ZJU-REAL/HugAgentOS">HugAgentOS</a></b> &nbsp; <img src="https://img.shields.io/github/stars/ZJU-REAL/HugAgentOS?style=social" alt="stars" align="absmiddle"><br>
<sub>A self-evolving AgentOS. Memory, skills, and orchestration improve with every task, and each evolution step is attributable, replayable, and reversible.</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/ZJU-REAL/Easel"><img src="assets/covers/easel.jpg" alt="Easel" width="100%"></a>
<b><a href="https://github.com/ZJU-REAL/Easel">Easel</a></b> &nbsp; <img src="https://img.shields.io/github/stars/ZJU-REAL/Easel?style=social" alt="stars" align="absmiddle"><br>
<sub>An open-source social-media agent: discover trends, create posts, audio, and video, publish across platforms, and learn what actually works.</sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/ZJU-REAL/ClawGUI"><img src="assets/covers/clawgui.jpg" alt="ClawGUI" width="100%"></a>
<b><a href="https://github.com/ZJU-REAL/ClawGUI">ClawGUI</a></b> &nbsp; <img src="https://img.shields.io/github/stars/ZJU-REAL/ClawGUI?style=social" alt="stars" align="absmiddle"><br>
<sub>Train, evaluate, and deploy GUI agents in one framework: online RL across parallel emulators and real Android, HarmonyOS, and iOS devices.</sub>
</td>
</tr>
</table>

<p align="center"><a href="https://zju-real.github.io/projects.html"><b>More projects →</b></a></p>

## Research map

### R · Reasoning: reason reliably

Models that can reason for as long as a problem requires, spend only the thinking it needs, and know when an answer is right.

| Direction | Focus | Representative work |
| :-- | :-- | :-- |
| **Long-horizon reasoning** | Break the context-length ceiling so reasoning can continue as long as the problem demands. | [InftyThink](https://github.com/ZJU-REAL/InftyThink) · [InftyThink+](https://github.com/ZJU-REAL/InftyThink-Plus) |
| **Efficient reasoning** | Fit the amount of thinking to the difficulty of the problem and stop overthinking. | [Self-Braking Tuning](https://github.com/ZJU-REAL/Self-Braking-Tuning) · [LAPO](https://github.com/ZJU-REAL/LAPO) · [Mind the Gap](https://github.com/ZJU-REAL/Mind-the-Gap) |
| **Verifiable reasoning** | Verifiers and rewards that can be trusted, and models that pause instead of fabricate. | [VerifyBench](https://github.com/ZJU-REAL/VerifyBench) · [CoVerRL](https://github.com/ZJU-REAL/CoVerRL) · [Pause or Fabricate?](https://github.com/ZJU-REAL/GRIL) |

### E · Embodied: inhabit physical bodies

Taking intelligence off the screen: understanding 3D space, anticipating how the world changes, and acting through a body.

| Direction | Focus | Representative work |
| :-- | :-- | :-- |
| **Spatial perception** | Measure and teach the 3D understanding that 2D pretraining lacks, including viewpoints other than the camera's. | [ViewSpatial-Bench](https://github.com/ZJU-REAL/ViewSpatial-Bench) · [SpatialLadder](https://github.com/ZJU-REAL/SpatialLadder) · [GPD](https://github.com/ZJU-REAL/GPD) |
| **Self-evolving spatial intelligence** | Let geometry and physical interaction supply their own supervision, without human labels. | [SpatialEvo](https://github.com/ZJU-REAL/SpatialEvo) · [Spatial-Interactor](https://arxiv.org/abs/2609.23038) |
| **Prediction and world models** | Reason about what happens next and keep a memory of the world over time. | [SpaceCast-Bench](https://github.com/ZJU-REAL/SpaceCast-Bench) · [WorldMemBench](https://github.com/ZJU-REAL/WorldMemBench) |
| **Embodied action** | Turn perception into reliable physical action and coordinated embodied behavior. | [VLA-Corrector](https://arxiv.org/abs/2607.01804) · [OmniEmbodied](https://github.com/ZJU-REAL/OmniEmbodied) |

### A · Agentic: act autonomously as agents

Agents that plan, use tools, and carry long-horizon tasks through to completion across screens, software, and the open web.

| Direction | Focus | Representative work |
| :-- | :-- | :-- |
| **GUI grounding** | Locate exactly where to act on a screen, with dense rewards, test-time learning, and adaptive zoom. | [GUI-G²](https://github.com/ZJU-REAL/GUI-G2) · [GUI-RCPO](https://github.com/ZJU-REAL/GUI-RCPO) · [Reliable Negatives](https://github.com/ZJU-REAL/CANL) · [UI-Zoomer](https://github.com/ZJU-REAL/UI-Zoomer) |
| **Computer-use agents** | Long-horizon control of real devices through multi-turn RL, GUI plus command line, and online self-improvement. | [UI-S1](https://github.com/X-PLUG/MobileAgent/tree/main/UI-S1) · [EMPO](https://aclanthology.org/2026.acl-long.428/) · [UI-Copilot](https://github.com/ZJU-REAL/UI-Copilot) · [HybridCUA](https://github.com/ZJU-REAL/HybridCUA) · [ComputerSD](https://github.com/ZJU-REAL/ComputerSD) · [Reflect, Revise, Reuse](https://arxiv.org/abs/2609.17653) · **[ClawGUI](https://github.com/ZJU-REAL/ClawGUI)** |
| **Deep research agents** | Search the open web, synthesize evidence, and carry a project from literature to a reviewed paper. | [IterSynth](https://arxiv.org/abs/2609.29444) · [BrowserForge](https://arxiv.org/abs/2608.24848) · [EviNote-RAG](https://arxiv.org/abs/2509.00877) · [PaperGym](https://github.com/ZJU-REAL/PaperGym) · **[Polaris](https://github.com/ZJU-REAL/Polaris)** |
| **Code agents** | Code and tests that co-evolve adversarially through reinforcement learning. | [Code-A1](https://github.com/ZJU-REAL/Code-A1) |
| **Creation agents** | Agents that discover, create, publish across platforms, and learn what actually works. | **[Easel](https://github.com/ZJU-REAL/Easel)** |
| **Tool orchestration** | LLMs as controllers that plan, call expert models and tools, and compose the result. | **[HuggingGPT](https://github.com/microsoft/JARVIS)** · [TaskBench](https://github.com/microsoft/JARVIS/tree/main/taskbench) |
| **Agent evaluation** | Interactive, personalized benchmarks and a plug-in harness that evaluates any agent in any environment. | [KnowU-Bench](https://github.com/ZJU-REAL/KnowU-Bench) · **[ageval](https://github.com/ZJU-REAL/ageval)** |

### L · Lifelong: learn continuously throughout their lifetime

Deployment is where learning continues: agents turn their own experience into guidance, skills, and better weights.

| Direction | Focus | Representative work |
| :-- | :-- | :-- |
| **Guided exploration** | Densify the sparse rewards of long-horizon agentic RL with adaptive hints and milestones. | [Agent-G²](https://github.com/ZJU-REAL/Agent-G2) · [BEACON](https://github.com/ZJU-REAL/BEACON) |
| **Skill internalization** | Discover skills in context, then internalize them into the policy across tasks and modalities. | [SKILL0](https://github.com/ZJU-REAL/SkillZero) · [ViSkill](https://github.com/ZJU-REAL/ViSkill) · [SkillRise](https://arxiv.org/abs/2607.26784) |
| **Self-distillation** | Agentic RL with on-policy self-distillation, and the family of methods built on it. | [SDAR](https://github.com/ZJU-REAL/SDAR) · [AgentOPSD](https://arxiv.org/abs/2608.05987) · [Pass the Baton](https://github.com/ZJU-REAL/Relay-OPD) · [RetireOPD](https://arxiv.org/abs/2609.20784) |
| **Post-deployment steering** | Adjust a deployed model's behavior at inference time without retraining. | **[EasySteer](https://github.com/ZJU-REAL/EasySteer)** |
| **Self-evolving systems** | Memory, skills, and orchestration that evolve with use, with every step attributable and reversible. | **[HugAgentOS](https://github.com/ZJU-REAL/HugAgentOS)** |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg">
  <img alt="" src="assets/divider-light.svg" width="100%">
</picture>

<div align="center">
<br>
<sub>If our work helps you, a ⭐ on the repository helps others find it too.</sub>
<br><br>
<a href="https://zju-real.github.io"><img src="https://img.shields.io/badge/REAL%20Lab-Zhejiang%20University-1D4ED8?style=for-the-badge" alt="REAL Lab, Zhejiang University"></a>
</div>
