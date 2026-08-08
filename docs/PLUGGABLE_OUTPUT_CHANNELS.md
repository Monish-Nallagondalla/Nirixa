# 🔌 Pluggable Output Channels & Multi-Platform Architecture
### How Nirixa OS Adapts to Any User Persona (Private Thinkers, Researchers, Founders & Writers)

---

## 🧭 The Core Philosophy: User-Agnostic Design

Nirixa OS is not hardcoded to any single publishing platform. What is a priority for one operator may be completely irrelevant to another:

- **The Private Researcher**: Wants 100% local cognitive retention, research paper synthesis, and zero public posting.
- **The Indie Builder**: Prioritizes X/Twitter, GitHub releases, and product changelogs.
- **The Industry & Product Leader**: Prioritizes LinkedIn, conference keynote outlines, and executive essays.
- **The Long-Form Essayist**: Prioritizes Substack, Medium, and book chapters.

Nirixa OS treats all external publishing targets as **optional, pluggable output adapters**.

---

## 🛠️ Configuration (`system/config/config.yaml`)

Users can enable, disable, or customize their active output adapters directly in configuration:

```yaml
system:
  name: "Nirixa OS"
  mode: "hybrid" # Options: private_only | research_only | omni_channel

publishing_channels:
  # 1. Private Only (Default: No external publishing)
  local_second_brain:
    enabled: true
    destination: "inbox/"
    format: "markdown"

  # 2. Professional & Industry Track
  linkedin:
    enabled: false # Toggle on if relevant to your workflow
    auto_compile_pdf_carousels: true
    max_char_limit: 3000

  # 3. Open-Source & Tech Track
  x_twitter:
    enabled: false
    thread_auto_split_limit: 280

  # 4. Long-Form Essay & Publication Track
  substack_or_blog:
    enabled: false
    destination: "content/essays/"
    export_format: "markdown"
```

---

## 🧩 Building a Custom Output Adapter

Any developer can create a custom channel adapter in under 20 lines of Python by implementing the `BaseOutputChannel` interface:

```python
class BaseOutputChannel:
    def __init__(self, config):
        self.config = config

    def format_asset(self, raw_thought, refined_thesis, metadata):
        """Transforms an Original Thought Asset into platform-native format."""
        raise NotImplementedError

    def publish(self, formatted_asset, stage="draft"):
        """Stages or exports the asset to the user's destination."""
        raise NotImplementedError
```

### Supported Native Formats:
- **Markdown & PDF**: Auto-compiled multi-slide documents for visual carousels.
- **Micro-Threads**: Strictly validated character splits ($<280$ chars).
- **Long-Form Essays**: Formatted with clear heading hierarchies for Substack, Medium, or arXiv.
