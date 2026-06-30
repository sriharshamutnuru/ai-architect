"""
Week 1 · Day 2 · Tuesday 6AM
Temperature, tokens, and top-p experiments — BFSI grounded
RBI Compliance RAG Agent portfolio project
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an RBI compliance officer assistant at an Indian bank.
You have deep knowledge of the RBI Master Direction on KYC 2016 and subsequent amendments.
Respond concisely and precisely."""

KYC_PROMPT = """A customer wants to open a savings account. They have provided:
- Aadhaar card (with masked number)
- PAN card
- 6-month bank statement

Based on RBI KYC norms, are these documents sufficient? 
Answer in 2-3 sentences only."""

CREATIVE_PROMPT = """Write a brief tagline for an RBI compliance training module 
that makes the topic feel engaging for bank staff. One sentence only."""


# ── Experiment 1: Temperature sweep on a deterministic compliance task ──────

def experiment_temperature_sweep():
    """
    Run the same KYC compliance query at T=0, T=0.5, T=1.0
    Demonstrates that compliance tasks should use T=0 for reproducibility.
    """
    print("\n" + "="*60)
    print("EXPERIMENT 1: Temperature sweep — KYC compliance query")
    print("="*60)

    temperatures = [0.0, 0.5, 1.0]

    for temp in temperatures:
        print(f"\n--- Temperature = {temp} ---")
        response = client.messages.create(
            model="claude-haiku-4-5",          # Haiku: fast + cheap for experiments
            max_tokens=200,
            temperature=temp,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": KYC_PROMPT}]
        )
        print(response.content[0].text.strip())
        print(f"[Tokens used: {response.usage.input_tokens} in / {response.usage.output_tokens} out]")


# ── Experiment 2: Top-p sweep on a creative task ────────────────────────────

def experiment_topp_sweep():
    """
    Run a creative task at top_p=0.3, top_p=0.7, top_p=1.0
    Shows how nucleus sampling affects creative diversity.
    """
    print("\n" + "="*60)
    print("EXPERIMENT 2: Top-p sweep — creative tagline task")
    print("="*60)

    top_p_values = [0.3, 0.7, 1.0]

    for p in top_p_values:
        print(f"\n--- top_p = {p} (temperature fixed at 0.8) ---")
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=80,
            temperature=0.8,
            top_p=p,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": CREATIVE_PROMPT}]
        )
        print(response.content[0].text.strip())


# ── Experiment 3: Token budget awareness ────────────────────────────────────

def experiment_token_budget():
    """
    Demonstrates token counting and cost awareness — critical for BFSI at scale.
    Shows input tokens vs output tokens and calculates indicative cost.
    
    Haiku pricing (as of late 2024): 
        ~$0.25 per million input tokens
        ~$1.25 per million output tokens
    Always check current Anthropic pricing at anthropic.com/pricing
    """
    print("\n" + "="*60)
    print("EXPERIMENT 3: Token budget — cost awareness at BFSI scale")
    print("="*60)

    # Count tokens WITHOUT making an inference call using count_tokens API
    token_count = client.messages.count_tokens(
        model="claude-haiku-4-5",
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": KYC_PROMPT}]
    )

    print(f"\nInput token count (no inference): {token_count.input_tokens}")

    # Now run and get actual usage
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": KYC_PROMPT}]
    )

    input_tok  = response.usage.input_tokens
    output_tok = response.usage.output_tokens

    # Indicative cost calculation (always verify current pricing)
    input_cost  = (input_tok  / 1_000_000) * 0.25
    output_cost = (output_tok / 1_000_000) * 1.25
    total_cost  = input_cost + output_cost

    print(f"Input tokens:  {input_tok}")
    print(f"Output tokens: {output_tok}")
    print(f"Indicative cost (1 call): ${total_cost:.6f}")

    # Scale to BFSI volume: 10,000 KYC queries/day
    daily_calls = 10_000
    daily_cost  = total_cost * daily_calls
    monthly_cost = daily_cost * 30

    print(f"\n--- At BFSI scale: {daily_calls:,} KYC queries/day ---")
    print(f"Daily cost:   ${daily_cost:.2f}")
    print(f"Monthly cost: ${monthly_cost:.2f}")
    print(f"\nArchitectural implication: at this scale, use Haiku for")
    print(f"structured extraction; escalate to Sonnet only for edge cases.")
    print(f"This is the 3-tier routing strategy (Haiku→Sonnet→Opus).")


# ── Experiment 4: Model comparison — same prompt, Haiku vs Sonnet ───────────

def experiment_model_routing():
    """
    Same compliance query on Haiku vs Sonnet.
    Demonstrates when to escalate in the 3-tier BFSI routing strategy.
    """
    print("\n" + "="*60)
    print("EXPERIMENT 4: Model routing — Haiku vs Sonnet for compliance")
    print("="*60)

    COMPLEX_PROMPT = """A foreign national residing in India on a work visa wants to 
    open an NRO account. They have a passport, visa document, and overseas address proof 
    but their Indian address is only a rental agreement not registered with local authorities.
    What does RBI KYC Master Direction say about this scenario?
    Be specific about which clause applies."""

    for model, label in [
        ("claude-haiku-4-5", "Haiku (fast / cheap)"),
        ("claude-sonnet-4-6", "Sonnet (capable / moderate cost)"),
    ]:
        print(f"\n--- {label} ---")
        response = client.messages.create(
            model=model,
            max_tokens=300,
            temperature=0,                # Always T=0 for compliance
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": COMPLEX_PROMPT}]
        )
        print(response.content[0].text.strip())
        print(f"[{response.usage.input_tokens} in / {response.usage.output_tokens} out tokens]")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Week 1 · Day 2 — Sampling parameters experiment suite")
    print("RBI Compliance RAG Agent · Portfolio project\n")

    experiment_temperature_sweep()
    experiment_topp_sweep()
    experiment_token_budget()
    experiment_model_routing()

    print("\n" + "="*60)
    print("All experiments complete. Commit to GitHub before 8:30am.")
    print("="*60)