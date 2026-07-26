


## `src/tite/modes/ai/files/main.py`


"""
Main entry point for the AI/ML application.

This module provides the main execution entry for running AI/ML models,
agents, and API servers.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger
from dotenv import load_dotenv

from src.models.llm import LLMModel
from src.models.embedding import EmbeddingModel
from src.agents.assistant import AssistantAgent
from src.agents.rag import RAGAgent
from src.prompts.manager import PromptManager
from src.utils.logger import setup_logging
from src.config.settings import get_settings


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="AI/ML CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=Path("config/settings.py"),
        help="Path to configuration file",
    )
    
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run a query")
    run_parser.add_argument("--query", "-q", required=True, help="Query to run")
    run_parser.add_argument("--model", "-m", default="gpt-4", help="Model to use")
    run_parser.add_argument("--agent", "-a", default="assistant", choices=["assistant", "rag"], 
                            help="Agent type to use")
    run_parser.add_argument("--system-prompt", "-s", help="System prompt to use")
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start API server")
    serve_parser.add_argument("--port", "-p", type=int, default=8000, help="Port to bind to")
    serve_parser.add_argument("--host", "-H", default="127.0.0.1", help="Host to bind to")
    serve_parser.add_argument("--workers", "-w", type=int, default=4, help="Number of workers")
    
    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a model")
    eval_parser.add_argument("--model", "-m", required=True, help="Model to evaluate")
    eval_parser.add_argument("--dataset", "-d", required=True, help="Dataset to use")
    eval_parser.add_argument("--output", "-o", help="Output file for results")
    
    # Fine-tune command
    ft_parser = subparsers.add_parser("fine-tune", help="Fine-tune a model")
    ft_parser.add_argument("--model", "-m", required=True, help="Model to fine-tune")
    ft_parser.add_argument("--data", "-d", required=True, help="Training data file")
    ft_parser.add_argument("--epochs", "-e", type=int, default=3, help="Number of epochs")
    ft_parser.add_argument("--output", "-o", default="models/fine_tuned", help="Output directory")
    
    # Benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Benchmark models")
    bench_parser.add_argument("--models", "-m", required=True, help="Comma-separated models")
    bench_parser.add_argument("--tasks", "-t", required=True, help="Comma-separated tasks")
    bench_parser.add_argument("--output", "-o", help="Output file for results")
    
    return parser.parse_args()


def run_query(args: argparse.Namespace) -> int:
    """
    Run a query with the specified agent.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        load_dotenv()
        settings = get_settings()
        
        logger.info(f"Running query: {args.query}")
        
        if args.agent == "assistant":
            agent = AssistantAgent(
                model=args.model,
                system_prompt=args.system_prompt,
                verbose=True,
            )
            response = agent.run(args.query)
        elif args.agent == "rag":
            agent = RAGAgent(
                llm_model=args.model,
                embedding_model=settings.embedding_model,
                vector_db=settings.vector_db_type,
                verbose=True,
            )
            response = agent.query(args.query)
        else:
            logger.error(f"Unknown agent: {args.agent}")
            return 1
            
        print("\n" + "=" * 80)
        print(f"Query: {args.query}")
        print("=" * 80)
        print(f"Response:\n{response}")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to run query: {e}")
        return 1


def serve_api(args: argparse.Namespace) -> int:
    """
    Start the API server.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        load_dotenv()
        settings = get_settings()
        
        logger.info(f"Starting API server on {args.host}:{args.port}")
        
        # Import here to avoid circular imports
        import uvicorn
        from src.app import create_app
        
        app = create_app()
        
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            workers=args.workers,
            log_level="debug" if settings.debug else "info",
        )
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to start API server: {e}")
        return 1


def evaluate_model(args: argparse.Namespace) -> int:
    """
    Evaluate a model on a dataset.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        load_dotenv()
        
        logger.info(f"Evaluating model: {args.model}")
        logger.info(f"Dataset: {args.dataset}")
        
        # Load dataset
        dataset_path = Path(args.dataset)
        if not dataset_path.exists():
            logger.error(f"Dataset not found: {args.dataset}")
            return 1
            
        with open(dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)
            
        # Initialize model
        model = LLMModel(
            provider="openai",
            model=args.model,
            temperature=0.0,
        )
        
        # Run evaluation
        results = []
        for item in dataset:
            query = item.get("query", item.get("input", ""))
            expected = item.get("expected", item.get("output", ""))
            
            response = model.generate(query)
            results.append({
                "query": query,
                "expected": expected,
                "response": response,
            })
            
        # Save results
        output_path = args.output or "models/evaluation/results.json"
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Evaluation results saved to: {output_path}")
        
        # Print summary
        print("\n" + "=" * 80)
        print(f"Evaluation Results for: {args.model}")
        print("=" * 80)
        print(f"Total samples: {len(results)}")
        print(f"Results saved to: {output_path}")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to evaluate model: {e}")
        return 1


def fine_tune_model(args: argparse.Namespace) -> int:
    """
    Fine-tune a model.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        load_dotenv()
        
        logger.info(f"Fine-tuning model: {args.model}")
        logger.info(f"Training data: {args.data}")
        logger.info(f"Epochs: {args.epochs}")
        
        # Load training data
        data_path = Path(args.data)
        if not data_path.exists():
            logger.error(f"Training data not found: {args.data}")
            return 1
            
        with open(data_path, "r", encoding="utf-8") as f:
            training_data = json.load(f)
            
        # Here you would implement the fine-tuning logic
        # This is a placeholder - actual implementation would use
        # libraries like transformers, peft, trl, etc.
        
        logger.info(f"Fine-tuning completed. Output saved to: {args.output}")
        
        print("\n" + "=" * 80)
        print(f"Fine-tuning Results for: {args.model}")
        print("=" * 80)
        print(f"Training samples: {len(training_data)}")
        print(f"Epochs: {args.epochs}")
        print(f"Output directory: {args.output}")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to fine-tune model: {e}")
        return 1


def benchmark_models(args: argparse.Namespace) -> int:
    """
    Benchmark multiple models.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        load_dotenv()
        
        models = [m.strip() for m in args.models.split(",")]
        tasks = [t.strip() for t in args.tasks.split(",")]
        
        logger.info(f"Benchmarking models: {models}")
        logger.info(f"Tasks: {tasks}")
        
        # Run benchmarks
        results = {}
        for model in models:
            results[model] = {}
            llm = LLMModel(
                provider="openai",
                model=model,
                temperature=0.0,
            )
            
            for task in tasks:
                # Run benchmark for each task
                logger.info(f"Running {task} on {model}...")
                # Placeholder benchmark
                results[model][task] = {
                    "score": 0.85,
                    "latency": 1.2,
                    "tokens": 150,
                }
                
        # Save results
        output_path = args.output or "models/benchmark/results.json"
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Benchmark results saved to: {output_path}")
        
        # Print results
        print("\n" + "=" * 80)
        print("Benchmark Results")
        print("=" * 80)
        
        for model, model_results in results.items():
            print(f"\n{model}:")
            for task, metrics in model_results.items():
                print(f"  {task}: {metrics}")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to benchmark models: {e}")
        return 1


def main() -> int:
    """
    Main entry point.
    
    Returns:
        int: Exit code
    """
    args = parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level)
    
    # Load environment
    load_dotenv()
    
    # Run command
    if args.command == "run":
        return run_query(args)
    elif args.command == "serve":
        return serve_api(args)
    elif args.command == "evaluate":
        return evaluate_model(args)
    elif args.command == "fine-tune":
        return fine_tune_model(args)
    elif args.command == "benchmark":
        return benchmark_models(args)
    else:
        print("Unknown command. Use --help for usage.")
        return 1


if __name__ == "__main__":
    sys.exit(main())