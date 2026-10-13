"""
Psychological Engagement Frameworks
Maps scientific theories to measurable content signals.

Theoretical grounding:
- Russell, J. A. (1980). A circumplex model of affect. Journal of Personality and Social Psychology.
- Berger, J. & Milkman, K. L. (2012). What makes online content viral? Journal of Marketing Research.
- Loewenstein, G. (1994). The psychology of curiosity: A review and reinterpretation.
- Cialdini, R. B. (1984). Influence: The Psychology of Persuasion.
- Green, M. C. & Brock, T. C. (2000). The role of transportation in the persuasiveness of narratives.
- Markus, H. & Wurf, E. (1987). The dynamic self-concept: A social psychological perspective.
- Seligman, M. E. P. (2011). Flourish: A Visionary New Understanding of Happiness and Well-being.
- Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk.
"""

ENGAGEMENT_DIMENSIONS = {
    "emotional_arousal": {
        "label": "Emotional Arousal",
        "short": "Arousal",
        "theory": "Russell's Circumplex Model (1980)",
        "description": "High-activation emotional states — both positive (awe, excitement) and "
                       "negative (anger, anxiety) — were linked to more sharing of news articles "
                       "(Berger & Milkman, 2012), while low-arousal states such as sadness were linked to less.",
        "high_positive": [
            "amazing", "incredible", "love", "excited", "thrilling", "breathtaking",
            "wonderful", "inspiring", "brilliant", "extraordinary", "magnificent",
            "spectacular", "heartwarming", "euphoric", "electrifying", "stunning",
        ],
        "high_negative": [
            "shocking", "outrageous", "devastating", "horrifying", "terrifying",
            "disturbing", "infuriating", "alarming", "appalling", "tragic",
            "explosive", "brutal", "catastrophic",
        ],
        "color": "#E74C3C",
        "weight": 1.3,
    },
    "curiosity_gap": {
        "label": "Curiosity Gap",
        "short": "Curiosity",
        "theory": "Loewenstein's Information Gap Theory (1994)",
        "description": "Content that reveals partial information creates an aversive knowledge "
                       "gap. The discomfort of not knowing drives engagement as a resolution behavior. "
                       "Questions, teaser phrasing, and incomplete narratives all exploit this mechanism.",
        "keywords": [
            "why", "how", "what if", "discover", "revealed", "secret", "hidden",
            "surprising", "unexpected", "truth", "behind", "untold", "mystery",
            "unknown", "never seen", "first time", "what really", "the reason",
            "you won't believe", "find out", "what happens when", "what nobody",
        ],
        "color": "#F39C12",
        "weight": 1.1,
    },
    "social_proof": {
        "label": "Social Proof",
        "short": "Social",
        "theory": "Cialdini's Principles of Influence (1984)",
        "description": "Explicit signals that others have already engaged — view counts, awards, "
                       "critical acclaim, community references — reduce the perceived risk of "
                       "engagement and increase trust in the content's value.",
        "keywords": [
            "award", "acclaimed", "nominated", "#1", "bestselling", "chart-topping",
            "millions", "thousands", "loved by", "praised by", "recommended",
            "popular", "hit", "phenomenon", "celebrated", "landmark",
            "critics", "audience favorite", "must-see", "everyone is talking",
            "season", "series", "emmy", "oscar", "bafta",
        ],
        "color": "#3498DB",
        "weight": 0.9,
    },
    "narrative_transport": {
        "label": "Narrative Transport",
        "short": "Narrative",
        "theory": "Green & Brock Transportation Model (2000)",
        "description": "Story-based content can absorb the audience into the narrative world. "
                       "Green & Brock found that more transported readers showed more story-consistent "
                       "beliefs; story markers, protagonists and conflict are text cues for that structure.",
        "story_markers": [
            "story", "journey", "discover", "when", "then", "finally", "realized",
            "never expected", "true story", "based on", "real", "life changed",
            "one day", "everything changed", "survived", "overcome", "grew up",
        ],
        "protagonist_markers": ["i", "she", "he", "they", "her", "his"],
        "conflict_markers": [
            "but", "however", "until", "challenge", "struggle", "obstacle",
            "against all odds", "despite", "impossible", "crisis", "threat",
        ],
        "color": "#9B59B6",
        "weight": 1.0,
    },
    "identity_resonance": {
        "label": "Identity Resonance",
        "short": "Identity",
        "theory": "Self-Concept Theory (Markus & Wurf, 1987)",
        "description": "Content that mirrors or affirms the viewer's existing or aspirational "
                       "self-concept creates a sense of personal relevance. Second-person language, "
                       "audience-specific framing, and aspirational identity cues all drive this effect.",
        "second_person": ["you", "your", "for you", "designed for you", "people like you"],
        "aspirational": [
            "become", "transform", "master", "achieve", "grow", "level up",
            "unlock", "elevate", "thrive", "lead", "build", "create",
        ],
        "community": [
            "community", "belong", "together", "us", "we", "our", "join",
            "connect", "tribe", "movement", "family",
        ],
        "color": "#1ABC9C",
        "weight": 1.0,
    },
    "perma_wellbeing": {
        "label": "PERMA Wellbeing",
        "short": "PERMA",
        "theory": "Seligman's PERMA Model (2011) — Positive Psychology",
        "description": "Content touching the five pillars of human flourishing (Positive Emotion, "
                       "Engagement/Flow, Relationships, Meaning, Accomplishment) resonates deeply "
                       "because it speaks to what people most fundamentally want from life.",
        "positive_emotion": ["happy", "joy", "love", "grateful", "inspired", "hopeful",
                              "warm", "delight", "cheerful", "uplifting"],
        "engagement_flow": ["absorbing", "immersive", "captivating", "engaging", "gripping",
                             "binge", "can't stop", "passionate", "compelling", "riveting"],
        "relationships": ["family", "friendship", "bond", "connection", "love", "together",
                          "community", "belonging", "partner", "team"],
        "meaning": ["purpose", "matter", "important", "legacy", "mission", "why",
                    "impact", "change", "difference", "humanity", "future"],
        "accomplishment": ["achieve", "success", "win", "goal", "milestone", "pride",
                            "overcome", "triumph", "record", "first", "landmark"],
        "color": "#27AE60",
        "weight": 1.0,
    },
    "scarcity_exclusivity": {
        "label": "Scarcity / Exclusivity",
        "short": "Scarcity",
        "theory": "Prospect Theory — Kahneman & Tversky (1979)",
        "description": "Perceived scarcity elevates the subjective value of content. "
                       "Exclusivity signals (premieres, limited series, insider access) "
                       "function as benign applications of loss-aversion in content marketing.",
        "keywords": [
            "limited series", "finale", "premiere", "debut", "first look",
            "exclusive", "only", "rare", "one-of-a-kind", "never before",
            "world premiere", "director's cut", "special edition", "extended",
            "behind the scenes", "sneak peek", "early access",
        ],
        "color": "#E67E22",
        "weight": 0.8,
    },
}


CONTENT_PROFILE_TYPES = {
    "Viral Emotion Driver":     "High arousal + strong negative or positive emotion. Built to spread.",
    "Curiosity Engine":         "Dominates on curiosity gap. Drives clicks and click-through rates.",
    "Community Builder":        "Identity resonance + PERMA relationships. Creates loyal audiences.",
    "Prestige Signal":          "Social proof + scarcity. Signals quality to undecided viewers.",
    "Narrative Immersive":      "Narrative transport dominant. Creates binge behavior and recall.",
    "Meaning-Led Content":      "PERMA meaning + identity. Appeals to purpose-driven audiences.",
    "Balanced Engagement":      "No single dominant dimension — broad appeal, moderate engagement.",
}
