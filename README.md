# 🤖 Anthropic Agents: Enhanced OpenAI Agents SDK with Citation Support

This repository extends the [OpenAI Agents SDK](https://platform.openai.com/docs/assistants/overview) to support both **OpenAI** and **Anthropic** models — with a particular focus on **Anthropic's sentence-level citation capabilities**. It provides a unified, pluggable interface that works seamlessly with both LLM providers, making it easier to build agents that are both flexible and accurate.

---

## ✨ Features

- **🧠 Multi-Provider Support**: Easily switch between OpenAI and Anthropic models.
- **🔗 Citation Integration**: Leverage Anthropic's sentence-level citation capabilities for greater factual accuracy.
- **🔌 Provider Abstraction**: Unified agent interface that supports both providers.
- **🔄 Seamless Switching**: Swap providers at runtime with a single method call.
- **📑 Citation Visualization**: Format and display citations alongside responses.

---

## 🛠️ Design Choices

### 🔄 Provider Selection Strategy

I chose a **factory pattern** for provider creation to:

- Abstract the details of provider initialization
- Make switching between providers simple
- Allow for future provider additions without modifying agent code

### 🧠 Citation Implementation

For citation handling, we made the following choices:

1. **Preservation of Original Response**  
   We keep the full Anthropic response data to ensure no information is lost.

2. **Custom Data Extension**  
   Citations are attached to the response's `custom_data` field for easy access.

3. **Formatted Output**  
   Helper methods provide human-readable citation formatting for display purposes.
