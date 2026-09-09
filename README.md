# Hybrid LLM NLP System for Plant Nursery

A hybrid Natural Language Processing (NLP) system for understanding customer queries in the plant nursery domain.

The system combines **Large Language Models (LLMs)** with **rule-based NLP techniques** to extract structured information from natural-language queries and use it for plant recommendations and customer support.

The project compares three different approaches:

1. **Rule-based NLP**
2. **LLM-only parsing**
3. **Hybrid LLM + rule-based parsing**

Multiple prompting strategies were also evaluated, ranging from **zero-shot to ten-shot prompting**.

---

## Features

The system analyzes a user's natural-language query and extracts four main types of information:

- **Intent** – price, availability, recommendation, delivery, location, working hours, contact, information, etc.
- **Plant** – plant species explicitly mentioned in the query
- **Conditions** – sunlight, shade, balcony, terrace, water requirements, hedge, evergreen, easy maintenance, fast growth, etc.
- **Location** – city or delivery location mentioned by the user

Example query:

```text
Treba mi zimzelena biljka za živu ogradu koja brzo raste.
```

Structured output:

```json
{
  "namere": ["preporuka"],
  "biljka": null,
  "uslovi": ["zimzelena", "živa ograda", "brz rast"],
  "lokacija": null
}
```

The structured result can then be used by the recommendation engine to search the plant database and generate appropriate recommendations.

---

## System Architecture

The hybrid approach combines LLM-based semantic understanding with deterministic rule-based extraction and validation.

```text
User Query
    │
    ▼
Text Normalization
    │
    ├───────────────┐
    ▼               ▼
LLM Parser      Rule-Based Parser
    │               │
    └───────┬───────┘
            ▼
     Result Merging
            │
            ▼
 Validation & Conflict
      Resolution
            │
            ▼
   Structured JSON
            │
            ▼
 Recommendation Engine
            │
            ▼
       Final Result
```

The goal of the hybrid architecture is to combine the flexibility of LLMs with the predictability and control of explicitly defined rules.

---

## Approaches

### 1. Rule-Based Parser

The rule-based implementation uses:

- text normalization
- regular expressions
- keyword matching
- predefined intent mappings
- plant-name matching
- condition extraction
- location extraction
- conflict-resolution rules

This approach is deterministic and does not require an LLM.

Main implementation:

```text
rulesOnly.py
```

---

### 2. LLM-Only Parser

The LLM-only approach relies primarily on a locally executed language model to understand the query and return structured information.

Main implementation:

```text
llmOnly.py
```

This approach provides greater semantic flexibility but gives less deterministic control over the extracted values.

---

### 3. Hybrid LLM + Rule-Based Parser

The hybrid system combines both approaches.

The LLM first performs semantic interpretation of the query, while deterministic rules are used to detect, validate, correct, and merge extracted information.

The final output is restricted to predefined intents, plants, conditions, and supported locations.

This reduces invalid or hallucinated values while preserving the semantic capabilities of the language model.

---

## Hybrid Processing Pipeline

A user query goes through several processing stages.

### 1. Text normalization

The input text is normalized to make rule-based matching more reliable.

This includes operations such as:

- converting text to lowercase
- removing diacritics for matching
- normalizing characters
- preparing text for regex-based detection

### 2. LLM extraction

The query is sent to the locally running LLM.

The model produces structured information containing:

```json
{
  "namere": [],
  "biljka": null,
  "uslovi": [],
  "lokacija": null
}
```

### 3. Rule-based extraction

Deterministic rules independently search the original query for:

- intents
- plant names
- recommendation conditions
- locations

### 4. Validation and merging

The LLM and rule-based results are combined.

Additional logic handles cases such as:

- duplicate intents
- conflicting conditions
- invalid plant names
- hallucinated plants
- missing values
- recommendation queries without an explicitly mentioned plant

### 5. Recommendation

The final structured representation can be passed to the recommendation engine, which searches the plant database according to the extracted conditions.

---

## Intent Classes

The system supports the following intents:

```text
cena
dostupnost
preporuka
lokacija
dostava
informacije
radno_vreme
kontakt
opste
```

Multiple intents can be detected in a single query.

For example:

```text
Koliko košta lavanda i da li je imate?
```

can produce:

```json
{
  "namere": ["cena", "dostupnost"],
  "biljka": "lavanda",
  "uslovi": [],
  "lokacija": null
}
```

---

## Extracted Conditions

The recommendation system supports multiple plant requirements, including:

```text
sunce
senka
polusenka
terasa
balkon
malo vode
srednje vode
puno vode
živa ograda
zimzelena
saksija
dvorište
ukrasna
mirisna
laka nega
brz rast
dugo cvetanje
cvetanje
medonosna
kamenjar
mala bašta
otporna
začinska
```

These conditions are used to identify suitable plants from the available dataset.

---

## Local LLM Execution

The language models are executed locally using **Ollama**.

The main model used for the hybrid experiments is:

```text
Qwen2.5:3b
```

An earlier implementation of the parser was also tested with:

```text
Llama3.2:3b
```

Running the models locally makes it possible to experiment without relying on an external LLM API.

---

## Prompting Experiments

Several prompting strategies were implemented to investigate how the number of examples provided to the LLM affects extraction performance.

The experiments include:

| Experiment | Prompting Strategy |
|---|---|
| `hybrid_zero.py` | Zero-shot |
| `hybrid_one.py` | One-shot |
| `hybrid_three.py` | Three-shot |
| `hybrid_five.py` | Five-shot |
| `hybrid_ten.py` | Ten-shot |

This allows different configurations of the same hybrid architecture to be evaluated under comparable conditions.

---

## Project Structure

```text
hybrid-llm-nlp-system/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── rules_only.py
│   ├── llm_only.py
│   ├── llm_parser.py
│   ├── recommendation_engine.py
│   ├── hybrid_zero.py
│   ├── hybrid_one.py
│   ├── hybrid_three.py
│   ├── hybrid_five.py
│   └── hybrid_ten.py
│
├── evaluation/
│   ├── test_llm.py
│   └── results/
│       └── evaluation CSV files
│
├── data/
│   ├── biljke3.csv
│   └── pitanja.csv
│
└── docs/
    └── project report
```

---

## Dataset

The project uses two main datasets.

### Plant Database

```text
data/biljke3.csv
```

Contains information about available plants and their characteristics.

The database is used both for validating plant names and for generating recommendations.

### Evaluation Queries

```text
data/pitanja.csv
```

Contains user queries used for evaluating the different NLP approaches.

---

## Evaluation

The evaluation script compares parser predictions with expected structured outputs.

```text
evaluation/test_llm.py
```

The system evaluates the extraction of:

- user intent
- plant name
- recommendation conditions
- location

Errors from individual experiments are stored as CSV files for further analysis.

This makes it possible to compare the behavior of:

```text
Rule-Based
     vs
LLM-Only
     vs
Hybrid LLM + Rules
```

as well as different few-shot configurations.

---

## Recommendation Engine

The project also contains an interactive recommendation system:

```text
src/recommendation_engine.py
```

It demonstrates how the NLP parser can be used in a practical application.

The basic pipeline is:

```text
Natural-language query
        ↓
NLP parsing
        ↓
Structured requirements
        ↓
Plant database filtering
        ↓
Recommended plants
```

This represents a simplified example of how the parser could be integrated into a chatbot or customer-support application for a plant nursery.

---

## Technologies

The project was developed using:

- **Python**
- **Ollama**
- **Qwen2.5**
- **Llama 3.2**
- **Pandas**
- **Regular Expressions (Regex)**
- **Structured JSON output**
- **Rule-Based NLP**
- **Large Language Models**
- **Prompt Engineering**

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sajko01/hybrid-llm-nlp-system.git
cd hybrid-llm-nlp-system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Ollama must be installed and running locally.

Pull the Qwen model:

```bash
ollama pull qwen2.5:3b
```

The earlier Llama-based experiment can be reproduced with:

```bash
ollama pull llama3.2:3b
```

---

## Running the Project

### Rule-Based Parser

```bash
python src/rules_only.py
```

### LLM-Only Parser

```bash
python src/llm_only.py
```

### Hybrid Parser

For example, to run the ten-shot configuration:

```bash
python src/hybrid_ten.py
```

Other configurations can be executed in the same way:

```bash
python src/hybrid_zero.py
python src/hybrid_one.py
python src/hybrid_three.py
python src/hybrid_five.py
python src/hybrid_ten.py
```

### Recommendation System

```bash
python src/recommendation_engine.py
```

### Evaluation

```bash
python evaluation/test_llm.py
```

The parser configuration used for evaluation can be selected in the evaluation script.

---

## Key Contributions

The main contributions of the project include:

- implementation and comparison of **rule-based, LLM-only, and hybrid NLP approaches**
- local LLM inference using Ollama
- structured extraction of multiple information types from natural-language queries
- deterministic validation of LLM outputs
- mechanisms for reducing invalid or hallucinated plant predictions
- conflict-resolution rules for extracted recommendation conditions
- support for multi-intent queries
- comparison of **zero-shot, one-shot, three-shot, five-shot, and ten-shot prompting**
- development of an evaluation pipeline
- integration of the parser with a practical plant recommendation engine

---

## Future Improvements

Possible extensions include:

- larger and more diverse evaluation datasets
- additional plant species and recommendation attributes
- comparison with larger LLMs
- quantitative latency and memory benchmarks
- automated evaluation across all prompting configurations
- REST API integration
- web-based chatbot interface
- retrieval-augmented generation (RAG)
- deployment using Docker

---

## Author

**Aleksandar Jovanović**

MSc Student in Artificial Intelligence and Machine Learning  
Faculty of Electronic Engineering  
University of Niš