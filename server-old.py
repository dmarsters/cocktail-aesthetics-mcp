"""
Cocktail Aesthetics MCP Server

Maps cocktail profiles to visual enhancement parameters using deterministic taxonomy.
Provides cost-optimized hybrid architecture: local mapping + single LLM synthesis.
"""

from fastmcp import FastMCP
from typing import Literal

mcp = FastMCP("cocktail-aesthetics")

# Comprehensive cocktail taxonomy with visual parameter mappings
COCKTAIL_TAXONOMY = {
    "negroni": {
        "family": "spirit_forward",
        "base_spirit": "gin",
        "color_palette": ["#8B1A1A", "#D2691E", "#FFA500"],
        "color_description": "bold triadic red-orange-amber",
        "lighting": "warm side-lit, Italian golden hour, amber backlight",
        "mood": "bitter sophistication, aperitivo elegance, modernist simplicity",
        "composition": "balanced triadic, architectural precision, geometric",
        "texture": "smooth with orange oil sheen, glass clarity, ice refraction",
        "cultural_context": "Italian design sensibility, mid-century modernism",
        "temporal_association": "pre-dinner, golden hour, 6pm ritual",
        "technique": "stirred - smooth gradients, elegant composure"
    },
    "martini": {
        "family": "spirit_forward",
        "base_spirit": "gin_or_vodka",
        "color_palette": ["#F5F5F5", "#E8E8E8", "#C0C0C0"],
        "color_description": "crystalline clear to pale silver",
        "lighting": "sharp key light, Art Deco chrome reflections, cold clarity",
        "mood": "geometric precision, sophisticated restraint, timeless elegance",
        "composition": "minimalist vertical, conical symmetry, negative space mastery",
        "texture": "ice-cold silky, pristine clarity, condensation droplets",
        "cultural_context": "Art Deco luxury, film noir mystique, James Bond cool",
        "temporal_association": "evening sophistication, cocktail hour proper",
        "technique": "stirred - crystalline perfection, no bubbles"
    },
    "mai_tai": {
        "family": "tiki",
        "base_spirit": "rum",
        "color_palette": ["#FF6B35", "#F7931E", "#8B4513", "#00A86B"],
        "color_description": "tropical sunset gradient with mint green accents",
        "lighting": "vintage tiki torch glow, warm tropical sunset, bamboo-filtered light",
        "mood": "escapist maximalism, mid-century exotica, playful abundance",
        "composition": "layered complexity, garnish abundance, vertical drama",
        "texture": "crushed ice shimmer, orgeat creaminess, multiple textures",
        "cultural_context": "Polynesian pop, 1950s escapism, Don the Beachcomber mystique",
        "temporal_association": "vacation mode, eternal summer, 5 o'clock somewhere",
        "technique": "shaken then built - dynamic layers, textured ice"
    },
    "old_fashioned": {
        "family": "spirit_forward",
        "base_spirit": "whiskey",
        "color_palette": ["#8B4513", "#D2691E", "#CD853F"],
        "color_description": "warm amber to deep mahogany",
        "lighting": "warm intimate spotlight, leather-bound library light, single source dramatic",
        "mood": "masculine refinement, contemplative sophistication, timeless tradition",
        "composition": "minimalist centered, single large cube as negative space, classic balance",
        "texture": "smooth whiskey viscosity, large ice cube clarity, sugar grain sparkle",
        "cultural_context": "gentleman's club, craft cocktail revival, bourbon heritage",
        "temporal_association": "after-work unwind, winter evening, slow contemplation",
        "technique": "stirred - deliberate slow integration, single large cube"
    },
    "aperol_spritz": {
        "family": "spritz",
        "base_spirit": "aperol",
        "color_palette": ["#FF4500", "#FF6347", "#FFA07A", "#FFD700"],
        "color_description": "sunset orange gradient with golden effervescence",
        "lighting": "soft diffused golden hour, piazza afternoon glow, sparkling highlights",
        "mood": "dolce vita ease, effervescent joy, social lightness",
        "composition": "bubbly vertical movement, casual asymmetry, orange slice geometry",
        "texture": "champagne bubble streams, prosecco effervescence, ice dilution",
        "cultural_context": "Italian aperitivo culture, European cafe society, Instagram aesthetic",
        "temporal_association": "afternoon pre-dinner, summer terrace, 4-6pm social hour",
        "technique": "built directly - casual construction, bubble preservation"
    },
    "espresso_martini": {
        "family": "after_dinner",
        "base_spirit": "vodka",
        "color_palette": ["#2C1810", "#3E2723", "#EFEBE9"],
        "color_description": "dark espresso with creamy foam crown",
        "lighting": "high contrast dramatic, nightclub spotlight, foam highlight",
        "mood": "caffeinated energy, modern nightlife, sophisticated hedonism",
        "composition": "high contrast zones, foam crown as focal point, three-bean symmetry",
        "texture": "velvety crema, syrupy body, silky foam",
        "cultural_context": "1990s London revival, nightlife glamour, coffee culture fusion",
        "temporal_association": "late night energy, dessert replacement, 11pm second wind",
        "technique": "shaken hard - espresso crema, frothy crown"
    },
    "mojito": {
        "family": "highball",
        "base_spirit": "rum",
        "color_palette": ["#98FF98", "#FFFFFF", "#F0FFF0", "#7CFC00"],
        "color_description": "fresh mint green with sparkling clarity",
        "lighting": "bright natural daylight, Caribbean sunshine, crystalline clarity",
        "mood": "refreshing vitality, tropical freshness, casual beachside ease",
        "composition": "vertical highball, muddled texture at base, ice and mint throughout",
        "texture": "crushed mint leaves, soda fizz, granulated sugar sparkle",
        "cultural_context": "Havana heritage, beach bar staple, Ernest Hemingway legend",
        "temporal_association": "hot afternoon refreshment, poolside leisure, summer peak",
        "technique": "muddled - textured organic elements, built with soda"
    },
    "margarita": {
        "family": "sour",
        "base_spirit": "tequila",
        "color_palette": ["#FFFACD", "#90EE90", "#FFFFFF"],
        "color_description": "pale lime yellow-green with salt crystal rim",
        "lighting": "bright Mexican sunshine, agave field light, salt crystal sparkle",
        "mood": "festive celebration, tequila confidence, citrus brightness",
        "composition": "wide coupe or rocks, salt rim as frame, lime wheel accent",
        "texture": "coarse salt crystals, icy dilution, citrus pulp",
        "cultural_context": "Mexican tradition, Tex-Mex Americana, vacation celebration",
        "temporal_association": "fiesta mood, summer evening, taco pairing",
        "technique": "shaken - frothy integration, salt rim ritual"
    },
    "manhattan": {
        "family": "spirit_forward",
        "base_spirit": "whiskey",
        "color_palette": ["#8B0000", "#A52A2A", "#CD5C5C"],
        "color_description": "deep ruby red with vermouth richness",
        "lighting": "warm amber bar light, wood-paneled intimacy, cherry glow",
        "mood": "New York sophistication, pre-Prohibition elegance, cocktail formality",
        "composition": "coupe or Nick & Nora elegance, cherry as jewel focal point",
        "texture": "silky vermouth integration, maraschino syrup viscosity",
        "cultural_context": "Manhattan club society, classic cocktail canon, Mad Men aesthetic",
        "temporal_association": "pre-dinner elegant, winter warmth, formal evening",
        "technique": "stirred - perfect integration, cherry garnish"
    },
    "penicillin": {
        "family": "modern_classic",
        "base_spirit": "scotch",
        "color_palette": ["#F4E4C1", "#FFD700", "#8B7355"],
        "color_description": "golden honey with smoky overlay",
        "lighting": "warm honey glow with mysterious smoky haze",
        "mood": "craft cocktail innovation, medicinal intrigue, smoky sophistication",
        "composition": "rocks glass grounded, smoke wisp drama, ginger spice texture",
        "texture": "honey viscosity, ginger pulp, Islay smoke",
        "cultural_context": "2000s craft cocktail movement, Sam Ross legend, modern canon",
        "temporal_association": "winter warmer, cold remedy mystique, evening contemplation",
        "technique": "shaken with float - layered smoke drama"
    },
    "daiquiri": {
        "family": "sour",
        "base_spirit": "rum",
        "color_palette": ["#FFFACD", "#F0E68C", "#FFFFFF"],
        "color_description": "pale lime clarity, crystalline simplicity",
        "lighting": "clean bright light, Caribbean clarity, lime zest highlights",
        "mood": "pure simplicity, rum authenticity, beach bar stripped-down",
        "composition": "minimalist coupe, three-ingredient honesty, lime wheel elegance",
        "texture": "silky shaken integration, slight foam cap, pure liquid",
        "cultural_context": "Hemingway Cuba, classic simplicity, anti-frozen backlash",
        "temporal_association": "hot afternoon perfection, beach sunset, summer purity",
        "technique": "shaken - frothy integration, elegant simplicity"
    },
    "boulevardier": {
        "family": "spirit_forward",
        "base_spirit": "whiskey",
        "color_palette": ["#8B0000", "#A0522D", "#CD853F"],
        "color_description": "deep burgundy red with bourbon warmth",
        "lighting": "warm bistro light, Parisian cafe glow, vermouth sheen",
        "mood": "Continental sophistication, American-in-Paris mystique, bitter elegance",
        "composition": "Nick & Nora or coupe, orange twist as focal point",
        "texture": "bourbon warmth, Campari bitter coating, vermouth silk",
        "cultural_context": "1920s Paris expatriate, Negroni's bourbon cousin, literary sophistication",
        "temporal_association": "pre-dinner Parisian, autumn evening, intellectual conversation",
        "technique": "stirred - smooth integration, orange oils"
    },
    "aviation": {
        "family": "floral_sour",
        "base_spirit": "gin",
        "color_palette": ["#E6E6FA", "#DDA0DD", "#F0E68C"],
        "color_description": "pale sky blue-violet from crème de violette",
        "lighting": "soft diffused ethereal, cloud-filtered light, lavender haze",
        "mood": "romantic nostalgia, pre-Prohibition revival, floral delicacy",
        "composition": "coupe elegance, cherry floating like cloud, pastel dream",
        "texture": "silky maraschino luxe, gin botanical, violet perfume",
        "cultural_context": "Golden Age aviation romance, craft cocktail archeology, violet mystique",
        "temporal_association": "romantic evening, spring celebration, vintage fantasy",
        "technique": "shaken - delicate frothy integration"
    },
    "pisco_sour": {
        "family": "sour",
        "base_spirit": "pisco",
        "color_palette": ["#FFFACD", "#FFFFFF", "#8B4513"],
        "color_description": "pale yellow with pure white egg foam crown",
        "lighting": "Andean sunlight, foam highlight, bitters dots as focal points",
        "mood": "Peruvian pride, South American sophistication, foam artistry",
        "composition": "coupe with foam crown, Angostura bitters dots as design",
        "texture": "silky egg white foam, pisco grape spirit, lime tartness",
        "cultural_context": "Peruvian national drink, Chilean rivalry, Lima cocktail culture",
        "temporal_association": "afternoon sophistication, ceviche pairing, celebration",
        "technique": "dry shake then wet shake - meringue foam perfection"
    },
    "corpse_reviver_2": {
        "family": "floral_sour",
        "base_spirit": "gin",
        "color_palette": ["#FFFACD", "#F0E68C", "#98FB98"],
        "color_description": "pale yellow-green with absinthe mist",
        "lighting": "ethereal morning light, absinthe louche, hair-of-the-dog clarity",
        "mood": "morning after mystique, restorative ritual, equal parts balance",
        "composition": "coupe precision, four equal parts harmony, absinthe rinse haze",
        "texture": "Lillet silk, absinthe anise coating, Cointreau citrus oil",
        "cultural_context": "Savoy cocktail canon, hangover cure legend, Harry Craddock mystique",
        "temporal_association": "brunch revival, morning restoration, hair of the dog",
        "technique": "shaken with absinthe rinse - louche mist drama"
    },
    "last_word": {
        "family": "floral_sour",
        "base_spirit": "gin",
        "color_palette": ["#90EE90", "#98FB98", "#F0E68C"],
        "color_description": "pale chartreuse green, equal parts balance",
        "lighting": "mysterious green glow, herbal liqueur luminescence, botanical clarity",
        "mood": "Prohibition mystique, equal parts egalitarian, craft cocktail resurrection",
        "composition": "coupe symmetry, lime wheel focus, green liqueur glow",
        "texture": "Chartreuse herbal viscosity, Maraschino luxe, lime tartness",
        "cultural_context": "Detroit Athletic Club origin, 2000s craft revival, equal parts philosophy",
        "temporal_association": "sophisticated evening, herbal complexity, balanced contemplation",
        "technique": "shaken - equal parts precision, balanced integration"
    },
    "dark_and_stormy": {
        "family": "highball",
        "base_spirit": "rum",
        "color_palette": ["#2C1810", "#8B4513", "#F4E4C1"],
        "color_description": "dark rum depths with ginger beer foam crown",
        "lighting": "stormy dramatic contrast, dark base with bright foam highlights",
        "mood": "Caribbean tempest, Bermuda tradition, spicy warmth",
        "composition": "highball verticality, dark rum base with ginger foam storm on top",
        "texture": "dark rum richness, ginger beer spice fizz, lime oil",
        "cultural_context": "Bermuda national drink, Gosling's trademark, tropical storm metaphor",
        "temporal_association": "hot afternoon cooling, tropical vacation, beach bar staple",
        "technique": "built - dramatic float, no stir preserves layers"
    },
    "sazerac": {
        "family": "spirit_forward",
        "base_spirit": "rye",
        "color_palette": ["#8B4513", "#D2691E", "#F5F5DC"],
        "color_description": "amber rye with absinthe haze, lemon oil mist",
        "lighting": "warm New Orleans gas lamp, absinthe mist glow, lemon oil atomization",
        "mood": "New Orleans mystique, Creole sophistication, ritual precision",
        "composition": "rocks glass ceremony, absinthe rinse ritual, lemon peel twist drama",
        "texture": "rye spice warmth, absinthe anise coating, sugar cube integration",
        "cultural_context": "New Orleans oldest cocktail claim, Creole heritage, French Quarter ritual",
        "temporal_association": "evening ceremony, contemplative sipping, bourbon street sophistication",
        "technique": "stirred with absinthe rinse - ritual performance, lemon oils only"
    },
    "bramble": {
        "family": "sour",
        "base_spirit": "gin",
        "color_palette": ["#FFFACD", "#8B008B", "#C71585"],
        "color_description": "pale lemon with dark blackberry liqueur drizzle",
        "lighting": "British summer garden light, berry stain drama, crushed ice sparkle",
        "mood": "modern British classic, blackberry hedgerow, garden party elegance",
        "composition": "rocks glass with crushed ice, liqueur drizzle as visual drama",
        "texture": "crushed ice pebbles, blackberry syrup drizzle, lemon tartness",
        "cultural_context": "Dick Bradsell invention, 1980s British cocktail renaissance, hedgerow foraging",
        "temporal_association": "summer garden party, British countryside, afternoon refreshment",
        "technique": "built on crushed ice - liqueur drizzle for visual effect"
    },
    "vieux_carre": {
        "family": "spirit_forward",
        "base_spirit": "rye_cognac",
        "color_palette": ["#8B0000", "#8B4513", "#A52A2A"],
        "color_description": "deep burgundy-amber blend, cognac and rye marriage",
        "lighting": "French Quarter dim lamp light, carousel bar glow, Benedictine sheen",
        "mood": "French Quarter decadence, Creole complexity, equal parts sophistication",
        "composition": "rocks glass grounded, lemon twist elegance, layered spirits",
        "texture": "cognac silk with rye spice, Benedictine herbal coating, bitters complexity",
        "cultural_context": "Hotel Monteleone legend, New Orleans French influence, carousel bar mystique",
        "temporal_association": "late evening sophistication, winter warmth, contemplative nightcap",
        "technique": "stirred - complex spirit integration, lemon twist"
    }
}

# Cocktail family characteristics for broader queries
FAMILY_CHARACTERISTICS = {
    "spirit_forward": {
        "description": "Minimal dilution, spirit-showcasing, sophisticated simplicity",
        "lighting": "warm intimate, dramatic single source, spirit color glow",
        "mood": "contemplative elegance, adult sophistication, slow sipping",
        "composition": "minimalist, centered focus, negative space mastery"
    },
    "sour": {
        "description": "Citrus-balanced, refreshing tartness, foam cap potential",
        "lighting": "bright citrus highlights, foam crown spotlight, clean clarity",
        "mood": "refreshing vitality, balanced sophistication, citrus brightness",
        "composition": "coupe elegance or rocks glass, foam/ice as texture"
    },
    "tiki": {
        "description": "Tropical maximalism, layered complexity, garnish abundance",
        "lighting": "warm tiki torch glow, tropical sunset, bamboo-filtered",
        "mood": "escapist fantasy, playful exoticism, vacation mindset",
        "composition": "vertical drama, layered colors, garnish explosion"
    },
    "highball": {
        "description": "Tall and refreshing, effervescent, casual elegance",
        "lighting": "bright natural or casual bar light, bubble highlights, ice sparkle",
        "mood": "casual refreshment, social ease, approachable sophistication",
        "composition": "vertical glass, ice and carbonation texture, simple garnish"
    },
    "after_dinner": {
        "description": "Rich and indulgent, dessert-like, coffee or cream elements",
        "lighting": "dramatic contrast, spotlight on crema/foam, nightlife glow",
        "mood": "indulgent sophistication, late night energy, dessert replacement",
        "composition": "high contrast zones, foam or cream as focal point"
    }
}

@mcp.tool()
def enhance_with_cocktail_aesthetic(
    base_prompt: str,
    cocktail: str
) -> dict:
    """
    Enhance an image prompt with cocktail-derived visual aesthetics.
    
    This tool maps cocktail profiles to visual enhancement parameters using deterministic
    taxonomy. The output is structured JSON that can be synthesized by an LLM into a
    natural language prompt.
    
    Args:
        base_prompt: The original image description (e.g., "a bottle of hot sauce", "portrait of a chef")
        cocktail: Name of cocktail (e.g., "negroni", "mai tai", "martini")
    
    Returns:
        Dictionary with cocktail-derived visual parameters and synthesis instructions
    """
    cocktail_key = cocktail.lower().replace(" ", "_").replace("-", "_")
    
    cocktail_data = COCKTAIL_TAXONOMY.get(cocktail_key)
    
    if not cocktail_data:
        available = ", ".join(sorted(COCKTAIL_TAXONOMY.keys()))
        return {
            "error": f"Cocktail '{cocktail}' not found in taxonomy",
            "available_cocktails": available,
            "suggestion": "Try one of the available cocktails or use list_available_cocktails tool"
        }
    
    enhancement = {
        "cocktail_name": cocktail,
        "base_prompt": base_prompt,
        "visual_parameters": {
            "color_palette": cocktail_data["color_palette"],
            "color_description": cocktail_data["color_description"],
            "lighting_style": cocktail_data["lighting"],
            "mood_keywords": cocktail_data["mood"],
            "composition_guide": cocktail_data["composition"],
            "texture_notes": cocktail_data["texture"],
            "cultural_context": cocktail_data["cultural_context"],
            "temporal_association": cocktail_data["temporal_association"],
            "technique_influence": cocktail_data["technique"]
        },
        "cocktail_metadata": {
            "family": cocktail_data["family"],
            "base_spirit": cocktail_data["base_spirit"]
        },
        "synthesis_instructions": {
            "approach": "Weave cocktail aesthetics naturally into the base prompt",
            "priority": "Color palette and lighting should be primary, mood and composition secondary",
            "avoid": "Don't literally mention the cocktail unless contextually appropriate",
            "style": "Create vivid, sensory-rich description that captures cocktail essence visually"
        }
    }
    
    return enhancement


@mcp.tool()
def list_available_cocktails() -> dict:
    """
    List all available cocktails with their families and brief descriptions.
    
    Returns:
        Dictionary organized by cocktail family with cocktail names and basic info
    """
    by_family = {}
    
    for cocktail_name, data in COCKTAIL_TAXONOMY.items():
        family = data["family"]
        if family not in by_family:
            by_family[family] = []
        
        by_family[family].append({
            "name": cocktail_name,
            "base_spirit": data["base_spirit"],
            "color_description": data["color_description"],
            "mood": data["mood"].split(",")[0],  # Just first mood keyword
            "era": data["cultural_context"].split(",")[0]
        })
    
    return {
        "total_cocktails": len(COCKTAIL_TAXONOMY),
        "families": list(by_family.keys()),
        "cocktails_by_family": by_family,
        "usage_tip": "Use enhance_with_cocktail_aesthetic with any cocktail name from this list"
    }


@mcp.tool()
def get_cocktail_details(cocktail: str) -> dict:
    """
    Get comprehensive details about a specific cocktail's visual profile.
    
    Args:
        cocktail: Name of cocktail (e.g., "negroni", "mai tai")
    
    Returns:
        Full cocktail taxonomy entry with all visual parameters
    """
    cocktail_key = cocktail.lower().replace(" ", "_").replace("-", "_")
    
    cocktail_data = COCKTAIL_TAXONOMY.get(cocktail_key)
    
    if not cocktail_data:
        available = ", ".join(sorted(COCKTAIL_TAXONOMY.keys()))
        return {
            "error": f"Cocktail '{cocktail}' not found",
            "available_cocktails": available
        }
    
    return {
        "cocktail_name": cocktail,
        "profile": cocktail_data,
        "family_characteristics": FAMILY_CHARACTERISTICS.get(cocktail_data["family"], {})
    }


@mcp.tool()
def search_cocktails_by_mood(
    mood: Literal[
        "sophisticated",
        "refreshing", 
        "escapist",
        "contemplative",
        "festive",
        "elegant",
        "playful",
        "mysterious",
        "indulgent"
    ]
) -> dict:
    """
    Find cocktails that match a desired mood or aesthetic feeling.
    
    Args:
        mood: Desired mood/feeling for the visual aesthetic
    
    Returns:
        List of cocktails that embody that mood with their visual characteristics
    """
    mood_lower = mood.lower()
    matching = []
    
    for cocktail_name, data in COCKTAIL_TAXONOMY.items():
        cocktail_mood = data["mood"].lower()
        if mood_lower in cocktail_mood:
            matching.append({
                "name": cocktail_name,
                "mood": data["mood"],
                "color_description": data["color_description"],
                "lighting": data["lighting"],
                "cultural_context": data["cultural_context"]
            })
    
    return {
        "mood_query": mood,
        "matches_found": len(matching),
        "cocktails": matching
    }


@mcp.tool()
def search_cocktails_by_color(
    color_preference: Literal[
        "red",
        "amber",
        "golden",
        "clear",
        "green",
        "purple",
        "orange",
        "dark",
        "pale"
    ]
) -> dict:
    """
    Find cocktails by their dominant color palette.
    
    Args:
        color_preference: Dominant color desired in the aesthetic
    
    Returns:
        List of cocktails featuring that color with their palettes
    """
    color_map = {
        "red": ["red", "burgundy", "ruby"],
        "amber": ["amber", "mahogany", "brown"],
        "golden": ["golden", "gold", "yellow"],
        "clear": ["clear", "crystalline", "silver", "white"],
        "green": ["green", "mint", "chartreuse", "lime"],
        "purple": ["purple", "violet", "lavender"],
        "orange": ["orange", "sunset"],
        "dark": ["dark", "espresso", "black"],
        "pale": ["pale", "light"]
    }
    
    search_terms = color_map.get(color_preference.lower(), [color_preference.lower()])
    matching = []
    
    for cocktail_name, data in COCKTAIL_TAXONOMY.items():
        color_desc = data["color_description"].lower()
        if any(term in color_desc for term in search_terms):
            matching.append({
                "name": cocktail_name,
                "color_description": data["color_description"],
                "color_palette": data["color_palette"],
                "lighting": data["lighting"]
            })
    
    return {
        "color_query": color_preference,
        "matches_found": len(matching),
        "cocktails": matching
    }


@mcp.tool()
def get_cocktail_family_aesthetic(
    family: Literal[
        "spirit_forward",
        "sour",
        "tiki",
        "highball",
        "after_dinner",
        "floral_sour",
        "spritz",
        "modern_classic"
    ]
) -> dict:
    """
    Get the general aesthetic characteristics of a cocktail family.
    
    Useful for understanding broader aesthetic categories rather than specific cocktails.
    
    Args:
        family: Cocktail family type
    
    Returns:
        Family characteristics and example cocktails from that family
    """
    family_chars = FAMILY_CHARACTERISTICS.get(family, {})
    
    examples = []
    for cocktail_name, data in COCKTAIL_TAXONOMY.items():
        if data["family"] == family:
            examples.append({
                "name": cocktail_name,
                "color_description": data["color_description"],
                "mood": data["mood"]
            })
    
    return {
        "family": family,
        "characteristics": family_chars,
        "example_cocktails": examples[:5],  # Show up to 5 examples
        "total_in_family": len(examples)
    }


if __name__ == "__main__":
    mcp.run()