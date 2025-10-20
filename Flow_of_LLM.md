graph TD
    A["🔤 INPUT: 'Which is the fastest running animal?'"] --> B["📝 TOKENIZATION<br/>which | is | the | fastest | running | animal | ?<br/>(7 tokens)"]
    
    B --> C["🔢 EMBEDDING LAYER<br/>Each token → vector<br/>which: [0.2, -0.5, 0.8, ...]<br/>is: [0.1, 0.3, -0.2, ...]<br/>...<br/>(e.g., 768 dimensions per token)"]
    
    C --> D["🧠 TRANSFORMER LAYERS<br/>(12-96 layers depending on model)<br/><br/>Layer 1: Attention + Feed-forward<br/>Layer 2: Attention + Feed-forward<br/>...<br/>Layer N: Attention + Feed-forward<br/><br/>Billions of learned parameters"]
    
    D --> E["⚖️ ATTENTION MECHANISM<br/>(each layer)<br/><br/>Token 'fastest' attends to:<br/>- 'animal' (high weight)<br/>- 'running' (high weight)<br/>- 'which' (low weight)<br/>- etc."]
    
    E --> F["📊 OUTPUT LOGITS<br/>Scores for next token prediction<br/>The: 0.1<br/>fastest: 0.05<br/>cheetah: 8.7 ⭐<br/>peregrine: 7.2<br/>... (50K+ tokens)"]
    
    F --> G["🎯 TOKEN SELECTION<br/>Pick highest scoring token<br/>→ 'The'"]
    
    G --> H["🔄 AUTOREGRESSIVE LOOP<br/>Use 'The' as input,<br/>predict next token → 'fastest'<br/>Then 'fastest' → 'animal'<br/>... repeat until done"]
    
    H --> I["📖 DECODE TO TEXT<br/>Generated tokens:<br/>[The, fastest, animal, is, a, cheetah, .]<br/><br/>OUTPUT: 'The fastest animal is a cheetah.'"]
    
    style A fill:#e1f5ff
    style I fill:#c8e6c9
    style D fill:#fff9c4
    style F fill:#ffe0b2
