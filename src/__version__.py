"""
Version information for Luminis AI Library Assistant
"""

__version__ = "1.0.2"
__version_info__ = (1, 0, 2)
__author__ = "Luminis AI Team"
__email__ = "info@luminis.ai"
__description__ = "AI-powered library assistant with multilingual support"
__url__ = "https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot"


def get_version():
    """Get the current version string"""
    return __version__


def get_version_info():
    """Get the current version as a tuple"""
    return __version_info__


def get_full_info():
    """Get full version information"""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "author": __author__,
        "email": __email__,
        "description": __description__,
        "url": __url__,
    }
