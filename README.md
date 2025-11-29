# Cocktail Aesthetics MCP

A deterministic visual vocabulary server that maps cocktail characteristics to locked aesthetic parameters for image generation. Part of the Lushy.app Visual Vocabularies ecosystem.

## What This Does

Instead of vague style descriptions, this MCP provides structured, reproducible aesthetic parameters for cocktail-inspired image generation. Specify a cocktail, get consistent color palettes, lighting approaches, composition strategies, and mood directives that stay locked across every generation.

No drift. No surprises.

## Quick Start

### Installation

```bash
git clone https://github.com/dmarsters/cocktail-aesthetics-mcp.git
cd cocktail-aesthetics-mcp
pip install -r requirements.txt
```

### Usage with Claude

Add to your Claude client configuration:

```json
{
  "mcpServers": {
    "cocktail-aesthetics": {
      "command": "python",
      "args": ["cocktail_aesthetics_mcp.py"]
    }
  }
}
```

Then use Claude to enhance prompts:

```
Enhance this prompt with Mai Tai aesthetics:
"A person walking through a Mediterranean alley at golden hour"
```

Claude will layer the Mai Tai vocabulary onto your prompt, locking in the specific color palette (#FF6B35, #F7931E, #8B4513, #00A86B), tiki_torch lighting, tropical mood with playful secondary notes, layered composition, and translucent texture.

## Available Cocktails

Eight cocktails with complete aesthetic vocabularies:

- **Negroni** (gin, bitter, sophisticated) — Ruby reds and burnt oranges, warm side-lit, balanced composition
- **Mai Tai** (rum, fruity, tropical) — Tropical oranges and greens, tiki torch lighting, layered depth
- **Daiquiri** (rum, sour, elegant) — Pale golds and creams, crisp backlighting, minimalist composition
- **Old Fashioned** (whiskey, spirit-forward, sophisticated) — Amber and brown, moody amber lighting, oily texture
- **Mojito** (rum, herbal, tropical) — Green and cream, diffused soft lighting, garnish-focused
- **Margarita** (tequila, sour, playful) — Tropical oranges and reds, golden hour, crystalline texture
- **Espresso Martini** (vodka, bitter, sophisticated) — Dark charcoal and chocolate with cream, moody amber, creamy texture
- **Sazerac** (whiskey, herbal, sophisticated) — Amber and gold, golden hour, balanced composition

## Architecture

Three-layer design separating categorical structure from creative synthesis:

### Layer 1: Olog Structure
Enums and categories that define the aesthetic space:
- **SpiritBase**: rum, whiskey, vodka, gin, tequila, cognac, mezcal
- **FlavorType**: bitter, sweet, sour, spirit_forward, herbal, fruity, creamy, spiced, smoky
- **LightingStyle**: warm_side_lit, tiki_torch, golden_hour, moody_amber, crisp_backlit, etc.
- **MoodDescriptor**: sophisticated, tropical, nostalgic, bold, elegant, playful, dark, aromatic
- **CompositionApproach**: balanced, layered, minimalist, dramatic, garnish_focused
- **TextureQuality**: smooth, crystalline, creamy, oily, effervescent, translucent, opaque, foamy

### Layer 2: Deterministic Morphisms
Zero-cost LLM parameter mapping. Pure taxonomy lookups:
- `spirit_base_to_warmth()` — Map spirit to thermal quality (0-10)
- `spirit_base_to_color_category()` — Map spirit to primary color
- `flavor_to_mood()` — Map flavor type to emotional tone
- `complexity_to_composition()` — Map ingredient complexity to visual strategy
- `bitterness_to_lighting()` — Map bitterness to lighting quality
- `build_visual_parameters()` — Master morphism orchestrating all mappings

### Layer 3: MCP Interface
Claude-facing tools for prompt enhancement:
- `list_cocktails()` — Get all available cocktails
- `get_cocktail_profile()` — Full flavor and visual profile
- `get_visual_parameters()` — Locked aesthetic parameters only
- `enhance_prompt_with_cocktail()` — Layer vocabulary onto a base prompt
- `search_cocktails_by_flavor()` — Find cocktails by flavor type
- `get_spirit_warmth()` — Check thermal warmth of a spirit

## How It Works

### The Problem It Solves

Style prompts are vague: "make it look tropical and sophisticated." This leads to drift:
- Generation 1: warm golden tones
- Generation 2: cooler oranges
- Generation 3: more saturated colors
- Generation 4: completely different mood

### The Solution: Locked Parameters

Visual vocabularies lock specific parameters:

```
Mai Tai Vocabulary:
  color_palette: ["#FF6B35", "#F7931E", "#8B4513", "#00A86B"]
  lighting: "tiki_torch"
  mood: "tropical"
  secondary_moods: ["aromatic", "playful"]
  composition: "layered"
  texture: "translucent"
  temperature: "warm"
```

Every generation with this vocabulary uses these exact parameters. Consistency guaranteed.

### Cost Efficiency

Traditional approach: send full prompt + style description to LLM for enhancement (expensive token cost)

This approach:
1. Deterministic mapping (zero tokens) — vocabulary lookup
2. Single LLM call — creative synthesis of base prompt + locked parameters

Result: ~60% token savings vs. pure LLM enhancement.

## Customization

These parameters aren't canonical. They're domain-informed choices you can edit, extend, or rebuild entirely.

### Edit a Cocktail

Modify `cocktail_profiles.json`:

```json
"mai_tai": {
  "name": "Mai Tai",
  "spirit_base": "rum",
  "color_palette": ["#FF6B35", "#F7931E", "#8B4513", "#00A86B"],
  "lighting": "tiki_torch"
}
```

Changes take effect immediately on restart.

### Add a New Cocktail

Add to `cocktail_profiles.json` with required fields:
- `name`: Display name
- `spirit_base`: Primary spirit
- `primary_flavor`: Flavor type
- `complexity`: simple, moderate, or complex
- `bitterness`, `sweetness`, `richness`: 0-10 scales
- `color_palette`: Array of hex codes
- `has_cream`, `has_ice`, `is_effervescent`: Boolean flags

### Extend the Taxonomy

Add new enums to `cocktail_ologs.py`:

```python
class LightingStyle(str, Enum):
    CANDLELIT = "candlelit"  # Your new lighting style
```

Then add corresponding morphism:

```python
@staticmethod
def your_new_morphism(input_value):
    # Your deterministic mapping
    return output_value
```

## Composition with Other Vocabularies

This vocabulary can compose with other visual vocabulary MCP servers:

```
Base Prompt: "A bottle of hot sauce on a kitchen shelf"
+ Cocktail Vocabulary (Mai Tai): tropical, layered, warm
+ Magazine Photography Vocabulary (Life 1960s): documentary, authentic, vintage
= Synthesized prompt with both aesthetics locked
```

Composition direction matters. Some vocabularies are generative (amplify each other), others absorptive (one overrides the other). See composition guide in the visual vocabularies series.

## Implementation Details

### Dependencies

- Python 3.8+
- fastmcp (for MCP server)
- No external API calls
- All operations deterministic and local

### File Structure

```
cocktail-aesthetics-mcp/
├── cocktail_aesthetics_mcp.py    # Layer 3: MCP interface
├── cocktail_ologs.py              # Layer 1 & 2: Taxonomy and morphisms
├── cocktail_profiles.json         # Cocktail data
├── requirements.txt               # Dependencies
└── README.md                       # This file
```

### Performance

- Cold start: ~100ms (olog loading)
- Per-query: <5ms (dictionary lookups)
- Token cost: Single LLM call for synthesis (vs. multiple calls without vocabulary)

## Example Usage

### Use Case 1: Consistent Visual Direction

You want images with "sophisticated, warm, spirit-forward aesthetic":

```
Prompt: "Old Fashioned aesthetic for a luxury whiskey campaign"
↓
MCP looks up Old Fashioned vocabulary
↓
Claude receives: moody_amber lighting, amber/brown colors, balanced composition, oily texture, sophisticated mood
↓
Final prompt includes these locked parameters
↓
Output: Consistent aesthetic across all generations
```

### Use Case 2: Exploring Flavor Profiles

Find cocktails with specific flavor characteristics:

```
Search: "bitter cocktails"
↓
Returns: Negroni, Espresso Martini
↓
You choose Negroni for its sophisticated, elegant mood
↓
Vocabulary applied to your image generation
```

### Use Case 3: Creative Combination

Layer multiple vocabularies for complex aesthetics:

```
Base: "A portrait of someone at a bar"
+ Cocktail (Negroni): sophisticated, elegant, balanced
+ Magazine Photography (Vogue 1980s): glamorous, dramatic, saturated
= Negroni-inspired portrait in 1980s Vogue aesthetic
```

## Limitations and Intentionality

These parameters represent specific aesthetic choices, not universal truth. A bartender might refine these differently. A cinematographer might build an entirely different set. The structure is what matters: locked parameters that compose predictably.

The vocabulary is most effective for:
- Brand consistency in product photography
- Thematic image series
- Exploring how specific aesthetic parameters affect output
- Building reproducible AI workflows

Use with caution for:
- Representing actual cocktail colors (real drinks vary by lighting and ingredients)
- Cultural accuracy (aesthetic choices are subjective)

## Contributing

This vocabulary is designed to be forked and modified. If you build variations or extensions:

1. Document your morphism logic
2. Test consistency across multiple generations
3. Consider composition with other vocabularies
4. Share your work

## License

See LICENSE

## Related

Part of the Lushy.app Visual Vocabularies ecosystem:
- [Magazine Photography Aesthetics](https://github.com/dmarsters/magazine-photography-mcp)
- [Slapstick Design Principles](https://github.com/dmarsters/slapstick-enhancer)
- [Terpene-based Aesthetics](https://github.com/dmarsters/terpene-mcp-server)
- [Constellation Composition](https://github.com/dmarsters/constellation-composition-mcp)

See the visual vocabularies intro post for context on how these systems work together.

## Questions?

Open an issue or reach out. This is an active project exploring how deterministic aesthetic structures can enhance creative AI workflows.
