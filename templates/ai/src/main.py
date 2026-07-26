"""
Main entry point for the AI/ML application.

This module provides the main entry point for the AI application
with support for LLMs, agents, and RAG.
"""

import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/ai.log", mode="a", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

from src.config import get_config
from src.models.model import LLMModel
from src.agents.agent import AssistantAgent
from src.prompts import PromptManager


def main() -> int:
    """
    Main entry point for the AI application.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    logger.info("Starting {{ project_name }} AI application...")
    
    try:
        # Load configuration
        config = get_config()
        logger.info(f"Configuration loaded: {config.get('model', 'default')}")
        
        # Initialize prompt manager
        prompt_manager = PromptManager()
        
        # Initialize model
        model = LLMModel(
            provider=config.get("provider", "openai"),
            model=config.get("model", "gpt-4"),
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 2000),
        )
        
        # Initialize agent
        agent = AssistantAgent(
            model=model,
            prompt_manager=prompt_manager,
            verbose=True,
        )
        
        # Run example interaction
        response = agent.run("Hello! Can you help me with a question?")
        print("\n" + "=" * 60)
        print("AI Response:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())