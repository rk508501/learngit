# LLM Pipeline: "Which is the fastest running animal?"

## STAGE 1: INPUT
```
┌─────────────────────────────────────────────┐
│  🔤 INPUT TEXT                              │
│  "Which is the fastest running animal?"     │
└─────────────────────────────────────────────┘
```

## STAGE 2: TOKENIZATION
```
┌─────────────────────────────────────────────┐
│  📝 TOKENIZE INTO TOKENS                    │
│                                              │
│  which | is | the | fastest | running |     │
│  animal | ?                                 │
│                                              │
│  Total: 7 tokens                            │
└─────────────────────────────────────────────┘
```

## STAGE 3: EMBEDDING LAYER
```
┌─────────────────────────────────────────────┐
│  🔢 TOKEN → EMBEDDING (VECTORIZATION)       │
│                                              │
│  which    → [0.2, -0.5, 0.8, ...]          │
│  is       → [0.1, 0.3, -0.2, ...]          │
│  the      → [-0.4, 0.6, 0.1, ...]          │
│  fastest  → [0.9, -0.1, 0.3, ...]          │
│  running  → [0.5, 0.4, -0.6, ...]          │
│  animal   → [-0.2, 0.8, 0.5, ...]          │
│  ?        → [0.0, 0.0, 0.1, ...]           │
│                                              │
│  (Each token = 768-4096 dimensions)         │
└─────────────────────────────────────────────┘
```

## STAGE 4: TRANSFORMER LAYERS
```
┌─────────────────────────────────────────────┐
│  🧠 PASS THROUGH TRANSFORMER                │
│                                              │
│  ┌─ Layer 1 ─────────────────────┐         │
│  │ Attention + Feed-forward      │         │
│  │ (Billions of parameters)      │         │
│  └──────────────────────────────┘         │
│           ↓                                 │
│  ┌─ Layer 2 ─────────────────────┐         │
│  │ Attention + Feed-forward      │         │
│  └──────────────────────────────┘         │
│           ↓                                 │
│         ... (repeat 12-96 layers)          │
│           ↓                                 │
│  ┌─ Layer N ─────────────────────┐         │
│  │ Attention + Feed-forward      │         │
│  └──────────────────────────────┘         │
└─────────────────────────────────────────────┘
```

## STAGE 5: ATTENTION MECHANISM (per layer)
```
┌─────────────────────────────────────────────┐
│  ⚖️ ATTENTION: WHICH TOKENS MATTER?         │
│                                              │
│  Token "fastest" pays attention to:         │
│  ├─ "animal"  → weight: 0.95 (high)        │
│  ├─ "running" → weight: 0.88 (high)        │
│  ├─ "is"      → weight: 0.42 (medium)      │
│  ├─ "which"   → weight: 0.12 (low)         │
│  └─ "?"       → weight: 0.05 (low)         │
│                                              │
│  (Each token attends to all other tokens)   │
└─────────────────────────────────────────────┘
```

## STAGE 6: OUTPUT LOGITS
```
┌─────────────────────────────────────────────┐
│  📊 PROBABILITY SCORES FOR NEXT TOKEN       │
│                                              │
│  cheetah    → 8.7  ⭐ (HIGHEST)            │
│  peregrine  → 7.2                          │
│  fastest    → 2.1                          │
│  The        → 1.8                          │
│  animal     → 0.9                          │
│  ... (50,000+ possible tokens)              │
│                                              │
│  Selected: "The"                            │
└─────────────────────────────────────────────┘
```

## STAGE 7: AUTOREGRESSIVE GENERATION
```
┌─────────────────────────────────────────────┐
│  🔄 REPEAT: USE OUTPUT AS NEW INPUT         │
│                                              │
│  Round 1:                                   │
│  [Which | is | the | fastest | ...] → The  │
│                                              │
│  Round 2:                                   │
│  [Which | is | the | fastest | ... | The]  │
│  → fastest                                  │
│                                              │
│  Round 3:                                   │
│  [Which | is | the | fastest | ... | The   │
│   | fastest] → animal                      │
│                                              │
│  ... continue until [STOP] token            │
└─────────────────────────────────────────────┘
```

## STAGE 8: FINAL DECODING
```
┌─────────────────────────────────────────────┐
│  📖 CONVERT TOKENS BACK TO TEXT             │
│                                              │
│  Generated Tokens:                          │
│  [The | fastest | animal | is | a |        │
│   cheetah | .]                              │
│                                              │
│  OUTPUT TEXT:                               │
│  "The fastest animal is a cheetah."         │
└─────────────────────────────────────────────┘
```

---

## Summary Flow
```
Text Input
    ↓
Tokenization (break into words/subwords)
    ↓
Embedding (tokens → vectors)
    ↓
Transformer Layers (process with attention)
    ↓
Attention Mechanism (determine relevance)
    ↓
Output Logits (score next token)
    ↓
Token Selection (pick highest score)
    ↓
Autoregressive Loop (repeat until complete)
    ↓
Decoding (vectors → readable text)
    ↓
Final Output
```
