"""Workflow implementations for ScholarAgents."""

from .experiment_design_workflow import ExperimentDesignWorkflow
from .literature_review_workflow import LiteratureReviewWorkflow
from .paper_writing_workflow import PaperWritingWorkflow

__all__ = [
    "ExperimentDesignWorkflow",
    "LiteratureReviewWorkflow",
    "PaperWritingWorkflow",
]
