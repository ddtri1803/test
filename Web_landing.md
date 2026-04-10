# 1) Civilization Architecture
- **Core Stack**: PHP 8.3 + MySQL 8 + TwindCSS.
- **Routing Primitive (immutable)**:
  - Product: `dropshipping.com/product:[slug]`
  - Control: `/control:[admin_slug]`, `/control:[user_slug]`
  - Gateway validator bắt buộc reject mọi format khác.
- **Layer Topology**:
  - `Civilization Core` (economy zones, market systems, product ecosystems, capital networks)
  - `Domain Services` (product, consumer, campaign, market, capital)
  - `Event Mesh` (entity/market/civilization bus)
  - `Plugin Runtime` (hot-swap, versioned, isolated)
  - `AI Runtime` (entity AI, market AI, civilization AI)
  - `Observability` (health index, saturation map, demand heatmap, capital graph)
- **Engineering Guarantees**:
  - strict API contracts (OpenAPI versioned)
  - schema versioning + compatibility layer
  - no breaking changes policy
  - feature flags + canary + zero-downtime deploy
  - modular monolith → service extraction ready

# 2) Economic Entity System
- **Entity Graph (node-based economy)**:
  - `ProductEntity`
  - `ConsumerEntity`
  - `CampaignEntity`
  - `CapitalEntity`
  - `MarketEntity`
- **Unified Contract**:
  - `entity_id`, `entity_type`, `version`, `state`, `metadata`, `links[]`
  - immutable event history + snapshot state.
- **Versioning**:
  - mỗi entity có multi-version (landing/content/price/strategy).
  - read/write qua compatibility adapter để không phá vỡ module cũ.
- **Plugin Attachment Points**:
  - entity-level hooks: `before_create`, `after_create`, `before_update`, `after_update`, `before_publish`.

# 3) Market Creation Engine
- **Autonomous Market Lifecycle**:
  1. detect whitespace opportunity
  2. synthesize new category hypothesis
  3. generate offer + narrative + segment
  4. spin up landing `product:[slug]`
  5. launch campaign mesh
  6. validate PMF signal
  7. scale or archive.
- **Core Services**:
  - `MarketDiscoveryService`
  - `CategorySynthesisService`
  - `OfferComposerService`
  - `GoToMarketOrchestrator`
- **Required Events**:
  - `market_created`, `demand_spike`, `capital_shift`, `view`, `click`, `purchase`.
- **Safety Rails**:
  - budget guardrails, compliance policies, saturation thresholds.

# 4) Capital Flow System
- **Capital as Flow Network**:
  - inflow, outflow, rotation, reinvestment loops.
- **Capital Engine Modules**:
  - `AllocationEngine` (ROI-weighted allocation)
  - `ReinvestmentEngine` (dynamic looping)
  - `CrossMarketBalancer` (capital movement giữa markets)
  - `RiskController` (drawdown + exposure limits)
- **Decision Inputs**:
  - conversion velocity, CAC/LTV spread, elasticity, market pressure.
- **Output Goal**:
  - maximize total civilization profit thay vì tối ưu cục bộ.

# 5) Demand Engineering System
- **Demand Lifecycle**:
  - discover latent pain → activate urgency → shape perception → reinforce intent.
- **Demand Engine Modules**:
  - `PainPointMiner`
  - `NarrativeGenerator`
  - `UrgencyAmplifier`
  - `PerceptionShaper`
  - `IntentReinforcer`
- **Execution Surface**:
  - landing variants, campaign variants, offer variants, pricing variants.
- **Measurement Events**:
  - `view`, `click`, `add_to_cart`, `purchase`, `demand_spike`.

# 6) AI Civilization Layers
- **Entity AI**:
  - optimize product page/version, offer framing, CTR/CVR micro-optimization.
- **Market AI**:
  - pricing adaptation, audience re-segmentation, demand redistribution.
- **Civilization AI**:
  - create markets from zero, global capital allocation, macro-strategy mutation.
- **Decision Loop**:
  - Observe → Simulate → Decide → Act → Evolve (simulation-first mandatory).
- **AI-Native Infrastructure**:
  - policy engine, model registry, prompt/version control, experiment tracking.

# 7) Evolution Loop
- **Mutation Axes**:
  - market mutation
  - product mutation
  - demand mutation
  - capital redistribution
- **Continuous Evolution Pipeline**:
  1. ingest event stream
  2. update global simulation
  3. generate strategy mutations
  4. run sandbox evaluation
  5. promote winning mutations via feature flags
  6. rollback automatically nếu health index giảm.
- **Global Fitness Function**:
  - weighted score = profit growth + market resilience + demand sustainability + capital efficiency.
- **End State**:
  - autonomous self-generating digital economy civilization.
