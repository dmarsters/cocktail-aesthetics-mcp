"""
Cocktail Aesthetics MCP Server
Layer 3: FastMCP interface for cocktail aesthetic enhancement

Provides Claude with tools to:
- Get visual aesthetic parameters for any cocktail
- Enhance image prompts with cocktail-inspired aesthetics
- Query cocktail flavor profiles
"""

from fastmcp import FastMCP
from typing import Optional
import json
import os

from cocktail_ologs import (
    CocktailOlogMorphisms,
    CocktailProfile,
    VisualParameters,
)

# Initialize MCP server
mcp = FastMCP("cocktail-aesthetics")

# ============================================================================
# COCKTAIL TAXONOMY DATA
# ============================================================================

COCKTAIL_TAXONOMY = {
    "negroni": {
        "name": "Negroni",
        "spirit_base": "gin",
        "primary_flavor": "bitter",
        "complexity": "simple",
        "bitterness": 8,
        "sweetness": 3,
        "richness": 6,
        "color_palette": ["#8B1A1A", "#D2691E", "#FFA500"],
        "has_cream": False,
        "has_ice": True,
        "is_effervescent": False,
        "description": "Classic aperitivo: gin, Campari, vermouth rosso. Bitter, bold, balanced.",
    },
    "mai_tai": {
        "name": "Mai Tai",
        "spirit_base": "rum",
        "primary_flavor": "fruity",
        "complexity": "complex",
        "bitterness": 2,
        "sweetness": 6,
        "richness": 8,
        "color_palette": ["#FF6B35", "#F7931E", "#8B4513", "#00A86B"],
        "has_cream": False,
        "has_ice": True,
        "is_effervescent": False,
        "description": "Tiki classic: aged rum, lime, orgeat, curaçao. Sweet, tropical, complex.",
    },
    "daiquiri": {
        "name": "Daiquiri",
        "spirit_base": "rum",
        "primary_flavor": "sour",
        "complexity": "simple",
        "bitterness": 1,
        "sweetness": 3,
        "richness": 3,
        "color_palette": ["#FFF8DC", "#FFE4B5", "#F0E68C"],
        "has_cream": False,
        "has_ice": True,
        "is_effervescent": False,
        "description": "Elegant simplicity: white rum, fresh lime, simple syrup.",
    },
    "old_fashioned": {
        "name": "Old Fashioned",
        "spirit_base": "whiskey",
        "primary_flavor": "spirit_forward",
        "complexity": "simple",
        "bitterness": 4,
        "sweetness": 2,
        "richness": 7,
        "color_palette": ["#8B4513", "#A0522D", "#654321"],
        "has_cream": False,
        "has_ice": True,
        "is_effervescent": False,
        "description": "Timeless classic: whiskey, sugar, bitters, orange twist.",
    },
    "mojito": {
        "name": "Mojito",
        "spirit_base": "rum",
        "primary_flavor": "herbal",
        "complexity": "moderate",
        "bitterness": 1,
        "sweetness": 4,
        "richness": 2,
        "color_palette": ["#00AA66", "#FFE4B5", "#FFFFFF"],
        "has_cream": False,
        "has_ice": True,
        "is_effervescent": True,
        "description": "Refreshing summer drink: white rum, mint, lime, soda, sugar.",
    },
    "margarita": {
        "name": "Margarita",
        "spirit_base": "tequila",
        "primary_flavor": "sour",
        "complexity": "moderate",
        "bitterness": 0,
        "sweetness": 4,
        "richness": 3,
        "color_palette": ["#FFE4B5", "#FFA500", "#FF6347"],
        "has_cream": False,
        "has_ice": True,
        "is_effervescent": False,
        "description": "Iconic: tequila, lime, triple sec, salt rim.",
    },
    "espresso_martini": {
        "name": "Espresso Martini",
        "spirit_base": "vodka",
        "primary_flavor": "bitter",
        "complexity": "moderate",
        "bitterness": 6,
        "sweetness": 5,
        "richness": 8,
        "color_palette": ["#2F4F4F", "#8B7355", "#FFFFFF"],
        "has_cream": False,
        "has_ice": False,
        "is_effervescent": False,
        "description": "Modern sophistication: vodka, coffee liqueur, espresso, cream.",
    },
    "sazerac": {
        "name": "Sazerac",
        "spirit_base": "whiskey",
        "primary_flavor": "herbal",
        "complexity": "simple",
        "bitterness": 5,
        "sweetness": 1,
        "richness": 6,
        "color_palette": ["#A0522D", "#8B4513", "#FFD700"],
        "has_cream": False,
        "has_ice": True,
        "is_effervescent": False,
        "description": "New Orleans classic: rye, absinthe, Peychaud's bitters.",
    },
}

# ============================================================================
# CACHED PROFILES
# ============================================================================

_profile_cache: dict = {}

def _ensure_cached():
    """Load all cocktail profiles into cache"""
    if not _profile_cache:
        for cocktail_key, cocktail_data in COCKTAIL_TAXONOMY.items():
            try:
                profile = CocktailOlogMorphisms.cocktail_to_profile(cocktail_data)
                _profile_cache[cocktail_key] = profile
            except Exception as e:
                print(f"Error processing {cocktail_key}: {e}")


# ============================================================================
# MCP TOOLS
# ============================================================================

@mcp.tool()
def list_cocktails() -> dict:
    """
    Get list of available cocktails.
    Returns cocktail names and their primary characteristics.
    """
    _ensure_cached()
    cocktails = []
    for key, profile in _profile_cache.items():
        cocktails.append({
            "id": key,
            "name": profile.name,
            "spirit_base": profile.spirit_base.value,
            "primary_flavor": profile.primary_flavor.value,
            "description": profile.description,
        })
    return {
        "cocktails": cocktails,
        "count": len(cocktails),
    }


@mcp.tool()
def get_cocktail_profile(cocktail_name: str) -> dict:
    """
    Get detailed profile for a specific cocktail.
    
    Args:
        cocktail_name: Name of cocktail (case-insensitive)
    
    Returns:
        Complete cocktail profile including flavor and visual parameters
    """
    _ensure_cached()
    
    key = cocktail_name.lower().replace(" ", "_").replace("-", "_")
    if key not in _profile_cache:
        return {"error": f"Cocktail '{cocktail_name}' not found"}
    
    profile = _profile_cache[key]
    return {
        "name": profile.name,
        "spirit_base": profile.spirit_base.value,
        "primary_flavor": profile.primary_flavor.value,
        "flavor_profile": {
            "complexity": profile.flavor_profile.complexity.value,
            "bitterness": profile.flavor_profile.bitterness,
            "sweetness": profile.flavor_profile.sweetness,
            "richness": profile.flavor_profile.richness,
            "warmth_level": profile.flavor_profile.warmth_level,
        },
        "description": profile.description,
    }


@mcp.tool()
def get_visual_parameters(cocktail_name: str) -> dict:
    """
    Get visual aesthetic parameters for a cocktail.
    Use this to enhance image generation prompts.
    
    Args:
        cocktail_name: Name of cocktail
    
    Returns:
        Visual parameters including color, lighting, mood, composition, texture
    """
    _ensure_cached()
    
    key = cocktail_name.lower().replace(" ", "_").replace("-", "_")
    if key not in _profile_cache:
        return {"error": f"Cocktail '{cocktail_name}' not found"}
    
    profile = _profile_cache[key]
    visual = profile.visual_parameters
    
    return {
        "cocktail": profile.name,
        "visual_parameters": visual.to_dict(),
        "composition_strategy": visual.composition_strategy.value,
        "temperature_vibe": visual.temperature_vibe.value,
        "mood_keywords": [visual.primary_mood.value] + [m.value for m in visual.secondary_moods],
    }


@mcp.tool()
def enhance_prompt_with_cocktail(base_prompt: str, cocktail_name: str) -> dict:
    """
    Enhance an image generation prompt with cocktail aesthetics.
    
    This tool provides deterministic visual parameters that can be incorporated
    into prompts for image generators. It combines the cocktail's:
    - Color palette
    - Lighting style
    - Mood and emotional tone
    - Composition approach
    - Texture characteristics
    
    Args:
        base_prompt: The original image prompt
        cocktail_name: Name of cocktail to inspire aesthetics
    
    Returns:
        Enhancement parameters ready to use in image generation
    """
    _ensure_cached()
    
    key = cocktail_name.lower().replace(" ", "_").replace("-", "_")
    if key not in _profile_cache:
        return {"error": f"Cocktail '{cocktail_name}' not found"}
    
    profile = _profile_cache[key]
    visual = profile.visual_parameters
    
    enhancement = {
        "original_prompt": base_prompt,
        "cocktail": profile.name,
        "color_direction": visual.color_palette,
        "lighting_style": visual.lighting_style.value,
        "mood_keywords": [visual.primary_mood.value] + [m.value for m in visual.secondary_moods],
        "composition_guide": visual.composition_strategy.value,
        "texture_notes": visual.texture_quality.value,
        "temperature_vibe": visual.temperature_vibe.value,
        "suggested_enhancement": (
            f"Add these aesthetic qualities to your prompt: {', '.join([visual.primary_mood.value] + [m.value for m in visual.secondary_moods])}. "
            f"Use {visual.lighting_style.value} lighting. "
            f"Color palette suggestion: {', '.join(visual.color_palette[:2])}. "
            f"Composition: {visual.composition_strategy.value}. "
            f"Texture: {visual.texture_quality.value}."
        ),
    }
    
    return enhancement


@mcp.tool()
def search_cocktails_by_flavor(flavor: str) -> dict:
    """
    Find cocktails matching a specific flavor profile.
    
    Args:
        flavor: Flavor type (bitter, sweet, sour, spirit_forward, herbal, fruity, creamy, spiced, smoky)
    
    Returns:
        List of cocktails with that primary flavor
    """
    _ensure_cached()
    
    flavor_lower = flavor.lower()
    matching = []
    
    for key, profile in _profile_cache.items():
        if profile.primary_flavor.value == flavor_lower:
            matching.append({
                "name": profile.name,
                "id": key,
                "description": profile.description,
            })
    
    return {
        "flavor": flavor_lower,
        "matches": matching,
        "count": len(matching),
    }


@mcp.tool()
def get_spirit_warmth(spirit_name: str) -> dict:
    """
    Get the warmth/nostalgia level of a spirit on a 0-10 scale.
    Warm spirits (rum, whiskey, cognac) suggest golden hour, ambient lighting.
    Cool spirits (vodka, gin) suggest crisp, clean aesthetics.
    
    Args:
        spirit_name: Type of spirit (rum, whiskey, vodka, gin, tequila, cognac, mezcal)
    
    Returns:
        Warmth level (0-10) and interpretation
    """
    spirit_lower = spirit_name.lower()
    
    warmth_map = {
        "rum": 9,
        "whiskey": 8,
        "cognac": 9,
        "mezcal": 8,
        "tequila": 7,
        "gin": 5,
        "vodka": 3,
    }
    
    if spirit_lower not in warmth_map:
        return {"error": f"Spirit '{spirit_name}' not recognized"}
    
    warmth = warmth_map[spirit_lower]
    interpretation = (
        "very warm, golden, nostalgic" if warmth >= 8 else
        "warm, moderate, balanced" if warmth >= 6 else
        "cool, crisp, clean"
    )
    
    return {
        "spirit": spirit_lower,
        "warmth_level": warmth,
        "interpretation": interpretation,
    }


# ============================================================================
# SERVER INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    # Load cache on startup
    _ensure_cached()
    print(f"✓ Loaded {len(_profile_cache)} cocktail profiles")
    print("Starting MCP server on stdio...")
    mcp.run()
