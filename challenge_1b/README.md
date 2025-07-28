# Round 1B: Persona-Driven Document Intelligence

**Theme: Connect What Matters — For the User Who Matters**

### Challenge Overview

In Round 1B, your task is to develop a system that intelligently analyzes a collection of related PDFs and, given a persona and their job-to-be-done, extracts and prioritizes the most relevant document sections—making discovery contextual and personalized.

#### Core requirements

- Input:  
  - 3–10 related PDF documents.  
  - A detailed persona definition.  
  - A clear job-to-be-done statement.

- Output:  
  - JSON file including metadata, extracted and ranked sections, and granular sub-section analyses.

#### Constraints

- CPU-only, offline execution.  
- Model size ≤1GB.  
- Maximum processing time: 60 seconds for 3–5 documents.  
- Dockerized solution.  
- No API/web calls or hardcoded logic.

#### Implementation Guidance

- Generalize for all kinds of document types and personae/jobs.  
- Make extraction logic robust—consider not only headings but also context, semantics, and possibly multilingual content.  
- Carefully structure your JSON output as per the challenge specification.  
- Modularize: reuse code and components from Round 1A wherever possible.

#### Submission Checklist

- Complete codebase with Dockerfile at root.  
- All dependencies included.  
- `approach_explanation.md` (300–500 words on methodology).  
- Simple instructions for building and running the solution.  
- JSON outputs stored in the expected format for each PDF set in `/app/output`.

**For both README files, update with team-specific build/run instructions and relevant technical details as your implementation advances.**
