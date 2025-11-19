"""
Cocktail Aesthetics Olog System
Three-layer architecture: Categorical taxonomy → Cocktail profiles → MCP interface

This olog formalizes the semantic relationships between:
- Cocktail types (spirit base, flavor profile, preparation style)
- Flavor characteristics (bitterness, sweetness, complexity, warmth)
- Visual parameters (color palette, lighting style, mood, composition, texture)

Using category theory principles to create deterministic parameter mappings
from cocktail characteristics → visual aesthetic parameters.
"""

from enum import Enum
from typing import Dict, List
from dataclasses import dataclass
import json


# ============================================================================
# LAYER 1: CATEGORICAL TAXONOMY (OLOG STRUCTURE)
# ============================================================================

class SpiritBase(str, Enum):
    """Primary spirit in cocktail"""
    RUM = "rum"
    WHISKEY = "whiskey"
    VODKA = "vodka"
    GIN = "gin"
    TEQUILA = "tequila"
    COGNAC = "cognac"
    MEZCAL = "mezcal"


class FlavorType(str, Enum):
    """Primary flavor characteristic"""
    BITTER = "bitter"
    SWEET = "sweet"
    SOUR = "sour"
    SPIRIT_FORWARD = "spirit_forward"
    HERBAL = "herbal"
    FRUITY = "fruity"
    CREAMY = "creamy"
    SPICED = "spiced"
    SMOKY = "smoky"


class ComplexityLevel(str, Enum):
    """Flavor and ingredient complexity"""
    SIMPLE = "simple"  # 2-3 ingredients
    MODERATE = "moderate"  # 4-5 ingredients
    COMPLEX = "complex"  # 6+ ingredients with layering


class ColorCategory(str, Enum):
    """High-level color grouping"""
    AMBER = "amber"
    RUBY = "ruby"
    GOLDEN = "golden"
    CLEAR = "clear"
    DARK = "dark"
    TROPICAL = "tropical"
    GREEN = "green"
    PURPLE = "purple"


class LightingStyle(str, Enum):
    """Lighting approach that suits the cocktail"""
    WARM_SIDE_LIT = "warm_side_lit"
    TIKI_TORCH = "tiki_torch"
    GOLDEN_HOUR = "golden_hour"
    MOODY_AMBER = "moody_amber"
    CRISP_BACKLIT = "crisp_backlit"
    NEON_ACCENT = "neon_accent"
    DIFFUSED_SOFT = "diffused_soft"
    DRAMATIC_SHADOW = "dramatic_shadow"


class MoodDescriptor(str, Enum):
    """Emotional/aesthetic quality"""
    SOPHISTICATED = "sophisticated"
    TROPICAL = "tropical"
    NOSTALGIC = "nostalgic"
    BOLD = "bold"
    ELEGANT = "elegant"
    PLAYFUL = "playful"
    DARK = "dark"
    AROMATIC = "aromatic"


class CompositionApproach(str, Enum):
    """Visual composition strategy"""
    BALANCED = "balanced"
    LAYERED = "layered"
    MINIMALIST = "minimalist"
    DRAMATIC = "dramatic"
    GARNISH_FOCUSED = "garnish_focused"


class TextureQuality(str, Enum):
    """Surface and transparency characteristics"""
    SMOOTH = "smooth"
    CRYSTALLINE = "crystalline"
    CREAMY = "creamy"
    OILY = "oily"
    EFFERVESCENT = "effervescent"
    TRANSLUCENT = "translucent"
    OPAQUE = "opaque"
    FOAMY = "foamy"


class TemperatureVibe(str, Enum):
    """Thermal quality conveyed"""
    WARM = "warm"
    HOT = "hot"
    COOL = "cool"
    ICY = "icy"
    AMBIENT = "ambient"


# ============================================================================
# LAYER 2: CATEGORICAL STRUCTURES (MORPHISM SOURCES/TARGETS)
# ============================================================================

@dataclass
class FlavorProfile:
    """Flavor characteristics of a cocktail"""
    primary_flavor: FlavorType
    secondary_flavors: List[FlavorType]
    complexity: ComplexityLevel
    warmth_level: int  # 0-10: warm spirits (rum, cognac, whiskey) vs cool (vodka, gin)
    bitterness: int  # 0-10
    sweetness: int  # 0-10
    richness: int  # 0-10: cream, fat, oils


@dataclass
class VisualParameters:
    """Visual aesthetic parameters for a cocktail"""
    primary_color_category: ColorCategory
    color_palette: List[str]  # Hex codes
    lighting_style: LightingStyle
    primary_mood: MoodDescriptor
    secondary_moods: List[MoodDescriptor]
    composition_strategy: CompositionApproach
    texture_quality: TextureQuality
    temperature_vibe: TemperatureVibe
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for prompt enhancement"""
        return {
            "primary_color": self.primary_color_category.value,
            "color_palette": self.color_palette,
            "lighting": self.lighting_style.value,
            "mood": self.primary_mood.value,
            "secondary_moods": [m.value for m in self.secondary_moods],
            "composition": self.composition_strategy.value,
            "texture": self.texture_quality.value,
            "temperature": self.temperature_vibe.value
        }


@dataclass
class CocktailProfile:
    """Complete profile of a cocktail for aesthetic mapping"""
    name: str
    spirit_base: SpiritBase
    primary_flavor: FlavorType
    flavor_profile: FlavorProfile  # Structured flavor data
    visual_parameters: VisualParameters
    description: str  # Natural language description


# ============================================================================
# LAYER 3: OLOG MORPHISMS (DETERMINISTIC MAPPINGS)
# ============================================================================

class CocktailOlogMorphisms:
    """
    Deterministic morphisms for cocktail aesthetic mapping.
    Maps: Cocktail characteristics → Visual parameters
    """

    @staticmethod
    def spirit_base_to_warmth(spirit: SpiritBase) -> int:
        """
        Morphism: SpiritBase → warmth_level (0-10)
        Determines thermal/nostalgic warmth of spirit
        """
        warmth_map = {
            SpiritBase.RUM: 9,  # Dark, caramel, tropical
            SpiritBase.WHISKEY: 8,  # Warm, oak, amber
            SpiritBase.COGNAC: 9,  # Rich, warm, luxurious
            SpiritBase.MEZCAL: 8,  # Smoky, earthy
            SpiritBase.TEQUILA: 7,  # Bright but earthy
            SpiritBase.GIN: 5,  # Crisp, herbal
            SpiritBase.VODKA: 3,  # Clean, neutral, cool
        }
        return warmth_map.get(spirit, 5)

    @staticmethod
    def spirit_base_to_color_category(spirit: SpiritBase) -> ColorCategory:
        """
        Morphism: SpiritBase → ColorCategory
        Spirits naturally suggest dominant colors
        """
        color_map = {
            SpiritBase.RUM: ColorCategory.GOLDEN,
            SpiritBase.WHISKEY: ColorCategory.AMBER,
            SpiritBase.COGNAC: ColorCategory.AMBER,
            SpiritBase.MEZCAL: ColorCategory.GOLDEN,
            SpiritBase.TEQUILA: ColorCategory.CLEAR,
            SpiritBase.GIN: ColorCategory.CLEAR,
            SpiritBase.VODKA: ColorCategory.CLEAR,
        }
        return color_map.get(spirit, ColorCategory.CLEAR)

    @staticmethod
    def flavor_to_mood(flavor: FlavorType) -> MoodDescriptor:
        """
        Morphism: FlavorType → MoodDescriptor
        Flavor characteristics map to emotional tone
        """
        mood_map = {
            FlavorType.BITTER: MoodDescriptor.SOPHISTICATED,
            FlavorType.SWEET: MoodDescriptor.PLAYFUL,
            FlavorType.SPIRIT_FORWARD: MoodDescriptor.BOLD,
            FlavorType.HERBAL: MoodDescriptor.ELEGANT,
            FlavorType.FRUITY: MoodDescriptor.TROPICAL,
            FlavorType.CREAMY: MoodDescriptor.NOSTALGIC,
            FlavorType.SMOKY: MoodDescriptor.DARK,
            FlavorType.SOUR: MoodDescriptor.BOLD,
            FlavorType.SPICED: MoodDescriptor.AROMATIC,
        }
        return mood_map.get(flavor, MoodDescriptor.SOPHISTICATED)

    @staticmethod
    def complexity_to_composition(complexity: ComplexityLevel) -> CompositionApproach:
        """
        Morphism: ComplexityLevel → CompositionApproach
        More complex drinks benefit from showing ingredient layering
        """
        composition_map = {
            ComplexityLevel.SIMPLE: CompositionApproach.MINIMALIST,
            ComplexityLevel.MODERATE: CompositionApproach.BALANCED,
            ComplexityLevel.COMPLEX: CompositionApproach.LAYERED,
        }
        return composition_map.get(complexity, CompositionApproach.BALANCED)

    @staticmethod
    def bitterness_to_lighting(bitterness: int) -> LightingStyle:
        """
        Morphism: bitterness_level → LightingStyle
        Rule: Bitter = high contrast, sophisticated lighting
        Sweet = soft, diffused lighting
        """
        if bitterness >= 7:
            return LightingStyle.DRAMATIC_SHADOW
        elif bitterness >= 5:
            return LightingStyle.WARM_SIDE_LIT
        else:
            return LightingStyle.DIFFUSED_SOFT

    @staticmethod
    def warmth_and_complexity_to_lighting(warmth: int, complexity: ComplexityLevel) -> LightingStyle:
        """
        Morphism: (warmth_level, complexity) → LightingStyle
        Combines spirit warmth with ingredient complexity
        """
        if warmth >= 8 and complexity == ComplexityLevel.COMPLEX:
            return LightingStyle.GOLDEN_HOUR  # Classic tiki/tropical
        elif warmth >= 8:
            return LightingStyle.MOODY_AMBER  # Warm, intimate
        elif warmth <= 4:
            return LightingStyle.CRISP_BACKLIT  # Clean, refreshing
        else:
            return LightingStyle.WARM_SIDE_LIT

    @staticmethod
    def texture_from_components(
        has_cream: bool, has_ice: bool, is_effervescent: bool
    ) -> TextureQuality:
        """
        Morphism: (has_cream, has_ice, is_effervescent) → TextureQuality
        Ingredient composition determines visible texture
        """
        if has_cream:
            return TextureQuality.CREAMY
        elif is_effervescent:
            return TextureQuality.EFFERVESCENT
        elif has_ice:
            return TextureQuality.CRYSTALLINE
        else:
            return TextureQuality.TRANSLUCENT

    @staticmethod
    def build_visual_parameters(
        spirit: SpiritBase,
        primary_flavor: FlavorType,
        complexity: ComplexityLevel,
        bitterness: int,
        sweetness: int,
        richness: int,
        color_palette: List[str],
        has_cream: bool = False,
        has_ice: bool = True,
        is_effervescent: bool = False,
    ) -> VisualParameters:
        """
        Master morphism: Cocktail characteristics → VisualParameters
        Orchestrates all sub-morphisms to create complete visual profile
        """
        primary_color = CocktailOlogMorphisms.spirit_base_to_color_category(spirit)
        primary_mood = CocktailOlogMorphisms.flavor_to_mood(primary_flavor)
        
        # Warmth is derived from spirit base
        warmth = CocktailOlogMorphisms.spirit_base_to_warmth(spirit)
        
        # Composition strategy from complexity
        composition = CocktailOlogMorphisms.complexity_to_composition(complexity)
        
        # Lighting combines multiple factors
        lighting = CocktailOlogMorphisms.warmth_and_complexity_to_lighting(warmth, complexity)
        
        # Texture from physical components
        texture = CocktailOlogMorphisms.texture_from_components(has_cream, has_ice, is_effervescent)
        
        # Temperature vibe correlates with warmth
        if warmth >= 8:
            temperature = TemperatureVibe.WARM
        elif warmth <= 3:
            temperature = TemperatureVibe.ICY
        else:
            temperature = TemperatureVibe.AMBIENT
        
        # Determine secondary moods from flavor complexity
        secondary_moods = []
        if richness >= 7:
            secondary_moods.append(MoodDescriptor.ELEGANT)
        if complexity == ComplexityLevel.COMPLEX:
            secondary_moods.append(MoodDescriptor.AROMATIC)
        if sweetness >= 6:
            secondary_moods.append(MoodDescriptor.PLAYFUL)

        return VisualParameters(
            primary_color_category=primary_color,
            color_palette=color_palette,
            lighting_style=lighting,
            primary_mood=primary_mood,
            secondary_moods=secondary_moods,
            composition_strategy=composition,
            texture_quality=texture,
            temperature_vibe=temperature,
        )

    @staticmethod
    def cocktail_to_profile(cocktail_data: Dict) -> CocktailProfile:
        """
        Morphism: Dict (raw cocktail data) → CocktailProfile
        Extracts and categorizes cocktail characteristics
        """
        spirit = SpiritBase(cocktail_data["spirit_base"].lower())
        primary_flavor_str = cocktail_data["primary_flavor"].lower()
        primary_flavor = FlavorType[primary_flavor_str.upper()]
        
        complexity_str = cocktail_data.get("complexity", "moderate").lower()
        complexity = ComplexityLevel(complexity_str)
        
        bitterness = cocktail_data.get("bitterness", 5)
        sweetness = cocktail_data.get("sweetness", 5)
        richness = cocktail_data.get("richness", 5)
        
        # Build flavor profile
        flavor_profile_obj = FlavorProfile(
            primary_flavor=primary_flavor,
            secondary_flavors=[],
            complexity=complexity,
            warmth_level=CocktailOlogMorphisms.spirit_base_to_warmth(spirit),
            bitterness=bitterness,
            sweetness=sweetness,
            richness=richness,
        )
        
        # Build visual parameters
        visual = CocktailOlogMorphisms.build_visual_parameters(
            spirit=spirit,
            primary_flavor=primary_flavor,
            complexity=complexity,
            bitterness=bitterness,
            sweetness=sweetness,
            richness=richness,
            color_palette=cocktail_data.get("color_palette", []),
            has_cream=cocktail_data.get("has_cream", False),
            has_ice=cocktail_data.get("has_ice", True),
            is_effervescent=cocktail_data.get("is_effervescent", False),
        )
        
        return CocktailProfile(
            name=cocktail_data["name"],
            spirit_base=spirit,
            primary_flavor=primary_flavor,
            flavor_profile=flavor_profile_obj,
            visual_parameters=visual,
            description=cocktail_data.get("description", ""),
        )
